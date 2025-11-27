# One Piece TCG – Biblioteca de Cartas (Vue + Flask + MongoDB)

**Aluno:** Filipe Satoyoshi Sakaida  
**Disciplina:** Programação Avançada  
**Prova 3 – Aplicação Web com Frontend em Vue.js, Backend em Flask e Banco NoSQL (MongoDB Atlas)**

Aplicação Web para consulta de cartas do **One Piece Card Game**, com:

- Frontend em **Vue.js**
- Backend em **Flask (Python)**
- Banco de dados **MongoDB Atlas (NoSQL)**
- Comunicação front–back via **Web Services REST (JSON)**

A aplicação permite:
- Login com usuário/senha
- Consulta de cartas do One Piece TCG
- Cadastro de cartas favoritas
- Edição de nota/comentário em favoritos
- Remoção de favoritos

Atende aos requisitos da disciplina:
- Separação em frontend (Vue) e backend (Flask)
- Uso de MongoDB Atlas com PyMongo
- CRUD completo em uma collection NoSQL
- Controle de acesso com login e senha
- Melhorias visuais (CSS e imagens)

---

## 1. Arquitetura do Projeto

Estrutura de pastas:

Prova 3/
├── onepiece-backend/      # API em Flask
├── onepiece-frontend/     # Aplicação Vue.js (SPA)
└── onepiece-import/       # Script Python para importar o CSV de cartas

Banco de Dados (MongoDB Atlas)

Cluster criado no MongoDB Atlas

Database: onepiece_db

Collections:

cards – cartas oficiais do One Piece TCG, importadas de um arquivo CSV (OPTCG_Cards.csv)

favorites – cartas favoritas do usuário, com campo extra de nota/comentário (note)

## 2. Backend (Flask + PyMongo)
2.1. Tecnologias

- Python 3
- Flask
- flask-cors
- PyMongo

2.2. Instalação

No terminal:

cd "Prova 3/onepiece-backend"

# criar ambiente virtual (macOS / Linux)
python3 -m venv venv

# ativar ambiente virtual
source venv/bin/activate

# instalar dependências
pip install flask flask-cors pymongo
# ou, se houver requirements.txt:
# pip install -r requirements.txt

2.3. Configuração da conexão com o MongoDB Atlas

No arquivo onepiece-backend/app.py existe a constante:

MONGO_URI = "mongodb+srv://<usuario>:<senha>@<cluster>.mongodb.net/?appName=Cluster0"


Substituir <usuario>, <senha> e <cluster> pelos dados do usuário e cluster criados no Atlas.

O backend usa:

from pymongo import MongoClient

client = MongoClient(MONGO_URI)
db = client["onepiece_db"]
cards_col = db["cards"]
favorites_col = db["favorites"]

2.4. Executar o backend

Com o ambiente virtual ativado:

cd "Prova 3/onepiece-backend"
source venv/bin/activate
python3 app.py


O servidor Flask subirá em:

http://127.0.0.1:5000

## 3. Frontend (Vue.js)
3.1. Tecnologias

Vue.js (criado com npm create vue@latest)

Vue Router

Fetch API para chamadas ao backend

3.2. Instalação

Em outro terminal:

cd "Prova 3/onepiece-frontend"

# instalar dependências
npm install

3.3. Executar o frontend
npm run dev


A aplicação ficará disponível em:

http://localhost:5173/


Importante: o backend Flask deve estar rodando em http://127.0.0.1:5000 para o frontend funcionar.

## 4. Funcionalidades Implementadas
4.1. Login (controle de acesso)

Página inicial (/) é uma tela de login.

A página envia um POST para /api/login no backend.

Credenciais padrão (para demonstração):

Usuário: admin

Senha: admin123

Em caso de sucesso:

O backend devolve um JSON com { success: true, token: "..." }

O frontend salva o token em localStorage (authToken)

O usuário é redirecionado para /cards

As rotas /cards e /favorites verificam a existência do token:

Se não houver token, o usuário é redirecionado de volta para / (login).

Atende ao requisito de implementação de controle de acesso com login e senha em página inicial.

4.2. Listagem de cartas (collection cards)

Página /cards:

Lista as cartas da collection cards vindas do MongoDB Atlas.

Mostra:

Nome da carta

Código

card_id

Cor

Tipo

Raridade

Expansão

Custo

Poder

Efeito

Imagem (card_image)

Possui:

Campo de busca por nome, que envia ?name= como query string para a API (/api/cards?name=Zoro).

Layout em grid com CSS.

Uso de figuras (imagens das cartas).

Cada carta possui um botão:

⭐ Favoritar

Faz POST para /api/favorites com o card_id.

Exibe um popup (toast) informando se:

A carta foi adicionada aos favoritos, ou

A carta já estava nos favoritos.

4.3. Favoritos com CRUD completo (collection favorites)

A collection favorites é usada para atender ao requisito de CRUD completo (Create, Retrieve, Update, Delete).

Cada documento em favorites contém pelo menos:

card_id: código da carta (ex.: OP09-118-0)

note: texto opcional com a nota/comentário do usuário

a) Create (C) – Criar favorito

Endpoint: POST /api/favorites

Corpo (JSON):

{
  "card_id": "OP09-118-0",
  "note": "Carta muito forte no meta"
}


Comportamento:

Verifica se a carta existe na collection cards.

Evita duplicados (não adiciona duas vezes o mesmo card_id).

Retorna 201 em caso de criação ou mensagem de “já está nos favoritos”.

No frontend, isso é disparado pelo botão ⭐ Favoritar na página /cards.

b) Retrieve (R) – Listar favoritos

Endpoint: GET /api/favorites

Retorna uma lista de favoritos, incluindo os dados da carta ligada ao card_id:

[
  {
    "id": "...",
    "card_id": "OP09-118-0",
    "note": "Minha anotação",
    "card": {
      "card_id": "OP09-118-0",
      "card_name": "...",
      "card_color": "...",
      "card_image": "...",
      "...": "..."
    }
  }
]


No frontend, essa listagem é exibida na página /favorites.

c) Update (U) – Atualizar nota/comentário

Endpoint: PUT /api/favorites/<fav_id>

Corpo (JSON):

{
  "note": "Nova anotação sobre a carta"
}


Atualiza apenas o campo note do documento com _id = fav_id.

Na página /favorites, cada carta favorita possui um campo textarea com a nota e um botão “Salvar nota”, que dispara esse PUT.
Em caso de sucesso, o usuário vê um popup (toast) com a mensagem “Nota atualizada com sucesso.”

d) Delete (D) – Remover favorito

Endpoint: DELETE /api/favorites/<fav_id>

Remove o documento da collection favorites.

Na página /favorites, o botão “Remover dos favoritos” dispara essa operação, atualiza a tela e exibe um popup informando o sucesso da remoção.

5. Endpoints da API (Resumo)

Base: http://127.0.0.1:5000

5.1. Sistema

GET /api/ping

Teste rápido da API.

Resposta: {"message": "pong"}

5.2. Autenticação

POST /api/login

Corpo:

{
  "username": "admin",
  "password": "admin123"
}


Resposta (sucesso):

{
  "success": true,
  "token": "onepiece-token"
}

5.3. Cartas (cards)

GET /api/cards

Query params opcionais:

name – filtro por nome (regex, case-insensitive)

color, type, expansion – preparados para filtros adicionais

Exemplo: /api/cards?name=Zoro

GET /api/cards/<card_id>

Exemplo: /api/cards/OP09-118-0

Retorna os dados completos de uma carta específica.

5.4. Favoritos (favorites)

GET /api/favorites

Lista todos os favoritos, incluindo os dados da carta.

POST /api/favorites

Adiciona uma carta aos favoritos.

Corpo:

{
  "card_id": "OP09-118-0",
  "note": "Minha anotação"
}


PUT /api/favorites/<fav_id>

Atualiza a nota de um favorito.

Corpo:

{
  "note": "Nova anotação"
}


DELETE /api/favorites/<fav_id>

Remove o favorito especificado.

6. Importação das cartas (Script auxiliar)

Na pasta onepiece-import/ existe um script Python responsável por:

Ler o arquivo CSV OPTCG_Cards.csv

Tratar os campos

Inserir os documentos na collection cards do MongoDB Atlas

Esse script é utilizado apenas para carga inicial dos dados e não é exposto no frontend.

7. Forma de entrega (GitHub)

Para envio ao GitHub:

Não versionar as pastas:

onepiece-backend/venv

onepiece-frontend/node_modules

Versionar:

Código do backend

Código do frontend

Script de importação (opcional)

Este arquivo README.md

8. Possíveis Melhorias Futuras

Cadastro de usuários reais na collection users (registro + login por banco).

Filtros avançados por cor, expansão e tipo na listagem de cartas.

Página de detalhes da carta (/cards/:card_id).

Layout mais próximo de sites como Liga One Piece / OneLogTCG.