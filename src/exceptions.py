import json


class ServiceRESTError(Exception):
    def __init__(self):
        self.code = 0
        self.error_name = self.__class__.__name__
        self.error_message = ""
        self.error_details = ""

    def __str__(self, *args, **kwargs):
        error_json = {}
        if self.error_name:
            error_json["name"] = self.error_name

        if self.error_message:
            error_json["message"] = self.error_message

        if self.error_details:
            error_json["details"] = self.error_details

        return json.dumps(error_json)


class FormatValidationError(ServiceRESTError):
    def __init__(self, missing_errors=None, type_errors=None, format_errors=None):
        super(self.__class__, self).__init__()
        self.code = 400
        self.status_code = 'E400'
        self.error_message = "Request not formatted properly."
        if missing_errors:
            self.error_message += " The following fields are missing: {missing}".format(missing=missing_errors)
        if format_errors:
            self.error_message += " The following fields have invalid format: {format}".format(format=format_errors)
        if type_errors:
            self.error_message += " The following fields have invalid value:"
            for err in type_errors:
                try:
                    self.error_message += " {field} should be of type {type}.".format(field=err[0], type=err[1])
                except:
                    pass


class ResourceFound(ServiceRESTError):
    code = 302

    def __init__(self):
        super(self.__class__, self).__init__()
        self.code=self.__class__.code
        self.status_code = 'E302'
        self.error_message = "Operation aborted because the requested resources are already existed"


class ResourceNotFoundError(ServiceRESTError):
    code = 404

    def __init__(self, missing_id):
        super(self.__class__, self).__init__()
        self.code=self.__class__.code
        self.error_message = "Operation aborted because the resource with the following entity was not found: {missing}".format(missing=missing_id)
        self.status_code = 'E404'


class EmptyResult(ServiceRESTError):
    code = 210

    def __init__(self):
        super(EmptyResult, self).__init__()
        self.code=self.__class__.code
        self.error_message = "Requested data can not be found"


class ForbiddenError(ServiceRESTError):
    code = 405

    def __init__(self):
        super(self.__class__, self).__init__()
        self.code=self.__class__.code
        self.error_message = "Forbidden request."
        self.status_code = 'E405'


class UnknownError(ServiceRESTError):
    code = 410

    def __init__(self, error_message=None):
        super(self.__class__, self).__init__()
        self.code=self.__class__.code
        self.status_code = 'E410'
        if error_message:
            self.error_message = error_message
        else:
            self.error_message = "Unknown error occurred. Please, try again later."


class DBError(ServiceRESTError):
    code = 420

    def __init__(self):
        super(self.__class__, self).__init__()
        self.code=self.__class__.code
        self.error_message = "Database failed to serve the request."


class FormatError(ServiceRESTError):
    code = 430

    def __init__(self):
        super(self.__class__, self).__init__()
        self.code=self.__class__.code
        self.status_code = 'E430'
        self.error_message = "Request not formatted properly."

