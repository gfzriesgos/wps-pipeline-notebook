#!/usr/bin/env python3

'''
This is the test file
for all of the conversion
library related python code.

To run the tests use pytest.
'''

import math

import lxml.etree as le
import pandas as pd

import gfzwpsformatconversions


def test_quakeml2df():
    '''
    Tests the conversion of quakeml xml data to a dataframe.
    '''
    raw_xml = b'''
    <eventParameters
        xmlns="http://quakeml.org/xmlns/bed/1.2"
        publicID="quakeml:quakeledger/0">
    <event publicID="quakeml:quakeledger/CHOA_116">
        <preferredOriginID>quakeml:quakeledger/CHOA_116</preferredOriginID>
        <preferredMagnitudeID>quakeml:quakeledger/CHOA_116</preferredMagnitudeID>
        <type>earthquake</type>
        <description> <text>expert</text> </description>
        <origin publicID="quakeml:quakeledger/CHOA_116"> <time>
                <value>2018-01-02T03:04:05.000000Z</value>
                <uncertainty>NaN</uncertainty>
            </time>
            <latitude>
                <value>-29.9883</value>
                <uncertainty>NaN</uncertainty>
            </latitude>
            <longitude>
                <value>-71.611</value>
                <uncertainty>NaN</uncertainty>
            </longitude>
            <depth>
                <value>32.0</value>
                <uncertainty>NaN</uncertainty>
            </depth>
            <creationInfo>
                <author>GFZ</author>
            </creationInfo>
            <originUncertainty>
                <horizontalUncertainty>NaN</horizontalUncertainty>
                <minHorizontalUncertainty>NaN</minHorizontalUncertainty>
                <maxHorizontalUncertainty>NaN</maxHorizontalUncertainty>
                <azimuthMaxHorizontalUncertainty>NaN</azimuthMaxHorizontalUncertainty>
            </originUncertainty>
        </origin>
        <magnitude publicID="quakeml:quakeledger/CHOA_116">
            <mag>
                <value>8.5</value>
                <uncertainty>NaN</uncertainty>
            </mag>
            <type>MW</type>
            <creationInfo>
                <author>GFZ</author>
            </creationInfo>
        </magnitude>
        <focalMechanism publicID="quakeml:quakeledger/CHOA_116">
            <nodalPlanes preferredPlane="1">
                <nodalPlane1> <strike>
                        <value>9.0</value>
                        <uncertainty>NaN</uncertainty>
                    </strike>
                    <dip>
                        <value>18.0</value>
                        <uncertainty>NaN</uncertainty>
                    </dip>
                    <rake>
                        <value>90.0</value>
                        <uncertainty>NaN</uncertainty>
                    </rake>
                </nodalPlane1>
            </nodalPlanes>
        </focalMechanism>
    </event>
    <event publicID="quakeml:quakeledger/CHOA_117">
        <preferredOriginID>quakeml:quakeledger/CHOA_117</preferredOriginID>
        <preferredMagnitudeID>quakeml:quakeledger/CHOA_117</preferredMagnitudeID>
        <type>earthquake</type>
        <description> <text>expert</text> </description>
        <origin publicID="quakeml:quakeledger/CHOA_117"> <time>
                <value>2018-01-01T00:00:00.000000Z</value>
                <uncertainty>NaN</uncertainty>
            </time>
            <latitude>
                <value>-30.4319</value>
                <uncertainty>NaN</uncertainty>
            </latitude>
            <longitude>
                <value>-71.6957</value>
                <uncertainty>NaN</uncertainty>
            </longitude>
            <depth>
                <value>32.0</value>
                <uncertainty>NaN</uncertainty>
            </depth>
            <creationInfo>
                <author>GFZ</author>
            </creationInfo>
            <originUncertainty>
                <horizontalUncertainty>NaN</horizontalUncertainty>
                <minHorizontalUncertainty>NaN</minHorizontalUncertainty>
                <maxHorizontalUncertainty>NaN</maxHorizontalUncertainty>
                <azimuthMaxHorizontalUncertainty>NaN</azimuthMaxHorizontalUncertainty>
            </originUncertainty>
        </origin>
        <magnitude publicID="quakeml:quakeledger/CHOA_117">
            <mag>
                <value>8.5</value>
                <uncertainty>NaN</uncertainty>
            </mag>
            <type>MW</type>
            <creationInfo>
                <author>GFZ</author>
            </creationInfo>
        </magnitude>
        <focalMechanism publicID="quakeml:quakeledger/CHOA_117">
            <nodalPlanes preferredPlane="1">
                <nodalPlane1> <strike>
                        <value>9.0</value>
                        <uncertainty>NaN</uncertainty>
                    </strike>
                    <dip>
                        <value>18.0</value>
                        <uncertainty>NaN</uncertainty>
                    </dip>
                    <rake>
                        <value>90.0</value>
                        <uncertainty>NaN</uncertainty>
                    </rake>
                </nodalPlane1>
            </nodalPlanes>
        </focalMechanism>
    </event>
    <event publicID="quakeml:quakeledger/CHOA_118">
        <preferredOriginID>quakeml:quakeledger/CHOA_118</preferredOriginID>
        <preferredMagnitudeID>quakeml:quakeledger/CHOA_118</preferredMagnitudeID>
        <type>earthquake</type>
        <description> <text>expert</text> </description>
        <origin publicID="quakeml:quakeledger/CHOA_118"> <time>
                <value>2018-01-01T00:00:00.000000Z</value>
                <uncertainty>NaN</uncertainty>
            </time>
            <latitude>
                <value>-30.8755</value>
                <uncertainty>NaN</uncertainty>
            </latitude>
            <longitude>
                <value>-71.7813</value>
                <uncertainty>NaN</uncertainty>
            </longitude>
            <depth>
                <value>32.0</value>
                <uncertainty>NaN</uncertainty>
            </depth>
            <creationInfo>
                <author>GFZ</author>
            </creationInfo>
            <originUncertainty>
                <horizontalUncertainty>NaN</horizontalUncertainty>
                <minHorizontalUncertainty>NaN</minHorizontalUncertainty>
                <maxHorizontalUncertainty>NaN</maxHorizontalUncertainty>
                <azimuthMaxHorizontalUncertainty>NaN</azimuthMaxHorizontalUncertainty>
            </originUncertainty>
        </origin>
        <magnitude publicID="quakeml:quakeledger/CHOA_118">
            <mag>
                <value>8.5</value>
                <uncertainty>NaN</uncertainty>
            </mag>
            <type>MW</type>
            <creationInfo>
                <author>GFZ</author>
            </creationInfo>
        </magnitude>
        <focalMechanism publicID="quakeml:quakeledger/CHOA_118">
            <nodalPlanes preferredPlane="1">
                <nodalPlane1> <strike>
                        <value>9.0</value>
                        <uncertainty>NaN</uncertainty>
                    </strike>
                    <dip>
                        <value>18.0</value>
                        <uncertainty>NaN</uncertainty>
                    </dip>
                    <rake>
                        <value>90.0</value>
                        <uncertainty>NaN</uncertainty>
                    </rake>
                </nodalPlane1>
            </nodalPlanes>
        </focalMechanism>
    </event>
    <event publicID="quakeml:quakeledger/CHOA_119">
        <preferredOriginID>quakeml:quakeledger/CHOA_119</preferredOriginID>
        <preferredMagnitudeID>quakeml:quakeledger/CHOA_119</preferredMagnitudeID>
        <type>earthquake</type>
        <description> <text>expert</text> </description>
        <origin publicID="quakeml:quakeledger/CHOA_119"> <time>
                <value>2018-01-01T00:00:00.000000Z</value>
                <uncertainty>NaN</uncertainty>
            </time>
            <latitude>
                <value>-31.3191</value>
                <uncertainty>NaN</uncertainty>
            </latitude>
            <longitude>
                <value>-71.8677</value>
                <uncertainty>NaN</uncertainty>
            </longitude>
            <depth>
                <value>32.0</value>
                <uncertainty>NaN</uncertainty>
            </depth>
            <creationInfo>
                <author>GFZ</author>
            </creationInfo>
            <originUncertainty>
                <horizontalUncertainty>NaN</horizontalUncertainty>
                <minHorizontalUncertainty>NaN</minHorizontalUncertainty>
                <maxHorizontalUncertainty>NaN</maxHorizontalUncertainty>
                <azimuthMaxHorizontalUncertainty>NaN</azimuthMaxHorizontalUncertainty>
            </originUncertainty>
        </origin>
        <magnitude publicID="quakeml:quakeledger/CHOA_119">
            <mag>
                <value>8.5</value>
                <uncertainty>NaN</uncertainty>
            </mag>
            <type>MW</type>
            <creationInfo>
                <author>GFZ</author>
            </creationInfo>
        </magnitude>
        <focalMechanism publicID="quakeml:quakeledger/CHOA_119">
            <nodalPlanes preferredPlane="1">
                <nodalPlane1> <strike>
                        <value>9.0</value>
                        <uncertainty>NaN</uncertainty>
                    </strike>
                    <dip>
                        <value>18.0</value>
                        <uncertainty>NaN</uncertainty>
                    </dip>
                    <rake>
                        <value>90.0</value>
                        <uncertainty>NaN</uncertainty>
                    </rake>
                </nodalPlane1>
            </nodalPlanes>
        </focalMechanism>
    </event>
    <event publicID="quakeml:quakeledger/CHOA_120">
        <preferredOriginID>quakeml:quakeledger/CHOA_120</preferredOriginID>
        <preferredMagnitudeID>quakeml:quakeledger/CHOA_120</preferredMagnitudeID>
        <type>earthquake</type>
        <description> <text>expert</text> </description>
        <origin publicID="quakeml:quakeledger/CHOA_120"> <time>
                <value>2018-01-01T00:00:00.000000Z</value>
                <uncertainty>NaN</uncertainty>
            </time>
            <latitude>
                <value>-31.7627</value>
                <uncertainty>NaN</uncertainty>
            </latitude>
            <longitude>
                <value>-71.955</value>
                <uncertainty>NaN</uncertainty>
            </longitude>
            <depth>
                <value>32.0</value>
                <uncertainty>NaN</uncertainty>
            </depth>
            <creationInfo>
                <author>GFZ</author>
            </creationInfo>
            <originUncertainty>
                <horizontalUncertainty>NaN</horizontalUncertainty>
                <minHorizontalUncertainty>NaN</minHorizontalUncertainty>
                <maxHorizontalUncertainty>NaN</maxHorizontalUncertainty>
                <azimuthMaxHorizontalUncertainty>NaN</azimuthMaxHorizontalUncertainty>
            </originUncertainty>
        </origin>
        <magnitude publicID="quakeml:quakeledger/CHOA_120">
            <mag>
                <value>8.5</value>
                <uncertainty>NaN</uncertainty>
            </mag>
            <type>MW</type>
            <creationInfo>
                <author>GFZ</author>
            </creationInfo>
        </magnitude>
        <focalMechanism publicID="quakeml:quakeledger/CHOA_120">
            <nodalPlanes preferredPlane="1">
                <nodalPlane1> <strike>
                        <value>9.0</value>
                        <uncertainty>NaN</uncertainty>
                    </strike>
                    <dip>
                        <value>18.0</value>
                        <uncertainty>NaN</uncertainty>
                    </dip>
                    <rake>
                        <value>90.0</value>
                        <uncertainty>NaN</uncertainty>
                    </rake>
                </nodalPlane1>
            </nodalPlanes>
        </focalMechanism>
    </event>
    <event publicID="quakeml:quakeledger/CHOA_121">
        <preferredOriginID>quakeml:quakeledger/CHOA_121</preferredOriginID>
        <preferredMagnitudeID>quakeml:quakeledger/CHOA_121</preferredMagnitudeID>
        <type>earthquake</type>
        <description> <text>expert</text> </description>
        <origin publicID="quakeml:quakeledger/CHOA_121"> <time>
                <value>2018-01-01T00:00:00.000000Z</value>
                <uncertainty>NaN</uncertainty>
            </time>
            <latitude>
                <value>-32.2063</value>
                <uncertainty>NaN</uncertainty>
            </latitude>
            <longitude>
                <value>-72.0433</value>
                <uncertainty>NaN</uncertainty>
            </longitude>
            <depth>
                <value>32.0</value>
                <uncertainty>NaN</uncertainty>
            </depth>
            <creationInfo>
                <author>GFZ</author>
            </creationInfo>
            <originUncertainty>
                <horizontalUncertainty>NaN</horizontalUncertainty>
                <minHorizontalUncertainty>NaN</minHorizontalUncertainty>
                <maxHorizontalUncertainty>NaN</maxHorizontalUncertainty>
                <azimuthMaxHorizontalUncertainty>NaN</azimuthMaxHorizontalUncertainty>
            </originUncertainty>
        </origin>
        <magnitude publicID="quakeml:quakeledger/CHOA_121">
            <mag>
                <value>8.5</value>
                <uncertainty>NaN</uncertainty>
            </mag>
            <type>MW</type>
            <creationInfo>
                <author>GFZ</author>
            </creationInfo>
        </magnitude>
        <focalMechanism publicID="quakeml:quakeledger/CHOA_121">
            <nodalPlanes preferredPlane="1">
                <nodalPlane1> <strike>
                        <value>9.0</value>
                        <uncertainty>NaN</uncertainty>
                    </strike>
                    <dip>
                        <value>18.0</value>
                        <uncertainty>NaN</uncertainty>
                    </dip>
                    <rake>
                        <value>90.0</value>
                        <uncertainty>NaN</uncertainty>
                    </rake>
                </nodalPlane1>
            </nodalPlanes>
        </focalMechanism>
    </event>
    <event publicID="quakeml:quakeledger/CHOA_110">
        <preferredOriginID>quakeml:quakeledger/CHOA_110</preferredOriginID>
        <preferredMagnitudeID>quakeml:quakeledger/CHOA_110</preferredMagnitudeID>
        <type>earthquake</type>
        <description> <text>expert</text> </description>
        <origin publicID="quakeml:quakeledger/CHOA_110"> <time>
                <value>2018-01-01T00:00:00.000000Z</value>
                <uncertainty>NaN</uncertainty>
            </time>
            <latitude>
                <value>-30.4383</value>
                <uncertainty>NaN</uncertainty>
            </latitude>
            <longitude>
                <value>-71.7235</value>
                <uncertainty>NaN</uncertainty>
            </longitude>
            <depth>
                <value>28.0</value>
                <uncertainty>NaN</uncertainty>
            </depth>
            <creationInfo>
                <author>GFZ</author>
            </creationInfo>
            <originUncertainty>
                <horizontalUncertainty>NaN</horizontalUncertainty>
                <minHorizontalUncertainty>NaN</minHorizontalUncertainty>
                <maxHorizontalUncertainty>NaN</maxHorizontalUncertainty>
                <azimuthMaxHorizontalUncertainty>NaN</azimuthMaxHorizontalUncertainty>
            </originUncertainty>
        </origin>
        <magnitude publicID="quakeml:quakeledger/CHOA_110">
            <mag>
                <value>8.0</value>
                <uncertainty>NaN</uncertainty>
            </mag>
            <type>MW</type>
            <creationInfo>
                <author>GFZ</author>
            </creationInfo>
        </magnitude>
        <focalMechanism publicID="quakeml:quakeledger/CHOA_110">
            <nodalPlanes preferredPlane="1">
                <nodalPlane1> <strike>
                        <value>9.0</value>
                        <uncertainty>NaN</uncertainty>
                    </strike>
                    <dip>
                        <value>18.0</value>
                        <uncertainty>NaN</uncertainty>
                    </dip>
                    <rake>
                        <value>90.0</value>
                        <uncertainty>NaN</uncertainty>
                    </rake>
                </nodalPlane1>
            </nodalPlanes>
        </focalMechanism>
    </event>
    <event publicID="quakeml:quakeledger/CHOA_111">
        <preferredOriginID>quakeml:quakeledger/CHOA_111</preferredOriginID>
        <preferredMagnitudeID>quakeml:quakeledger/CHOA_111</preferredMagnitudeID>
        <type>earthquake</type>
        <description> <text>expert</text> </description>
        <origin publicID="quakeml:quakeledger/CHOA_111"> <time>
                <value>2018-01-01T00:00:00.000000Z</value>
                <uncertainty>NaN</uncertainty>
            </time>
            <latitude>
                <value>-30.8819</value>
                <uncertainty>NaN</uncertainty>
            </latitude>
            <longitude>
                <value>-71.8082</value>
                <uncertainty>NaN</uncertainty>
            </longitude>
            <depth>
                <value>28.0</value>
                <uncertainty>NaN</uncertainty>
            </depth>
            <creationInfo>
                <author>GFZ</author>
            </creationInfo>
            <originUncertainty>
                <horizontalUncertainty>NaN</horizontalUncertainty>
                <minHorizontalUncertainty>NaN</minHorizontalUncertainty>
                <maxHorizontalUncertainty>NaN</maxHorizontalUncertainty>
                <azimuthMaxHorizontalUncertainty>NaN</azimuthMaxHorizontalUncertainty>
            </originUncertainty>
        </origin>
        <magnitude publicID="quakeml:quakeledger/CHOA_111">
            <mag>
                <value>8.0</value>
                <uncertainty>NaN</uncertainty>
            </mag>
            <type>MW</type>
            <creationInfo>
                <author>GFZ</author>
            </creationInfo>
        </magnitude>
        <focalMechanism publicID="quakeml:quakeledger/CHOA_111">
            <nodalPlanes preferredPlane="1">
                <nodalPlane1> <strike>
                        <value>9.0</value>
                        <uncertainty>NaN</uncertainty>
                    </strike>
                    <dip>
                        <value>18.0</value>
                        <uncertainty>NaN</uncertainty>
                    </dip>
                    <rake>
                        <value>90.0</value>
                        <uncertainty>NaN</uncertainty>
                    </rake>
                </nodalPlane1>
            </nodalPlanes>
        </focalMechanism>
    </event>
    <event publicID="quakeml:quakeledger/CHOA_112">
        <preferredOriginID>quakeml:quakeledger/CHOA_112</preferredOriginID>
        <preferredMagnitudeID>quakeml:quakeledger/CHOA_112</preferredMagnitudeID>
        <type>earthquake</type>
        <description> <text>expert</text> </description>
        <origin publicID="quakeml:quakeledger/CHOA_112"> <time>
                <value>2018-01-01T00:00:00.000000Z</value>
                <uncertainty>NaN</uncertainty>
            </time>
            <latitude>
                <value>-31.3255</value>
                <uncertainty>NaN</uncertainty>
            </latitude>
            <longitude>
                <value>-71.8938</value>
                <uncertainty>NaN</uncertainty>
            </longitude>
            <depth>
                <value>28.0</value>
                <uncertainty>NaN</uncertainty>
            </depth>
            <creationInfo>
                <author>GFZ</author>
            </creationInfo>
            <originUncertainty>
                <horizontalUncertainty>NaN</horizontalUncertainty>
                <minHorizontalUncertainty>NaN</minHorizontalUncertainty>
                <maxHorizontalUncertainty>NaN</maxHorizontalUncertainty>
                <azimuthMaxHorizontalUncertainty>NaN</azimuthMaxHorizontalUncertainty>
            </originUncertainty>
        </origin>
        <magnitude publicID="quakeml:quakeledger/CHOA_112">
            <mag>
                <value>8.0</value>
                <uncertainty>NaN</uncertainty>
            </mag>
            <type>MW</type>
            <creationInfo>
                <author>GFZ</author>
            </creationInfo>
        </magnitude>
        <focalMechanism publicID="quakeml:quakeledger/CHOA_112">
            <nodalPlanes preferredPlane="1">
                <nodalPlane1> <strike>
                        <value>9.0</value>
                        <uncertainty>NaN</uncertainty>
                    </strike>
                    <dip>
                        <value>18.0</value>
                        <uncertainty>NaN</uncertainty>
                    </dip>
                    <rake>
                        <value>90.0</value>
                        <uncertainty>NaN</uncertainty>
                    </rake>
                </nodalPlane1>
            </nodalPlanes>
        </focalMechanism>
    </event>
    <event publicID="quakeml:quakeledger/CHOA_113">
        <preferredOriginID>quakeml:quakeledger/CHOA_113</preferredOriginID>
        <preferredMagnitudeID>quakeml:quakeledger/CHOA_113</preferredMagnitudeID>
        <type>earthquake</type>
        <description> <text>expert</text> </description>
        <origin publicID="quakeml:quakeledger/CHOA_113"> <time>
                <value>2018-01-01T00:00:00.000000Z</value>
                <uncertainty>NaN</uncertainty>
            </time>
            <latitude>
                <value>-31.7691</value>
                <uncertainty>NaN</uncertainty>
            </latitude>
            <longitude>
                <value>-71.9802</value>
                <uncertainty>NaN</uncertainty>
            </longitude>
            <depth>
                <value>28.0</value>
                <uncertainty>NaN</uncertainty>
            </depth>
            <creationInfo>
                <author>GFZ</author>
            </creationInfo>
            <originUncertainty>
                <horizontalUncertainty>NaN</horizontalUncertainty>
                <minHorizontalUncertainty>NaN</minHorizontalUncertainty>
                <maxHorizontalUncertainty>NaN</maxHorizontalUncertainty>
                <azimuthMaxHorizontalUncertainty>NaN</azimuthMaxHorizontalUncertainty>
            </originUncertainty>
        </origin>
        <magnitude publicID="quakeml:quakeledger/CHOA_113">
            <mag>
                <value>8.0</value>
                <uncertainty>NaN</uncertainty>
            </mag>
            <type>MW</type>
            <creationInfo>
                <author>GFZ</author>
            </creationInfo>
        </magnitude>
        <focalMechanism publicID="quakeml:quakeledger/CHOA_113">
            <nodalPlanes preferredPlane="1">
                <nodalPlane1> <strike>
                        <value>9.0</value>
                        <uncertainty>NaN</uncertainty>
                    </strike>
                    <dip>
                        <value>18.0</value>
                        <uncertainty>NaN</uncertainty>
                    </dip>
                    <rake>
                        <value>90.0</value>
                        <uncertainty>NaN</uncertainty>
                    </rake>
                </nodalPlane1>
            </nodalPlanes>
        </focalMechanism>
    </event>
    <event publicID="quakeml:quakeledger/CHOA_114">
        <preferredOriginID>quakeml:quakeledger/CHOA_114</preferredOriginID>
        <preferredMagnitudeID>quakeml:quakeledger/CHOA_114</preferredMagnitudeID>
        <type>earthquake</type>
        <description> <text>expert</text> </description>
        <origin publicID="quakeml:quakeledger/CHOA_114"> <time>
                <value>2018-01-01T00:00:00.000000Z</value>
                <uncertainty>NaN</uncertainty>
            </time>
            <latitude>
                <value>-32.2127</value>
                <uncertainty>NaN</uncertainty>
            </latitude>
            <longitude>
                <value>-72.0675</value>
                <uncertainty>NaN</uncertainty>
            </longitude>
            <depth>
                <value>28.0</value>
                <uncertainty>NaN</uncertainty>
            </depth>
            <creationInfo>
                <author>GFZ</author>
            </creationInfo>
            <originUncertainty>
                <horizontalUncertainty>NaN</horizontalUncertainty>
                <minHorizontalUncertainty>NaN</minHorizontalUncertainty>
                <maxHorizontalUncertainty>NaN</maxHorizontalUncertainty>
                <azimuthMaxHorizontalUncertainty>NaN</azimuthMaxHorizontalUncertainty>
            </originUncertainty>
        </origin>
        <magnitude publicID="quakeml:quakeledger/CHOA_114">
            <mag>
                <value>8.0</value>
                <uncertainty>NaN</uncertainty>
            </mag>
            <type>MW</type>
            <creationInfo>
                <author>GFZ</author>
            </creationInfo>
        </magnitude>
        <focalMechanism publicID="quakeml:quakeledger/CHOA_114">
            <nodalPlanes preferredPlane="1">
                <nodalPlane1> <strike>
                        <value>9.0</value>
                        <uncertainty>NaN</uncertainty>
                    </strike>
                    <dip>
                        <value>18.0</value>
                        <uncertainty>NaN</uncertainty>
                    </dip>
                    <rake>
                        <value>90.0</value>
                        <uncertainty>NaN</uncertainty>
                    </rake>
                </nodalPlane1>
            </nodalPlanes>
        </focalMechanism>
    </event>
    <event publicID="quakeml:quakeledger/CHOA_115">
        <preferredOriginID>quakeml:quakeledger/CHOA_115</preferredOriginID>
        <preferredMagnitudeID>quakeml:quakeledger/CHOA_115</preferredMagnitudeID>
        <type>earthquake</type>
        <description> <text>expert</text> </description>
        <origin publicID="quakeml:quakeledger/CHOA_115"> <time>
                <value>2018-01-01T00:00:00.000000Z</value>
                <uncertainty>NaN</uncertainty>
            </time>
            <latitude>
                <value>-32.6563</value>
                <uncertainty>NaN</uncertainty>
            </latitude>
            <longitude>
                <value>-72.1558</value>
                <uncertainty>NaN</uncertainty>
            </longitude>
            <depth>
                <value>28.0</value>
                <uncertainty>NaN</uncertainty>
            </depth>
            <creationInfo>
                <author>GFZ</author>
            </creationInfo>
            <originUncertainty>
                <horizontalUncertainty>NaN</horizontalUncertainty>
                <minHorizontalUncertainty>NaN</minHorizontalUncertainty>
                <maxHorizontalUncertainty>NaN</maxHorizontalUncertainty>
                <azimuthMaxHorizontalUncertainty>NaN</azimuthMaxHorizontalUncertainty>
            </originUncertainty>
        </origin>
        <magnitude publicID="quakeml:quakeledger/CHOA_115">
            <mag>
                <value>8.0</value>
                <uncertainty>NaN</uncertainty>
            </mag>
            <type>MW</type>
            <creationInfo>
                <author>GFZ</author>
            </creationInfo>
        </magnitude>
        <focalMechanism publicID="quakeml:quakeledger/CHOA_115">
            <nodalPlanes preferredPlane="1">
                <nodalPlane1> <strike>
                        <value>9.0</value>
                        <uncertainty>NaN</uncertainty>
                    </strike>
                    <dip>
                        <value>18.0</value>
                        <uncertainty>NaN</uncertainty>
                    </dip>
                    <rake>
                        <value>90.0</value>
                        <uncertainty>NaN</uncertainty>
                    </rake>
                </nodalPlane1>
            </nodalPlanes>
        </focalMechanism>
    </event>
</eventParameters>
    '''

    xml = le.fromstring(raw_xml)
    dataframe = gfzwpsformatconversions.QuakeML.from_xml(xml).to_geodataframe()

    assert len(dataframe) == 12

    first_one = dataframe.iloc[0]
    assert first_one['eventID'] == 'quakeml:quakeledger/CHOA_116'
    assert first_one['type'] == 'expert'
    assert first_one['year'] == 2018
    assert first_one['month'] == 1
    assert first_one['day'] == 2
    assert first_one['hour'] == 3
    assert first_one['minute'] == 4
    assert first_one['second'] == 5
    assert math.isnan(first_one['timeUncertainty'])
    assert -29.99 < first_one['latitude'] < -29.98
    assert math.isnan(first_one['latitudeUncertainty'])
    assert -71.62 < first_one['longitude'] < -71.61
    assert math.isnan(first_one['longitudeUncertainty'])
    assert 31.9 < first_one['depth'] < 32.1
    assert first_one['agency'] == 'GFZ'
    assert 8.49 < first_one['magnitude'] < 8.51
    assert math.isnan(first_one['magnitudeUncertainty'])
    assert math.isnan(first_one['minHorizontalUncertainty'])
    assert math.isnan(first_one['maxHorizontalUncertainty'])
    assert math.isnan(first_one['horizontalUncertainty'])
    assert 8.9 < first_one['strike'] < 9.1
    assert math.isnan(first_one['strikeUncertainty'])
    assert 17.9 < first_one['dip'] < 18.1
    assert math.isnan(first_one['dipUncertainty'])
    assert 89.9 < first_one['rake'] < 90.1
    assert math.isnan(first_one['rakeUncertainty'])

    assert 'geometry' in dataframe.keys()

    assert -71.62 < first_one['geometry'].x < -71.6
    assert -29.99 < first_one['geometry'].y < 29.98


def test_quakemldf2xml():
    '''
    Tests the conversion from a quakeml dataframe
    back to xml.
    '''
    dataframe = pd.DataFrame({
        'eventID': [
            'quakeml:quakeledger/CHOA_122',
            'quakeml:quakeledger/CHOA_123'
        ],
        'agency': ['GFZ', 'GFZ'],
        'Identifier': [math.nan, math.nan],
        'year': [2018, 2018],
        'month': [1, 1],
        'day': [2, 1],
        'hour': [3, 0],
        'minute': [4, 0],
        'second': [5, 0],
        'timeUncertainty': [math.nan, math.nan],
        'longitude': [-71.2736, -71.3583],
        'longitudeUncertainty': [math.nan, math.nan],
        'latitude': [-28.6384, -29.082],
        'latitudeUncertainty': [math.nan, math.nan],
        'horizontalUncertainty': [math.nan, math.nan],
        'maxHorizontalUncertainty': [math.nan, math.nan],
        'minHorizontalUncertainty': [math.nan, math.nan],
        'azimuthMaxHorizontalUncertainty': [math.nan, math.nan],
        'depth': [43, 43],
        'depthUncertainty': [math.nan, math.nan],
        'magnitude': [9, 9],
        'magnitudeUncertainty': [math.nan, math.nan],
        'rake': [90, 90],
        'rakeUncertainty': [math.nan, math.nan],
        'dip': [18, 18],
        'dipUncertainty': [math.nan, math.nan],
        'strike': [9, 9],
        'strikeUncertainty': [math.nan, math.nan],
        'type': ['expert', 'expert'],
        'probability': [math.nan, math.nan],
    })

    assert len(dataframe) == 2

    xml = gfzwpsformatconversions.QuakeMLDataframe.from_dataframe(
        dataframe
    ).to_xml()

    assert len(xml) == 2

    xmlns = 'http://quakeml.org/xmlns/bed/1.2'

    first_one = xml[0]
    assert first_one.get('publicID') == 'quakeml:quakeledger/CHOA_122'
    assert first_one.find(
        '{' + xmlns + '}preferredOriginID'
    ).text == 'quakeml:quakeledger/CHOA_122'
    assert first_one.find(
        '{' + xmlns + '}preferredMagnitudeID'
    ).text == 'quakeml:quakeledger/CHOA_122'
    assert first_one.find('{' + xmlns + '}type').text == 'earthquake'
    assert first_one.find(
        '{' + xmlns + '}description'
    ).find('{' + xmlns + '}text').text == 'expert'

    first_origin = first_one.find('{' + xmlns + '}origin')

    assert first_origin.get('publicID') == 'quakeml:quakeledger/CHOA_122'
    assert first_origin.find(
        '{' + xmlns + '}time'
    ).find(
        '{' + xmlns + '}value'
    ).text == '2018-01-02T03:04:05.000000Z'
    assert first_origin.find(
        '{' + xmlns + '}time'
    ).find(
        '{' + xmlns + '}uncertainty'
    ).text == 'NaN'
    assert first_origin.find(
        '{' + xmlns + '}latitude'
    ).find('{' + xmlns + '}value').text == '-28.6384'
    assert first_origin.find(
        '{' + xmlns + '}latitude'
    ).find('{' + xmlns + '}uncertainty').text == 'NaN'
    assert first_origin.find(
        '{' + xmlns + '}longitude'
    ).find('{' + xmlns + '}value').text == '-71.2736'
    assert first_origin.find(
        '{' + xmlns + '}longitude'
    ).find('{' + xmlns + '}uncertainty').text == 'NaN'
    assert first_origin.find(
        '{' + xmlns + '}depth'
    ).find('{' + xmlns + '}value').text == '43'
    assert first_origin.find(
        '{' + xmlns + '}depth'
    ).find('{' + xmlns + '}uncertainty').text == 'NaN'

    first_origin_uncertainty = first_origin.find(
        '{' + xmlns + '}originUncertainty'
    )

    assert first_origin_uncertainty.find(
        '{' + xmlns + '}horizontalUncertainty'
    ).text == 'NaN'
    assert first_origin_uncertainty.find(
        '{' + xmlns + '}minHorizontalUncertainty'
    ).text == 'NaN'
    assert first_origin_uncertainty.find(
        '{' + xmlns + '}maxHorizontalUncertainty'
    ).text == 'NaN'
    assert first_origin_uncertainty.find(
        '{' + xmlns + '}azimuthMaxHorizontalUncertainty'
    ).text == 'NaN'

    first_magnitude = first_one.find('{' + xmlns + '}magnitude')

    assert first_magnitude.get('publicID') == 'quakeml:quakeledger/CHOA_122'
    assert first_magnitude.find(
        '{' + xmlns + '}mag'
    ).find('{' + xmlns + '}value').text == '9'
    assert first_magnitude.find(
        '{' + xmlns + '}mag'
    ).find('{' + xmlns + '}uncertainty').text == 'NaN'
    assert first_magnitude.find(
        '{' + xmlns + '}type'
    ).text == 'MW'
    assert first_magnitude.find(
        '{' + xmlns + '}creationInfo'
    ).find('{' + xmlns + '}author').text == 'GFZ'

    first_focal_mechanisms = first_one.find('{' + xmlns + '}focalMechanism')

    assert first_focal_mechanisms.get(
        'publicID'
    ) == 'quakeml:quakeledger/CHOA_122'

    first_nodal_planes = first_focal_mechanisms.find(
        '{' + xmlns + '}nodalPlanes'
    )

    assert first_nodal_planes.get('preferredPlane') == '1'

    first_nodal_plane1 = first_nodal_planes.find(
        '{' + xmlns + '}nodalPlane1'
    )

    assert first_nodal_plane1.find(
        '{' + xmlns + '}strike'
    ).find('{' + xmlns + '}value').text == '9'
    assert first_nodal_plane1.find(
        '{' + xmlns + '}strike'
    ).find('{' + xmlns + '}uncertainty').text == 'NaN'
    assert first_nodal_plane1.find(
        '{' + xmlns + '}dip'
    ).find('{' + xmlns + '}value').text == '18'
    assert first_nodal_plane1.find(
        '{' + xmlns + '}dip'
    ).find('{' + xmlns + '}uncertainty').text == 'NaN'
    assert first_nodal_plane1.find(
        '{' + xmlns + '}rake'
    ).find('{' + xmlns + '}value').text == '90'
    assert first_nodal_plane1.find(
        '{' + xmlns + '}rake'
    ).find('{' + xmlns + '}uncertainty').text == 'NaN'

    # and it should be possible to do the translation back to dataframe

    quakeml_instance = gfzwpsformatconversions.QuakeML.from_string(
        le.tostring(xml)
    )
    quakeml_instance.to_dataframe()
    # and again
    quakeml_instance = gfzwpsformatconversions.QuakeML.from_xml(xml)
    quakeml_instance.to_dataframe()
