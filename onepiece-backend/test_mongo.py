from pymongo import MongoClient

MONGO_URI = "mongodb+srv://onepiece-user:onepiece123@cluster0.l7ruwos.mongodb.net/?appName=Cluster0"

# timeout baixo só pra não ficar esperando 20s
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

print("SEEDS:", client._topology_settings.seeds)

try:
    result = client.admin.command("ping")
    print("PING OK:", result)
except Exception as e:
    print("ERRO AO CONECTAR:")
    print(repr(e))
