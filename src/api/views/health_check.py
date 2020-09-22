from flask_restful import Resource


class HealthCheck(Resource):

    def get(self):
        """
        HTTP VERB: GET
        path: /health-check
        Description: Check if app is alive
        """
        return {'alive': True}

