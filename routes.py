from fastapi import APIRouter, Request, Depends, HTTPException, UploadFile,Query, Form
from sqlalchemy.orm import Session
from typing import List,Annotated
import service, models, schemas
from fastapi import Query
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/signup')
async def post_signup(name: Annotated[str, Query(max_length=100)], address: Annotated[str, Query(max_length=100)], mobile: Annotated[str, Query(max_length=100)], password: Annotated[str, Query(max_length=100)], email: Annotated[str, Query(max_length=100, pattern='/^[\\w-\\.]+@([\\w-]+\\.)+[\\w-]{2,4}$/')], db: Session = Depends(get_db)):
    try:
        return await service.post_signup(db, name, address, mobile, password, email)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post('/login')
async def post_login(email: Annotated[str, Query(max_length=100)], password: Annotated[str, Query(max_length=100)], db: Session = Depends(get_db)):
    try:
        return await service.post_login(db, email, password)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

