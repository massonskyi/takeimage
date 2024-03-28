import requests
import json


class ChatAi:
    key: str

    # f36cfec8-127d-4992-8c80-6981e1021a4c secret_key
    def auth(self):
        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

        payload = 'scope=GIGACHAT_API_PERS'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': '4a090690-e949-43fb-bf26-b4150fa7db73',
            'Authorization': 'Basic '
                             'NGEwOTA2OTAtZTk0OS00M2ZiLWJmMjYtYjQxNTBmYTdkYjczOmYzNmNmZWM4LTEyN2QtNDk5Mi04YzgwLTY5ODFlMTAyMWE0Yw=='
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False).json()

        self.key = response['access_token']

    def query(self, query, temperature=0.7, top_p=0.1, n=1, stream=False, max_tokens=512, repetition_penalty=1):
        self.auth()
        url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
        payload = json.dumps({
            "model": "GigaChat:latest",
            "messages": [
                {
                    "role": "user",
                    "content": f"{query}"
                }
            ],
            "temperature": temperature,
            "top_p": top_p,
            "n": n,
            "stream": stream,
            "max_tokens": max_tokens,
            "repetition_penalty": repetition_penalty
        })
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.key}'
        }
        response = requests.request("POST", url, headers=headers, data=payload, verify=False).json()
        return response['choices'][0]['message']['content']
