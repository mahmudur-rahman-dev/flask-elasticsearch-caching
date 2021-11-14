import jwt


def decode(jwtToken):
    return jwt.decode(jwtToken, "secret", algorithms=["HS256"])

