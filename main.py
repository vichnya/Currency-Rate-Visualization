import datetime
from urllib.request import urlopen
from xml.etree import ElementTree as ET

import matplotlib.pyplot as plt
import numpy as np


CURRENCIES = [
    "R01239",  # Евро
    "R01235",  # Доллар США
    "R01035",  # Фунт стерлингов
    "R01090B", # Китайский юань
    "R01535",  # Японская иена
    "R01820",  # Белорусский рубль
    "R01760",  # Украинская гривна
    "R01700J", # Казахстанский тенге
    "R01115",  # Швейцарский франк
    "R01585F", # Польский злотый
    "R01565",  # Турецкая лира
]


def get_currencies(currencies_ids=None):
    """Получает актуальные курсы выбранных валют."""
    if currencies_ids is None:
        currencies_ids = CURRENCIES

    url = "https://www.cbr.ru/scripts/XML_daily.asp"
    response = urlopen(url)

    root = ET.parse(response).getroot()
    result = {}

    for element in root.findall("Valute"):
        valute_id = element.get("ID")

        if valute_id in currencies_ids:
            name = element.find("Name").text
            value = element.find("Value").text
            result[name] = value

    return result


def get_currencies_year(currency_id="R01235"):
    """Получает динамику курса валюты за последние 12 месяцев."""
    today = datetime.date.today()
    year_ago = today - datetime.timedelta(days=365)

    date_req1 = year_ago.strftime("%d/%m/%Y")
    date_req2 = today.strftime("%d/%m/%Y")

    url = (
        "https://www.cbr.ru/scripts/XML_dynamic.asp"
        f"?date_req1={date_req1}"
        f"&date_req2={date_req2}"
        f"&VAL_NM_RQ={currency_id}"
    )

    response = urlopen(url)
    root = ET.parse(response).getroot()

    result = {}

    for element in root.findall("Record"):
        date = element.get("Date")
        value = element.find("Value").text
        result[date] = value

    return result


def visualize_data():
    """Строит графики курсов валют."""
    currencies = get_currencies()

    names = list(currencies.keys())
    values = [
        float(value.replace(",", "."))
        for value in currencies.values()
    ]

    dollar_history = get_currencies_year()

    dates = [
        datetime.datetime.strptime(date, "%d.%m.%Y")
        for date in dollar_history.keys()
    ]

    dollar_values = [
        float(value.replace(",", "."))
        for value in dollar_history.values()
    ]

    fig, axes = plt.subplots(2, 1, figsize=(12, 9))

    x_positions = np.arange(len(names))

    axes[0].bar(x_positions, values)
    axes[0].set_title("Текущие курсы валют ЦБ РФ")
    axes[0].set_ylabel("Курс")
    axes[0].set_xlabel("Валюта")
    axes[0].set_xticks(x_positions)
    axes[0].set_xticklabels(names, rotation=45, ha="right")
    axes[0].grid(axis="y")

    axes[1].plot(dates, dollar_values)
    axes[1].set_title("Динамика курса доллара США за последние 12 месяцев")
    axes[1].set_ylabel("Курс, руб.")
    axes[1].set_xlabel("Дата")
    axes[1].grid(True)

    fig.suptitle("Курсы валют Центрального банка РФ")
    plt.tight_layout()
    plt.show()


def main():
    visualize_data()


if __name__ == "__main__":
    main()
