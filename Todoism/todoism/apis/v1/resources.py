from flask.views import MethodView
from flask import jsonify, request, current_app, g

from todoism.models import Item
from todoism.apis.v1.errors import api_abort


class ItemAPI(MethodView):

    def get(self, item_id):
        item = Item.query.get_or_404(item_id)
        if g.current_user != item.author:
            return api_abort(403)
        return jsonify()