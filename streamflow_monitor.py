# Importing the neccessary libraries
import urllib.parse
import urllib.request
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Getting the gage information
station_number = input("What is the USGS Station ID?\t")
start_date = input("Start Date (YYYY-MM-DD):\t")
end_date = input("End Date (YYYY-MM-DD):\t")
folder = os.getcwd()
# Getting
section1 = 'https://nwis.waterdata.usgs.gov/nwis/dv?referred_module=sw&search_site_no='
section2 = '&search_site_no_match_type=exact&site_tp_cd=OC&site_tp_cd=OC-CO&site_tp_cd=ES&site_tp_cd='\
    'LK&site_tp_cd=ST&site_tp_cd=ST-CA&site_tp_cd=ST-DCH&site_tp_cd=ST-TS&index_pmcode_00060=1&group_key='\
    'NONE&sitefile_output_format=html_table&column_name=agency_cd&column_name=site_no&column_name=station_nm&range_selection=date_range&begin_date='
section3 = '&end_date='
section4 = '&format=rdb&date_format=YYYY-MM-DD&rdb_compression=value&list_of_search_criteria=search_site_no%2Csite_tp_cd%2Crealtime_parameter_selection'

link = (section1 + station_number + section2 +
        start_date + section3 + end_date + section4)
print("Click here to see the generated USGS link: \n", link)

USGS_page = urllib.request.urlopen(link)
downloaded_data = USGS_page.read()

str_data = downloaded_data.decode()
type(str_data)
# str_data

f_str_data = str_data.split('\n')
# f_str_data

station_name = ''

for line in range(len(f_str_data)):
    if f_str_data[line].startswith("#    USGS"):
        station_name = f_str_data[line][3:]
print(station_name)

date_flow = ''

for line in range(len(f_str_data)):
    if f_str_data[line].startswith("USGS"):
        data = f_str_data[line][14:]
        columns = data.split('\t')
        rows = ','.join([columns[0], (columns[1])])
        date_flow += rows + '\n'
date_flow = date_flow.encode()

with open(folder+'/USGS_Data_for_' + station_number + '.csv', 'wb') as text:
    text.write(date_flow)

    filename = folder+'/USGS_Data_for_' + station_number + '.csv'
columns = ['Date', 'Discharge (cfs)']
df = pd.read_csv(filename, header=None, names=columns, parse_dates=[0])
df = df.set_index(['Date'])
df['Discharge (cfs)'] = pd.to_numeric(df['Discharge (cfs)'], errors='coerce')
df.head()

df.plot(figsize=(14, 5), title=station_name,
        xlabel="Time", ylabel="Discharge (cfs)")
