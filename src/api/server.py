from flask import Flask, request, render_template, make_response  # , jsonify   # no need to jsonify, because Flask RESTful does it for us
from flask_restful import Resource, Api  # resource is everything that the API can return


def init_flask():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(Main, "/")

    api.add_resource(JokeRating, "/rating/<user_id>")  # the same as @app.route("/student/<string:name>")

    app.run(port=5000, debug=True)


class Main(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html'), 200, headers)


class JokeRating(Resource):

    def post(self, user_id):
        print(user_id)
        num = request.form.get('rating', "NaN")
        return {"rating": num}, 201


init_flask()
