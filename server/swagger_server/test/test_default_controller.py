# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.user import User  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_activate_user(self):
        """Test case for activate_user


        """
        query_string = [('token', 'token_example')]
        response = self.client.open(
            '/api/v1/user/confirm',
            method='POST',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_create_user(self):
        """Test case for create_user


        """
        user = User()
        response = self.client.open(
            '/api/v1/user/create',
            method='POST',
            data=json.dumps(user),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_random_number(self):
        """Test case for get_random_number


        """
        secret_session_token = 'secret_session_token_example'
        response = self.client.open(
            '/api/v1/random_number',
            method='GET',
            data=json.dumps(secret_session_token),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_login_user(self):
        """Test case for login_user


        """
        user = User()
        response = self.client.open(
            '/api/v1/user/login',
            method='POST',
            data=json.dumps(user),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
