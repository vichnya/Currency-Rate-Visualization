import matplotlib.pyplot as plt

plt.rcdefaults()

import numpy as np
import datetime
import certifi
import ssl
from urllib.request import urlopen
from xml.etree import ElementTree as ET


ssl_context = ssl.create_default_context(
    cafile=certifi.where()
)


def get_currencies(currencies_ids_lst=[
    'R01239', 'R01235', 'R01035', 'R01090B', 'R01535', 'R01820', 'R01760',
    'R01700J', 'R01115', 'R01585F', 'R01565'
]):
    cur_res_str = urlopen(
        "https://www.cbr.ru/scripts/XML_daily.asp",
        context=ssl_context
    )

    result = {}

    cur_res_xml = ET.parse(cur_res_str)
    root = cur_res_xml.getroot()

    valutes = root.findall('Valute')

    for el in valutes:
        valute_id = el.get('ID')

        if str(valute_id) in currencies_ids_lst:
            valute_cur_val = el.find('Value').text
            result[el.find('Name').text] = valute_cur_val

    return result


def get_currencies_year(currencies_id='R01235'):
    today = datetime.date.today()

    date_req1 = (
        today - datetime.timedelta(days=365)
    ).strftime('%d/%m/%Y')

    date_req2 = today.strftime('%d/%m/%Y')

    cur_res_str = urlopen(
        f"https://www.cbr.ru/scripts/XML_dynamic.asp"
        f"?date_req1={date_req1}"
        f"&date_req2={date_req2}"
        f"&VAL_NM_RQ={currencies_id}",
        context=ssl_context
    )

    result = {}

    cur_res_xml = ET.parse(cur_res_str)
    root = cur_res_xml.getroot()

    valutes = root.findall('Record')

    for el in valutes:
        valute_date = el.get('Date')
        valute_cur_val = el.find('Value').text
        result[valute_date] = valute_cur_val

    return result


cur_vals = get_currencies()

objects = cur_vals.keys()

y_pos = np.arange(len(objects))

x_pos = [
    float(item.replace(",", "."))
    for item in cur_vals.values()
]

fig, axs = plt.subplots(
    2, 1,
    figsize=(12, 9),
    sharey=False
)

for i in range(len(x_pos)):
    axs[0].bar(y_pos[i], x_pos[i])

axs[0].set_ylabel('Курс валюты')
axs[0].set_xlabel('Номер валюты')
axs[0].set_title('Текущий курс валют')

axs[0].set_xticks(y_pos)
axs[0].set_xticklabels(
    range(1, len(objects) + 1)
)

axs[0].legend(
    objects,
    bbox_to_anchor=(1, 1)
)

cur_vals_year = get_currencies_year()

objects_year = cur_vals_year.keys()

dates = [
    datetime.datetime.strptime(
        date,
        '%d.%m.%Y'
    )
    for date in objects_year
]

x_pos = [
    float(item.replace(",", "."))
    for item in cur_vals_year.values()
]

axs[1].plot(dates, x_pos)

axs[1].set_ylabel('Курс валюты')
axs[1].set_xlabel('Дата')
axs[1].set_title(
    'Динамика курса доллара США за последние 12 месяцев'
)

axs[1].legend(['Доллар США'])
axs[1].grid(True)

fig.suptitle('Курсы валют Центрального банка РФ')

plt.tight_layout()
plt.show()
