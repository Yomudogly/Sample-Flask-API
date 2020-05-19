
from flask import jsonify, request
from flask_restx import Namespace, Resource, abort

from models import Model_cat
from pagination import get_paginated_list


########### API MODEL CATEGORY ###########

api = Namespace(
    'model-category', description='Operations related to model category table')


# GET ALL MODELS
@api.route('')
class AllModels(Resource):

    @api.doc(responses={404: 'Models not found', 200: 'Ok'})
    def get(self):
        models = Model_cat.query.all()
        models = list(map(lambda x: x.serialize(), models))

        return jsonify(get_paginated_list(models, '/model-category',
                                          start=request.args.get('start', 1),
                                          limit=request.args.get('limit', 20)
                                          ))

########################################################
########################################################
########################################################
