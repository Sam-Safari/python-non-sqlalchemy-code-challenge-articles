from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Engine is defined here for convenience; tests use their own engines where appropriate.
engine = create_engine("sqlite:///one_to_many.db")
Base = declarative_base()


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    genre = Column(String)
    platform = Column(String)
    price = Column(Integer)

    # One-to-many relationship: a game has many reviews
    reviews = relationship("Review", backref=backref("game"))

    def __repr__(self):
        return f"Game(id={self.id}, title={self.title}, platform={self.platform})"


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    score = Column(Integer)
    comment = Column(String)

    game_id = Column(Integer, ForeignKey("games.id"))

    def __repr__(self):
        return f"Review(id={self.id}, score={self.score}, game_id={self.game_id})"


# helper to get a session (tests may use their own engine/session)
def get_session(db_url: str = "sqlite:///one_to_many.db"):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()
