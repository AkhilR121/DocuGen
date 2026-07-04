from typing import List, Optional
from sqlalchemy.orm import Session


class ExampleService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> List:
        """Get all examples with pagination"""
        return []

    def get_by_id(self, id: int) -> Optional[dict]:
        """Get example by ID"""
        return None

    def create(self, data: dict) -> dict:
        """Create new example"""
        return data

    def update(self, id: int, data: dict) -> Optional[dict]:
        """Update existing example"""
        return None

    def delete(self, id: int) -> bool:
        """Delete example"""
        return False
