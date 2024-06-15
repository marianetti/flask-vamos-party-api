from flask_restx import Namespace, Resource

discotecas_namespace = Namespace('discotecas', description="namespace para discotecas")

@discotecas_namespace.route('/discotecas')
class GetCreate(Resource):

    def get(self):
        pass

    def post(self):
        pass


@discotecas_namespace.route('/discoteca/<int:disco_id>')
class GetUpdateDelete(Resource):

    def get(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
