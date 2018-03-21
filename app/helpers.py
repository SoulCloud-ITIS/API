from app import ma


class BookWithMarksSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'author', 'description', 'url', 'mark')


class BookWithMarks:
    schema = BookWithMarksSchema()

    def __init__(self, book, mark):
        self.id = book.id
        self.name = book.name
        self.author = book.author
        self.description = book.description
        self.url = book.url
        self.mark = mark
