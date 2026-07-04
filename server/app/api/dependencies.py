from typing import Generator
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db


def get_current_db(db: Session = Depends(get_db)) -> Generator:
    try:
        yield db
    finally:
        pass
