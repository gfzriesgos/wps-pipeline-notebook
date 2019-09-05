#!/usr/bin/env python3

'''
This is the test file
for all of the conversion
library related python code.

To run the tests use pytest.
'''

import math

import lxml.etree as le

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
    dataframe = gfzwpsformatconversions.quakeml2df(xml)

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
