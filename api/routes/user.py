from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserOut
from schemas.token import Token
from controllers import user_controller
from services.auth_service import verify_password, create_access_token
from database.connection import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_controller.create_user(db, user)

@router.get("/", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
    return user_controller.get_all_users(db)

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = user_controller.get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
