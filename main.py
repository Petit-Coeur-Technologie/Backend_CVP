from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def index_root():
    return {"message": "Bienvenue sur l'interface de developpement de conakry ville propre"}