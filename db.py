from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

engine = create_engine('sqlite:///foo.db', echo=True) #


class Base(DeclarativeBase):
    pass


class Posts(Base):
    __tablename__ = 'posts'

    metadata = MetaData()
    id: Mapped[int] = mapped_column(primary_key=True)
    cookie: Mapped[str] = mapped_column()
    post_name: Mapped[str] = mapped_column()


def db_connect():
    engine = create_engine('sqlite:///foo.db', echo=True, pool_pre_ping=True)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    session.commit()
    return session


Posts.metadata.create_all(engine, checkfirst=True)
Session = sessionmaker(bind=engine)
session = Session(bind=engine.connect())
session.commit()

