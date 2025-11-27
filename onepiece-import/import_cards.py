import csv
from pymongo import MongoClient

MONGO_URI = "mongodb+srv://onepiece-user:onepiece123@cluster0.l7ruwos.mongodb.net/?appName=Cluster0"

DB_NAME = "onepiece_db"
COLLECTION_NAME = "cards"

CSV_FILE = "OPTCG_Cards.csv"

NUMERIC_FIELDS = [
    "card_art_variant",
    "card_power",
    "card_cost",
    "card_counter",
    "card_banned",
]

def convert_numeric_fields(row):
    for field in NUMERIC_FIELDS:
        if field in row:
            value = row[field].strip()
            if value == "":
                row[field] = None
            else:
                try:
                    row[field] = int(value)
                except ValueError:
                    row[field] = value
    return row

def main():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    documents = []
    with open(CSV_FILE, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row = convert_numeric_fields(row)
            documents.append(row)

    if documents:
        result = collection.insert_many(documents)
        print(f"Inseridos {len(result.inserted_ids)} documentos na collection '{COLLECTION_NAME}'.")
    else:
        print("Nenhum dado encontrado no CSV.")

if __name__ == "__main__":
    main()
