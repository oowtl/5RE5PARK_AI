from fastapi import FastAPI
import uvicorn

# router
from web import make_tts

app = FastAPI()


app.include_router(make_tts.router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
