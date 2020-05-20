import os
from healthcheck import HealthCheck

from flask import Flask, request, jsonify, Blueprint
from flask_migrate import Migrate
from flask_restx import Api
from flask_cors import CORS
from utils import APIException
from models import db


from brands import api as br
from modelcategories import api as mc
from productdetails import api as pd
from sizes import api as sz
from products import api as pr
from media import api as ms
from categories import api as ct

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_CONNECTION_STRING")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

blueprint = Blueprint("api", __name__)
api = Api(
    blueprint,
    title="SnkrsDen API👟",
    version="v1.0",
    contact="SnkrsDen",
    contact_url="https://snkrsden.com",
    contact_email="info@snkrsden.com",
    description="""RESTFUL API
          
            📎 Comments and tips:
          
            ✓ For queries by multiple arguments you should pass them separated with + sign""",
    default="uncategorized",
    ordered=True,
)

api.add_namespace(br)
api.add_namespace(ct)
api.add_namespace(ms)
api.add_namespace(mc)
api.add_namespace(pr)
api.add_namespace(pd)
api.add_namespace(sz)


app.register_blueprint(blueprint)

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)


# wrap the flask app and give a heathcheck url
health = HealthCheck(app, "/healthcheck")


def health_database_status():
    is_database_working = True
    output = "database is ok"

    try:
        # to check database we will execute raw query
        session = db.session()
        session.execute("SELECT 1")
    except Exception as e:
        output = str(e)
        is_database_working = False

    return is_database_working, output


health.add_check(health_database_status)


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# this only runs if `$ python src/main.py` is executed
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=PORT, debug=False)
