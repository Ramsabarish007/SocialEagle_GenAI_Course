import os
from livekit import api

# Use your dev credentials
API_KEY = "devkey"
API_SECRET = "secret"

def create_token():
    token = api.AccessToken(API_KEY, API_SECRET) \
        .with_identity("python-user") \
        .with_name("Python User") \
        .with_grants(api.VideoGrants(
            room_join=True,
            room="my-room",
        ))
    
    print(token.to_jwt())

if __name__ == "__main__":
    create_token()