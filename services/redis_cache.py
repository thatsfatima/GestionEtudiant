import redis
import json

class RedisCache:
    def __init__(self):
        self.client = redis.Redis(host='localhost', port=6379, decode_responses=True)

    def set_etudiant(self, telephone, data):
        self.client.set(telephone, json.dumps(data))

    def get_etudiant(self, telephone):
        data = self.client.get(telephone)
        return json.loads(data) if data else None

    def clear_cache(self):
        self.client.flushdb()

    def get_etudiants(self):
        data = self.redis.get("etudiants")
        if data:
            return json.loads(data)
        return None

    def set_etudiants_bulk(self, etudiants):
        self.redis.set("etudiants", json.dumps(etudiants))

    def delete_etudiant(self, telephone):
        self.redis.delete(f"etudiant:{telephone}")
        self.redis.delete("etudiants")
