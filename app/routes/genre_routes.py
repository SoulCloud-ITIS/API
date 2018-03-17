from app import app, db
from app.models import Genre


@app.route("/genres", methods=['GET'])
def get_all_genres():
    genres = Genre.query.all()
    return Genre.schema.jsonify(genres, True)

