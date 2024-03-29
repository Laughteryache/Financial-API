from fastapi import HTTPException

# Module with exceptions (exceptions may have been written incorrectly)

UserAlreadyExistsException = HTTPException(
    status_code=401, detail="User already exists"
)

IncorrectLoginDataException = HTTPException(
    status_code=409, detail="Incorrect username | password"
)

TokenNotFoundedException = HTTPException(status_code=401, detail="Token is not found")

InvalidTokenException = HTTPException(status_code=401, detail="Invalid JWT token")


UserNotFoundedException = HTTPException(status_code=401, detail="User is not found")

IncorrectPasswordException = HTTPException(status_code=401, detail="Incorrect password")

NoAccessToException = HTTPException(status_code=401, detail="No access to")

UsernameIsTakenException = HTTPException(status_code=401, detail="Username is taken")
