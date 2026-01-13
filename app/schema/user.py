from pydantic import BaseModel,EmailStr,field_validator


## LOGIN 
class LoginSchema(BaseModel):
    email: EmailStr
    password: str

## CREATE USER
class CreateUserSchema(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    password: str

## UPDATE USER
class UpdateSchema(BaseModel):
    firstname: str
    lastname: str


## CHANGE PASSWORD
class ChangepasswordSchema(BaseModel):
    password: str
    confirm_password: str

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, confirm_password, info):
        password = info.data.get("password")
        if password != confirm_password:
            raise ValueError("Password and confirm password do not match")
        return confirm_password
