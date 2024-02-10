## AliceTypes

Библиотека моделей Pydantic-V2 для валидации протокола Я.Диалогов

## Установка:

```shell
pip install alice_types
```

## Использование

<details>
<summary><strong>Пример с FastApi</strong></summary>

```python
from alice_types.response import AliceResponse
from alice_types.request import AliceRequest
from fastapi import FastAPI

app = FastAPI()


@app.post(path="/")
async def handler(alice_request: AliceRequest):
    reply = AliceResponse()

    if alice_request.is_new_session():
        reply.response.text = "Привет, скажи что-нибудь и я это повторю"
        return reply

    reply.response.text = alice_request.request.original_utterance
    return reply
```

</details>

<details>
<summary><strong>Пример с AIOHttp</strong></summary>

```python
from alice_types.response import AliceResponse
from alice_types.request import AliceRequest
from aiohttp import web


async def handler(request):
    body = await request.json()
    alice_request = AliceRequest.model_validate(body)

    reply = AliceResponse()

    if alice_request.is_new_session():
        reply.response.text = "Привет, скажи что-нибудь и я это повторю"
    else:
        reply.response.text = alice_request.request.original_utterance

    body = reply.model_dump()
    return web.json_response(body)


app = web.Application()
app.router.add_post('/', handler)

if __name__ == "__main__":
    web.run_app(app)

```

</details>

### Расширение типов полей

В библиотеке имеются модели с динамически расширяемыми полями:

- [request.State](https://github.com/Demetrous-fd/alice_types/blob/main/examples/extend_fields/state.py)
    - State.extend_session_model(model: BaseModel)
    - State.extend_user_model(model: BaseModel)
    - State.extend_application_model(model: BaseModel)
- [request.RequestPurchase.payload](https://github.com/Demetrous-fd/alice_types/blob/main/examples/extend_fields/purchase.py)
  - RequestPurchase.extend_payload_model(model: BaseModel)

### Ограничение размера хранилищ для модели ответа

В модели AliceResponse по умолчанию установлен стандартный размер хранилищ (1 КБ), который можно изменить при
необходимости:

```python
from alice_types.response import AliceResponse

AliceResponse.set_session_state_limit_size(1024 * 8)
AliceResponse.set_user_state_limit_size(1024 * 16)
AliceResponse.set_application_state_limit_size(1024 * 32)
```

### Публичные методы
<details>
<summary>AliceRequest</summary>
<ul>
<li>AliceRequest.is_ping()</li>
<li>AliceRequest.is_new_session()</li>
<li>AliceRequest.authorization_is_completed()</li>
</ul>

```python
from alice_types.response import AliceResponse, Response
from alice_types.request import AliceRequest


async def handler(alice_request: AliceRequest):
    if alice_request.is_ping():
        return AliceResponse(
            response=Response(
                text="pong"
            )
        )
    
    elif alice_request.is_new_session():
        return AliceResponse(
            response=Response(
                text="Привет, скажи что-нибудь и я это повторю"
            )
        )
    
    elif alice_request.authorization_is_completed():
        return AliceResponse(
            response=Response(
                text="Ты авторизован это хорошо 👍"
            )
        )
    ...
```
</details>
<details>
<summary>AliceRequest.request.nlu.entities</summary> 

<ul>
<li>entities.get(entity_type: SlotsType | str) - <strong>Возвращает список сущностей заданного типа.</strong></li>
<li>entity.available() - <strong>Возвращает список доступных атрибутов объекта, у которых значение не равно None. Метод доступен у всех сущностей.</strong></li>
<li>EntityDatetime.to_datetime(timezone: pytz.BaseTzInfo | str | None = None)</li>
</ul>

```python
from typing import List

from alice_types.request import AliceRequest, SlotsType, EntityFio, EntityDatetime


async def handler(alice_request: AliceRequest):
    fio_entities: List[EntityFio] = alice_request.request.nlu.entities.get(SlotsType.YANDEX_FIO)
    names = []
    for entity in fio_entities:
        if "first_name" in entity.value.available():
            names.append(entity.value.first_name)

    dates = []
    datetime_entities: List[EntityDatetime] = alice_request.request.nlu.entities.get(SlotsType.YANDEX_DATETIME)
    for entity in datetime_entities:
        dates.append(
            entity.to_datetime(
                timezone=alice_request.meta.timezone  # Default: None
            )
        )
    ...
```

</details>
<details>

<summary>AliceRequest.request.meta.interfaces</summary>

<ul>
<li>interfaces.has(interface: Union[InterfaceType, str]) - <strong>Проверяет, существует ли этот интерфейс.</strong></li>
<li>interfaces.available() - <strong>Возвращает список доступных интерфейсов.</strong></li>
</ul>

```python
from alice_types.request import AliceRequest, InterfaceType


async def handler(alice_request: AliceRequest):
    if alice_request.meta.interfaces.has(InterfaceType.SCREEN):
        pass
```
</details>


### Примеры

- [EchoBot](https://github.com/Demetrous-fd/alice_types/blob/main/examples/base.py)
- [Авторизация](https://github.com/Demetrous-fd/alice_types/blob/main/examples/auth.py)
- Расширение типов полей:
    - [request.State](https://github.com/Demetrous-fd/alice_types/blob/main/examples/extend_fields/state.py)
    - [request.RequestPurchase.payload](https://github.com/Demetrous-fd/alice_types/blob/main/examples/extend_fields/purchase.py)
