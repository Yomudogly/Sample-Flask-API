from flask import jsonify, request
from flask_restx import Namespace, Resource, abort

from models import Sizes_shoes
from pagination import get_paginated_list


########### API SIZES ###########
api = Namespace('sizes', description='Operations related to sizes table')


# GET ALL SIZES
@api.route('')
class AllSizes(Resource):

    @api.doc(responses={404: 'Sizes not found', 200: 'Ok'})
    def get(self):
        sizes = Sizes_shoes.query.all()
        sizes = list(map(lambda x: x.serialize(), sizes))

        return jsonify(get_paginated_list(sizes, '/sizes',
                                          start=request.args.get('start', 1),
                                          limit=request.args.get('limit', 20)
                                          ))


# SIZES BY ID
@api.route('/<int:id>')
@api.doc(params={'id': 'integer'})
class SizesById(Resource):

    @api.doc(responses={404: 'Size not found', 200: 'Ok'})
    def get(self, id: int):
        size = Sizes_shoes.query.get(id)
        if size:
            return jsonify(size.serialize())
        abort(404, f'Size with id {id} does not exist')


# SIZES BY BRAND ID
@api.route('/brand-id/<int:brand_id>')
@api.doc(params={'brand_id': 'integer'})
class SizesByBrandId(Resource):

    @api.doc(responses={404: 'Sizes not found', 200: 'Ok'})
    def get(self, brand_id: int):
        sizes = Sizes_shoes.query.filter_by(brand_id=brand_id).all()
        if sizes:
            sizes = list(map(lambda x: x.serialize(), sizes))
            return jsonify(get_paginated_list(sizes,
                                              f'/brand-id/{brand_id}',
                                              start=request.args.get(
                                                  'start', 1),
                                              limit=request.args.get(
                                                  'limit', 20)
                                              ))
        abort(404, f'Sizes with brand id {brand_id} do not exist')


# SIZES BY TYPE ID
@api.route('/type-id/<string:sizes_types_id>')
@api.doc(params={'sizes_types_id': 'string - m, w, td, gs, y or kids'})
class SizesByTypeId(Resource):

    @api.doc(responses={404: 'Sizes not found', 200: 'Ok'})
    def get(self, sizes_types_id: str):
        sizes = Sizes_shoes.query.filter_by(
            sizes_types_id=sizes_types_id).all()
        if sizes:
            sizes = list(map(lambda x: x.serialize(), sizes))
            return jsonify(get_paginated_list(sizes,
                                              f'/type-id/{sizes_types_id}',
                                              start=request.args.get(
                                                  'start', 1),
                                              limit=request.args.get(
                                                  'limit', 20)
                                              ))
        abort(404, f'Sizes with type id {sizes_types_id} do not exist')


# SIZES BY US
@api.route('/us/<string:us>')
@api.doc(params={'us': 'string in format number+letter or number+dot+number'})
class SizesByUS(Resource):

    @api.doc(responses={404: 'Sizes not found', 200: 'Ok'})
    def get(self, us: str):
        sizes = Sizes_shoes.query.filter_by(us=us).all()
        if sizes:
            sizes = list(map(lambda x: x.serialize(), sizes))
            return jsonify(get_paginated_list(sizes,
                                              f'/us/{us}',
                                              start=request.args.get(
                                                  'start', 1),
                                              limit=request.args.get(
                                                  'limit', 20)
                                              ))
        abort(404, f'Sizes with us {us} do not exist')


# SIZES BY UK
@api.route('/uk/<string:uk>')
@api.doc(params={'uk': 'string in format number+dot+number'})
class SizesByUK(Resource):

    @api.doc(responses={404: 'Sizes not found', 200: 'Ok'})
    def get(self, uk: str):
        sizes = Sizes_shoes.query.filter_by(uk=uk).all()
        if sizes:
            sizes = list(map(lambda x: x.serialize(), sizes))
            return jsonify(get_paginated_list(sizes,
                                              f'/uk/{uk}',
                                              start=request.args.get(
                                                  'start', 1),
                                              limit=request.args.get(
                                                  'limit', 20)
                                              ))
        abort(404, f'Sizes with uk {uk} do not exist')


# SIZES BY CM
@api.route('/cm/<float:cm>')
@api.doc(params={'cm': 'float'})
class SizesByCM(Resource):

    @api.doc(responses={404: 'Sizes not found', 200: 'Ok'})
    def get(self, cm: float):
        sizes = Sizes_shoes.query.filter_by(cm=cm).all()
        if sizes:
            sizes = list(map(lambda x: x.serialize(), sizes))
            return jsonify(get_paginated_list(sizes,
                                              f'/cm/{cm}',
                                              start=request.args.get(
                                                  'start', 1),
                                              limit=request.args.get(
                                                  'limit', 20)
                                              ))
        abort(404, f'Sizes with cm {cm} do not exist')

 # SIZES BY EUROPE


@api.route('/europe/<float:europe>')
@api.doc(params={'europe': 'float'})
class SizesByEurope(Resource):

    @api.doc(responses={404: 'Sizes not found', 200: 'Ok'})
    def get(self, europe: float):
        sizes = Sizes_shoes.query.filter_by(europe=europe).all()
        if sizes:
            sizes = list(map(lambda x: x.serialize(), sizes))
            return jsonify(get_paginated_list(sizes,
                                              f'/europe/{europe}',
                                              start=request.args.get(
                                                  'start', 1),
                                              limit=request.args.get(
                                                  'limit', 20)
                                              ))
        abort(404, f'Sizes with europe size {europe} do not exist')


# SIZES BY INCH
@api.route('/inch/<float:inch>')
@api.doc(params={'inch': 'float'})
class SizesByInch(Resource):

    @api.doc(responses={404: 'Sizes not found', 200: 'Ok'})
    def get(self, inch: float):
        sizes = Sizes_shoes.query.filter_by(inch=inch).all()
        if sizes:
            sizes = list(map(lambda x: x.serialize(), sizes))
            return jsonify(get_paginated_list(sizes,
                                              f'/inch/{inch}',
                                              start=request.args.get(
                                                  'start', 1),
                                              limit=request.args.get(
                                                  'limit', 20)
                                              ))
        abort(404, f'Sizes with inch {inch} do not exist')


# SIZES BY WOMAN
@api.route('/woman/<float:woman>')
@api.doc(params={'woman': 'float'})
class SizesByWoman(Resource):

    @api.doc(responses={404: 'Sizes not found', 200: 'Ok'})
    def get(self, woman: float):
        sizes = Sizes_shoes.query.filter_by(woman=woman).all()
        if sizes:
            sizes = list(map(lambda x: x.serialize(), sizes))
            return jsonify(get_paginated_list(sizes,
                                              f'/woman/{woman}',
                                              start=request.args.get(
                                                  'start', 1),
                                              limit=request.args.get(
                                                  'limit', 20)
                                              ))
        abort(404, f'Sizes with woman size {woman} do not exist')


########################################################
########################################################
########################################################
