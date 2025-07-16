from pydantic import BaseModel


class Envs(BaseModel):
    frontend_url: str
    gateway_url: str
    profile_url: str
    test_username: str
    test_password: str
    registration_url: str
    auth_url: str
    api_auth_url: str
