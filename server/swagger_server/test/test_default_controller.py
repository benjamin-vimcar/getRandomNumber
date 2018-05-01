# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO
import jwt

from swagger_server.models.user import User  # noqa: E501
from swagger_server.test import BaseTestCase
from swagger_server.get_random_number import db
from swagger_server.get_random_number.backend import (
    SUPER_SECRET_SECRET_KEY, SUPER_SECRET_CONFIRMATION_KEY)


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_activate_user(self):
        """Test case for activate_user


        """
        db.DB = {"email@test.com": {'confirmed': False}}
        token = jwt.encode(
            {'user': "email@test.com"},
            SUPER_SECRET_CONFIRMATION_KEY,
            algorithm='HS256')

        response = self.client.open(
            '/api/v1/user/confirm',
            method='POST',
            content_type='application/json',
            query_string=[('token', token)])
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_create_user(self):
        """Test case for create_user


        """
        user = User(email="email@test.com", password="test_password")
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
        response = self.client.open(
            '/api/v1/random_number',
            method='GET',
            headers={'Authorization': b"Bearer " + jwt.encode(
                {'user': "email@test.com"},
                SUPER_SECRET_SECRET_KEY,
                algorithm='HS256')},
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_random_number_missing_auth(self):
        """Test case for get_random_number with missing header


        """
        response = self.client.open(
            '/api/v1/random_number',
            method='GET',
            content_type='application/json')
        self.assert403(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_random_number_invalid_auth(self):
        """Test case for get_random_number with incorrect auth data
        """
        response = self.client.open(
            '/api/v1/random_number',
            method='GET',
            headers={'Authorization': b'foo'},
            content_type='application/json')
        self.assert403(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_login_user(self):
        """Test case for login_user


        """
        db.DB = {"email@test.com": {'password': "test_password"}}
        user = User(email="email@test.com", password="test_password")
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
