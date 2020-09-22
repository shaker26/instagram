import copy
import json as jsonlib

from tests import base
from src import utils
from src import app, db


class Base(base.Base):
    """Base test class for integration tests."""
    def setUp(self):
        super(Base, self).setUp()
        app.testing = True
        # Use this to send requests to the Flask app.
        self.app = app.test_client()

        # Rollback any transaction in process and recreate the database from scratch.
        #
        # Per http://stackoverflow.com/questions/24289808/drop-all-freezes-in-flask-with-sqlalchemy,
        # the hangs I was sometimes seeing in my test runs may have had to do
        # with outstanding transactions.  Automatically rolling back any
        # pending transaction seems to have fixed the hangs. -- ODS 13 Apr 2016
        db.session.rollback()
        utils.resetDB(db)

    def assertJSONEqual(self, one, two, msg=None):
        """Checks that both objects (JSON, lists, and/or dictionaries) are equal."""
        one = jsonlib.loads(jsonlib.dumps(one))
        two = jsonlib.loads(jsonlib.dumps(two))

        if type(one) != type(two):
            if msg is None:
                msg = 'Expected both objects to be of the same type, got {} and {}.'.format(
                    type(one), type(two))
            self.fail(msg)

        elif isinstance(one, dict):
            self.assertDictEqual(one, two)

        elif isinstance(one, list):
            self.assertListEqual(one, two)

        else:
            if msg is None:
                msg = 'Unexpected object types, got {} and {}.'.format(type(one), type(two))
            self.fail(msg)

    def assertBadRequest(self, response, reason=None, msg=None):
        """Checks that the response returned a status of 400 Bad Request."""
        self.assertEqual(400, response.status_code, msg)
        if reason:
            self.assertReasonEquals(response, reason)

    def assertUnauthorized(self, response, reason=None, msg=None):
        """Checks that the response returned a status of 401 Unauthorized."""
        self.assertEqual(401, response.status_code, msg)
        if reason:
            self.assertReasonEquals(response, reason)


    def assertForbidden(self, response, reason=None, msg=None):
        """Checks that the response returned a status of 403 Forbidden."""
        self.assertEqual(403, response.status_code, msg)
        if reason:
            self.assertReasonEquals(response, reason)

    def assertNotFound(self, response, reason=None, msg=None):
        """Checks that the response returned a status of 404 Not Found."""
        self.assertEqual(404, response.status_code, msg)
        if reason:
            self.assertReasonEquals(response, reason)

    def assertConflict(self, response, reason=None, msg=None):
        """Checks that the response returned a status of 409 Conflict."""
        self.assertEqual(409, response.status_code, msg)
        if reason:
            self.assertReasonEquals(response, reason)

    def assertReasonEquals(self, response, reason):
        """Checks that the response's reason field equals what is expected."""
        self.assertEqual(reason, self.getJsonData(response)['reason'])

    def assertSuccess(self, response, msg=None):
        """Checks that the response returned a status considered successful (200-204)."""
        if response.status_code < 200 or response.status_code > 204:
            if msg is None:
                msg = 'Expected success status code, got {}. Response:\n{}'.format(
                    response.status_code, response.data)
            self.fail(msg)

    def _buildHeadersAndParams(self, headers, params):
        headers = {} if headers is None else copy.deepcopy(headers)
        params = {} if params is None else copy.deepcopy(params)
        return headers, params

    def get(self, url, data=None, json=None, headers=None, params=None):
        """Retrieve some data from our Flask app at the given URL.

        :param url: (string) The part of the URL path after https://<host>/api/v1;
          the rest of the URL will be filled in for you
        :param data: (string) The bytestring to post in the body. Exactly one
          of data and json must be specified.
        :param json: (object) Data to be JSON-encoded and posted in the body.
          The content type will be set to application/json.
        :param headers: (dict) A dictionary of HTTP headers to set on the
          request
        :param params: (dict) A dictionary of query-string parameters to set
          on the request
        """
        headers, params = self._buildHeadersAndParams(headers, params)
        if json:
            data = jsonlib.dumps(json)
            headers['Content-Type'] = 'application/json'
        return self.app.get('/api/v1' + url, data=data, headers=headers, query_string=params)

    def post(self, url, data=None, json=None, headers=None, params=None):
        """Post some data to our Flask app at the given URL.

        :param url: (string) The part of the URL path after https://<host>/v1;
          the rest of the URL will be filled in for you
        :param data: (string) The bytestring to post in the body. Exactly one
          of data and json must be specified.
        :param json: (object) Data to be JSON-encoded and posted in the body.
          The content type will be set to application/json.
        :param headers: (dict) A dictionary of HTTP headers to set on the
          request
        :param params: (dict) A dictionary of query-string parameters to set
          on the request
        :return: (flask.Response) The response from the API.
        """
        assert not (data and json)
        headers, params = self._buildHeadersAndParams(headers, params)
        if json:
            data = jsonlib.dumps(json)
            headers['Content-Type'] = 'application/json'
        return self.app.post('/api/v1' + url, data=data, headers=headers, query_string=params)

    def put(self, url, data=None, json=None, headers=None, params=None):
        """Put some data at the given URL in our Flask app.

        :param url: (string) The part of the URL path after https://<host>/v1;
          the rest of the URL will be filled in for you
        :param data: (string) The bytestring to post in the body. Exactly one
          of data and json must be specified.
        :param json: (object) Data to be JSON-encoded and posted in the body.
          The content type will be set to application/json.
        :param headers: (dict) A dictionary of HTTP headers to set on the
          request
        :param params: (dict) A dictionary of query-string parameters to set
          on the request
        :return: (flask.Response) The response from the API.
        """
        assert not (data and json)
        headers, params = self._buildHeadersAndParams(headers, params)
        if json:
            data = jsonlib.dumps(json)
            headers['Content-Type'] = 'application/json'
        return self.app.put('/api/v1' + url, data=data, headers=headers, query_string=params)

    def delete(self, url, data=None, json=None, headers=None):
        """Delete some data from our Flask app at the given URL.

        :param url: (string) The part of the URL path after https://<host>/v1;
          the rest of the URL will be filled in for you
        :param headers: (dict) A dictionary of HTTP headers to set on the
          request
        :return: (flask.Response) The response from the API.
        """
        headers, params = self._buildHeadersAndParams(headers, None)
        if json:
            data = jsonlib.dumps(json)
            headers['Content-Type'] = 'application/json'
        return self.app.delete('/api/v1' + url, data=data, headers=headers, query_string=params)

    def patch(self, url, data=None, json=None, headers=None, params=None):
        """Update some data at the given URL in our Flask app.

        :param url: (string) The part of the URL path after https://<host>/v1;
          the rest of the URL will be filled in for you
        :param data: (string) The bytestring to post in the body. Exactly one
          of data and json must be specified.
        :param json: (object) Data to be JSON-encoded and posted in the body.
          The content type will be set to application/json.
        :param headers: (dict) A dictionary of HTTP headers to set on the
          request
        :param params: (dict) A dictionary of query-string parameters to set
          on the request
        :return: (flask.Response) The response from the API.
        """
        assert not (data and json)
        headers, params = self._buildHeadersAndParams(headers, params)
        if json:
            data = jsonlib.dumps(json)
            headers['Content-Type'] = 'application/json'
        return self.app.patch('/api/v1' + url, data=data, headers=headers, query_string=params)

    def getJsonData(self, response):
        """Unmarshal and return the JSON data in the response body.

        Also checks that the response type is application/json.

        :param response: (flask.Response) The response to decode
        :return: (object) The JSON-deserialized data
        """
        self.assertEqual('application/json', response.headers['Content-Type'])
        return jsonlib.loads(response.data)

    def jsonPostAndReturn(self, url, data=None, params=None):
        """Post JSON data to the given URL and return the result.

        Fails the current test if the operation is not successful.

        :param url: (string) The URL to post to
        :param data: (object) Data to be JSON-serialized and sent as the body
          of the request
        :param params: (dict) A dictionary of query-string parameters to set
          on the request
        :return: (object) The JSON-deserialized body of the response
        """
        response = self.post(url, json=data, params=params)
        self.assertSuccess(response)
        return self.getJsonData(response)

    def jsonGetAndReturn(self, url, params=None):
        """Get a JSON document at the given URL.

        Fails the current test if the operation is not successful.

        :return: (object) The JSON-deserialized body of the response
        """
        response = self.get(url, params=params)
        self.assertSuccess(response)
        return self.getJsonData(response)

    def jsonPutAndReturn(self, url, data=None):
        """Put a JSON document at the given URL.

        Fails the current test if the operation is not successful.

        :return: (object) The JSON-deserialized body of the response
        """
        response = self.put(url, json=data)
        self.assertSuccess(response)
        return self.getJsonData(response)

    def jsonPatchAndReturn(self, url, data=None):
        """Patches with a JSON document at the given URL.

        Fails the current test if the operation is not successful.

        :return: (object) The JSON-deserialized body of the response
        """
        response = self.patch(url, json=data)
        self.assertSuccess(response)
        return self.getJsonData(response)

    def assertPatched(self, original, updated, patch_dict):
        """Checks whether the given structure was patched properly.

        The original structure is considered properly patched if:
        - for every field that _was not_ updated, the value stayed the same
        - for every field that _was_ updated, the value is the updated value

        :param original: (dict) The structure pre-update
        :param updated: (dict) The structure post-update
        :param patch_dict: (dict) The fields that should have been updated, and
          their updated values
        """
        for key, updated_value in updated.iteritems():
            if key in patch_dict:
                if patch_dict[key] is not None:
                    self.assertEqual(patch_dict[key], updated_value)
            else:
                self.assertEqual(original[key], updated_value)
