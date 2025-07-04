from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt

# Configuración
SECRET_KEY = "supersecreto"  # 👈 Puedes guardarlo en un .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hashear contraseña
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verificar contraseña
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Crear token JWT
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
