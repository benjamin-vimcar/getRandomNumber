#!/usr/bin/env python3

import connexion
import logging

from swagger_server import encoder


def main():
    logging.basicConfig(level=logging.INFO)

    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api(
        'swagger.yaml',
        validate_responses=True,
        arguments={'title': 'getRandomNumber'})
    app.run(port=8080)


if __name__ == '__main__':
    main()
