#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Arnaud Mazier
# Created Date: 15/06/2021
# Institution: University of Luxembourg
# Contact: ziemnono@gmail.com
# Project: Esch 2022
# Funding: This work was supported by the European Union’s Horizon 2020 research
# and innovation programme under the Marie Sklodowska-Curie grant agreement No. 764644.
# =============================================================================
"""This file has been built for downloading a xml file giving road traffic information
in Luxembourg. Then relevant features can be extracted  into a xlsx file for post-treatment."""

import os
import urllib.request
import xml.etree.ElementTree as et
from datetime import datetime

import pandas as pd


def read_url(url, xml_filename):
    """read the data from the URL and create an xml file"""
    # Open a connection to a URL using urllib
    web_url = urllib.request.urlopen(url)

    # Get the result code and print information
    print("result code: " + str(web_url.getcode()))
    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print("if 200, " + url + " successfully reached the " + dt_string)

    # Read the data from the URL and print it and get rid of xmlns which is troublesome
    xmlns = ' xmlns="http://datex2.eu/schema/2/2_0"'
    data = web_url.read().decode("utf-8").replace(xmlns, '')
    f = open(xml_filename, "w+")
    f.write(data)
    f.close()


def read_xml(xml_filename):
    """Check if the file exists, parse the file and extract the relevant data
     return a dictionary with the correct elements"""
    # Parse the xml file
    if not os.path.exists(xml_filename):
        return
    tree = et.parse(xml_filename)
    root = tree.getroot()

    features_list = ["publicationTime", "value", "latitude", "longitude", "offsetDistance",
                     "directionBoundOnLinearSection", "roadNumber", "distanceAlong", "speed", "percentage",
                     "vehicleFlowRate"]  # all keys to be extracted from xml
    dict = {}
    for keys in features_list:
        if keys == "distanceAlong":
            # distanceAlong is present 2 times, we only take one
            dict[keys] = [element.text for count, element in enumerate(root.findall(".//" + keys)) if
                          count % 2 == 0]
        elif keys == "value":
            # we only want the english version
            dict["value"] = [element.text for count, element in enumerate(root.findall(".//" + keys)) if
                             count % 2 == 0]
            dict["lang"] = [element.attrib["lang"] for count, element in enumerate(root.findall(".//" + keys)) if
                            count % 2 == 0]
        elif keys == "offsetDistance":
            # offsetDistance is present 2 times, we only take one
            dict[keys] = [element.text for count, element in enumerate(root.findall(".//" + keys + "/" + keys)) if
                          count % 2 == 0]
        else:
            dict[keys] = [element.text for element in root.findall(".//" + keys)]
    # publicationTime is present only on time in the file, we multiply it for the excel layout
    dict["publicationTime"] = dict["publicationTime"] * max([len(dict[i]) for i in dict])

    return dict


def to_excel(dict, xlsx_filename):
    """Generate an excel file with the given data"""
    # I noticed that sometimes the dataset is empty, in this case we just write an empty dictionary
    try:
        df = pd.DataFrame(data=dict)
        len_data = len(dict["publicationTime"])
    except ValueError:
        dict = {}
        len_data = 0
        df = pd.DataFrame(data=dict)

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(xlsx_filename, engine='xlsxwriter')

    # If the xlsx file already exists, append at the end of it (a bit ugly but read mode is only possible with openpyxl
    if not os.path.exists(xlsx_filename):
        df.to_excel(writer, sheet_name=xlsx_filename, index=False)
    else:
        old_df = pd.read_excel(xlsx_filename, engine="openpyxl", sheet_name=xlsx_filename)
        updated_df = old_df.append(df)
        updated_df.to_excel(writer, sheet_name=xlsx_filename, index=False)

    # Get the worksheet object.
    worksheet = writer.sheets[xlsx_filename]

    # Set the column width and format.
    for idx, col in enumerate(df):  # loop through all columns
        series = df[col]
        max_len = max((
            series.astype(str).map(len).max(),  # len of largest item
            len(str(series.name))  # len of column name/header
        )) + 1  # adding a little extra space
        worksheet.set_column(idx, idx, max_len)  # set column width

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
    print(xlsx_filename, "successfully saved, " + str(len_data) + " lines have been added")


if __name__ == '__main__':
    # To work in the current directory
    if __file__ == "main.py":
        os.chdir(os.getcwd())
    else:
        os.chdir(os.path.dirname(__file__))

    b40_url = 'https://www.cita.lu/info_trafic/datex/trafficstatus_b40'
    b40_xml_filename = "trafficstatus_b40.xml"
    b40_xlsx_filename = "trafficstatus_b40.xlsx"

    a4_url = 'https://www.cita.lu/info_trafic/datex/trafficstatus_a4'
    a4_xml_filename = "trafficstatus_a4.xml"
    a4_xlsx_filename = "trafficstatus_a4.xlsx"

    read_url(b40_url, b40_xml_filename)
    data = read_xml(b40_xml_filename)
    to_excel(data, b40_xlsx_filename)

    read_url(a4_url, a4_xml_filename)
    data = read_xml(a4_xml_filename)
    to_excel(data, a4_xlsx_filename)
