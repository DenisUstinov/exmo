# exmo
Модуль exmo предоставляет простой и удобный интерфейс для подключения к веб-сокету биржи Exmo и обработки получаемых ответов.

## Установка
Вы можете установить exmo с помощью pip из GitHub, выполнив следующую команду:
```bash
pip install git+https://github.com/DenisUstinov/exmo.git --use-pep517
```

## Пример использования
Примеры использования пакета exmo для работы с публичными и приватными данными представлены ниже.

### Работа с публичными данными
```python
# Public data
import asyncio
from exmo.websocket import Client

# Реализуйте свой обработчик полученных данных
async def my_handler(response):
    print(response)

async def main():
    data = {
        "url": "wss://ws-api.exmo.com:443/v1/public",
        "init_messages": (
            '{"id":1,"method":"subscribe","topics":["spot/trades:BTC_USD", "spot/ticker:LTC_USD"]}',
        )
    }

    client = Client(my_handler)
    task = asyncio.create_task(client.listen(data))
    await asyncio.gather(task)

asyncio.run(main())
```
Первым делом мы импортируем класс Client из нашего пакета exmo.

Затем создаем асинхронный обработчик my_handler, который будет вызываться при получении ответа от сервера и выводить его в консоль.

Далее в функции main() создаем словарь data, содержащий URL-адрес для подключения к API и сообщения для инициализации подписки на определенные темы.

Создаем экземпляр класса Client, передавая ему наш обработчик my_handler, и запускаем его метод listen() в отдельном потоке при помощи функции asyncio.create_task().

Наконец, используя asyncio.gather(), ждем завершения задачи и выходим из функции.

Таким образом, этот код позволяет подключаться к публичному API Exmo и получать данные о сделках и котировках.

### Работа с приватными данными
```python
# Private data
import asyncio
import os
from exmo.websocket import Client

# Реализуйте свой обработчик полученных данных
async def my_handler(response):
    print(response)

async def main():
    api_key = os.getenv('API_KEY')
    secret_key = os.getenv('SECRET_KEY')
    data = {
        "url": "wss://ws-api.exmo.com:443/v1/private",
        "init_messages": (
            Client.create_login_message(api_key, secret_key),
            '{"id":1,"method":"subscribe","topics":["spot/orders","spot/user_trades"]}',
        )
    }

    client = Client(my_handler)
    task = asyncio.create_task(client.listen(data))
    await asyncio.gather(task)

asyncio.run(main())
```
Для приватных данных нужно передать ключ и секретный ключ в качестве параметров для функции Client.create_login_message(api_key, secret_key).

### Работа с приватными и публичными данными
```python
# Public and private data
import asyncio
import os
from exmo.websocket import Client


# Реализуйте свой обработчик полученных данных
async def my_handler(response):
    print(response)


async def main():
    data_public_1 = {
        "url": "wss://ws-api.exmo.com:443/v1/public",
        "init_messages": (
            '{"id":1,"method":"subscribe","topics":["spot/trades:BTC_USDT"]}',
        )
    }
    
    data_public_2 = {
        "url": "wss://ws-api.exmo.com:443/v1/public",
        "init_messages": (
            '{"id":1,"method":"subscribe","topics":["spot/ticker:BTC_USDT"]}',
        )
    }

    api_key = os.getenv('API_KEY')
    secret_key = os.getenv('SECRET_KEY')
    data_privet = {
        "url": "wss://ws-api.exmo.com:443/v1/private",
        "init_messages": (
            Client.create_login_message(api_key, secret_key),
            '{"id":1,"method":"subscribe","topics":["spot/wallet"]}',
        )
    }

    client = Client(my_handler)
    tasks = [
        asyncio.create_task(client.listen(data_public_1)),
        asyncio.create_task(client.listen(data_public_2)),
        asyncio.create_task(client.listen(data_privet))
    ]
    await asyncio.gather(*tasks)

asyncio.run(main())
```
В data указываются параметры подключения к Websocket API биржи.

## Автор
Пакет exmo разработан ChatGPT и Denis Ustinov.