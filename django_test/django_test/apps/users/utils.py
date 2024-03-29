from .contants import expires_at


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'user_id': user.id,
        'username': user.name,
        'token': token,
        'expires_at': expires_at
    }