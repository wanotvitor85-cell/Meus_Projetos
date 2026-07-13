#Criar um sistema backend para cadastro de clientes com as seguintes funcionalidades:
#1. cadastrar cliente(Post)
#2. Listar clientes(Get)
#3. Atualizar cliente(Put)
#4. Deletar cliente(Delete)


#Importar framework e outras bibliotecas necessárias
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
#Criar a aplicação FastAPI
app = FastAPI()
#Facilitar a criação de clientes com a classe Cliente
class Cliente(BaseModel):
    nome_cliente: str
    email_cliente: str
    telefone_cliente: str
#Transformar a classe Cliente em um dicionário para otimizar a manipulação dos dados
clients = {}
#1.1.Listar clientes(Get)
@app.get("/clientes")
def get_clientes_cadastrados (page: int = 1, limit: int = 10):    #Criar a paginação para a listagem de clientes, com os parâmetros page e limit.
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Page e limit devem ser maiores que 0.")
    if not clients:
        return {"message": "Não existem clientes cadastrados."}
    organizador = sorted(clients.items(), key=lambda x: x[0])  # Ordena os clientes por ID
    start = (page - 1) * limit
    end = start + limit
    clients_paginated = [
        {"id": id, "nome_cliente": cliente_data["nome_cliente"], "email_cliente": cliente_data["email_cliente"], "telefone_cliente": cliente_data["telefone_cliente"]}
        for id, cliente_data in organizador[start:end]
        
    ]
    return {
        "page": page,
        "limit": limit,
        "total_clientes": len(clients),
        "clientes": clients_paginated
    }

#Post - Adicionar um novo cliente
@app.post("/adicionar_cliente")
def adiciona_cliente(id: int, cliente: Cliente):
    if id in clients:
        raise HTTPException(status_code=400, detail="Cliente já existe.")
    else:
        clients[id] = cliente.model_dump()
    return {"message": "Cliente adicionado com sucesso."}

#Put- Atualizar os dados de um cliente existente

@app.put("/atualizar_cadastro_cliente/{id}")
def atualiza_cliente(id: int, cliente: Cliente):
    meu_cliente = clients.get(id)
    if not meu_cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    else:
        clients[id] = cliente.model_dump()
        return {"message": "Cliente atualizado com sucesso."}
    

#Delete - Remover um cliente
@app.delete("/remover_cliente/{id}")
def remove_cliente(id: int):
    if id not in clients:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    else:
        del clients[id]
        return {"message": "Cliente removido com sucesso."}
    

