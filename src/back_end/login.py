import requests as req
import json

def to(username = 'aboba', password = 'aboba', homeserver = 'https://matrix.org'):
    response = None
    if not username or not password or not homeserver:
        response = req.Response()
        response.status_code = 400
        response._content = b'{"error": "Bad request"}'
        return response
    response = req.post(
        url=homeserver + '/_matrix/client/r0/login',
        data=json.dumps({
            'user': username,
            'password': password,
            'type': 'm.login.password'
        }),
        headers={
            'Content-Type': 'm.login.password'
        }
    )
    return response
    
    # print(response.text)
