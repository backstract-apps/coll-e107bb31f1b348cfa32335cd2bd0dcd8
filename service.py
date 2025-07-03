from sqlalchemy.orm import Session, aliased
from sqlalchemy import and_, or_
from typing import *
from fastapi import Request, UploadFile, HTTPException
import models, schemas
import boto3
import jwt
import datetime
import requests
from pathlib import Path


async def post_signup(
    db: Session, name: str, address: str, mobile: str, password: str, email: str
):

    import uuid

    try:
        id: str = str(uuid.uuid4())
        print(f"id: {id}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

    record_to_be_added = {
        "name": name,
        "email": email,
        "mobile": address,
        "address": address,
        "password": password,
    }
    new_profile = models.Profile(**record_to_be_added)
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    test = new_profile.to_dict()

    res = {
        "test": test,
    }
    return res


async def post_login(db: Session, email: str, password: str):

    query = db.query(models.Profile)
    query = query.filter(
        and_(
            models.Profile.email == header_email,
            models.Profile.password == header_password,
        )
    )

    test = query.first()

    test = (
        (test.to_dict() if hasattr(test, "to_dict") else vars(test)) if test else test
    )

    bs_jwt_payload = {
        "exp": int(
            (datetime.datetime.utcnow() + datetime.timedelta(seconds=10000)).timestamp()
        ),
        "data": test,
    }

    test1 = jwt.encode(
        bs_jwt_payload,
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0.KMUFsIDTnFmyG3nMiGM6H9FNFUROf3wh7SmqJp-QV30",
        algorithm="HS256",
    )

    res = {
        "test": test,
        "test1": test1,
    }
    return res
