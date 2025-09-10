from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()
EXPECTED_TOKEN = "CAT&DOGS!"

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Vérification du token d'authentification"""
    if credentials.credentials != EXPECTED_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials