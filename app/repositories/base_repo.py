from typing import TypeVar, Generic, Type, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import cast
from app.core.database import Base

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], db: AsyncSession):
        self.model = model
        self.db = db

    async def get(self, id: int) -> Optional[T]:
        result = await self.db.execute(select(self.model).filter(self.model.id == id))
        return result.scalars().first()

    async def get_all(self) -> list[T]:
        result = await self.db.execute(select(self.model))
        return cast(list[T], result.scalars().all())

    async def create(self, obj_in: dict) -> T:
        obj = self.model(**obj_in)
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def update(self, id: int, obj_in: dict) -> Optional[T]:
        obj = await self.get(id)
        if not obj:
            return None
        for key, value in obj_in.items():
            setattr(obj, key, value)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def delete(self, id: int) -> bool:
        obj = await self.get(id)
        if not obj:
            return False
        await self.db.delete(obj)   # ✅ with AsyncSession
        await self.db.commit()
        return True
