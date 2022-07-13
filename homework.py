from http import HTTPStatus
import logging
import sys
import requests
import telegram
import time
from os import getenv

from dotenv import load_dotenv

load_dotenv()


PRACTICUM_TOKEN = getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = getenv('TELEGRAM_CHAT_ID')

RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)
formatter = logging.Formatter(
    '%(asctime)s, [%(levelname)s] %(message)s'
)
handler.setFormatter(formatter)


def send_message(bot, message):
    """Отправляет сообщение в Telegram чат.
    Принимает на вход два параметра: экземпляр класса
    Bot и строку с текстом сообщения.
    """
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logger.info(f'Успешная отправка сообщения в Telegram: {message}')
    except Exception as error:
        logger.error(f'Сбой при отправке сообщения в Telegram: {error}')


def get_api_answer(current_timestamp):
    """Запрос к единственному эндпоинту API-сервиса.
    В качестве параметра параметра функция получает временную метку.
    В случае успешного запроса должна вернуть ответ API, преобразовав
    его из формата JSON к типам данных Python.
    """
    timestamp = current_timestamp
    params = {'from_date': timestamp}
    headers = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}
    try:
        homeworks = requests.get(ENDPOINT, headers=headers, params=params)
    except Exception as error:
        logger.error(f'Ошибка при запросе к API Практикум.Домашка: {error}')
    if homeworks.status_code != HTTPStatus.OK:
        raise Exception(
            f'Код HTTP ответа при запросе к API - {homeworks.status_code}'
        )
    return homeworks.json()


def check_response(response):
    """Проверка ответа API на корректность.
    В качестве параметра функция получает ответ API, приведенный к типам
    данных Python. Если ответ API соответствует ожиданиям, то функция
    должна вернуть список домашних работ (он может быть и пустым),
    доступный в ответе API по ключу 'homeworks'.
    """
    if response == {}:
        logger.error('Ответ от API содержит пустой словарь')
        raise Exception('Ответ от API содержит пустой словарь')
    if not isinstance(response, dict):
        logger.error('Ответ от API не является словарем')
        raise TypeError('Ответ от API не является словарем')
    homeworks = response.get('homeworks')
    if homeworks is not None:
        if isinstance(homeworks, list):
            return homeworks
        else:
            logger.error(
                'Данные в ответе API по ключу "homeworks" не являются словарем'
            )
    else:
        logger.error('Ответ от API не содержит ключ "homeworks"')
        raise KeyError('Ответ от API не содержит ключ "homeworks"')


def parse_status(homework):
    """Извлекает из информации о конкретной домашней работе статус работы.
    В качестве параметра функция получает только один элемент из списка
    домашних работ. В случае успеха, функция возвращает подготовленную для
    отправки в Telegram строку, содержащую один из вердиктов словаря
    HOMEWORK_STATUSES.
    """
    homework_name = homework.get('homework_name')
    homework_status = homework.get('status')
    verdict = HOMEWORK_STATUSES.get(homework_status)
    if homework_name is None:
        logger.error(
            'Словарь с домашней работой не содержит ключ "homework_name"'
        )
        raise KeyError(
            'Словарь с домашней работой не содержит ключ "homework_name"'
        )
    if homework_status is None:
        logger.error('Словарь с домашней работой не содержит ключ "status"')
        raise KeyError(
            'Словарь с домашней работой не содержит ключ "status"'
        )
    if verdict is None:
        logger.error(
            'Недокументированный статус домашней работы'
        )
        raise KeyError('Недокументированный статус домашней работы')
    return (
        f'Изменился статус проверки работы "{homework_name}". {verdict}'
    )


def check_tokens():
    """Проверка доступности переменных окружения, которые необходимы для
    работы программы. Если отсутствует хотя бы одна переменная окружения
    — функция должна вернуть False, иначе — True.
    """
    return all((PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID))


def main():
    """Основная логика работы бота."""
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = 0
    if check_tokens():
        while True:
            try:
                response = get_api_answer(current_timestamp)
                homeworks = check_response(response)
                if len(homeworks):
                    message = parse_status(homeworks[0])
                    send_message(bot, message)
                else:
                    logger.debug('В ответе отстутвуют новые статусы проверки')
                current_timestamp = response.get('current_date')
                time.sleep(RETRY_TIME)
            except Exception as error:
                message = f'Сбой в работе программы: {error}'
                send_message(bot, message)
                time.sleep(RETRY_TIME)
    else:
        message = 'Отсутвует (нет доступа) к переменной окружения'
        logger.critical(message)
        send_message(bot, message)


if __name__ == '__main__':
    main()
