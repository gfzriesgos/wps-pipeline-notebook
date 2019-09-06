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

from osgeo import osr


def _add_quakeml_namespace(element):
    '''
    Adds the namespace to the quakeml xml elements.
    '''
    return '{http://quakeml.org/xmlns/bed/1.2}' + element


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


class QuakeML():
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
                _add_quakeml_namespace('value')))
        uncertainty = QuakeML._as_float(
            parent.find(childname).findtext(
                _add_quakeml_namespace('uncertainty')))
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

    @staticmethod
    def _fill_series_from_origin_time(series, origin):
        # time
        year, month, day, hour, minute, second = _utc2event(
            origin.find(_add_quakeml_namespace('time')).findtext(
                _add_quakeml_namespace('value')))
        series.year = year
        series.month = month
        series.day = day
        series.hour = hour
        series.minute = minute
        series.second = second

        series.timeUncertainty = float(origin.find(
            _add_quakeml_namespace('time')).findtext(
                _add_quakeml_namespace('uncertainty')))

    @staticmethod
    def _fill_series_from_origin(series, origin):
        QuakeML._fill_series_from_origin_time(series, origin)
        # latitude/longitude/depth
        latitude, latitude_uncertainty = QuakeML._get_uncertain_child(
            origin, _add_quakeml_namespace('latitude'))

        series.latitude = latitude
        series.latitudeUncertainty = latitude_uncertainty

        longitude, longitude_uncertainty = QuakeML._get_uncertain_child(
            origin, _add_quakeml_namespace('longitude'))

        series.longitude = longitude
        series.longitudeUncertainty = longitude_uncertainty

        depth, depth_uncertainty = QuakeML._get_uncertain_child(
            origin, _add_quakeml_namespace('depth'))

        series.depth = depth
        series.depthUncertainty = depth_uncertainty

        # agency/provider
        series.agency = origin.find(
            _add_quakeml_namespace('creationInfo')).findtext(
                _add_quakeml_namespace('author'))
        QuakeML._fill_series_from_origin_uncertainty(
            series,
            origin.find(
                _add_quakeml_namespace('originUncertainty')
            )
        )

    @staticmethod
    def _fill_series_from_origin_uncertainty(series, origin_uncertainty):
        series.horizontalUncertainty = QuakeML._as_float(
            origin_uncertainty.find(
                _add_quakeml_namespace('horizontalUncertainty')).findtext(
                    _add_quakeml_namespace('value')))
        series.minHorizontalUncertainty = QuakeML._as_float(
            origin_uncertainty.find(_add_quakeml_namespace(
                'minHorizontalUncertainty')).findtext(
                    _add_quakeml_namespace('value')))
        series.maxHorizontalUncertainty = QuakeML._as_float(
            origin_uncertainty.find(_add_quakeml_namespace(
                'maxHorizontalUncertainty')).findtext(
                    _add_quakeml_namespace('value')))
        series.horizontalUncertainty = QuakeML._as_float(
            origin_uncertainty.find(_add_quakeml_namespace(
                'azimuthMaxHorizontalUncertainty')).findtext(
                    _add_quakeml_namespace('value')))

    @staticmethod
    def _fill_series_from_magnitude(series, magnitude):
        mag_value, mag_uncertainty = QuakeML._get_uncertain_child(
            magnitude, _add_quakeml_namespace('mag'))

        series.magnitude = mag_value
        series.magnitudeUncertainty = mag_uncertainty

    @staticmethod
    def _fill_series_from_nodal_planes(series, nodal_planes):
        preferred_plane = nodal_planes.get('preferredPlane')
        preferred_plane = nodal_planes.find(_add_quakeml_namespace(
            'nodalPlane' + preferred_plane))
        # GET uncertain child!!
        strike, strike_uncertainty = QuakeML._get_uncertain_child(
            preferred_plane, _add_quakeml_namespace('strike'))

        series.strike = strike
        series.strikeUncertainty = strike_uncertainty

        dip, dip_uncertainty = QuakeML._get_uncertain_child(
            preferred_plane, _add_quakeml_namespace('dip'))

        series.dip = dip
        series.dipUncertainty = dip_uncertainty

        rake, rake_uncertainty = QuakeML._get_uncertain_child(
            preferred_plane, _add_quakeml_namespace('rake'))

        series.rake = rake
        series.rake_uncertainty = rake_uncertainty

    @staticmethod
    def _fill_series(series, event):
        # get ID
        series.eventID = event.attrib['publicID']
        # type
        series.type = event.find(
            _add_quakeml_namespace('description')).findtext(
                _add_quakeml_namespace('text'))

        QuakeML._fill_series_from_origin(
            series,
            event.find(
                _add_quakeml_namespace(
                    'origin'
                )
            )
        )
        QuakeML._fill_series_from_magnitude(
            series,
            event.find(
                _add_quakeml_namespace(
                    'magnitude'
                )
            )
        )
        QuakeML._fill_series_from_nodal_planes(
            series,
            event.find(
                _add_quakeml_namespace('focalMechanism')
            ).find(
                _add_quakeml_namespace('nodalPlanes')
            )
        )

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
            QuakeML._fill_series(catalog.iloc[i], event)
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


class QuakeMLDataframe():
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

    @staticmethod
    def _add_focal_mechanism_element(event, quake):
        # plane (write only fault plane not auxilliary)
        focal_mechanism = le.SubElement(
            event,
            _add_quakeml_namespace('focalMechanism'),
            {
                'publicID': QuakeMLDataframe._add_id_prefix(
                    str(quake.eventID)
                )
            }
        )
        nodal_planes = le.SubElement(
            focal_mechanism,
            _add_quakeml_namespace('nodalPlanes'),
            {
                'preferredPlane': '1'
            }
        )
        nodal_plane1 = le.SubElement(
            nodal_planes,
            _add_quakeml_namespace('nodalPlane1')
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

    @staticmethod
    def _add_origin_element(event, quake):
        # origin
        origin = le.SubElement(
            event,
            _add_quakeml_namespace('origin'),
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
            _add_quakeml_namespace('creationInfo')
        )
        author = le.SubElement(creation_info, _add_quakeml_namespace('author'))
        author.text = quake.agency
        # originUncertainty
        origin_uncertainty = le.SubElement(
            origin,
            _add_quakeml_namespace('originUncertainty')
        )
        horizontal_uncertainty = le.SubElement(
            origin_uncertainty,
            _add_quakeml_namespace('horizontalUncertainty')
        )
        horizontal_uncertainty.text = QuakeMLDataframe._format_xsdouble(
            quake.horizontalUncertainty
        )
        min_horizontal_uncertainty = le.SubElement(
            origin_uncertainty,
            _add_quakeml_namespace('minHorizontalUncertainty')
        )
        min_horizontal_uncertainty.text = \
            QuakeMLDataframe._format_xsdouble(
                quake.minHorizontalUncertainty
            )
        max_horizontal_uncertainty = le.SubElement(
            origin_uncertainty,
            _add_quakeml_namespace('maxHorizontalUncertainty')
        )
        max_horizontal_uncertainty.text = \
            QuakeMLDataframe._format_xsdouble(
                quake.maxHorizontalUncertainty
            )
        azimuth_max_horizontal_uncertainty = le.SubElement(
            origin_uncertainty,
            _add_quakeml_namespace('azimuthMaxHorizontalUncertainty')
        )
        azimuth_max_horizontal_uncertainty.text = \
            QuakeMLDataframe._format_xsdouble(
                quake.azimuthMaxHorizontalUncertainty
            )

    @staticmethod
    def _add_magnitude_element(event, quake):
        # magnitude
        magnitude = le.SubElement(
            event,
            _add_quakeml_namespace('magnitude'),
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
        mtype = le.SubElement(magnitude, _add_quakeml_namespace('type'))
        mtype.text = 'MW'
        creation_info = le.SubElement(
            magnitude,
            _add_quakeml_namespace('creationInfo')
        )
        author = le.SubElement(creation_info, _add_quakeml_namespace('author'))
        author.text = quake.agency

    def to_xml(self):
        '''
        Given a pandas dataframe with events returns QuakeML version of
        the catalog
        '''
        add_namespace = _add_quakeml_namespace
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
            QuakeMLDataframe._add_origin_element(event, quake)
            QuakeMLDataframe._add_magnitude_element(event, quake)
            QuakeMLDataframe._add_focal_mechanism_element(event, quake)

        return quakeml

    @staticmethod
    def _add_uncertain_child(parent, childname, value, uncertainty):
        '''
        Adds an uncertain child with value/uncertainty pair
        '''
        add_namespace = _add_quakeml_namespace
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


class Shakemap():
    '''
    Class for accessing the shakemap data.
    '''
    def __init__(self, shakeml, x_column='LON', y_column='LAT'):
        self._shakeml = shakeml
        self._x_column = x_column
        self._y_column = y_column

    @classmethod
    def from_xml(cls, shakemap_xml):
        '''
        Constructs the instane from an xml element.
        '''
        return cls(shakemap_xml)

    def to_intensity_geodataframe(self):
        '''
        Returns the concent of the intensity map
        as a geodataframe.
        '''
        dataframe = self.to_intensity_dataframe()
        geodataframe = gpd.GeoDataFrame(
            dataframe,
            geometry=gpd.points_from_xy(
                dataframe[self._x_column],
                dataframe[self._y_column]
            )
        )
        return geodataframe

    @staticmethod
    def _extract_numbers_from_grid(grid_data):
        tokens = tokenize.tokenize(
            io.BytesIO(
                grid_data.text.encode('utf-8')
            ).readline
        )
        token_before = None
        for token in tokens:
            # number
            if token.type == 2:
                value = float(token.string)
                if token_before is not None and token_before.string == '-':
                    value = -1 * value
                yield value
            token_before = token

    def _grid_to_data_dict(self, grid_data, column_names, value_column_prefix):
        data_dict = collections.defaultdict(list)

        index = 0
        for value in Shakemap._extract_numbers_from_grid(grid_data):
            # 2 is number
            if index >= len(column_names):
                index = 0
            name = column_names[index]
            if name not in (self._x_column, self._y_column):
                name = value_column_prefix + name
            data_dict[name].append(value)
            index += 1
        return data_dict

    def _grid_to_dataframe(self, grid_data, column_names, value_column_prefix):
        data_dict = self._grid_to_data_dict(
            grid_data,
            column_names,
            value_column_prefix
        )
        return pd.DataFrame(data_dict)

    def to_xml_string(self):
        '''
        Returns the xml as a string.
        '''
        xml = self.to_xml()
        return le.tostring(xml, pretty_print=True, encoding='unicode')

    def to_xml(self):
        '''
        Returns the data as xml structure.
        '''
        return self._shakeml

    def to_event_geodataframe_or_none(self):
        '''
        Returns the event in a geodataframe
        or returns None if there is no data about
        the event.
        '''
        series = self.to_event_series_or_none()
        if series is None:
            return None
        dataframe = pd.DataFrame([series])
        geodataframe = gpd.GeoDataFrame(
            dataframe,
            geometry=gpd.points_from_xy(
                dataframe['longitude'],
                dataframe['latitude']
            )
        )
        return geodataframe

    def to_event_series_or_none(self):
        '''
        Returns a dataframe with the event
        data.
        '''
        nsmap = self._shakeml.nsmap
        event = self._shakeml.find('event', namespaces=nsmap)

        if event is None:
            return None

        index = [i for i in range(max(1, len(event)))]
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
            'timeError',
            'longitude',
            'latitude',
            'SemiMajor90',
            'SemiMinor90',
            'ErrorStrike',
            'depth',
            'depthError',
            'magnitude',
            'sigmaMagnitude',
            'rake',
            'dip',
            'strike',
            'type',
            'probability',
            'fuzzy',
        ]
        result_df = pd.DataFrame(index=index, columns=columns)
        result_df['eventID'] = event.attrib['event_id']
        result_df['agency'] = event.attrib['event_network']
        year, month, day, hour, minute, second = \
            _utc2event(event.attrib['event_timestamp'])
        result_df['year'] = year
        result_df['month'] = month
        result_df['day'] = day
        result_df['hour'] = hour
        result_df['minute'] = minute
        result_df['second'] = second
        result_df['depth'] = float(event.attrib['depth'])
        result_df['magnitude'] = float(event.attrib['magnitude'])
        result_df['longitude'] = float(event.attrib['lon'])
        result_df['latitude'] = float(event.attrib['lat'])
        result_df['type'] = self._shakeml.attrib['shakemap_event_type']

        return result_df.iloc[0]

    def to_intensity_dataframe(self):
        '''
        Converts the intensities to
        a dataframe.
        '''

        shakeml = self._shakeml
        nsmap = shakeml.nsmap

        # columns
        grid_fields = shakeml.findall('grid_field', namespaces=nsmap)

        # indices (start at 1) & argsort them
        column_idxs = [
            int(grid_field.attrib['index']) - 1
            for grid_field in grid_fields
        ]
        idxs_sorted = np.argsort(column_idxs)
        column_names = [
            grid_field.attrib['name']
            for grid_field in grid_fields
        ]
        columns = [column_names[idx] for idx in idxs_sorted]

        # get grid
        grid_data = self._grid_to_dataframe(
            shakeml.find('grid_data', namespaces=nsmap),
            columns,
            'value_'
        )

        # get units
        for grid_field in grid_fields:
            unit_name = grid_field.attrib['name']
            unit_value = grid_field.attrib['units']
            if unit_name not in (self._x_column, self._y_column):
                grid_data['unit_' + unit_name] = unit_value
        return grid_data

    def to_intensity_raster(self, value_column):
        '''
        Returns the shakemap intensities as a raster.
        '''
        dataframe = self.to_intensity_dataframe()
        return Shakemap.dataframe2raster(
            dataframe,
            self._x_column,
            self._y_column,
            value_column,
        )

    @staticmethod
    def _map_to_integers_and_get_old_cell_size(series):
        sorted_values = sorted(set(series))

        cell_size = np.mean(np.diff(sorted_values))

        map_values = {}
        for index, value in enumerate(sorted_values):
            map_values[value] = index

        mapped_series = series.apply(lambda x: map_values[x])

        return mapped_series, cell_size

    @staticmethod
    def dataframe2raster(dataframe, x_column, y_column, value_column):
        '''
        Converts the dataframe to a raster.
        Please note: this works only for
        regular grids at the moment.
        '''
        intermediate_dataframe = pd.DataFrame({
            'value': dataframe[value_column]
        })

        intermediate_dataframe['x'], x_cell_size = \
            Shakemap._map_to_integers_and_get_old_cell_size(
                dataframe[x_column]
            )
        intermediate_dataframe['y'], y_cell_size = \
            Shakemap._map_to_integers_and_get_old_cell_size(
                dataframe[y_column]
            )

        raster = gr.from_pandas(
            intermediate_dataframe,
            value='value',
            x='x',
            y='y'
        )
        raster.bounds = (
            dataframe[x_column].min(),
            dataframe[y_column].min(),
            dataframe[x_column].max(),
            dataframe[y_column].max()
        )
        raster.x_cell_size = np.abs(x_cell_size)
        raster.y_cell_size = -1 * np.abs(y_cell_size)
        proj = osr.SpatialReference()
        proj.ImportFromEPSG(4326)
        raster.projection = proj
        raster.xmin = raster.bounds[0]
        raster.xmax = raster.bounds[2]
        raster.ymin = raster.bounds[1]
        raster.ymax = raster.bounds[3]
        raster.geot = (
            # first one is the minimum x
            raster.xmin,
            # then the x_cell_size
            raster.x_cell_size,
            0,
            # then the hights possible y
            raster.ymax,
            0,
            # and the y cell size
            raster.y_cell_size
        )
        return raster
