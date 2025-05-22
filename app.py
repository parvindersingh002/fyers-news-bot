from flask import Flask, request
import requests

app = Flask(__name__)

client_id = "KPDSVZIUOM-100@app"  # already @APP added
secret_key = "3LT3278EP5"
redirect_uri = "https://9bd3-2404-7c80-4c-9282-a10a-9383-8c84-ef21.ngrok-free.app/callback"

@app.route('/')
def login():
    auth_url = (
        f"https://api.fyers.in/api/v2/generate-authcode?"
        f"client_id={client_id}&"
        f"redirect_uri={redirect_uri}&"
        f"response_type=code&state=xyz"
    )
    return f'<a href="{auth_url}">Login with Fyers</a>'

@app.route('/callback')
def callback():
    auth_code = request.args.get('code')
    print("Auth Code received:", auth_code)
    if not auth_code:
        return "No auth code received or error occurred"

    token_url = "https://api.fyers.in/api/v2/token"
    payload = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "secret_key": secret_key,
        "redirect_uri": redirect_uri,
        "code": auth_code
    }

    token_response = requests.post(token_url, json=payload)
    data = token_response.json()

    return f"Access Token Response:<br>{data}"

if __name__ == '__main__':
    app.run(port=5000)
