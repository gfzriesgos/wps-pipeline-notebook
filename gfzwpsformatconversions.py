#!/usr/bin/env python3

'''
This is a module
for format conversions
of wps in- and output data
in the riesgos project for
services provided by the GFZ.

A log of this code comes from here:
https://raw.githubusercontent.com/gfzriesgos/quakeledger/master/quakeml.py
'''

import collections
import math
import io
import tokenize

import geopandas as gpd
import georasters as gr
import lxml.etree as le
import numpy as np
import pandas as pd


class QuakeMLNamespaceAdderMixin():
    '''
    A common Method for all those
    xml handlers that need the quakeml
    namespace.
    '''
    @staticmethod
    def _add_namespace(element):
        '''
        Adds the namespace to the quakeml xml elements.
        '''
        return '{http://quakeml.org/xmlns/bed/1.2}' + element

class UtcToEventMixin():

    @staticmethod
    def _utc2event(utc):
        '''
        Given utc string returns list with year,month,day,hour,minute,second
        '''
        # last part usually either Z(ulu) or UTC, if not fails
        if utc[-3:] == 'UTC':
            utc = utc[:-2]
        elif utc[-1:] == 'Z':
            pass
        else:
            raise Exception(
                'Cannot handle timezone other than Z(ulu) or UTC: {}'.format(
                    utc))
        date, time = utc.split('T')
        return [
            int(v)
            if i < 5
            else float(v)
            for i, v in enumerate(
                [
                    int(d)
                    for d
                    in date.split('-')
                ] + [
                    float(t)
                    for t
                    in time[:-1].split(':')
                ]
            )
        ]

class QuakeML(QuakeMLNamespaceAdderMixin, UtcToEventMixin):
    '''
    Class for handling quakeml data conversion.
    '''
    def __init__(self, xml):
        self._xml = xml

    @staticmethod
    def _get_uncertain_child(parent, childname):
        '''
        Given a childname returns value and uncertainty
        '''
        value = QuakeML._as_float(
            parent.find(childname).findtext(
                QuakeML._add_namespace('value')))
        uncertainty = QuakeML._as_float(
            parent.find(childname).findtext(
                QuakeML._add_namespace('uncertainty')))
        return [value, uncertainty]

    def to_geodataframe(self):
        '''
        Returns a geopandas dataframe using the latitude and longitude columns.
        '''
        dataframe = self.to_dataframe()
        geodataframe = gpd.GeoDataFrame(
            dataframe,
            geometry=gpd.points_from_xy(
                dataframe['longitude'],
                dataframe['latitude'])
        )
        return geodataframe

    def to_dataframe(self):
        '''
        Converts the quakeml data to a pandas dataframe.
        '''
        # initialize catalog
        index = [i for i in range(len(self._xml))]
        columns = [
            'eventID',
            'agency',
            'Identifier',
            'year',
            'month',
            'day',
            'hour',
            'minute',
            'second',
            'timeUncertainty',
            'longitude',
            'longitudeUncertainty',
            'latitude',
            'latitudeUncertainty',
            'horizontalUncertainty',
            'maxHorizontalUncertainty',
            'minHorizontalUncertainty',
            'azimuthMaxHorizontalUncertainty',
            'depth',
            'depthUncertainty',
            'magnitude',
            'magnitudeUncertainty',
            'rake',
            'rakeUncertainty',
            'dip',
            'dipUncertainty',
            'strike',
            'strikeUncertainty',
            'type',
            'probability'
        ]
        catalog = pd.DataFrame(index=index, columns=columns)
        # add individual events to catalog
        for i, event in enumerate(self._xml):
            # get ID
            catalog.iloc[i].eventID = event.attrib['publicID']
            # type
            catalog.iloc[i].type = event.find(
                QuakeML._add_namespace('description')).findtext(
                    QuakeML._add_namespace('text'))
            # origin
            origin = event.find(QuakeML._add_namespace('origin'))
            # time
            year, month, day, hour, minute, second = QuakeML._utc2event(
                origin.find(QuakeML._add_namespace('time')).findtext(
                    QuakeML._add_namespace('value')))
            catalog.iloc[i].year = year
            catalog.iloc[i].month = month
            catalog.iloc[i].day = day
            catalog.iloc[i].hour = hour
            catalog.iloc[i].minute = minute
            catalog.iloc[i].second = second

            catalog.iloc[i].timeUncertainty = float(origin.find(
                QuakeML._add_namespace('time')).findtext(
                    QuakeML._add_namespace('uncertainty')))
            # latitude/longitude/depth
            latitude, latitude_uncertainty = QuakeML._get_uncertain_child(
                origin, QuakeML._add_namespace('latitude'))

            catalog.iloc[i].latitude = latitude
            catalog.iloc[i].latitudeUncertainty = latitude_uncertainty

            longitude, longitude_uncertainty = QuakeML._get_uncertain_child(
                origin, QuakeML._add_namespace('longitude'))

            catalog.iloc[i].longitude = longitude
            catalog.iloc[i].longitudeUncertainty = longitude_uncertainty

            depth, depth_uncertainty = QuakeML._get_uncertain_child(
                origin, QuakeML._add_namespace('depth'))

            catalog.iloc[i].depth = depth
            catalog.iloc[i].depthUncertainty = depth_uncertainty

            # agency/provider
            catalog.iloc[i].agency = origin.find(
                QuakeML._add_namespace('creationInfo')).findtext(
                    QuakeML._add_namespace('author'))
            # magnitude
            magnitude = event.find(QuakeML._add_namespace('magnitude'))
            mag_value, mag_uncertainty = QuakeML._get_uncertain_child(
                magnitude, QuakeML._add_namespace('mag'))

            catalog.iloc[i].magnitude = mag_value
            catalog.iloc[i].magnitudeUncertainty = mag_uncertainty

            # originUncertainty
            origin_uncertainty = origin.find(
                QuakeML._add_namespace('originUncertainty'))
            catalog.iloc[i].horizontalUncertainty = QuakeML._as_float(
                origin_uncertainty.find(
                    QuakeML._add_namespace('horizontalUncertainty')).findtext(
                        QuakeML._add_namespace('value')))
            catalog.iloc[i].minHorizontalUncertainty = QuakeML._as_float(
                origin_uncertainty.find(QuakeML._add_namespace(
                    'minHorizontalUncertainty')).findtext(
                        QuakeML._add_namespace('value')))
            catalog.iloc[i].maxHorizontalUncertainty = QuakeML._as_float(
                origin_uncertainty.find(QuakeML._add_namespace(
                    'maxHorizontalUncertainty')).findtext(
                        QuakeML._add_namespace('value')))
            catalog.iloc[i].horizontalUncertainty = QuakeML._as_float(
                origin_uncertainty.find(QuakeML._add_namespace(
                    'azimuthMaxHorizontalUncertainty')).findtext(
                        QuakeML._add_namespace('value')))

            # plane
            nodal_planes = event.find(
                QuakeML._add_namespace('focalMechanism')).find(
                    QuakeML._add_namespace('nodalPlanes'))
            preferred_plane = nodal_planes.get('preferredPlane')
            preferred_plane = nodal_planes.find(QuakeML._add_namespace(
                'nodalPlane' + preferred_plane))
            # GET uncertain child!!
            strike, strike_uncertainty = QuakeML._get_uncertain_child(
                preferred_plane, QuakeML._add_namespace('strike'))

            catalog.iloc[i].strike = strike
            catalog.iloc[i].strikeUncertainty = strike_uncertainty

            dip, dip_uncertainty = QuakeML._get_uncertain_child(
                preferred_plane, QuakeML._add_namespace('dip'))

            catalog.iloc[i].dip = dip
            catalog.iloc[i].dipUncertainty = dip_uncertainty

            rake, rake_uncertainty = QuakeML._get_uncertain_child(
                preferred_plane, QuakeML._add_namespace('rake'))

            catalog.iloc[i].rake = rake
            catalog.iloc[i].rake_uncertainty = rake_uncertainty

        return catalog


    @staticmethod
    def _as_float(possible_value):
        try:
            return float(possible_value)
        except ValueError:
            return math.nan
        except TypeError:
            return math.nan

    @classmethod
    def from_string(cls, xml_string):
        '''
        Reads the content from an xml string.
        '''
        xml = le.fromstring(xml_string)
        return cls(xml)

    @classmethod
    def from_xml(cls, xml):
        '''
        Reads the content from the xml data structure.
        '''
        return cls(xml)


class QuakeMLDataframe(QuakeMLNamespaceAdderMixin):
    '''
    Class to wrap the dataframe
    with quakeml data
    for conversions to xml.
    '''
    def __init__(self, dataframe):
        self._dataframe = dataframe

    @classmethod
    def from_dataframe(cls, dataframe):
        '''
        Reads the content from a dataframe.
        '''
        return cls(dataframe)

    def to_xml_string(self):
        '''
        Converts the dataframe to xml and gives the xml text back.
        '''
        xml = self.to_xml()
        return le.tostring(xml, pretty_print=True, encoding='unicode')

    def to_xml(self):
        '''
        Given a pandas dataframe with events returns QuakeML version of
        the catalog
        '''
        add_namespace = QuakeMLDataframe._add_namespace
        quakeml = le.Element(
            add_namespace('eventParameters'),
            publicID=QuakeMLDataframe._add_id_prefix('0')
        )
        # go through all events
        for i in range(len(self._dataframe)):
            quake = self._dataframe.iloc[i]
            event = le.SubElement(
                quakeml,
                add_namespace('event'),
                {
                    'publicID': QuakeMLDataframe._add_id_prefix(
                        str(quake.eventID))
                }
            )
            preferred_origin_id = le.SubElement(
                event,
                add_namespace('preferredOriginID')
            )
            preferred_origin_id.text = QuakeMLDataframe._add_id_prefix(
                str(quake.eventID)
            )
            preferred_magnitude_id = le.SubElement(
                event,
                add_namespace('preferredMagnitudeID')
            )
            preferred_magnitude_id.text = QuakeMLDataframe._add_id_prefix(
                str(quake.eventID)
            )
            qtype = le.SubElement(event, add_namespace('type'))
            qtype.text = 'earthquake'
            description = le.SubElement(event, add_namespace('description'))
            text = le.SubElement(description, add_namespace('text'))
            text.text = str(quake.type)
            # origin
            origin = le.SubElement(
                event,
                add_namespace('origin'),
                {
                    'publicID': QuakeMLDataframe._add_id_prefix(
                        str(quake.eventID)
                    )
                }
            )
            origin = QuakeMLDataframe._add_uncertain_child(
                origin,
                childname='time',
                value=QuakeMLDataframe._event2utc(quake),
                uncertainty=QuakeMLDataframe._format_xsdouble(
                    quake.timeUncertainty
                )
            )
            origin = QuakeMLDataframe._add_uncertain_child(
                origin,
                childname='latitude',
                value=str(quake.latitude),
                uncertainty=QuakeMLDataframe._format_xsdouble(
                    quake.latitudeUncertainty
                )
            )
            origin = QuakeMLDataframe._add_uncertain_child(
                origin,
                childname='longitude',
                value=str(quake.longitude),
                uncertainty=QuakeMLDataframe._format_xsdouble(
                    quake.longitudeUncertainty
                )
            )
            origin = QuakeMLDataframe._add_uncertain_child(
                origin,
                childname='depth',
                value=str(quake.depth),
                uncertainty=QuakeMLDataframe._format_xsdouble(
                    quake.depthUncertainty
                )
            )
            creation_info = le.SubElement(
                origin,
                add_namespace('creationInfo')
            )
            author = le.SubElement(creation_info, add_namespace('author'))
            author.text = quake.agency
            # originUncertainty
            origin_uncertainty = le.SubElement(
                origin,
                add_namespace('originUncertainty')
            )
            horizontal_uncertainty = le.SubElement(
                origin_uncertainty,
                add_namespace('horizontalUncertainty')
            )
            horizontal_uncertainty.text = QuakeMLDataframe._format_xsdouble(
                quake.horizontalUncertainty
            )
            min_horizontal_uncertainty = le.SubElement(
                origin_uncertainty,
                add_namespace('minHorizontalUncertainty')
            )
            min_horizontal_uncertainty.text = \
                QuakeMLDataframe._format_xsdouble(
                    quake.minHorizontalUncertainty
                )
            max_horizontal_uncertainty = le.SubElement(
                origin_uncertainty,
                add_namespace('maxHorizontalUncertainty')
            )
            max_horizontal_uncertainty.text = \
                QuakeMLDataframe._format_xsdouble(
                    quake.maxHorizontalUncertainty
                )
            azimuth_max_horizontal_uncertainty = le.SubElement(
                origin_uncertainty,
                add_namespace('azimuthMaxHorizontalUncertainty')
            )
            azimuth_max_horizontal_uncertainty.text = \
                QuakeMLDataframe._format_xsdouble(
                    quake.azimuthMaxHorizontalUncertainty
                )
            # magnitude
            magnitude = le.SubElement(
                event,
                add_namespace('magnitude'),
                {
                    'publicID': QuakeMLDataframe._add_id_prefix(
                        str(quake.eventID)
                    )
                }
            )
            magnitude = QuakeMLDataframe._add_uncertain_child(
                magnitude,
                childname='mag',
                value=str(quake.magnitude),
                uncertainty=QuakeMLDataframe._format_xsdouble(
                    quake.magnitudeUncertainty
                )
            )
            mtype = le.SubElement(magnitude, add_namespace('type'))
            mtype.text = 'MW'
            creation_info = le.SubElement(
                magnitude,
                add_namespace('creationInfo')
            )
            author = le.SubElement(creation_info, add_namespace('author'))
            author.text = quake.agency
            # plane (write only fault plane not auxilliary)
            focal_mechanism = le.SubElement(
                event,
                add_namespace('focalMechanism'),
                {
                    'publicID': QuakeMLDataframe._add_id_prefix(
                        str(quake.eventID)
                    )
                }
            )
            nodal_planes = le.SubElement(
                focal_mechanism,
                add_namespace('nodalPlanes'),
                {
                    'preferredPlane': '1'
                }
            )
            nodal_plane1 = le.SubElement(
                nodal_planes,
                add_namespace('nodalPlane1')
            )
            nodal_plane1 = QuakeMLDataframe._add_uncertain_child(
                nodal_plane1,
                childname='strike',
                value=str(quake.strike),
                uncertainty=QuakeMLDataframe._format_xsdouble(
                    quake.strikeUncertainty
                )
            )
            nodal_plane1 = QuakeMLDataframe._add_uncertain_child(
                nodal_plane1,
                childname='dip',
                value=str(quake.dip),
                uncertainty=QuakeMLDataframe._format_xsdouble(
                    quake.dipUncertainty
                )
            )
            nodal_plane1 = QuakeMLDataframe._add_uncertain_child(
                nodal_plane1,
                childname='rake',
                value=str(quake.rake),
                uncertainty=QuakeMLDataframe._format_xsdouble(
                    quake.rakeUncertainty
                )
            )

        return quakeml

    @staticmethod
    def _add_uncertain_child(parent, childname, value, uncertainty):
        '''
        Adds an uncertain child with value/uncertainty pair
        '''
        add_namespace = QuakeMLDataframe._add_namespace
        child = le.SubElement(parent, add_namespace(childname))
        val = le.SubElement(child, add_namespace('value'))
        val.text = str(value)
        unc = le.SubElement(child, add_namespace('uncertainty'))
        unc.text = str(uncertainty)
        return parent

    @staticmethod
    def _add_id_prefix(element):
        '''
        Adds an id prefix if necessary.
        '''
        id_prefix = 'quakeml:quakeledger/'
        if element.startswith(id_prefix):
            return element
        return id_prefix + element

    @staticmethod
    def _format_xsdouble(value):
        '''
        Converts the value for a xsdouble field
        to a number or NaN.
        '''
        if value is None or math.isnan(value):
            return 'NaN'

        return str(value)

    @staticmethod
    def _event2utc(event):
        '''
        given event returns UTC string
        '''
        date = event.fillna(0)
        return '{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:09f}Z'.format(
            int(date.year),
            int(max(date.month, 1)),
            int(max(date.day, 1)),
            int(date.hour),
            int(date.minute),
            date.second
        )


class Shakemap(UtcToEventMixin):
    def __init__(self, shakeml, x_column='LON', y_column='LAT'):
        self._shakeml = shakeml
        self._x_column = x_column
        self._y_column = y_column

    @classmethod
    def from_xml(cls, shakemap_xml):
        return cls(shakemap_xml)

    def to_intensity_geodataframe(self):
        dataframe = self.to_intensity_dataframe()
        geodataframe = gpd.GeoDataFrame(
            dataframe,
            geometry=gpd.points_from_xy(
                dataframe[self._x_column],
                dataframe[self._y_column]
            )
        )
        return geodataframe

    def to_intensity_dataframe(self):
        '''
        Converts the intensities to
        a dataframe.
        '''

        shakeml = self._shakeml
        nsmap = shakeml.nsmap

        #columns
        grid_fields = shakeml.findall('grid_field',namespaces = nsmap)

        #indices (start at 1) & argsort them
        column_idxs = [int(grid_field.attrib['index'])-1 for grid_field in grid_fields]
        idxs_sorted = np.argsort(column_idxs)
        column_names = [grid_field.attrib['name'] for grid_field in grid_fields]
        columns = [column_names[idx] for idx in idxs_sorted]

        grid_data = shakeml.find('grid_data',namespaces = nsmap)

        data_dict = collections.defaultdict(list)
        tokens = tokenize.tokenize(
            io.BytesIO(
                grid_data.text.encode('utf-8')
            ).readline
        )
        index = 0
        token_before = None
        for token in tokens:
            # 2 is number
            if token.type == 2:
                if index >= len(column_names):
                    index = 0
                name = column_names[index]
                if name not in (self._x_column, self._y_column):
                    name = 'value_' + name
                value = float(token.string)
                if token_before is not None and token_before.string == '-':
                    value = -1 * value
                data_dict[name].append(value)
                index += 1
            token_before = token

        #get grid
        grid_data = pd.DataFrame(data_dict)

        #get units
        for grid_field in grid_fields:
            unit_name = grid_field.attrib['name']
            unit_value = grid_field.attrib['units']
            if unit_name not in (self._x_column, self._y_column):
                grid_data['unit_' + unit_name] = unit_value
        return grid_data

    def to_intensity_raster(self, value_column):
        dataframe = self.to_intensity_dataframe()
        return Shakemap.dataframe2raster(
            dataframe,
            self._x_column,
            self._y_column,
            value_column,
        )

    @staticmethod
    def dataframe2raster(dataframe, x_column, y_column, value_column):
        # the following code works as long as the grid
        # is regular
        # it will not work if the grid is irregular
        sorted_x_values = sorted(set(dataframe[x_column]))
        sorted_y_values = sorted(set(dataframe[y_column]))

        x_cell_size = np.mean(np.diff(sorted_x_values))
        y_cell_size = np.mean(np.diff(sorted_y_values))

        map_x_values = {}
        for index, x_value in enumerate(sorted_x_values):
            map_x_values[x_value] = index
        map_y_values = {}
        for index, y_value in enumerate(sorted_y_values):
            map_y_values[y_value] = index

        intermediate_dataframe = pd.DataFrame({
            'value': dataframe[value_column]
        })

        intermediate_dataframe['x'] = dataframe[x_column].apply(lambda x: map_x_values[x])
        intermediate_dataframe['y'] = dataframe[y_column].apply(lambda y: map_y_values[y])

        raster = gr.from_pandas(intermediate_dataframe, value='value', x='x', y='y')
        raster.bounds = (
            dataframe[x_column].min(),
            dataframe[y_column].min(),
            dataframe[x_column].max(),
            dataframe[y_column].max()
        )
        raster.x_cell_size = x_cell_size
        raster.y_cell_size = y_cell_size
        # TODO
        # check if this handling is enough
        # to make this work for the raster conversion
        return raster




