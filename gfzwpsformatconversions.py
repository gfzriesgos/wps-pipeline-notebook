#!/usr/bin/env python3

'''
This is a module
for format conversions
of wps in- and output data
in the riesgos project for
services provided by the GFZ.
'''

import math

import lxml.etree as le
import pandas as pd


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
                QuakeML._add_namespace('value')))
        uncertainty = QuakeML._as_float(
            parent.find(childname).findtext(
                QuakeML._add_namespace('uncertainty')))
        return [value, uncertainty]

    @staticmethod
    def _add_namespace(element):
        '''
        Adds the namespace to the quakeml xml elements.
        '''
        return '{http://quakeml.org/xmlns/bed/1.2}' + element

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


# the skeleton of the code is from here:
# https://raw.githubusercontent.com/gfzriesgos/quakeledger/master/quakeml.py
# (the code there may be replaced by using this file later)
def quakeml2df(quakeml_xml):
    '''
    Transforms the xml of a quakeml file to a data frame.
    '''
    quakeml = QuakeML.from_xml(quakeml_xml)
    return quakeml.to_dataframe()
