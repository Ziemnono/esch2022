import os
import urllib.request
import xml.etree.ElementTree as et

import pandas as pd


# from lxml import etree as et


def read_url(url, xml_filename):
    # read the data from the URL and create an xml file

    # open a connection to a URL using urllib
    web_url = urllib.request.urlopen(url)

    # get the result code and print it
    print("result code: " + str(web_url.getcode()))

    # read the data from the URL and print it and get rid of xmlns which is troublesome
    xmlns = ' xmlns="http://datex2.eu/schema/2/2_0"'
    data = web_url.read().decode("utf-8").replace(xmlns, '')
    f = open(xml_filename, "w+")
    f.write(data)
    f.close()


def read_xml(xml_filename):
    # Check if the file exists, parse the file and extract the relevant data
    # return a dictionary with the correct elements

    if not os.path.exists(xml_filename):
        return
    tree = et.parse(xml_filename)
    root = tree.getroot()

    keys = ["publicationTime", "latitude", "longitude", "vehicleFlowRate"]  # all keys to be extracted from xml
    latitude_key = ["49.50394", "49.50413", "49.501606", "49.501408"]  # the desired latitude
    longitude_key = ["5.9460163", "5.9458966", "5.9444437", "5.9445815"]  # the desired longitude
    dict = {}
    count = 0  # count to simply avoid to have 2 identical keys, it will change maybe later on
    take_next = False  # variable indicating that if we find a longitude or latitude present in our key then we can take
    # the next key otherwise we pass to the next longitude or latitude

    for elem in root.iter():
        if elem.tag == keys[0]:
            dict[keys[0]] = elem.text
        if elem.tag == keys[1] and elem.text in latitude_key:
            dict[keys[1] + " " + str(count)] = elem.text
            take_next = True
        elif elem.tag == keys[1]:
            take_next = False
        if elem.tag == keys[2] and elem.text in longitude_key:
            dict[keys[2] + " " + str(count)] = elem.text
            take_next = True
        elif elem.tag == keys[2]:
            take_next = False
        if elem.tag == keys[3] and take_next:
            dict[keys[3] + " " + str(count)] = elem.text
            count += 1
    return dict


def to_excel(dict, xlsx_filename):
    # Generate an excel file with the given data
    df = pd.DataFrame(data=dict, index=[0])

    if not os.path.exists(xlsx_filename):
        df.to_excel(xlsx_filename, sheet_name=xlsx_filename, index=False)
    else:
        old_df = pd.read_excel(xlsx_filename, engine="openpyxl", sheet_name=xlsx_filename)
        updated_df = old_df.append(df)
        updated_df.to_excel(xlsx_filename, sheet_name=xlsx_filename, index=False)


if __name__ == '__main__':
    url = 'https://www.cita.lu/info_trafic/datex/trafficstatus_b40'
    xml_filename = "trafficstatus_b40.xml"
    xlsx_filename = "trafficstatus_b40.xlsx"

    # to work in the current directory
    os.chdir(os.getcwd())

    read_url(url, xml_filename)
    data = read_xml(xml_filename)
    to_excel(data, xlsx_filename)
