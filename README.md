# Telegram-бот
![](https://ru.financemagnates.com/wp-content/uploads/2016/10/faenza_telegram_by_xaviermartinezf-d7qafub.png)
### Назначение
Telegram-бот, который обращается к API сервиса Практикум.Домашка и отслеживает статус домашней работы: взята ли ваша домашка в ревью, проверена ли она, а если проверена — то принял её ревьюер или вернул на доработку.


### Функции бота:
-   раз в 10 минут опрашивает API сервиса Практикум.Домашка и проверяет статус отправленной на ревью домашней работы;
-   при обновлении статуса анализирует ответ API и отправляет соответствующее уведомление в Telegram;
-   логирует свою работу и сообщает вам о важных проблемах сообщением в Telegram.

### Логирование работы:
-   отсутствие обязательных переменных окружения во время запуска бота (уровень CRITICAL).
-   удачная отправка любого сообщения в Telegram (уровень INFO);
-   сбой при отправке сообщения в Telegram (уровень ERROR);
-   недоступность эндпоинта  [https://practicum.yandex.ru/api/user_api/homework_statuses/](https://practicum.yandex.ru/api/user_api/homework_statuses/)  (уровень ERROR);
-   любые другие сбои при запросе к эндпоинту (уровень ERROR);
-   отсутствие ожидаемых ключей в ответе API (уровень ERROR);
-   недокументированный статус домашней работы, обнаруженный в ответе API (уровень ERROR);
-   отсутствие в ответе новых статусов (уровень DEBUG).

### Технологии

* [python-dotenv](https://pypi.org/project/python-dotenv/)
* [python-telegram-bot](https://pypi.org/project/python-telegram-bot/)

### Для локального запуска проекта необходимо:

Клонировать репозиторий и перейти в него в командной строке:

```sh
git clone git@github.com:Kolanser/homework_bot.git
cd homework_bot
```

Cоздать и активировать виртуальное окружение:

```sh
python -m venv env
source venv/Scripts/activate
```

Обновить pip:

```sh
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```sh
pip install -r requirements.txt
```

Запустить проект:
```sh
python homework.py run
```

### Деплой бота на [Heroku](https://www.heroku.com/)
Чтобы всё запустилось, в репозиторий нужно поместить два служебных файла:

-   **requirements.txt**  со списком зависимостей, чтобы Heroku знал, какие пакеты ему нужно установить;
-   файл  [**Procfile**](/Procfile), в котором должна быть указана «точка входа» — файл, который должен быть выполнен для запуска проекта.

### Автор
[**Николай Слесарев**](github.com/Kolanser)
