import os
from flask import Flask, request, jsonify, json,Response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

project_dir = os.path.dirname(os.path.abspath(__file__))
database_url = "sqlite:///{}".format(os.path.join(project_dir, "movie.db"))
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
db =SQLAlchemy(app)
ma = Marshmallow(app)

db = SQLAlchemy(app)
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    
    def __init__(self,id, title):
        self.id = id
        self.title = title
    

class MovieSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title')

movie_schema = MovieSchema()
movie_schema = MovieSchema(many=True)


# endpoint to create new Movie
@app.route("/add", methods =["POST"])
def add_movie():
    movie_id = request.json['id'];
    movie_name = request.json['title']
    new_movie = Movie(movie_id, movie_name)
    db.session.add(new_movie)
    db.session.commit()
    return jsonify({'msg':"movie added successfully"})

# endpoint to create get all movies
@app.route("/view-all", methods =["GET"])
def get_all_movies():
    all_movies = Movie.query.all()
    output = movie_schema.dump(all_movies)
    return jsonify(output)


# endpoint to delete movie using by movie id
@app.route("/delete/<id>", methods=["DELETE"])
def user_delete(id):
    movie = Movie.query.get(id)
    print("movie " , movie)
    db.session.delete(movie)
    db.session.commit()
    return {'msg':'movie deleted successfully'}                     


# endpoint to update movie
@app.route('/update/<id>' , methods = ["PUT"])
def update_movie_name(id):
    movie = Movie.query.get(id)
    movie_name = request.json['title']   
    movie.title = movie_name
    db.session.commit()
    return ({'msg':'movie data updated successfully'})





if __name__ == '__main__':
    app.run(debug=True)    