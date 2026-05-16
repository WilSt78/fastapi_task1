from pydantic import SecretStr

TOKEN_EXPIRE_TIME = 5
SECRET_KEY = SecretStr('oknbgfreszqasxcftgbnmkoikl')
ALGORITHM = "HS256"