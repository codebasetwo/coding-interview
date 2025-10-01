from pydantic import BaseModel, Field, EmailStr, computed_field

class SignupRequest(BaseModel):
    user_name: str = Field(..., min_length=3, max_length=50, example="john_doe")
    email: EmailStr = Field(..., example="john.doe@example.com")
    password: str = Field(..., min_length=6, max_length=32, example="securepassword123")
    first_name: str = Field(...,  max_length=50, example="John")
    last_name: str = Field(...,  max_length=50, example="Doe")
    middle_name: str | None = None
    
    @computed_field
    @property
    def full_name(self) -> str:
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        
        return f"{self.first_name} {self.last_name}"
    

class SigninRequest(BaseModel):
    user_name: str | None = None
    email: str | None = None
    password: str


class PasswordResetRequestModel(BaseModel):
    email: str


class PasswordResetConfirmModel(BaseModel):
    new_password: str
    confirm_new_password: str