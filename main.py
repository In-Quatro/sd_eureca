import csv
import logging
import os
import time
import re
from config import (ADDRESS_ID, DATE_ID, DESCRIPTION_XPATH,
                    MENU, METRO_ID, PART_ID, PRIORITY,
                    PRIORITY_ID, RESPONSIBLE, RESPONSIBLE_XPATH,
                    TOPIC, TOPIC_ID,
                    )

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


load_dotenv()
USERNAME = os.getenv('USER_NAME')
PASSWORD = os.getenv('PASSWORD')
URL = (os.getenv('URL') +
       'sd/operator/#add:task$task::task!{%22fast%22:%22true%22}')

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s - %(asctime)s  - %(message)s',
                    datefmt='%H:%M:%S')

driver_options = webdriver.EdgeOptions()
driver_options.add_argument("--headless")
driver = webdriver.Edge(options=driver_options)


def authorization() -> None:
    """Авторизация на сайте."""
    logging.info('Начинаю процесс авторизации')

    # Пользователь
    field_username = driver.find_element(By.ID, 'username')
    field_username.clear()
    field_username.send_keys(USERNAME)

    #  Пароль
    field_password = driver.find_element(By.ID, 'password')
    field_password.clear()
    field_password.send_keys(PASSWORD)
    field_password.send_keys(Keys.ENTER)
    time.sleep(7)
    logging.info('Авторизация прошла успешна')


def fill_topic() -> None:
    """Заполнение поля Тема."""
    field_new = driver.find_element(By.ID, TOPIC_ID)
    field_new.send_keys(TOPIC)


def fill_description(description: str) -> None:
    """Заполнение поля Описание."""
    field_description = driver.find_element(By.XPATH, DESCRIPTION_XPATH)
    field_description.click()
    field_description.send_keys(Keys.BACKSPACE)
    field_description.send_keys(description)


def fill_address(address: str) -> None:
    """Заполнение поля Адрес."""
    field_address = driver.find_element(By.ID, ADDRESS_ID)
    field_address.send_keys(address)


def fill_part(part: str) -> None:
    """Заполнение поля РМ и ЗИП."""
    field_part = driver.find_element(By.ID, PART_ID)
    field_part.send_keys(part, Keys.ENTER)


def fill_priority() -> None:
    """Заполнение поля Приоритет."""
    field_priority = driver.find_element(By.ID, PRIORITY_ID)
    field_priority.clear()
    field_priority.send_keys(PRIORITY, Keys.ENTER)


def fill_date(date: str) -> None:
    """Заполнение поля Дата."""
    field_date = driver.find_element(By.ID, DATE_ID)
    field_date.clear()
    field_date.send_keys(f'{date}.2024 10:00', Keys.ENTER)


def fill_responsible() -> None:
    """Заполнение поля Ответственный."""
    field_responsible = driver.find_element(By.XPATH, RESPONSIBLE_XPATH)
    field_responsible.clear()
    field_responsible.send_keys(RESPONSIBLE)


def fill_metro(metro: str) -> None:
    """Заполнение поля Метро."""
    field_metro = driver.find_element(By.ID, METRO_ID)
    time.sleep(1)
    field_metro.send_keys(metro, Keys.TAB, Keys.ENTER)


def main() -> None:
    """Главна логика скрипта."""
    num: str = input(
        'Выберите из списка:\n'
        '1 - Отвезти документы\n'
        '2 - Забрать документы\n'
    )

    date: str = input('Введите дату в формате "ДД.ММ"\n')
    copy: str = '3' if num == '1' else '2'
    part: str = 'Документы взять в офисе' if num == '1' else '-'
    csv_file: str = 'data.csv'

    driver.get(url=URL)
    logging.info('Открываю URL, ожидайте')
    authorization()
    logging.info('Начинаю создавать задачи, ожидайте')
    with open(csv_file, encoding='ANSI') as file:
        file_reader = csv.DictReader(file, delimiter=";")
        for row in file_reader:
            time.sleep(2)

            # Список полей
            kod_mo: str = row['Код МО']
            address: str = row['Адрес для подписания']
            metro: str = row['Метро']
            contact_1: str = row['Кому отдавать 1']
            telephone_1: str = row['Телефон 1']
            contact_2: str = row['Кому отдавать 2']
            telephone_2: str = row['Телефон 2']
            note: str = row['Примечание']
            count: str = row['Всего']
            description: str = (
                f'{kod_mo} - {MENU[num]} ({count} шт. по {copy} экземпляра)\n'
                f'\n{contact_1}\n'
                f'{telephone_1}\n\n'
                f'{contact_2}\n'
                f'{telephone_2}\n\n'
                f'{note}'
            )

            fill_topic()
            fill_description(description)
            fill_address(address)
            fill_part(part)
            fill_priority()
            fill_date(date)
            fill_responsible()
            fill_metro(metro)

            time.sleep(2)
            title = driver.find_element(By.CSS_SELECTOR, '.gwt-HTML.GHRP-MCCY')
            title = ''.join(re.findall(r'\d{5}', title.text))
            driver.get(url=URL)
            time.sleep(1)
            logging.info(f'Задача "{title}" для "{kod_mo}" создана')

    logging.info('Все задачи созданы')
    driver.quit()


if __name__ == "__main__":
    main()
