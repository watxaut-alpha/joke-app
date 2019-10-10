import requests
from flask import Flask, render_template, make_response
from flask_restful import Resource, Api  # resource is everything that the API can return

try:
    from src.api.secret import FLASK_PORT
except ModuleNotFoundError:
    from secret import FLASK_PORT


app = Flask(__name__)
api = Api(app)


class Main(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        r_cat = requests.get("https://api.thecatapi.com/v1/images/search")
        if r_cat:  # status 200
            url = r_cat.json()[0]["url"]
        else:
            url = "Cat not found"

        return make_response(render_template('index.html', url=url), 200, headers)


class JokeRating(Resource):

    def get(self, joke_id, id_hash, rating):
        print(joke_id, id_hash, rating)

        return make_response(render_template('thanks_rating.html', rating=rating), 200, {'Content-Type': 'text/html'})

    # def post(self, joke_id, id_hash):
    #     rating = request.form.get("rating", "NaN")
    #     print(joke_id, id_hash, rating)
    #     return {"rating": rating}, 201


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


api.add_resource(Main, "/")
api.add_resource(JokeRating, "/rating/<joke_id>/<id_hash>/<rating>")

app.run(port=FLASK_PORT, host="0.0.0.0")
