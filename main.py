from PIL import Image
from fastapi import FastAPI, UploadFile, Form
from io import BytesIO

import openai
import os

openai.api_key = os.getenv("OPENAI_KEY")

app = FastAPI()


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
