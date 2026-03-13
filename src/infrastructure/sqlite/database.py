from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, inspect, text
from pathlib import Path

from .models.userModel import User
from .models.baseModel import Base


db_path = Path(__file__).parent.parent / "sqlite" / "sqlite.db"


class Database:
    def __init__(self):
        self._db_url = f"sqlite:///{db_path}"
        self._engine = create_engine(
            self._db_url, connect_args={
                "check_same_thread": False})

    def init_db(self):
        Base.metadata.create_all(bind=self._engine)

    @property
    def engine(self):
        return self._engine

    @contextmanager
    def session(self):
        connection = self._engine.connect()
        Session = sessionmaker(bind=self._engine)
        session = Session()

        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
            connection.close()


database = Database()


def get_db():
    with database.session() as session:
        yield session
