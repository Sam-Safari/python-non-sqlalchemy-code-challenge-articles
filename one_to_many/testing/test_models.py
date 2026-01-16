import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from one_to_many.models import Base, Game, Review


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    sess = Session()
    yield sess
    sess.close()


def test_game_review_relationship(session):
    # create a game
    g = Game(title="Test Game", genre="Action", platform="PC", price=50)
    session.add(g)
    session.commit()

    # add reviews referring to the game
    r1 = Review(score=8, comment="Great", game_id=g.id)
    r2 = Review(score=6, comment="Okay", game_id=g.id)
    session.add_all([r1, r2])
    session.commit()

    # relationship: game -> reviews
    assert len(g.reviews) == 2
    titles = [r.comment for r in g.reviews]
    assert "Great" in titles and "Okay" in titles

    # relationship: review -> game
    assert r1.game.id == g.id


def test_multiple_games_and_reviews(session):
    g1 = Game(title="G1", genre="X", platform="P1", price=10)
    g2 = Game(title="G2", genre="Y", platform="P2", price=20)
    session.add_all([g1, g2])
    session.commit()

    session.add(Review(score=5, comment="c1", game_id=g1.id))
    session.add(Review(score=7, comment="c2", game_id=g1.id))
    session.add(Review(score=9, comment="c3", game_id=g2.id))
    session.commit()

    assert len(session.query(Review).filter_by(game_id=g1.id).all()) == 2
    assert len(g1.reviews) == 2
    assert len(g2.reviews) == 1
