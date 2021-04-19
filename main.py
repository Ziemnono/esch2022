import os
import urllib.request
import xml.etree.ElementTree as et
import pandas as pd


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
    # return a 2 dimensional list without "header"

    if not os.path.exists(xml_filename):
        return
    tree = et.parse(xml_filename)
    root = tree.getroot()
    # print(et.tostring(root, encoding='utf8').decode('utf8'))
    # for elem in root.iter():
    #     print(elem.tag, elem.attrib, elem.text)

    dict_keys = ["publicationTime", "latitude"]  # all keys to be extracted from xml
    dict = {}
    counter = 0
    for elem in root.iter():
        for keys in dict_keys:
            if elem.tag == keys:
                if keys in dict:
                    keys += "_" + str(counter)
                    counter += 1
                dict[keys] = elem.text
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
