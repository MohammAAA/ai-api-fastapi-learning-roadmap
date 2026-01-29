'''
Locust is a load testing tool
It shall be run before deploying
'''

from locust import HttpUser, task

class User(HttpUser):
    @task
    def ask_ai(self):
        self.client.post("/api/v1/chat", 
            params={"conversation_id": "locust_test", "message": "Hello"})