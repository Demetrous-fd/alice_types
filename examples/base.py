from alice_types.response import AliceResponse
from alice_types.request import AliceRequest
from fastapi import FastAPI

app = FastAPI()


@app.post(path="/")
async def handler(alice_request: AliceRequest):
    reply = AliceResponse()

    if alice_request.is_ping():
        reply.response.text = "pong"
        return reply

    if alice_request.is_new_session():
        reply.response.text = "Привет, скажи что-нибудь и я это повторю"
        return reply

    reply.response.text = alice_request.request.original_utterance
    return reply


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=3000)
