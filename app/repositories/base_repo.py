from typing import TypeVar, Generic, Type

from sqlalchemy.orm import Session

from app.core.database import Base

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], db: Session):
        self.model = model
        self.db = db

    def get(self, id: int) -> T | None:
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(self) -> list[T]:
        return self.db.query(self.model).all()

    def create(self, obj_in: dict) -> T:
        obj = self.model(**obj_in)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, id: int, obj_in: dict) -> T | None:
        obj = self.get(id)
        if not obj:
            return None
        for key, value in obj_in.items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, id: int) -> bool:
        obj = self.get(id)
        if not obj:
            return False
        self.db.delete(obj)
        self.db.commit()
        return True
