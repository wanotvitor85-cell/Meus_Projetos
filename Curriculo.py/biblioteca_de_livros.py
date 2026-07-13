#API de livros
#Para usar o script corretamente é necessário colocar o script Poetry.lock e pyproject.toml, além de instalar o FastApi e Insomnia
# GET, POST, PUT, DELETE

# GET - Buscar os dados dos livros
# POST - Adicionar um novo livro
# PUT - Atualizar os dados de um livro existente
# DELETE - Remover um livro

#Estrutura CRUD
# Create - Criar um novo recurso (POST)
# Read - Ler ou buscar um recurso (GET)
# Update - Atualizar um recurso existente (PUT)
# Delete - Remover um recurso (DELETE)

#Importes 
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import secrets
import os
# Fim de importes 

app = FastAPI()
# Get - Buscar os dados dos livros
meus_livros = {}
class Livro(BaseModel):
    nome_livro: str
    autor_livro: str
    ano_publicado: int
@app.get("/")

@app.get("/livros")
def get_livros(page: int = 1, limit: int = 10):
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Page e limit devem ser maiores que 0.")
    if not meus_livros:
        return {"message": "Não existem livros cadastrados."}
    livros_ordenados =  sorted(meus_livros.items(), key=lambda x: x[0])  # Ordena os livros por ID
    start = (page - 1) * limit
    end = start + limit
    livros_paginated = [
        {"id": id, "nome_livro": livro_data["nome_livro"], "autor_livro": livro_data["autor_livro"], "ano_publicado": livro_data["ano_publicado"]}
        for id, livro_data in livros_ordenados[start:end]
    ]
    return {
        "page": page,
        "limit": limit,
        "total_livros": len(meus_livros),
        "livros": livros_paginated
    }

# Post - Adicionar um novo livro
@app.post("/adicionar_livro")
def post_livros(id: int, livro: Livro):
    if id in meus_livros:
        raise HTTPException(status_code=400, detail="Livro já existe.")
    else:
         meus_livros[id] = livro.model_dump()
    return {"message": "Livro adicionado com sucesso."}

# Put - Atualizar os dados de um livro existente
@app.put('/atualizar_livro/{id}')
def put_livros(id: int, livro: Livro):
    meu_livro = meus_livros.get(id)
    if not meu_livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")
    else:
        meus_livros[id] = livro.model_dump()
    return {"message": "Livro atualizado com sucesso."}
    

# Delete - Remover um livro
@app.delete('/remover_livro/{id}')
def delete_livros(id: int):
    if id not in meus_livros:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")
    else:
        del meus_livros[id]
    return {"message": "Livro removido com sucesso."}
