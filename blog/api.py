from flask import current_app
from flask_restful import Resource, Api, reqparse
import markdown
from markupsafe import escape


api = Api(current_app)
parser = reqparse.RequestParser()
parser.add_argument('mdtext')

class MarkApi(Resource):
    def get(self):
        return {'status': 'ok'}

    def post(self):
        args = parser.parse_args()
        tmp_html = markdown.markdown(args['mdtext'], extensions=['extra', 'codehilite', 'toc'])
        return {'html': tmp_html}
        
def set_resources():
    api.add_resource(MarkApi, '/markapi/')