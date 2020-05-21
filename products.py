from flask import jsonify, request, json
from flask_restx import Namespace, Resource, abort
from sqlalchemy import desc, text
from datetime import date

from models import db, Product, Model_cat, Brand, Media_storage
from pagination import get_paginated_list


########### API PRODUCTS ###########
api = Namespace("products", description="Operations related to product table")


# GET ALL PRODUCTS
@api.route("")
class AllProducts(Resource):
    @api.doc(responses={404: "Products not found", 200: "Ok"})
    def get(self):
        products = Product.query.all()

        if products:
            products = list(map(lambda x: x.serialize(), products))
            return jsonify(
                get_paginated_list(
                    products,
                    start=request.args.get("start", 1),
                    limit=request.args.get("limit", 25),
                )
            )
        abort(404)


# PRODUCTS SORTED BY LOWEST ASK DATE
@api.route("/lowest-ask-date")
class ProductSortedByLowestAskDate(Resource):
    @api.doc(responses={404: "Can't sort products by lowest ask date", 200: "Ok"})
    def get(self):
        products = Product.query.order_by(desc(Product.lowest_ask_date)).all()
        # products = Product.query.filter(Product.lower_ask_date>=date) -- for queries less then or more then !!!

        if products:
            products = list(map(lambda x: x.serialize(), products))
            return jsonify(
                get_paginated_list(
                    products,
                    start=request.args.get("start", 1),
                    limit=request.args.get("limit", 10),
                )
            )
        abort(404)


# PRODUCTS SORTED BY HIGHEST OFFER DATE
@api.route("/highest-offer-date")
class ProductSortedByHighestOfferDate(Resource):
    @api.doc(responses={404: "Can't sort products by highest offer date", 200: "Ok"})
    def get(self):
        products = Product.query.order_by(desc(Product.highest_offer_date)).all()
        # products = Product.query.filter(Product.highest_offer_date>=date) -- for queries less then or more then !!!

        if products:
            products = list(map(lambda x: x.serialize(), products))
            return jsonify(
                get_paginated_list(
                    products,
                    start=request.args.get("start", 1),
                    limit=request.args.get("limit", 10),
                )
            )
        abort(404)


# PRODUCTS SORTED BY RECENTLY VIEWED
@api.route("/recently-viewed")
class ProductSortedByRecentlyViewed(Resource):
    @api.doc(responses={404: "Can't sort products by recently viewed date", 200: "Ok"})
    def get(self):
        products = Product.query.order_by(desc(Product.recently_viewed)).all()

        if products:
            products = list(map(lambda x: x.serialize(), products))
            return jsonify(
                get_paginated_list(
                    products,
                    start=request.args.get("start", 1),
                    limit=request.args.get("limit", 10),
                )
            )
        abort(404)


# PRODUCTS SORTED BY POPULARITY (# VISITS)
@api.route("/visits")
class ProductSortedByVisits(Resource):
    @api.doc(responses={404: "Can't sort products by visits", 200: "Ok"})
    def get(self):
        products = Product.query.order_by(desc(Product.visit)).all()

        if products:
            products = list(map(lambda x: x.serialize(), products))
            return jsonify(
                get_paginated_list(
                    products,
                    start=request.args.get("start", 1),
                    limit=request.args.get("limit", 10),
                )
            )
        abort(404)


# PRODUCTS SORTED BY RELEASE DATE (ASC ORDER STARTING FROM TODAY)
@api.route("/release-date")
class ProductSortedByReleaseDate(Resource):
    @api.doc(responses={404: "Can't sort products by release date", 200: "Ok"})
    def get(self):
        products = (
            Product.query.filter(Product.release_date > date.today())
            .order_by(Product.release_date)
            .all()
        )

        if products:
            products = list(map(lambda x: x.serialize(), products))
            return jsonify(
                get_paginated_list(
                    products,
                    start=request.args.get("start", 1),
                    limit=request.args.get("limit", 8),
                )
            )
        abort(404)


# PRODUCTS BY BRAND SLUG
@api.route("/<string:brand_slug>")
@api.doc(params={"brand_slug": "string"})
class ProductsByBrandSlug(Resource):
    @api.doc(responses={404: "Slug not found", 200: "Ok"})
    def get(self, brand_slug: str):
        brand = Brand.query.filter_by(slug=brand_slug).first()

        if brand:
            products = Product.query.filter_by(brand_id=brand.id).all()

            if products:
                products = list(map(lambda x: x.serialize(), products))
                return jsonify(
                    get_paginated_list(
                        products,
                        start=request.args.get("start", 1),
                        limit=request.args.get("limit", 40),
                    )
                )
            abort(404)
        else:
            abort(404)


# PRODUCTS BY BRAND SLUG AND MODEL SLUG
@api.route("/<string:brand_slug>/<string:model_slug>")
@api.doc(params={"brand_slug": "string", "model_slug": "string"})
class ProductsByBrandModelSlug(Resource):
    @api.doc(responses={404: "Slug not found", 200: "Ok"})
    def get(self, brand_slug: str, model_slug: str):
        brand = Brand.query.filter_by(slug=brand_slug).first()
        model = Model_cat.query.filter(
            Model_cat.slug_full.ilike(f"%{model_slug}%")
        ).all()

        if brand and model:
            products = []
            for m in model:
                product = Product.query.filter_by(
                    brand_id=brand.id, model_cat_id=m.id
                ).all()
                products += product

            if products:
                products = list(map(lambda x: x.serialize(), products))
                return jsonify(
                    get_paginated_list(
                        products,
                        start=request.args.get("start", 1),
                        limit=request.args.get("limit", 40),
                    )
                )
            abort(404)
        elif not brand or not model:
            abort(404)


# PRODUCTS BY BRAND SLUG AND MODEL SLUG AND SUBMODEL SLUG
@api.route("/<string:brand_slug>/<string:model_slug>/<string:model_slug_1>")
@api.doc(
    params={"brand_slug": "string", "model_slug": "string", "model_slug_1": "string"}
)
class ProductsByBrandModelSubModelSlug(Resource):
    @api.doc(responses={404: "Slug not found", 200: "Ok"})
    def get(self, brand_slug: str, model_slug: str, model_slug_1: str):
        brand = Brand.query.filter_by(slug=brand_slug).first()

        model = Model_cat.query.filter(
            Model_cat.slug_full.ilike(f"%{model_slug}%")
        ).all()
        model_1 = Model_cat.query.filter(
            Model_cat.slug_full.ilike(f"%{model_slug_1}%")
        ).all()
        print(len(model))
        if brand and model_1 and len(model) != 0:
            products = []

            for m in model_1:
                product = Product.query.filter_by(
                    brand_id=brand.id, model_cat_id=m.id
                ).all()
                products += product

            if products:
                products = list(map(lambda x: x.serialize(), products))

                return jsonify(
                    get_paginated_list(
                        products,
                        start=request.args.get("start", 1),
                        limit=request.args.get("limit", 40),
                    )
                )
            abort(404)
        elif not brand or not model_1:
            abort(404)
        abort(404)


# PRODUCTS BY BRAND SLUG AND MODEL SLUG AND 2 SUBMODEL SLUGS
@api.route(
    "/<string:brand_slug>/<string:model_slug>/<string:model_slug_1>/<string:model_slug_2>"
)
@api.doc(
    params={
        "brand_slug": "string",
        "model_slug": "string",
        "model_slug_1": "string",
        "model_slug_2": "string",
    }
)
class ProductsByBrandModel2SubModelSlug(Resource):
    @api.doc(responses={404: "Slug not found", 200: "Ok"})
    def get(
        self, brand_slug: str, model_slug: str, model_slug_1: str, model_slug_2: str
    ):
        brand = Brand.query.filter_by(slug=brand_slug).first()
        model = Model_cat.query.filter(
            Model_cat.slug_full.ilike(f"%{model_slug}%")
        ).all()
        model_1 = Model_cat.query.filter(
            Model_cat.slug_full.ilike(f"%{model_slug_1}%")
        ).all()
        model_2 = Model_cat.query.filter(
            Model_cat.slug_full.ilike(f"%{model_slug_2}%")
        ).all()

        if brand and model_2 and len(model) != 0 and len(model_1) != 0:
            products = []
            for m in model_2:
                product = Product.query.filter_by(
                    brand_id=brand.id, model_cat_id=m.id
                ).all()

            if products:
                print(len(products))
                products = list(map(lambda x: x.serialize(), products))
                return jsonify(
                    get_paginated_list(
                        products,
                        start=request.args.get("start", 1),
                        limit=request.args.get("limit", 40),
                    )
                )
            abort(404)
        elif not brand or not model_2:
            abort(404)
        abort(404)


# PRODUCTS BY MODEL SLUG
@api.route("/model/<string:model_slug>")
@api.doc(params={"model_slug": "string"})
class ProductsByModelSlug(Resource):
    @api.doc(responses={404: "Slug not found", 200: "Ok"})
    def get(self, model_slug: str):

        model = Model_cat.query.filter(
            Model_cat.slug_full.ilike(f"%{model_slug}%")
        ).all()

        products = []

        for m in model:
            product = Product.query.filter_by(model_cat_id=m.id).all()
            products += product

        if products:
            products = list(map(lambda x: x.serialize(), products))

            return jsonify(
                get_paginated_list(
                    products,
                    start=request.args.get("start", 1),
                    limit=request.args.get("limit", 20),
                )
            )
        abort(404)


########################################################
########################################################
########################################################


# TODO SAMPLE OF SQL QUERY USAGE IN FLASK
# # PRODUCTS SORTED BY HIGHEST OFFER DATE
# @api.route("/highest-offer-date")
# class ProductSortedByHighestOfferDate(Resource):
#     @api.doc(responses={404: "Can't sort products by highest offer date", 200: "Ok"})
#     def get(self):

#         sql = text(
#             "Select p.*,m.url,m.alt from product p JOIN media_storage m ON p.id = m.product_id order by p.highest_offer_date desc"
#         )

#         products = db.engine.execute(sql)

#         if products:

#             return jsonify(
#                 get_paginated_list(
#                     [dict(row) for row in products],
#                     "/highest-offer-date",
#                     start=request.args.get("start", 1),
#                     limit=request.args.get("limit", 10),
#                 )
#             )
#         abort(400)
