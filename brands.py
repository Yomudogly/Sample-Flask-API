from flask import request, jsonify
from main import api, get_paginated_list
from models import Brand


br = api.namespace('brands', description='Operations related to brand table')


# GET ALL BRANDS
@br.route('')
class AllBrands(Resource):

    @api.doc(responses={404: 'Brands not found', 200: 'Ok'})
    def get(self):
        brands = Brand.query.all()
        brands = list(map(lambda x: x.serialize(), brands))

        return jsonify(get_paginated_list(brands, '/brands',
                                          start=request.args.get('start', 1),
                                          limit=request.args.get('limit', 20)
                                          ))