from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import os

MONGO_URI = "mongodb+srv://onepiece-user:onepiece123@cluster0.l7ruwos.mongodb.net/?appName=Cluster0"

VALID_USER = "admin"
VALID_PASS = "admin123"

app = Flask(__name__)
CORS(app)

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = client["onepiece_db"]

cards_col = db["cards"]
favorites_col = db["favorites"]
users_col = db["users"]  



def serialize_card(doc):
    return {
        "id": str(doc.get("_id")),
        "card_id": doc.get("card_id"),
        "card_code": doc.get("card_code"),
        "card_name": doc.get("card_name"),
        "card_color": doc.get("card_color"),
        "card_type": doc.get("card_type"),
        "card_rarity": doc.get("card_rarity"),
        "card_expansion": doc.get("card_expansion"),
        "card_cost": doc.get("card_cost"),
        "card_power": doc.get("card_power"),
        "card_counter": doc.get("card_counter"),
        "card_effect": doc.get("card_effect"),
        "card_trigger": doc.get("card_trigger"),
        "card_image": doc.get("card_image"),
        "card_banned": doc.get("card_banned"),
    }

def serialize_favorite(doc):
    return {
        "id": str(doc.get("_id")),
        "card_id": doc.get("card_id"),
    }

def get_current_user_id():
    """
    Lê o user_id do header 'X-User-Id'.
    """
    user_id = request.headers.get("X-User-Id")
    if not user_id:
        return None

    try:
        _ = ObjectId(user_id)
    except Exception:
        return None

    return user_id


@app.route("/api/ping")
def ping():
    return {"message": "pong"}


@app.route("/api/cards", methods=["GET"])
def list_cards():
    """
    Lista cartas com filtros simples por query string:
    - ?name=Zoro
    - ?color=Red
    - ?type=Character
    - ?expansion=OP01
    """

    query = {}

    name = request.args.get("name")
    color = request.args.get("color")
    card_type = request.args.get("type")
    expansion = request.args.get("expansion")

    if name:
        query["card_name"] = {"$regex": name, "$options": "i"}

    if color:
        query["card_color"] = color

    if card_type:
        query["card_type"] = card_type

    if expansion:
        query["card_expansion"] = expansion

    cursor = cards_col.find(query).limit(50)
    cards = [serialize_card(doc) for doc in cursor]

    return jsonify(cards)


@app.route("/api/favorites", methods=["GET"])
def list_favorites():
    """
    Lista favoritos do usuário logado.
    Lê o user_id do header X-User-Id.
    """

    user_id = get_current_user_id()
    if not user_id:
        return jsonify({"error": "Usuário não autenticado"}), 401

    favorites = []
    for fav in favorites_col.find({"user_id": user_id}):
        card = cards_col.find_one({"card_id": fav.get("card_id")})
        favorites.append({
            "id": str(fav.get("_id")),
            "card_id": fav.get("card_id"),
            "note": fav.get("note", ""),
            "card": serialize_card(card) if card else None,
        })
    return jsonify(favorites)



@app.route("/api/favorites", methods=["POST"])
def add_favorite():
    """
    Adiciona uma carta aos favoritos do usuário logado.
    Espera JSON: { "card_id": "OP01-001-0", "note": "alguma anotação" }
    """

    user_id = get_current_user_id()
    if not user_id:
        return jsonify({"error": "Usuário não autenticado"}), 401

    data = request.get_json() or {}
    card_id = data.get("card_id")
    note = data.get("note", "")

    if not card_id:
        return jsonify({"error": "card_id é obrigatório"}), 400

    # Verifica se a carta existe
    card = cards_col.find_one({"card_id": card_id})
    if not card:
        return jsonify({"error": "Carta não encontrada"}), 404

    # Evita duplicado para o MESMO usuário
    existing = favorites_col.find_one({"user_id": user_id, "card_id": card_id})
    if existing:
        return jsonify({
            "message": "Carta já está nos favoritos",
            "id": str(existing["_id"]),
            "card_id": existing["card_id"],
            "note": existing.get("note", ""),
        }), 200

    result = favorites_col.insert_one({
        "user_id": user_id,
        "card_id": card_id,
        "note": note
    })

    return jsonify({
        "id": str(result.inserted_id),
        "card_id": card_id,
        "note": note,
    }), 201


@app.route("/api/favorites/<fav_id>", methods=["PUT"])
def update_favorite(fav_id):
    """
    Atualiza a nota (note) de um favorito do usuário logado.
    Espera JSON: { "note": "novo texto" }
    """

    user_id = get_current_user_id()
    if not user_id:
        return jsonify({"error": "Usuário não autenticado"}), 401

    data = request.get_json() or {}
    note = data.get("note")

    if note is None:
        return jsonify({"error": "note é obrigatório"}), 400

    try:
        oid = ObjectId(fav_id)
    except Exception:
        return jsonify({"error": "ID inválido"}), 400

    result = favorites_col.update_one(
        {"_id": oid, "user_id": user_id},
        {"$set": {"note": note}}
    )

    if result.matched_count == 0:
        return jsonify({"error": "Favorito não encontrado"}), 404

    fav = favorites_col.find_one({"_id": oid})

    return jsonify({
        "id": str(fav["_id"]),
        "card_id": fav["card_id"],
        "note": fav.get("note", ""),
    }), 200



@app.route("/api/favorites/<fav_id>", methods=["DELETE"])
def delete_favorite(fav_id):
    """
    Remove um favorito pelo ID, apenas se pertencer ao usuário logado.
    """

    user_id = get_current_user_id()
    if not user_id:
        return jsonify({"error": "Usuário não autenticado"}), 401

    try:
        oid = ObjectId(fav_id)
    except Exception:
        return jsonify({"error": "ID inválido"}), 400

    result = favorites_col.delete_one({"_id": oid, "user_id": user_id})

    if result.deleted_count == 0:
        return jsonify({"error": "Favorito não encontrado"}), 404

    return jsonify({"success": True}), 200




@app.route("/api/register", methods=["POST"])
def register():
    """
    Cadastro de novo usuário.
    Espera JSON: { "username": "fulano", "password": "senha123" }
    """

    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"success": False, "error": "username e password são obrigatórios"}), 400

    # Verifica se já existe usuário com esse nome
    existing = users_col.find_one({"username": username})
    if existing:
        return jsonify({"success": False, "error": "Usuário já existe"}), 400

    password_hash = generate_password_hash(password)

    result = users_col.insert_one({
        "username": username,
        "password_hash": password_hash
    })

    return jsonify({
        "success": True,
        "message": "Usuário cadastrado com sucesso",
        "user_id": str(result.inserted_id),
        "username": username
    }), 201


@app.route("/api/login", methods=["POST"])
def login():
    """
    Login de usuário cadastrado no Mongo.
    Espera JSON: { "username": "...", "password": "..." }
    """

    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"success": False, "error": "username e password são obrigatórios"}), 400

    user = users_col.find_one({"username": username})
    if not user:
        return jsonify({"success": False, "error": "Usuário não encontrado"}), 401

    if not check_password_hash(user.get("password_hash", ""), password):
        return jsonify({"success": False, "error": "Senha incorreta"}), 401

    # Para simplificar, o "token" vai ser o próprio user_id
    user_id = str(user["_id"])

    return jsonify({
        "success": True,
        "token": user_id,       # usamos o próprio user_id como token
        "user_id": user_id,
        "username": user["username"]
    }), 200



@app.route("/api/cards/<card_id>", methods=["GET"])
def get_card(card_id):


    doc = cards_col.find_one({"card_id": card_id})

    if not doc:
        return jsonify({"error": "Card not found"}), 404

    return jsonify(serialize_card(doc))


if __name__ == "__main__":
    app.run(debug=True)
