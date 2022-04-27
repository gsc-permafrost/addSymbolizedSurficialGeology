# -*- coding: utf-8 -*-
"""
Codes and descriptions are from the GSC Surficial Geology Style Chart V2.3.14 (April 2018)

Author: rparker
Created: 2021-06-01
"""

import os
import sys
import arcpy
import shutil
import sqlite3
import json
import pandas as pd

scratch = r"C:\scratch"
os.makedirs(scratch, exist_ok=True)
arcpy.env.overwriteOutput = True

getCodeScript = """
import pandas as pd

def getCode(sg, tblPath):
    tbl = pd.read_csv(tblPath, index_col="Value")
    out = tbl.loc[sg, "Unnamed: 0"]
    return out
"""

sgCodes = {"3.01.15.001": "Isn",
           "3.01.15.002": "I",
           "3.01.14.715": "H",
           "3.01.02.011": "Owf",
           "3.01.02.013": "Owb",
           "3.01.02.015": "Ows",
           "3.01.02.023": "Ov",
           "3.01.02.025": "Ob",
           "3.01.02.012": "O",
           "3.01.03.295": "El",
           "3.01.03.299": "Er",
           "3.01.03.292": "Ev",
           "3.01.03.297": "E",
           "3.01.01.107": "Cf",
           "3.01.01.097": "Ca",
           "3.01.01.155": "Cz",
           "3.01.01.139": "Cg",
           "3.01.01.092": "Cv",
           "3.01.01.095": "Cb",
           "3.01.01.152": "C",
           "3.01.04.265": "Ap",
           "3.01.04.257": "Af",
           "3.01.04.255": "Ai",
           "3.01.04.269": "At",
           "3.01.04.252": "Av",
           "3.01.04.267": "Ab",
           "3.01.04.263": "A",
           "3.01.05.582": "Lr",
           "3.01.05.585": "Ld",
           "3.01.05.573": "Ln",
           "3.01.05.577": "Lo",
           "3.01.05.572": "Lv",
           "3.01.05.575": "Lb",
           "3.01.05.583": "L",
           "3.01.06.495": "Mt",
           "3.01.06.497": "Mr",
           "3.01.06.507": "Md",
           "3.01.06.492": "Mi",
           "3.01.06.493": "Mn",
           "3.01.06.509": "Mo",
           "3.01.06.502": "Mv",
           "3.01.06.505": "Mb",
           "3.01.06.503": "M",
           "3.01.09.487": "GMr",
           "3.01.09.525": "GMd",
           "3.01.09.512": "GMi",
           "3.01.09.513": "GMn",
           "3.01.09.519": "GMo",
           "3.01.09.527": "GMf",
           "3.01.09.517": "GMm",
           "3.01.09.483": "GMv",
           "3.01.09.485": "GMb",
           "3.01.09.515": "GM",
           "3.01.08.645": "GLr",
           "3.01.08.613": "GLd",
           "3.01.08.612": "GLn",
           "3.01.08.637": "GLo",
           "3.01.08.615": "GLf",
           "3.01.08.617": "GLm",
           "3.01.08.635": "GLh",
           "3.01.08.642": "GLv",
           "3.01.08.647": "GLb",
           "3.01.08.643": "GL",
           "3.01.07.249": "GFp",
           "3.01.07.237": "GFt",
           "3.01.07.225": "GFf",
           "3.01.07.215": "GFh",
           "3.01.07.217": "GFc",
           "3.01.07.219": "GFk",
           "3.01.07.229": "GFr",
           "3.01.07.223": "GFv",
           "3.01.07.247": "GFb",
           "3.01.07.235": "GF",
           "3.01.10.357": "Tg",
           "3.01.10.375": "Th",
           "3.01.10.377": "Tm",
           "3.01.10.385": "Tr",
           "3.01.10.387": "Ts",
           "3.01.10.439": "Tp",
           "3.01.10.057": "Tx",
           "3.01.10.355": "Tv",
           "3.01.10.359": "Tb",
           "3.01.10.373": "T",
           "3.01.11.175": "Wv",
           "3.01.11.169": "Wb",
           "3.01.11.177": "W",
           "3.01.16.705": "Vpy",
           "3.01.16.707": "V",
           "3.01.12.082": "U",
           "3.01.13.192": "R1",
           "3.01.13.187": "R2",
           "3.01.13.183": "R3",
           "3.01.13.185": "R"}

sgCodeDescriptions = {"3.01.15.001": "Glacier Ice or Snowpack: snowpacks",
                      "3.01.15.002": "Glacier Ice or Snowpack: Glacier-icefield-icecap",
                      "3.01.14.715": "Anthropogenic deposits: undifferentiated",
                      "3.01.02.011": "Organic deposits: fen",
                      "3.01.02.013": "Organic deposits: bog",
                      "3.01.02.015": "Organic deposits: salt marsh",
                      "3.01.02.023": "Organic deposits: veneer",
                      "3.01.02.025": "Organic deposits: blanket",
                      "3.01.02.012": "Organic deposits: undifferentiated",
                      "3.01.03.295": "Eolian sediments: loess",
                      "3.01.03.299": "Eolian sediments: dunes",
                      "3.01.03.292": "Eolian sediments: veneer",
                      "3.01.03.297": "Eolian sediments: undifferentiated",
                      "3.01.01.107": "Colluvial and Mass-wasting deposits",
                      "3.01.01.097": "Colluvial and Mass-wasting deposits: apron or talus scree",
                      "3.01.01.155": "Colluvial and Mass-wasting deposits: landslide",
                      "3.01.01.139": "Colluvial and Mass-wasting deposits: rock-glacier",
                      "3.01.01.092": "Colluvial and Mass-wasting deposits: veneer",
                      "3.01.01.095": "Colluvial and Mass-wasting deposits: blanket",
                      "3.01.01.152": "Colluvial and Mass-wasting deposits: undifferentiated",
                      "3.01.04.265": "Alluvial sediments: floodplain",
                      "3.01.04.257": "Alluvial sediments: fan",
                      "3.01.04.255": "Alluvial sediments: intertidal or estuarine",
                      "3.01.04.269": "Alluvial sediments: terraced",
                      "3.01.04.252": "Alluvial sediments: veneer",
                      "3.01.04.267": "Alluvial sediments: blanket",
                      "3.01.04.263": "Alluvial sediments: undifferentiated",
                      "3.01.05.582": "Lacustrine sediments: beach",
                      "3.01.05.585": "Lacustrine sediments: deltaic",
                      "3.01.05.573": "Lacustrine sediments: littoral and nearshore",
                      "3.01.05.577": "Lacustrine sediments: offshore",
                      "3.01.05.572": "Lacustrine sediments: veneer",
                      "3.01.05.575": "Lacustrine sediments: blanket",
                      "3.01.05.583": "Lacustrine sediments: undifferentiated",
                      "3.01.06.495": "Marine sediments: terraced",
                      "3.01.06.497": "Marine sediments: beach",
                      "3.01.06.507": "Marine sediments: deltaic",
                      "3.01.06.492": "Marine sediments: intertidal",
                      "3.01.06.493": "Marine sediments: littoral and nearshore",
                      "3.01.06.509": "Marine sediments: offshore",
                      "3.01.06.502": "Marine sediments: veneer",
                      "3.01.06.505": "Marine sediments: blanket",
                      "3.01.06.503": "Marine sediments: undifferentiated",
                      "3.01.09.487": "Glaciomarine sediments: beach",
                      "3.01.09.525": "Glaciomarine sediments: deltaic",
                      "3.01.09.512": "Glaciomarine sediments: intertidal",
                      "3.01.09.513": "Glaciomarine sediments: littoral and nearshore",
                      "3.01.09.519": "Glaciomarine sediments: offshore",
                      "3.01.09.527": "Glaciomarine sediments: submarine outwash fan",
                      "3.01.09.517": "Glaciomarine sediments: submarine moraine",
                      "3.01.09.483": "Glaciomarine sediments: veneer",
                      "3.01.09.485": "Glaciomarine sediments: blanket",
                      "3.01.09.515": "Glaciomarine sediments: undifferentiated",
                      "3.01.08.645": "Glaciolacustrine sediments: beach",
                      "3.01.08.613": "Glaciolacustrine sediments: deltaic",
                      "3.01.08.612": "Glaciolacustrine sediments: littoral and nearshore",
                      "3.01.08.637": "Glaciolacustrine sediments: offshore",
                      "3.01.08.615": "Glaciolacustrine sediments: subaqueous outwash fan",
                      "3.01.08.617": "Glaciolacustrine sediments: subaqueous moraine",
                      "3.01.08.635": "Glaciolacustrine sediments: hummocky",
                      "3.01.08.642": "Glaciolacustrine sediments: veneer",
                      "3.01.08.647": "Glaciolacustrine sediments: blanket",
                      "3.01.08.643": "Glaciolacustrine sediments: undifferentiated",
                      "3.01.07.249": "Glaciofluvial sediments: outwash plain",
                      "3.01.07.237": "Glaciofluvial sediments: terraced",
                      "3.01.07.225": "Glaciofluvial sediments: outwash fan",
                      "3.01.07.215": "Glaciofluvial sediments: hummocky",
                      "3.01.07.217": "Glaciofluvial sediments: ice-contact",
                      "3.01.07.219": "Glaciofluvial sediments: kame terrace",
                      "3.01.07.229": "Glaciofluvial sediments: esker",
                      "3.01.07.223": "Glaciofluvial sediments: veneer",
                      "3.01.07.247": "Glaciofluvial sediments: blanket",
                      "3.01.07.235": "Glaciofluvial sediments: undifferentiated",
                      "3.01.10.357": "Glacial sediments: rock-glacierized moraine",
                      "3.01.10.375": "Glacial sediments: hummocky till",
                      "3.01.10.377": "Glacial sediments: moraine complex",
                      "3.01.10.385": "Glacial sediments: ridged till, moraine",
                      "3.01.10.387": "Glacial sediments: streamlined till",
                      "3.01.10.439": "Glacial sediments: till plain",
                      "3.01.10.057": "Glacial sediments: weathered till",
                      "3.01.10.355": "Glacial sediments: veneer",
                      "3.01.10.359": "Glacial sediments: blanket",
                      "3.01.10.373": "Glacial sediments: undifferentiated",
                      "3.01.11.175": "Weathered bedrock or regolith: veneer",
                      "3.01.11.169": "Weathered bedrock or regolith: blanket",
                      "3.01.11.177": "Weathered bedrock or regolith: undifferentiated",
                      "3.01.16.705": "Volcanic deposits: pyroclastic sediments",
                      "3.01.16.707": "Volcanic deposits: undifferentiated",
                      "3.01.12.082": "Undifferentiated deposits: undifferentiated",
                      "3.01.13.192": "Bedrock: sedimentary",
                      "3.01.13.187": "Bedrock: igneous",
                      "3.01.13.183": "Bedrock: metamorphic",
                      "3.01.13.185": "Bedrock: undifferentiated"}


def main():
    sgLayerName = sys.argv[1]
    inputField = sys.argv[2]
    addCodes = sys.argv[3]

    aprx = arcpy.mp.ArcGISProject('CURRENT')
    mapProject = aprx.listMaps(aprx.activeMap.name)[0]
    sgLayer = mapProject.listLayers(sgLayerName)[0]

    stylePath = os.path.join(os.path.dirname(__file__), "GSC_SymbolStandard_v2-3-14.stylx")
    con = sqlite3.connect(stylePath)
    styleDb = pd.read_sql_query("SELECT * from ITEMS", con, index_col="NAME")

    sgCodesDf = pd.DataFrame(sgCodes, index=["Value"]).T
    tblPath = os.path.join(scratch, "sgCodesTbl.csv")
    sgCodesDf.to_csv(tblPath)

    codeField = "SYMBOL_CODE"
    exp = "getCode(str(!" + inputField + "!), r\"" + tblPath + "\")"
    code = getCodeScript

    arcpy.AddMessage("Calculating field...")
    try:
        arcpy.management.AddField(in_table=sgLayer, field_name=codeField, field_type="TEXT")
    except:
        print("Field already exists.")
    arcpy.management.CalculateField(in_table=sgLayer, field=codeField, expression=exp, expression_type="PYTHON",
                                    code_block=code)

    arcpy.AddMessage("Applying symbology...")
    sym = sgLayer.symbology
    sym.updateRenderer('UniqueValueRenderer')
    sym.renderer.fields = [codeField]
    sgLayer.symbology = sym

    lyrCim = sgLayer.getDefinition('V2')

    for group in lyrCim.renderer.groups:
        for cls in group.classes:
            label = cls.label
            unitStyleText = styleDb.loc[label, "CONTENT"]
            unitStyleDic = json.loads(unitStyleText[:-1])
            newSymbolLayer = []
            for element in unitStyleDic["symbolLayers"]:
                if element["type"] == "CIMSolidFill":
                    newSymbol = arcpy.cim.CIMSymbols.CIMSolidFill()
                    newSymbol.enable = element["enable"]
                    newSymbol.color = element["color"]
                    newSymbolLayer.append(newSymbol)
                elif element["type"] == "CIMCharacterMarker":
                    newSymbol = arcpy.cim.CIMSymbols.CIMCharacterMarker()
                    newSymbol.enable = element["enable"]
                    newSymbol.anchorPointUnits = element["anchorPointUnits"]
                    newSymbol.dominantSizeAxis3D = element["dominantSizeAxis3D"]
                    newSymbol.size = element["size"]
                    newSymbol.billboardMode3D = element["billboardMode3D"]
                    newSymbol.markerPlacement = element["markerPlacement"]
                    newSymbol.characterIndex = element["characterIndex"]
                    newSymbol.fontFamilyName = element["fontFamilyName"]
                    newSymbol.fontStyleName = element["fontStyleName"]
                    newSymbol.fontType = element["fontType"]
                    newSymbol.scaleX = element["scaleX"]
                    newSymbol.symbol = element["symbol"]
                    newSymbol.scaleSymbolsProportionally = element["scaleSymbolsProportionally"]
                    newSymbol.respectFrame = element["respectFrame"]
                    newSymbolLayer.append(newSymbol)
                else:
                    arcpy.AddMessage("##############")
                    arcpy.AddMessage(element)
            cls.symbol.symbol.symbolLayers = newSymbolLayer

            if addCodes == "true":
                cls.label = sgCodeDescriptions[label] + " (" + sgCodes[label] + ")"
            else:
                cls.label = sgCodeDescriptions[label]
    sgLayer.setDefinition(lyrCim)
    shutil.rmtree(scratch, ignore_errors=True)
    return


if __name__ == '__main__':
    main()
