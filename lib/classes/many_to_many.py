class Article:
    all = []

    def __init__(self, author, magazine, title):
        # validate types
        from classes.many_to_many import Author, Magazine

        if not isinstance(author, Author):
            raise Exception("author must be an Author instance")
        if not isinstance(magazine, Magazine):
            raise Exception("magazine must be a Magazine instance")
        if not isinstance(title, str) or not (5 <= len(title) <= 50):
            raise Exception("title must be a string length 5-50")

        object.__setattr__(self, "author", author)
        object.__setattr__(self, "magazine", magazine)
        object.__setattr__(self, "title", title)
        Article.all.append(self)

    def __setattr__(self, name, value):
        from classes.many_to_many import Author, Magazine

        if name == "title":
            # cannot change title once set
            if hasattr(self, "title"):
                raise Exception("title is immutable")
            if not isinstance(value, str) or not (5 <= len(value) <= 50):
                raise Exception("title must be a string length 5-50")
            object.__setattr__(self, name, value)
        elif name == "author":
            if not isinstance(value, Author):
                raise Exception("author must be an Author instance")
            object.__setattr__(self, name, value)
        elif name == "magazine":
            if not isinstance(value, Magazine):
                raise Exception("magazine must be a Magazine instance")
            object.__setattr__(self, name, value)
        else:
            object.__setattr__(self, name, value)


class Author:
    def __init__(self, name):
        # initialize name only if valid string and length > 0
        if not isinstance(name, str):
            raise Exception("name must be a string")
        if len(name) == 0:
            raise Exception("name must be longer than 0 characters")
        object.__setattr__(self, "name", name)

    def __setattr__(self, name, value):
        if name == "name":
            # name is immutable once set and must be non-empty string
            if not hasattr(self, "name"):
                if not isinstance(value, str) or len(value) == 0:
                    raise Exception("name must be a non-empty string")
                object.__setattr__(self, name, value)
            else:
                # cannot change name once set
                raise Exception("name is immutable")
        else:
            object.__setattr__(self, name, value)

    def articles(self):
        # return list of Article instances authored by this author
        return [a for a in Article.all if a.author is self]

    def magazines(self):
        # unique list of Magazine instances for which the author has written
        mags = [a.magazine for a in self.articles()]
        # preserve order and unique
        seen = []
        for m in mags:
            if m not in seen:
                seen.append(m)
        return seen

    def add_article(self, magazine, title):
        # create and return new Article associated with this author
        new_article = Article(self, magazine, title)
        return new_article

    def topic_areas(self):
        # returns unique list of categories (strings) of magazines the author has contributed to
        mags = self.magazines()
        if not mags:
            return None
        cats = [m.category for m in mags]
        # unique while preserving order
        seen = []
        for c in cats:
            if c not in seen:
                seen.append(c)
        return seen


class Magazine:
    all = []

    def __init__(self, name, category):
        # set validated name and category
        if not isinstance(name, str):
            raise Exception("name must be a string")
        if not (2 <= len(name) <= 16):
            raise Exception("name must be between 2 and 16 characters")
        object.__setattr__(self, "name", name)

        if not isinstance(category, str):
            raise Exception("category must be a string")
        if len(category) == 0:
            raise Exception("category must be longer than 0 characters")
        object.__setattr__(self, "category", category)

        Magazine.all.append(self)

    def __setattr__(self, name, value):
        if name == "name":
            # mutable but must be str length 2-16
            if not isinstance(value, str):
                raise Exception("name must be a string")
            if not (2 <= len(value) <= 16):
                raise Exception("name must be between 2 and 16 characters")
            object.__setattr__(self, name, value)
        elif name == "category":
            if not isinstance(value, str):
                raise Exception("category must be a string")
            if len(value) == 0:
                raise Exception("category must be longer than 0 characters")
            object.__setattr__(self, name, value)
        else:
            object.__setattr__(self, name, value)

    def articles(self):
        return [a for a in Article.all if a.magazine is self]

    def contributors(self):
        authors = [a.author for a in self.articles()]
        seen = []
        for au in authors:
            if au not in seen:
                seen.append(au)
        return seen

    def article_titles(self):
        arts = self.articles()
        if not arts:
            return None
        return [a.title for a in arts]

    def contributing_authors(self):
        arts = self.articles()
        if not arts:
            return None
        counts = {}
        for a in arts:
            counts[a.author] = counts.get(a.author, 0) + 1
        res = [author for author, cnt in counts.items() if cnt > 2]
        return res if res else None

    @classmethod
    def top_publisher(cls):
        # Return the Magazine instance with the most articles
        # If no articles exist, return None
        # We'll rely on Article.all for global article list
        try:
            from classes.many_to_many import Article
        except Exception:
            return None

        if not hasattr(Article, "all") or not Article.all:
            return None

        # count articles per magazine
        counts = {}
        for a in Article.all:
            counts[a.magazine] = counts.get(a.magazine, 0) + 1

        # find magazine with max count
        top = max(counts.items(), key=lambda kv: kv[1])[0]
        return top