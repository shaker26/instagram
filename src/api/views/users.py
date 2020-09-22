import traceback
from flask_restful import Resource
from flask import current_app, request

from src.api.controller.users import UsersController
from src.exceptions import *

class Users(Resource):
    """
    HTTP VERB: GET
    path: /user?user_id=test
    Description: Get user info by given user id.
    """
    def get(self):
        try:
            # Validate that user_id exists in query params
            args = request.args

            if 'user_id' not in args:
                raise FormatValidationError

            # Create instance of InsightsController Class
            controllerObject = UsersController()
            user = controllerObject.get_user(user_id=args['user_id'])
            return user, 200

        except Exception as e:
            current_app.logger.debug(
                'URL: /instagram/user, Method: GET, failed with exception {exception}'.format(exception=e))

            current_app.logger.debug(traceback.format_exc())
            if not issubclass(e.__class__, ServiceRESTError):
                e = UnknownError()

            response = {'status': False, 'status_code': e.status_code, 'message': e.error_message}
            return json.dumps(response), e.code

        except FormatValidationError as e:
            current_app.logger.debug(
                'URL: /instagram/user, Method: GET, failed with exception {exception}'.format(exception=e))
            current_app.logger.debug(traceback.format_exc())
            return json.dumps({'status': False, 'status_code': e.status_code, 'message': e.error_message}), e.code


