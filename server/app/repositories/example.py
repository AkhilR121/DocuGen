from typing import List, Optional
from sqlalchemy.orm import Session


class ExampleRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_all(self, skip: int = 0, limit: int = 100) -> List:
        """Find all examples"""
        return []

    def find_by_id(self, id: int) -> Optional[dict]:
        """Find example by ID"""
        return None

    def create(self, data: dict) -> dict:
        """Create new example"""
        return data

    def update(self, id: int, data: dict) -> Optional[dict]:
        """Update example"""
        return None

    def delete(self, id: int) -> bool:
        """Delete example"""
        return False
