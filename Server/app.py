#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
import requests
import json
from flask_cors import CORS, cross_origin
from src.learn import getRandomMovie, getRecomendation,getManyRecomendations

app = Flask(__name__, static_url_path="")
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
movieList = ''
movieListArray = []
movieFeatures = []


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

# Updates the new information aobut the user
@app.route('/add_movie', methods=['POST'])
def add_movie():
    if not request.json or not 'title' in request.json:
        abort(400)

    #movieListArray.append(request.json['title'])
    movieFeatures.append(getRecomendation(request.json['title'])[0])
    movieListArray = getManyRecomendations(movieFeatures)
    response = app.response_class(
        response=json.dumps(movieListArray),
        status=200,
        mimetype='application/json'
    )
    return response
   

# Gets the movies depending on current user
@app.route('/movies')
@cross_origin()
def movies():
    #res = requests.get('https://jsonplaceholder.typicode.com/users')

    newMovie = getRandomMovie()
    return newMovie, 201


if __name__ == '__main__':
    app.run(debug=True)
