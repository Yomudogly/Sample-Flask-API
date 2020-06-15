from flask import jsonify, request
from flask_restx import Namespace, Resource, abort

from models import Category
from pagination import get_paginated_list


########### API CATEGORY ###########

api = Namespace("category", description="Operations related to category table")


# GET ALL MODELS
@api.route("")
class AllCategories(Resource):
    @api.doc(responses={404: "Categories not found", 200: "Ok"})
    def get(self):
        categories = Category.query.all()
        categories = list(map(lambda x: x.serialize(), categories))

        return jsonify(
            get_paginated_list(
                categories,
                start=request.args.get("start", 1),
                limit=request.args.get("limit", 20),
            )
        )
