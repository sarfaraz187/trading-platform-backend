import uuid
from fastapi import FastAPI, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from typing import Optional

from config.database import engine, get_db, Base
from model import User
from schema import UserCreate, UserResponse, UserUpdate, KycStatus

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(redirect_slashes=True)

# Get all users.
@app.get("/", response_model=list[UserResponse])
@app.get("", response_model=list[UserResponse])
def get_users(
    skip: int = 0, 
    limit: int = 100,
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
    kyc_status: Optional[str] = None,
    country: Optional[str] = None,
    db: Session = Depends(get_db)
):
    print(f"------ Inside GET Users ------")
    query = db.query(User)
    
    # Apply filters if provided.
    if role:
        query = query.filter(User.role == role)
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    if kyc_status:
        query = query.filter(User.kyc_status == kyc_status)
    if country:
        query = query.filter(User.country == country)
        
    users = query.offset(skip).limit(limit).all()
    return users

# Create a new user.
@app.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    print(f"------ Inside POST Users ------")

    # Check if user already exists by email or firebase_uid
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    if db.query(User).filter(User.firebase_uid == user.firebase_uid).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this Firebase ID already exists"
        )
    
    # Create user object.
    db_user = User(**user.model_dump())
    
    # Save to database
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

# Get user by firebase UID
@app.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: str, db: Session = Depends(get_db)):

    print("------ Inside GET User ------")
    try:
        print(f"Fetching user with ID: {user_id}")
        # uuid_obj = uuid.UUID(user_id)
        # db_user = db.query(User).filter(User.id == uuid_obj).first()
        db_user = db.query(User).filter(User.firebase_uid == user_id).first()

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid firebase ID"
        )
        
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user

# Update user
@app.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: str, user_update: UserUpdate, db: Session = Depends(get_db)):
    try:
        print("User ID : {user_id}")
        db_user = db.query(User).filter(User.firebase_uid == user_id).first()
        print("Found USER: ", db_user)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid UUID format"
        )
        
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update user with non-None values
    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if value is not None:  # Skip None values
            setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

# Delete a user from database
@app.delete("/{user_id}", response_model=UserResponse)
def delete_user(user_id: str, db: Session = Depends(get_db)):
    try:
        db_user = db.query(User).filter(User.firebase_uid == user_id).first()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid UUID format"
        )
        
    db.delete(db_user)
    db.commit()
    return db_user
        
# Update user balance
@app.patch("/{user_id}/balance", response_model=UserResponse)
def update_balance(
    user_id: str, 
    balance_update: float, 
    db: Session = Depends(get_db)
):
    try:
        db_user = db.query(User).filter(User.firebase_uid == user_id).first()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid UUID format"
        )
        
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update balance
    db_user.balance = balance_update
    
    db.commit()
    db.refresh(db_user)
    return db_user

# Update user KYC status
@app.patch("/{user_id}/kyc", response_model=UserResponse)
def update_kyc_status(
    user_id: str, 
    kyc_status: KycStatus, 
    db: Session = Depends(get_db)
):
    try:
        db_user = db.query(User).filter(User.firebase_uid == user_id).first()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid UUID format"
        )
        
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update KYC status
    db_user.kyc_status = kyc_status
    
    db.commit()
    db.refresh(db_user)
    return db_user

# Get user by Firebase UID
# @app.get("/users/firebase/{firebase_uid}", response_model=UserResponse)
# def get_user_by_firebase(firebase_uid: str, db: Session = Depends(get_db)):
#     db_user = db.query(User).filter(User.firebase_uid == firebase_uid).first()
#     if db_user is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="User not found"
#         )
#     return db_user

# Optional: Run the app with uvicorn
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)