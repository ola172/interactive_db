from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from app.config import settings

DATABASE_URL = settings.DATABASE_URL

Base = declarative_base()

class Database:
    def __init__(self, url: str = None):
        # use the Pydantic URL, but cast to str
        self.engine = create_engine(str(url or settings.DATABASE_URL), echo=True, future=True)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def create_tables(self):
        """Create all tables"""
        Base.metadata.create_all(bind=self.engine)

    def get_session(self) -> Session:
        """Dependency for FastAPI or manual use"""
        return self.SessionLocal()
