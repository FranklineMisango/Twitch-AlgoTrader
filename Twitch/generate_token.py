import requests
from config import TWITCH_TOKEN
from config import TWITCH_CLIENT_ID
from config import TWITCH_APP_SECRET

client_id = TWITCH_CLIENT_ID
client_secret = TWITCH_APP_SECRET
redirect_uri = "http://localhost"
grant_type = "authorization_code"
code = "AUTHORIZATION_CODE"
# Construct the authorization URL with scopes
scopes = "chat:read chat:edit channel:moderate"  # Add the desired scopes here
auth_url = f"https://id.twitch.tv/oauth2/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope={scopes}"
# Redirect the user to the authorization URL
print("Please visit the following URL and authorize your application:")
print(auth_url)

# After the user authorizes your application, they will be redirected to the redirect_uri with the authorization code appended as a query parameter.

# Retrieve the authorization code from the redirected URL
authorization_code = input("Enter the authorization code from the redirected URL: ")

# Make a POST request to the token endpoint
token_url = "https://id.twitch.tv/oauth2/token"
payload = {
    "client_id": client_id,
    "client_secret": client_secret,
    "redirect_uri": redirect_uri,
    "grant_type": "authorization_code",
    "code": authorization_code
}

response = requests.post(token_url, data=payload)

# Extract the access token from the response
if response.status_code == 200:
    data = response.json()
    access_token = data["access_token"]
    expires_in = data["expires_in"]
    print("Access token:", access_token)
    print("Token expires in", expires_in, "seconds")

else:
    print("Failed to obtain access token:", response.text)