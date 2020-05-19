from flask import jsonify, request
from flask_restx import Namespace, Resource, abort
from sqlalchemy import desc

from models import Product
from pagination import get_paginated_list


########### API PRODUCTS ###########
api = Namespace(
    'products', description='Operations related to product table')


# GET ALL PRODUCTS
@api.route('')
class AllProducts(Resource):

    @api.doc(responses={404: 'Products not found', 200: 'Ok'})
    def get(self):
        products = Product.query.all()
        products = list(map(lambda x: x.serialize(), products))

        return jsonify(get_paginated_list(products, '/products',
                                          start=request.args.get('start', 1),
                                          limit=request.args.get('limit', 20)
                                          ))


# PRODUCTS SORTED BY LOWEST ASK DATE
@api.route('/lowest-ask-date')
class ProductSortedByLowestAskDate(Resource):

    @api.doc(responses={404: 'Can\'t sort products by lowest ask date', 200: 'Ok'})
    def get(self):
        products = Product.query.order_by(
            desc(Product.lowest_ask_date)).all()
        # products = Product.query.filter(Product.lowest_ask_date<=date) -- for queries less then or more then !!!
        if products:
            products = list(map(lambda x: x.serialize(), products))

            return jsonify(get_paginated_list(products,
                                              f'/sort/lowest-ask-date',
                                              start=request.args.get(
                                                  'start', 1),
                                              limit=request.args.get(
                                                  'limit', 10)
                                              ))
        abort(400)


# PRODUCTS SORTED BY HIGHEST OFFER DATE
@api.route('/highest-offer-date')
class ProductSortedByHighestOfferDate(Resource):

    @api.doc(responses={404: 'Can\'t sort products by highest offer date', 200: 'Ok'})
    def get(self):
        products = Product.query.order_by(
            desc(Product.highest_offer_date)).all()
        # products = Product.query.filter(Product.highest_offer_date>=date) -- for queries less then or more then !!!
        if products:
            products = list(map(lambda x: x.serialize(), products))

            return jsonify(get_paginated_list(products,
                                              f'/sort/highest-offer-date',
                                              start=request.args.get(
                                                  'start', 1),
                                              limit=request.args.get(
                                                  'limit', 10)
                                              ))
        abort(400)


# PRODUCTS SORTED BY RECENTLY VIEWED
@api.route('/recently-viewed')
class ProductSortedByRecentlyViewed(Resource):

    @api.doc(responses={404: 'Can\'t sort products by recently viewed date', 200: 'Ok'})
    def get(self):
        products = Product.query.order_by(
            desc(Product.recently_viewed)).all()
        # products = Product.query.filter(Product.recently_viewed>=date) -- for queries less then or more then !!!
        if products:
            products = list(map(lambda x: x.serialize(), products))

            return jsonify(get_paginated_list(products,
                                              f'/sort/recently-viewed',
                                              start=request.args.get(
                                                  'start', 1),
                                              limit=request.args.get(
                                                  'limit', 10)
                                              ))
        abort(400)
        
        

# PRODUCTS SORTED BY POPULARITY (# VISITS)
@api.route('/visits')
class ProductSortedByVisits(Resource):

    @api.doc(responses={404: 'Can\'t sort products by visits', 200: 'Ok'})
    def get(self):
        products = Product.query.order_by(
            desc(Product.visit)).all()
        # products = Product.query.filter(Product.recently_viewed>=date) -- for queries less then or more then !!!
        if products:
            products = list(map(lambda x: x.serialize(), products))

            return jsonify(get_paginated_list(products,
                                              f'/sort/recently-viewed',
                                              start=request.args.get(
                                                  'start', 1),
                                              limit=request.args.get(
                                                  'limit', 10)
                                              ))
        abort(400)


# PRODUCTS BY BRAND SLUG AND MODEL SLUG
@api.route('/<string:brand_slug>/<string:model_slug>', '/<string:brand_slug>')
@api.doc(params={'brand_slug': 'string'})
class ProductsByBrandAndModelSlug(Resource):

    @api.doc(responses={404: 'Slug not found', 200: 'Ok'})
    def get(self, brand_slug: str, model_slug=None):

        brand = Brand.query.filter_by(slug=brand_slug).first()
        model = Model_cat.query.filter_by(slug=model_slug).first()
        if brand and not model:
            products = Product.query.filter_by(brand_id=brand.id).all()
            if products:
                products = list(map(lambda x: x.serialize(), products))

                return jsonify(get_paginated_list(products,
                                                  f'/{brand_slug}',
                                                  start=request.args.get(
                                                      'start', 1),
                                                  limit=request.args.get(
                                                      'limit', 20)
                                                  ))
            abort(404)
        elif brand and model:
            products = Product.query.filter_by(
                brand_id=brand.id, model_cat_id=model.id).all()
            if products:
                products = list(map(lambda x: x.serialize(), products))

                return jsonify(get_paginated_list(products,
                                                  f'/{brand_slug}/{model_slug}',
                                                  start=request.args.get(
                                                      'start', 1),
                                                  limit=request.args.get(
                                                      'limit', 20)
                                                  ))
            abort(404)
        else:
            abort(404)


# PRODUCTS BY MODEL SLUG
@api.route('/model/<string:model_slug>')
@api.doc(params={'model_slug': 'string'})
class ProductsByModelSlug(Resource):

    @api.doc(responses={404: 'Slug not found', 200: 'Ok'})
    def get(self, model_slug: str):

        model = Model_cat.query.filter_by(slug=model_slug).first()
        products = Product.query.filter_by(model_cat_id=model.id).all()
        if products:
            products = list(map(lambda x: x.serialize(), products))

            return jsonify(get_paginated_list(products,
                                              f'/model/{model_slug}',
                                              start=request.args.get(
                                                  'start', 1),
                                              limit=request.args.get(
                                                  'limit', 20)
                                              ))
        abort(404)


########################################################
########################################################
########################################################
