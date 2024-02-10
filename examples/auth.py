from alice_types.response import AliceResponse, directives
from alice_types.request import AliceRequest
from fastapi import FastAPI

app = FastAPI()


@app.post(path="/")
async def handler(alice_request: AliceRequest):
    reply = AliceResponse()

    if alice_request.session.user.access_token is None:
        # Если пользователь зашел с колонки, то ему предложат открыть навык на телефоне
        reply.response.directives = directives.Directives(
            start_account_linking=directives.StartAccountLinking()
        )
        return reply

    elif alice_request.authorization_is_completed():
        reply.response.text = "Поздравляем, вы авторизованы 🎉"
        return reply

    elif alice_request.session.user.access_token:
        reply.response.text = "Вы авторизованы это хорошо 👍"
        return reply

    reply.response.text = "👀"
    return reply


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=3000)
