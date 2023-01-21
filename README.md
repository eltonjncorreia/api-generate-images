# API para gerar imagens com OpenAI

Gerar uma variação de imagens

```
bash
curl --location --request POST 'http://localhost:8000/images/variation' \
--form 'file=@"///wsl$/Ubuntu-20.04/home/elton/files/gato.png"'
```

Gerar imagem por textos

```
bash
curl --location --request POST 'http://localhost:8000/images/new' \
--form 'prompt="adicione um macbook na mesa"'
```
