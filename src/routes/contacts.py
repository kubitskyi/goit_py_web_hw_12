from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from sqlalchemy.orm import Session

from src.database.connect import get_db
from src.database.models import User
from src.services.auth import auth_service
from src.schemas import ContactSchema, ContactBirthday
from src.repository import contacts as repository_contacts

router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.get("/", response_model=List[ContactSchema])
async def read_contacts(limit: int = Query(10, le=1000), offset: int = 0, db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)) -> List[ContactSchema]:
    contacts = await repository_contacts.get_contacts(limit, offset, db, current_user)
    return contacts


@router.get("/search", response_model=List[ContactSchema])
async def search_contacts(query: str = Query(default='', min_length=1), db: Session = Depends(get_db),
                          current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.search_contacts(query, db, current_user)
    return contacts


@router.get("/birthday/", response_model=List[ContactBirthday])
async def get_contacts_birthday(db: Session = Depends(get_db),
                                current_user: User = Depends(auth_service.get_current_user)):
    birthdays = await repository_contacts.get_birthdays_week(db, current_user)
    return birthdays


@router.get("/{contact_id}", response_model=ContactSchema)
async def get_contact(contact_id: int = Path(..., ge=0), db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)) -> ContactSchema:
    contact = await repository_contacts.get_contact(contact_id, db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.post("/", response_model=ContactSchema, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactSchema, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)) -> ContactSchema:
    contact = await repository_contacts.create_contact(body, db, current_user)
    return contact


@router.put("/{contact_id}", response_model=ContactSchema)
async def update_contact(body: ContactSchema, contact_id: int = Path(..., ge=0), db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)) -> ContactSchema:
    contact = await repository_contacts.update_contact(body, contact_id, db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_contact(contact_id: int = Path(..., ge=0), db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.remove_contact(contact_id, db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact