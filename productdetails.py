from flask import jsonify, request
from flask_restx import Namespace, Resource, abort

from models import Product_detail
from pagination import get_paginated_list


########### API PRODUCT DETAILS ###########
api = Namespace('product-details',
                description='Operations related to product details table')


# GET ALL PRODUCT DETAILS
@api.route('')
class AllProductDetails(Resource):

    @api.doc(responses={404: 'Product details not found', 200: 'Ok'})
    def get(self):
        products = Product_detail.query.all()
        products = list(map(lambda x: x.serialize(), products))

        return jsonify(get_paginated_list(products,
                                          '',
                                          start=request.args.get('start', 1),
                                          limit=request.args.get('limit', 20)
                                          ))


# PRODUCT DETAILS BY ID
@api.route('/<int:id>')
@api.doc(params={'id': 'id'})
class ProductDetailsById(Resource):

    @api.doc(responses={404: 'Id not found', 200: 'Ok'})
    def get(self, id: int):

        products = Product_detail.query.get(id)
        if products:
            return jsonify(products.serialize())
        abort(404, f'Product detail with id {id} does not exist')


# PRODUCT DETAILS BY PRODUCT ID
@api.route('/product-id/<int:id>')
@api.doc(params={'id': 'integer'})
class ProductDetailsByProductId(Resource):

    @api.doc(responses={404: 'Product id not found', 200: 'Ok'})
    def get(self, id: int):
        products = Product_detail.query.filter_by(product_id=id).all()

        if products:
            products = list(map(lambda x: x.serialize(), products))

            return jsonify(get_paginated_list(products,
                                              f'/product-id/{id}',
                                              start=request.args.get(
                                                  'start', 1),
                                              limit=request.args.get(
                                                  'limit', 20)
                                              ))
        abort(400)


# PRODUCT DETAILS BY SIZES_SHOES ID
@api.route('/sizes-id/<int:id>')
@api.doc(params={'id': 'integer'})
class ProductDetailsBySizesShoes(Resource):

    @api.doc(responses={404: 'Sizes shoes id not found', 200: 'Ok'})
    def get(self, id: int):
        products = Product_detail.query.filter_by(sizes_shoes_id=id).all()

        if products:
            products = list(map(lambda x: x.serialize(), products))
            return jsonify(get_paginated_list(products,
                                              f'/sizes-id/{id}',
                                              start=request.args.get(
                                                  'start', 1),
                                              limit=request.args.get(
                                                  'limit', 20)
                                              ))
        abort(400)


# PRODUCT DETAILS BY SIZE
@api.route('/size/<float:size>')
@api.doc(params={'size': 'float number in format x.x'})
class ProductDetailsBySize(Resource):

    @api.doc(responses={404: 'Size not found', 200: 'Ok'})
    def get(self, size: float):
        products = Product_detail.query.filter_by(sizes_shoes_val=size).all()
        if products:
            products = list(map(lambda x: x.serialize(), products))

            return jsonify(get_paginated_list(products,
                                              f'/size/{size}',
                                              start=request.args.get(
                                                  'start', 1),
                                              limit=request.args.get(
                                                  'limit', 20)
                                              ))
        else:
            abort(400)


# PRODUCT DETAILS BY LOWEST ASK PRICE
@api.route('/lowest-ask/<float:ask>')
@api.doc(params={'ask': 'float in format x.xx'})
class ProductDetailsByLowestAsk(Resource):

    @api.doc(responses={404: 'Lowest asking price not found', 200: 'Ok'})
    def get(self, ask: float):
        products = Product_detail.query.filter_by(lowest_ask=ask).all()
        # products = Product_detail.query.filter(Product_detail.lowest_ask<=ask) -- for queries less then or more then !!!
        if products:
            products = list(map(lambda x: x.serialize(), products))

            return jsonify(get_paginated_list(products,
                                              f'/lowest-ask/{ask}',
                                              start=request.args.get(
                                                  'start', 1),
                                              limit=request.args.get(
                                                  'limit', 20)
                                              ))
        abort(400)


# PRODUCT DETAILS BY HIGHEST OFFER
@api.route('/high-offer/<float:offer>')
@api.doc(params={'offer': 'float in format x.xx'})
class ProductDetailsByHighestOffer(Resource):

    @api.doc(responses={404: 'Highest offer not found', 200: 'Ok'})
    def get(self, offer: float):
        products = Product_detail.query.filter_by(highest_offer=offer).all()
        # products = Product_detail.query.filter(Product_detail.highest_offer<=offer) -- for queries less then or more then !!!
        if products:
            products = list(map(lambda x: x.serialize(), products))

            return jsonify(get_paginated_list(products,
                                              f'/high-offer/{offer}',
                                              start=request.args.get(
                                                  'start', 1),
                                              limit=request.args.get(
                                                  'limit', 20)
                                              ))
        abort(400)


# PRODUCT DETAILS BY LAST SALE PRICE
@api.route('/last-sale/<float:last_sale>')
@api.doc(params={'last_sale': 'float in format x.xx'})
class ProductDetailsByLastSale(Resource):

    @api.doc(responses={404: 'Last sale price not found', 200: 'Ok'})
    def get(self, last_sale: float):
        products = Product_detail.query.filter_by(last_sale=last_sale).all()
        # products = Product_detail.query.filter(Product_detail.last_sale<=last_sale) -- for queries less then or more then !!!
        if products:
            products = list(map(lambda x: x.serialize(), products))

            return jsonify(get_paginated_list(products,
                                              f'/last-sale/{last_sale}',
                                              start=request.args.get(
                                                  'start', 1),
                                              limit=request.args.get(
                                                  'limit', 20)
                                              ))
        abort(400)


# PRODUCT DETAILS BY LAST SALE DATE
@api.route('/last-sale-date/<string:date>')
@api.doc(params={'date': 'string in a format YYYY-MM-DD'})
class ProductDetailsByReleaseDate(Resource):

    @api.doc(responses={404: 'Last sale date not found', 200: 'Ok'})
    def get(self, date: str):
        products = Product_detail.query.filter(
            Product_detail.last_sale_date.contains(date))
        # products = Product_detail.query.filter(Product_detail.last_sale_date<=date) -- for queries less then or more then !!!
        if products:
            products = list(map(lambda x: x.serialize(), products))

            return jsonify(get_paginated_list(products,
                                              f'/last-sale-date/{date}',
                                              start=request.args.get(
                                                  'start', 1),
                                              limit=request.args.get(
                                                  'limit', 20)
                                              ))
        abort(400)


# ##### PRODUCT DETAILS BY SALES #####
@api.route('/sales/<int:sales>')
@api.doc(params={'sales': 'integer'})
class ProductDetailsBySales(Resource):

    @api.doc(responses={404: 'Sales not found', 200: 'Ok'})
    def get(self, sales: int):
        products = Product_detail.query.filter_by(sales=sales).all()
        # products = Product_detail.query.filter(Product_detail.sales<=sales) -- for queries less then or more then !!!
        if products:
            products = list(map(lambda x: x.serialize(), products))

            return jsonify(get_paginated_list(products,
                                              f'/sales/{sales}',
                                              start=request.args.get(
                                                  'start', 1),
                                              limit=request.args.get(
                                                  'limit', 20)
                                              ))
        else:
            abort(400)


########################################################
########################################################
########################################################



################ NEED TO CHECK ########################


# ##### SLUG #####
# @pd.route('/slug/<string:slug>')
# @api.doc(params={'slug': 'string in a format str+str1+str2'})
# class ProductDetailsBySlug(Resource):

#     #### GET PRODUCT DETAILS BY SLUG ####
#     @api.doc(responses={404: 'Slug not found', 200: 'Ok'})
#     def get(self, slug: str):

#         slug_ = list(slug.split("+"))

#         if len(slug_) is 1:
#             products = Product_detail.query.filter(Product_detail.slug.contains(slug_[0]))
#         else:
#             products = Product_detail.query.filter(Product_detail.slug.contains(slug_[0]))
#             for i in range(1, len(slug_)):
#                 products = products.filter(Product_detail.slug.contains(slug_[i]))

#         if products:
#             products = list(map(lambda x: x.serialize(), products))

#             return jsonify(get_paginated_list(products,
#                 f'/slug/{slug}',
#                 start=request.args.get('start', 1),
#                 limit=request.args.get('limit', 20)
#             ))
#         else:
#             abort (404)


# ##### PRODUCT NAME #####
# @pd.route('/product-name/<string:name>')
# @api.doc(params={'name': 'string in a format str+str1+str2'})
# class ProductDetailsByProductName(Resource):

#     #### GET PRODUCT DETAILS BY PRODUCT NAME ####
#     @api.doc(responses={404: 'Product name not found', 200: 'Ok'})
#     def get(self, name: str):

#         name_ = list(name.split("+"))

#         if len(name_) is 1:
#             products = Product_detail.query.filter(Product_detail.product_name.contains(name_[0]))
#         else:
#             products = Product_detail.query.filter(Product_detail.product_name.contains(name_[0]))
#             for i in range(1, len(name_)):
#                 products = products.filter(Product_detail.product_name.contains(name_[i]))

#         if products:
#             products = list(map(lambda x: x.serialize(), products))

#             return jsonify(get_paginated_list(products,
#                 f'/product-name/{name}',
#                 start=request.args.get('start', 1),
#                 limit=request.args.get('limit', 20)
#             ))
#         else:
#             abort (404)


# ##### BRAND NAME #####
# @pd.route('/brand-name/<string:name>')
# @api.doc(params={'name': 'string in a format str+str1+str2'})
# class ProductDetailsByBrandName(Resource):

#     #### GET PRODUCT DETAILS BY BRAND NAME ####
#     @api.doc(responses={404: 'Brand name not found', 200: 'Ok'})
#     def get(self, name: str):

#         name_ = list(name.split("+"))

#         if len(name_) is 1:
#             products = Product_detail.query.filter(Product_detail.brand_name.contains(name_[0]))
#         else:
#             products = Product_detail.query.filter(Product_detail.brand_name.contains(name_[0]))
#             for i in range(1, len(name_)):
#                 products = products.filter(Product_detail.brand_name.contains(name_[i]))

#         if products:
#             products = list(map(lambda x: x.serialize(), products))

#             return jsonify(get_paginated_list(products,
#                 f'/brand-name/{name}',
#                 start=request.args.get('start', 1),
#                 limit=request.args.get('limit', 20)
#             ))
#         else:
#             abort (404)


# ##### MODEL CATEGORY #####
# @pd.route('/category/<string:category>')
# @api.doc(params={'category': 'string in a format str+str1+str2'})
# class ProductDetailsByModelCategory(Resource):

#     #### GET PRODUCT DETAILS BY MODEL CATEGORY ####
#     @api.doc(responses={404: 'Model category not found', 200: 'Ok'})
#     def get(self, category: str):

#         category_ = list(category.split("+"))

#         if len(category_) is 1:
#             products = Product_detail.query.filter(Product_detail.model_cat_name.contains(category_[0]))
#         else:
#             products = Product_detail.query.filter(Product_detail.model_cat_name.contains(category_[0]))
#             for i in range(1, len(category_)):
#                 products = products.filter(Product_detail.model_cat_name.contains(category_[i]))
#         if products:
#             products = list(map(lambda x: x.serialize(), products))
#             return jsonify(get_paginated_list(products,
#                 f'/category/{category}',
#                 start=request.args.get('start', 1),
#                 limit=request.args.get('limit', 20)
#             ))
#         else:
#             abort (404)
