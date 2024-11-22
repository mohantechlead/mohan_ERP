import requests

class GeminiAPI:
    BASE_URL = "https://api.gemini.com"  # Update with the actual API base URL

    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key

    def analyze_data(self, query):
        url = f"{self.BASE_URL}/analyze"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }
        data = {"query": query}
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.text}
