from flask import session
from functools import wraps
import requests

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print("decorator works!")
        user = dict(session).get('profile', None)

        if not user:
            return 'You aint logged in, no page for u!'
        else:
            print(user)
            token = user['token']

            url = 'http://localhost:8000/api/protected'
            headers = {'Authorization': 'Bearer {}'.format(token)}

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                # Successful response
                data = response.json()
                print(data['id'])
                return f(*args, **kwargs)
            else:
                # Error response
                return 'You aint logged in, no page for u!'
    return decorated_function