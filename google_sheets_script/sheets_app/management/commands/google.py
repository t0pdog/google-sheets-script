import time
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

from django.core.management.base import BaseCommand
import gspread

from sheets_app.models import Orders


class Command(BaseCommand):
    """
    Командой python manage.py google запускаем скрипт опроса гугл документа.
    """

    def handle(self, *args, **options):
        print("Скрипт запустился")

        try:
            # Авторизуемся в Гугл
            client = gspread.service_account(filename='/app/sheets_app/management/commands/gspread/service_account.json')
            last_sheet_update = ''
            
            # Объявляем счетчик, для того чтобы каждый час обновлять курс валют
            counter = 0
            # Получаем первый раз курс валют
            DOLL_TO_RUB_RATE = get_currency_rate()
            print(DOLL_TO_RUB_RATE)

            # запускаем скрипт в цикл проверки изменений каждые 60 секунд
            while True:
                sheet_update = client.open("Kanalservice test").lastUpdateTime

                if sheet_update != last_sheet_update:
                    last_sheet_update = sheet_update

                    # Получаем первую страницу Гугл таблицы и затем список заказов
                    sheet = client.open("Kanalservice test").sheet1
                    list_ord = sheet.get_all_values()[1:]

                    for i in list_ord:
                        # Проверяем заказы в БД на соответствие заказам в Гугл Таблице
                        try:
                            order_in_bd = Orders.objects.get(order_number=int(i[1]))

                            if order_in_bd.price_usd != int(i[2]):
                                order_in_bd.price_usd = int(i[2])
                                order_in_bd.price_rub = round(order_in_bd.price_usd*DOLL_TO_RUB_RATE, 2)
                                order_in_bd.save()

                            if order_in_bd.number != int(i[0]):
                                order_in_bd.number = int(i[0])
                                order_in_bd.save()

                            if order_in_bd.shipping_date != datetime.strptime(i[3], '%d.%m.%Y'):
                                order_in_bd.shipping_date = datetime.strptime(i[3], '%d.%m.%Y')
                                order_in_bd.save()
                            else:
                                pass
                        # Если не находим заказ в БД то создаем его
                        except:
                            Orders.objects.create(
                                number=int(i[0]),
                                order_number=int(i[1]),
                                price_usd=int(i[2]),
                                price_rub=round(int(i[2])*DOLL_TO_RUB_RATE, 2),
                                shipping_date=datetime.strptime(i[3], '%d.%m.%Y')
                                )

                    # Удаляем ненужные заказы
                    # Достаем список заказов из базы данных
                    orders_in_bd = Orders.objects.all()
                    # Сравниваем количество заказов в Гугл и в БД
                    if len(list_ord) != len(orders_in_bd):
                        # Достаем номера списка заказов для сверки
                        order_numbers_in_db = list(orders_in_bd.values_list('order_number', flat=True))
                        # Берем номера заказов из Гугл для сравнения
                        list_order_nums = [lst[1] for lst in list_ord]
                        # Составляем список ненужных заказов
                        difference = [x for x in order_numbers_in_db if str(x) not in list_order_nums]
                        # Удаляем ненужные заказы
                        for i in difference:
                            Orders.objects.filter(order_number=i).delete()

                print("прошел цикл")
                counter +=1
                # счетчик обнуляется каждый час
                if counter > 60:
                    counter = 0
                    # Обновляем курс валют
                    DOLL_TO_RUB_RATE = get_currency_rate()

                print(counter)
                # ждем 60 секунд
                time.sleep(60)

                print("новый цикл")

        except requests.exceptions.RequestException as e:
            print("Error: {}".format(e))


def get_currency_rate(char_code_currency="USD"):
    """
    Получаем курс доллара в формате XML с сайта ЦБ РФ
    https://www.cbr.ru/scripts/XML_daily.asp
    с использованием XPath выражения и ElementTree.
    """
    return float(
        ET.fromstring(requests.get('https://www.cbr.ru/scripts/XML_daily.asp').text)
        .find('./Valute[CharCode="USD"]/Value')
        .text.replace(',', '.')
        )
