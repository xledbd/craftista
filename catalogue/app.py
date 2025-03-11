import boto3.dynamodb
from flask import Flask, jsonify, render_template
from datetime import datetime
import socket
import os
import json
import boto3
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger(__name__)

app = Flask(__name__)

class Products:
    def __init__(self, dyn_resource):
        """
        :param dyn_resource: A Boto3 DynamoDB resource.
        """
        self.dyn_resource = dyn_resource
        # The table variable is set during the scenario in the call to
        # 'exists' if the table exists..
        self.table = None

    def exists(self, table_name):
        """
        Determines whether a table exists. As a side effect, stores the table in
        a member variable.

        :param table_name: The name of the table to check.
        :return: True when the table exists; otherwise, False.
        """
        try:
            table = self.dyn_resource.Table(table_name)
            table.load()
            exists = True
        except ClientError as err:
            if err.response["Error"]["Code"] == "ResourceNotFoundException":
                exists = False
            else:
                logger.error(
                    "Couldn't check for existence of %s. Here's why: %s: %s",
                    table_name,
                    err.response["Error"]["Code"],
                    err.response["Error"]["Message"],
                )
                raise
        else:
            self.table = table
        return exists
    
    def get_product(self, product_id):
        """
        Gets product data from the table for a specific product.

        :param id: The id of the product.
        :return: The data about the requested product.
        """
        try:
            response = self.table.get_item(Key={"id": product_id})
        except ClientError as err:
            logger.error(
                "Couldn't get product %s from table %s. Here's why: %s: %s",
                id,
                self.table.name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
        else:
            return response["Item"]
        
    def scan_products(self):
        """
        Scans for all products.

        :return: The list of products.
        """
        products = []
        scan_kwargs = {}
        try:
            done = False
            start_key = None
            while not done:
                if start_key:
                    scan_kwargs["ExclusiveStartKey"] = start_key
                response = self.table.scan(**scan_kwargs)
                products.extend(response.get("Items", []))
                start_key = response.get("LastEvaluatedKey", None)
                done = start_key is None
        except ClientError as err:
            logger.error(
                "Couldn't scan for products. Here's why: %s: %s",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise

        return products
    
with open("config.json", "r") as config_file:
    config_data = json.load(config_file) 

if (config_data.get("data_source") == "db"):
    table_name = config_data.get("db_name")
    products = Products(boto3.resource("dynamodb"))
    products_exists = products.exists(table_name)
else:
    with open('products.json', 'r') as f:
        products = json.load(f)

@app.route('/')
def home():
    system_info = get_system_info()
    app_version = config_data.get("app_version", "N/A")  # Default to "N/A" if no version is found
    return render_template('index.html', current_year=datetime.now().year, system_info=system_info, version=app_version)

@app.route('/api/products', methods=['GET'])

def get_products():
    if (config_data.get("data_source") == "db"):
        return jsonify(products.scan_products()), 200
    else:
        return jsonify(products), 200


@app.route('/api/products/<string:product_id>', methods=['GET'])
def get_product(product_id):
    product = products.get_product(product_id)
    if product is not None:
        return jsonify(product)
    else:
        return jsonify({'message': 'Product not found'}), 404

def get_system_info():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    # Additional logic for container and Kubernetes check
    is_container = os.path.exists('/.dockerenv')
    is_kubernetes = os.path.exists('/var/run/secrets/kubernetes.io/serviceaccount')
    
    return {
        "hostname": hostname,
        "ip_address": ip_address,
        "is_container": is_container,
        "is_kubernetes": is_kubernetes
    }


if __name__ == "__main__":
    app.run(debug=True)

