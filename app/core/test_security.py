import pytest
from datetime import timedelta, datetime
from jose import jwt, JWTError
from app.core.security import create_access_token, SECRET_KEY, ALGORITHM

# app/core/test_security.py

def test_create_access_token_success():
    data = {"sub": "testuser"}
    token = create_access_token(data)
    assert token is not None

def test_create_access_token_contains_data():
    data = {"sub": "testuser"}
    token = create_access_token(data)
    decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded_data["sub"] == "testuser"

def test_create_access_token_expiration():
    data = {"sub": "testuser"}
    expires_delta = timedelta(minutes=1)
    token = create_access_token(data, expires_delta)
    decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    expire_time = datetime.utcfromtimestamp(decoded_data["exp"])
    assert expire_time < datetime.utcnow() + timedelta(minutes=2)
    assert expire_time > datetime.utcnow()

def test_create_access_token_default_expiration():
    data = {"sub": "testuser"}
    token = create_access_token(data)
    decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    expire_time = datetime.utcfromtimestamp(decoded_data["exp"])
    assert expire_time < datetime.utcnow() + timedelta(minutes=16)
    assert expire_time > datetime.utcnow() + timedelta(minutes=14)

def test_create_access_token_invalid_token():
    invalid_token = "invalid.token.string"
    with pytest.raises(JWTError):
        jwt.decode(invalid_token, SECRET_KEY, algorithms=[ALGORITHM])

def test_create_access_token_expired_token():
    data = {"sub": "testuser"}
    expires_delta = timedelta(seconds=-1)
    token = create_access_token(data, expires_delta)
    with pytest.raises(JWTError):
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

def test_create_access_token_missing_data():
    with pytest.raises(TypeError):
        create_access_token()
