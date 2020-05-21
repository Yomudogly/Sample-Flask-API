
from flask import jsonify, request
from flask_restx import Namespace, Resource, abort

from models import Brand
from pagination import get_paginated_list

########### API BRAND ###########

api = Namespace('brands', description='Operations related to brand table')


# GET ALL BRANDS
@api.route('')
class AllBrands(Resource):

    @api.doc(responses={404: 'Brands not found', 200: 'Ok'})
    def get(self):
        brands = Brand.query.all()
        brands = list(map(lambda x: x.serialize(), brands))

        return jsonify(get_paginated_list(brands,
                                          start=request.args.get('start', 1),
                                          limit=request.args.get('limit', 20)
                                          ))

########################################################
########################################################
########################################################
