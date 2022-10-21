from typing import Dict, List
import requests
from datetime import datetime, timedelta

def get_usage_data(cookies: List[Dict], interval = "d", previous_days = 35):

  headers = {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:105.0) Gecko/20100101 Firefox/105.0',
      'Accept': 'application/json',
      'Accept-Language': 'en-US,en;q=0.5',
      'Referer': 'https://evergy.com/ma/energy-dashboard/energy-usage',
      'Origin': 'https://evergy.com',
      'Connection': 'keep-alive',
      'Sec-Fetch-Dest': 'empty',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Site': 'same-origin',
      'DNT': '1',
      'Sec-GPC': '1',
      'Pragma': 'no-cache',
      'Cache-Control': 'no-cache',
  }

  from_date = datetime.today() - timedelta(days=previous_days)

  params = {
    'interval': interval,
    'size': previous_days,
    'from': from_date.strftime(r'%m/%d/%Y')
  }

  request_body = [
    {
        'title': 'Day',
        'fieldName': 'period',
        'cssClass': 'table-col-lg',
    },
    {
        'title': 'Date',
        'fieldName': 'date',
        'format': 'dateMMDD',
        'cssClass': 'sortable-table__column--date sortable-table__column--date table-col-xs',
    },
    {
        'title': 'Usage (kWh)',
        'fieldName': 'usage',
        'format': 'integer',
        'cssClass': 'sortable-table__column--integer sortable-table__column--integer table-col-xs',
    },
    {
        'title': 'Peak Demand (kW)',
        'fieldName': 'peakDemand',
        'format': 'kw',
        'cssClass': '  table-col-md',
        'hasTooltip': True,
        'tooltipContent': 'Peak Demand is the highest level of electricity used during a given time frame.',
    },
    {
        'title': 'Peak Time',
        'fieldName': 'peakDateTime',
        'format': 'right',
        'cssClass': '  table-col-md',
    },
    {
        'title': 'High Temp',
        'fieldName': 'maxTemp',
        'format': 'temperature',
        'cssClass': 'sortable-table__column--temperature sortable-table__column--temperature table-col-md',
    },
    {
        'title': 'Low Temp',
        'fieldName': 'minTemp',
        'format': 'temperature',
        'cssClass': 'sortable-table__column--temperature sortable-table__column--temperature table-col-md',
    },
    {
        'title': 'Avg Temp',
        'fieldName': 'avgTemp',
        'format': 'temperature',
        'cssClass': 'sortable-table__column--temperature sortable-table__column--temperature table-col-xs',
    },
  ]

  session = requests.Session()
  for cookie in cookies:
    session.cookies.set(cookie['name'], cookie['value'])

  response = session.post('https://evergy.com/api/report/usage/4387311000/download', params=params,headers=headers, json=request_body, stream=True)

  filename = datetime.now().strftime(r'%Y_%m_%d-%I_%M_%S_%p') + '.csv'

  with open(filename, 'wb') as fd:
    for chunk in response.iter_content(chunk_size=128):
      fd.write(chunk)

  print('results written to ' + filename)