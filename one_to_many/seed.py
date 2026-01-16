from models import get_session, Game, Review
from faker import Faker

fake = Faker()

def seed(n_games: int = 3, reviews_per_game: int = 3):
    session = get_session("sqlite:///one_to_many.db")
    for i in range(n_games):
        g = Game(title=fake.sentence(nb_words=3), genre=fake.word(), platform=fake.word(), price=fake.random_int(10, 70))
        session.add(g)
        session.commit()
        for j in range(reviews_per_game):
            r = Review(score=fake.random_int(1, 10), comment=fake.sentence(), game_id=g.id)
            session.add(r)
    session.commit()

if __name__ == '__main__':
    seed()
