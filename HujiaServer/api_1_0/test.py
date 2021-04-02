from . import api
from flask import jsonify, json


@api.route("/")
def index():

    data = {
       'name':'zs'

    }

    js_data = json.dumps(data)


    return jsonify(err='100', msg=js_data)


