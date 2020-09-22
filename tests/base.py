import json
import chai
import requests


class Base(chai.Chai):
    """Base test class for all tests."""
    def setUp(self):
        super(Base, self).setUp()
        self.stubRequests()

    def tearDown(self):
        super(Base, self).tearDown()

    def stubRequests(self):
        """Make sure all of the 'requests' library's actions are stubbed out.

        This protects us from making an inadvertent outbound HTTP request during
        testing.
        """
        requests_funcs = ['request', 'head', 'options', 'get', 'post', 'put', 'delete', 'patch']
        for func in requests_funcs:
            self.stub(requests, func)

    def mockResponse(self, status, data):
        """Mocks a requests.Response with the given status and JSON data."""
        response = self.mock()
        response.status_code = status
        response.headers = {'Content-Type': 'application/json; charset=utf-8'}
        response.text = json.dumps(data)
        self.expect(response.json).any_args().at_least(0).returns(data)
        return response
