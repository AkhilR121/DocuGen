from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_db
from app.schemas.example import Example, ExampleCreate, ExampleUpdate

router = APIRouter()


@router.get("/", response_model=List[Example])
def get_examples(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_current_db)
):
    """
    Retrieve examples.
    """
    return []


@router.get("/{id}", response_model=Example)
def get_example(
    id: int,
    db: Session = Depends(get_current_db)
):
    """
    Get example by ID.
    """
    raise HTTPException(status_code=404, detail="Example not found")


@router.post("/", response_model=Example)
def create_example(
    example_in: ExampleCreate,
    db: Session = Depends(get_current_db)
):
    """
    Create new example.
    """
    return example_in


@router.put("/{id}", response_model=Example)
def update_example(
    id: int,
    example_in: ExampleUpdate,
    db: Session = Depends(get_current_db)
):
    """
    Update an example.
    """
    raise HTTPException(status_code=404, detail="Example not found")


@router.delete("/{id}")
def delete_example(
    id: int,
    db: Session = Depends(get_current_db)
):
    """
    Delete an example.
    """
    raise HTTPException(status_code=404, detail="Example not found")
