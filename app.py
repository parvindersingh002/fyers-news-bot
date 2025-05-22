from flask import Flask, request, redirect
import requests
import urllib.parse

app = Flask(__name__)

client_id = "KPDSVZIUOM-100@APP"  # apna client id yahan likho
secret_key = "3LT3278EP5"          # apna secret key yahan likho
redirect_uri = "https://your-ngrok-url.ngrok.io/callback"  # apna HTTPS ngrok ya deployed URL

@app.route('/')
def home():
    # URL encode redirect_uri
    encoded_redirect_uri = urllib.parse.quote(redirect_uri, safe='')

    auth_url = (
        f"https://api.fyers.in/api/v2/generate-authcode?"
        f"client_id={client_id}&"
        f"redirect_uri={encoded_redirect_uri}&"
        f"response_type=code&state=xyz"
    )
    return f'<h2>Login with Fyers</h2><a href="{auth_url}">Click here to Login</a>'

@app.route('/callback')
def callback():
    # print all query params for debugging
    print("Callback Query Params:", request.args)
    
    auth_code = request.args.get('code')
    error = request.args.get('error')

    if error:
        return f"Error during authorization: {error}"

    if not auth_code:
        return "No auth code received or error occurred"

    # Exchange auth code for access token
    token_url = "https://api.fyers.in/api/v2/token"
    payload = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "secret_key": secret_key,
        "redirect_uri": redirect_uri,
        "code": auth_code
    }

    # Use JSON payload for POST request
    token_response = requests.post(token_url, json=payload)
    data = token_response.json()
    print("Token Response:", data)

    return f"<h3>Access Token Response:</h3><pre>{data}</pre>"

if __name__ == '__main__':
    app.run(port=5000, debug=True)
