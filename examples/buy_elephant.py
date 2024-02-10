from alice_types.response import AliceResponse, Button, Response
from alice_types.request import AliceRequest
from pydantic import BaseModel, Field
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


link = 'https://market.yandex.ru/search?text=слон'
OK_Button = Button(
    title='Ладно',
    url=link
)


def get_suggests(alice_request: AliceRequest):
    # Получаем данные из SessionState
    data = alice_request.state.session

    # Выбираем две первые подсказки из массива.
    suggests = [text for text in data[:2]]

    # Если осталась только одна подсказка, предлагаем
    # подсказку (кнопку) со ссылкой на Яндекс.Маркет.
    if len(suggests) < 2:
        suggests.append(OK_Button)

    # Обновляем данные в хранилище, убираем первую подсказку, чтобы подсказки менялись
    # dp.storage.update_data(user_id, suggests=data[1:])
    return suggests


async def handle_new_session(alice_request: AliceRequest):
    suggests = get_suggests(alice_request)
    return AliceResponse(
        response=Response(
            text='Привет! Купи слона!',
            buttons=suggests
        )
    )


def handle_user_agrees():
    return AliceResponse(
        response=Response(
            text=f'Слона можно найти на Яндекс.Маркете!\n{link}'
        )
    )


def handle_all_other_requests(alice_request: AliceRequest):
    # Всеми силами убеждаем пользователя купить слона,
    # предлагаем варианты ответа на основе текста запроса
    user_answer = alice_request.request.original_utterance
    suggests = get_suggests(alice_request)
    return AliceResponse(
        response=Response(
            text=f'Все говорят "{user_answer}", а ты купи слона!',
            buttons=suggests
        )
    )


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=3000)
