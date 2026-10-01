import hashlib
import unittest

from app import app


class APITestCase(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True)
        self.client = app.test_client()

    def test_health(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "ok")
        self.assertIsInstance(response.json["host"], str)
        self.assertIsInstance(response.json["ts"], (int, float))

    def test_items(self):
        response = self.client.get("/items")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 50)
        self.assertEqual(response.json[0], {"id": 1, "nome": "Produto 1", "preco": 1.5})
        self.assertEqual(response.json[-1]["id"], 50)

    def test_existing_item(self):
        for item_id in (1, 50):
            with self.subTest(item_id=item_id):
                response = self.client.get(f"/items/{item_id}")
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json["id"], item_id)

    def test_missing_item(self):
        for item_id in (0, 51):
            with self.subTest(item_id=item_id):
                response = self.client.get(f"/items/{item_id}")
                self.assertEqual(response.status_code, 404)
                self.assertEqual(response.json, {"erro": "não encontrado"})

    def test_unknown_route(self):
        self.assertEqual(self.client.get("/unknown").status_code, 404)

    def test_cpu_default(self):
        response = self.client.get("/cpu")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["iteracoes"], 20000)
        self.assertEqual(len(response.json["hash"]), 16)

    def test_cpu_minimum_and_hash(self):
        response = self.client.get("/cpu?n=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "iteracoes": 1,
            "hash": hashlib.sha256(b"sd").hexdigest()[:16],
        })

    def test_cpu_maximum(self):
        response = self.client.get("/cpu?n=1000000")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["iteracoes"], 1000000)

    def test_cpu_invalid_input(self):
        for value in ("abc", "", "1.5", "0", "-1", "1000001", "9" * 5000):
            with self.subTest(value=value[:30]):
                response = self.client.get("/cpu", query_string={"n": value})
                self.assertEqual(response.status_code, 400)
                self.assertIn("erro", response.json)


if __name__ == "__main__":
    unittest.main()
