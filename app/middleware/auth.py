# middleware/auth.py
from typing import List
from fastapi import HTTPException, Security
from fastapi.security import SecurityScopes
from ..services.auth import get_current_user

async def check_roles(security_scopes: SecurityScopes, user: dict = Security(get_current_user)):
    if not security_scopes.scopes:
        return user
        
    for role in security_scopes.scopes:
        if role not in user["roles"]:
            raise HTTPException(
                status_code=403,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": f"Bearer scope={security_scopes.scope_str}"},
            )
    return user