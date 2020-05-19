from flask import jsonify, request
from flask_restx import Namespace, Resource, abort
from datetime import date

from models import db, Media_storage
from pagination import get_paginated_list


########### API MEDIA STORAGE ###########
api = Namespace(
    'media', description='Operations related to media storage table')


# GET ALL MEDIA
@api.route('')
class AllMedia(Resource):

    # GET
    @api.doc(responses={404: 'Media not found', 200: 'Ok'})
    def get(self):
        media = Media_storage.query.all()
        media = list(map(lambda x: x.serialize(), media))

        return jsonify(get_paginated_list(media, '/media',
                                          start=request.args.get('start', 1),
                                          limit=request.args.get('limit', 20)
                                          ))

    # POST
    @api.doc(responses={404: 'Media not posted', 200: 'Ok'})
    @api.doc(params={'alt': 'string',
                     'url': 'string',
                     'type': 'string',
                     'product_id': 'integer',
                     'transaction_id': 'integer',
                     'verification_id': 'integer'})
    def post(self):
        body = request.get_json()
        today = date.today()
        # decoded = base64.b64decode(body['image']) - incase to encode in binary
        media = Media_storage(
            alt=body['alt'],
            created_at=today,
            url=body['url'],
            type=body['type'],
            product_id=body['product_id'],
            transaction_id=body['transaction_id'],
            verification_id=body['verification_id'])
        db.session.add(media)
        db.session.commit()
        return jsonify(media.serialize())


# MEDIA BY PRODUCT ID
@api.route('/product/<int:id>')
@api.doc(params={'id': 'int'})
class MediaByProductId(Resource):

    @api.doc(responses={404: 'Media not found', 200: 'Ok'})
    def get(self, id: int):
        media = Media_storage.query.filter_by(product_id=id).all()
        if media:
            media = list(map(lambda x: x.serialize(), media))
            return jsonify(get_paginated_list(media,
                                              f'/product/{id}',
                                              start=request.args.get(
                                                  'start', 1),
                                              limit=request.args.get(
                                                  'limit', 10)
                                              ))
        abort(404, f'Media with product id {id} does not exist')


########################################################
########################################################
########################################################
