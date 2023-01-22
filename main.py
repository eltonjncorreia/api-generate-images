from PIL import Image
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, Form
from io import BytesIO

import openai
import os

from config import get_settings
from payload import Payload

load_dotenv()

settings = get_settings()
app = FastAPI()
openai.api_key = os.getenv("OPENAI_KEY")


@app.post("/images/new/")
async def image_new(prompt: str = Form("prompt")):
    if prompt:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024",
        )

        return response


@app.post("/images/variation")
async def variation_image(file: UploadFile):
    img_resized = resize_image(file=file)

    if img_resized:
        response = openai.Image.create_variation(
            image=img_resized,
            n=10,
            size="1024x1024",
        )

        return response


@app.post("/text/")
async def completations(payload: Payload):
    return openai.Completion.create(
        engine="text-davinci-002",
        prompt=(f"{payload.prompt}: {payload.text}"),
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )


def resize_image(file: UploadFile):
    # Abrir a imagem
    with Image.open(file.filename) as img:
        # Redimensionar a imagem
        img = img.resize((700, 700))

        # converter RGB para RGBA pois a OpenAI esperar RGBA
        img = img.convert("RGBA")

        # buffer
        byte_stream = BytesIO()

        # Salvar a imagem redimensionada
        img.save(byte_stream, format="PNG")

        return byte_stream.getvalue()
