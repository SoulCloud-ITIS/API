from app import ma


class BookWithMarksSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'author', 'description', 'text_url', 'coef_love', 'coef_fantastic', 'coef_fantasy',
                  'coef_detective', 'coef_adventure', 'coef_art', 'mark')


class BookWithMarks:
    schema = BookWithMarksSchema()

    def __init__(self, book, mark):
        self.id = book.id
        self.name = book.name
        self.author = book.author
        self.description = book.description
        self.text_url = book.text_url
        self.coef_love = book.coef_love
        self.coef_fantasy = book.coef_fantasy
        self.coef_fantastic = book.coef_fantastic
        self.coef_detective = book.coef_detective
        self.coef_adventure = book.coef_adventure
        self.coef_art = book.coef_art
        self.mark = mark
