from models import get_session, Game, Review

if __name__ == "__main__":
    session = get_session("sqlite:///one_to_many.db")

    # create sample data if none exists
    if session.query(Game).count() == 0:
        g = Game(title="Breath of the Wild", genre="Action-adventure", platform="Switch", price=60)
        session.add(g)
        session.commit()
        r1 = Review(score=10, comment="A classic!", game_id=g.id)
        r2 = Review(score=9, comment="Loved it", game_id=g.id)
        session.add_all([r1, r2])
        session.commit()

    game = session.query(Game).first()
    print(game)
    print("reviews:", game.reviews)
