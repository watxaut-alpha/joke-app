from flask import Flask, request, render_template, make_response
from flask_restful import Resource, Api  # resource is everything that the API can return


app = Flask(__name__)
api = Api(app)


class Main(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html'), 200, headers)


class JokeRating(Resource):

    def get(self, joke_id, id_hash, rating):
        print(joke_id, id_hash, rating)
        return {"rating": rating}, 201


api.add_resource(Main, "/")
api.add_resource(JokeRating, "/rating/<joke_id>/<id_hash>/<rating>")  # the same as @app.route("/student/<string:name>")

app.run(port=5000, debug=True)