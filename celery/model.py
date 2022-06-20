from pydantic import BaseModel


class UserRegister(BaseModel):
    task_id: str = "user.register"
    count: int = 0

    def add():
        self.count += 1

class UserLogin(BaseModel):
    task_id: str = "user.login"
    count: int = 0


class UserLoginFederated(BaseModel):
    task_id: str = "user.login.federated"
    count: int = 0

class UserRegisterFederated(BaseModel):
    task_id: str = "user.register.federated"
    count: int = 0

