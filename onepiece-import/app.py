from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import os

MONGO_URI = "mongodb+srv://onepiece-user:onepiece123@cluster0.l7ruwos.mongodb.net/?appName=Cluster0"
print("DEBUG MONGO_URI:", MONGO_URI)  # <- ADICIONA ESTA LINHA

app = Flask(__name__)
CORS(app)  

client = MongoClient(MONGO_URI)
db = client["onepiece_db"]
cards_col = db["cards"]


def serialize_card(doc):
    """Converte o documento do Mongo em algo que o JSON entende."""
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
        # Pesquisa por nome aproximado, case-insensitive
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


@app.route("/api/cards/<card_id>", methods=["GET"])
def get_card(card_id):
    """
    Busca uma carta pelo campo card_id do CSV.
    Exemplo: /api/cards/OP01-001
    """

    doc = cards_col.find_one({"card_id": card_id})

    if not doc:
        return jsonify({"error": "Card not found"}), 404

    return jsonify(serialize_card(doc))


if __name__ == "__main__":
    app.run(debug=True)
