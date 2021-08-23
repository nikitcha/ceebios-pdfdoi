from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import get_page, update_page
from pydantic import BaseModel
import ml
import database

app = FastAPI()
origins = ['http://localhost:3000']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Page(BaseModel):
    id: int
    tokens: list
    classes: list

@app.get("/")
async def read_root():
    return {"Ping":"Pong"}

@app.post("/api/tokens/")
async def load_tokens():
    database.process_tokens()

@app.get("/api/page/{id}")
async def api_get_page(id):
    response = get_page(id)
    if response:
        return response
    raise HTTPException(404, 'Page number {} not in DB'.format(id))

@app.post("/api/dois/")
async def api_save_page():
    pages = database.get_annotated_pages()
    ml.get_dois(pages)

@app.post("/api/save/")
async def api_save_page(page:Page):
    update_page(page.id, page.tokens, True)

@app.post("/api/reset/")
async def api_reset_page(page:Page):
    update_page(page.id, page.tokens, False)

@app.post("/api/convert/")
async def api_reset_page():
    database.pdf_to_json()