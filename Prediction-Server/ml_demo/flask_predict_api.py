#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 21:06:35 2018

@author: parimal karkar
"""

import pickle
import numpy as np
from flasgger import Swagger
import json
import boto3
import os
from flask import Flask, request, redirect, url_for
app = Flask(__name__)
swagger = Swagger(app)

awsAccessKey = os.environ.get('AWS_ACCESS_KEY')
awsSecretKey = os.environ.get('AWS_SECRET_KEY')

client = boto3.client(
    's3',
    # Hard coded strings as credentials, not recommended.
    aws_access_key_id=awsAccessKey,
    aws_secret_access_key=awsSecretKey
)


@app.route("/predict/<bucket_name>/<obj_key>", methods=['POST'])
def predict(bucket_name,obj_key):
    """
     generalized implementation for prediction
    :param bucket_name:
    :param obj_key:
    :return:
    """
    input_payload = request.get_data()
    prediction_input = json.loads(input_payload)
    client.download_file(bucket_name, obj_key, obj_key)
    with open(obj_key, 'rb') as model_file:
        model = pickle.load(model_file)
    prediction_output = model.predict(prediction_input)
    result = str(prediction_output)
    print(result)
    return result


@app.route("/iris/predict", methods=['POST'])
def predict_iris():
    """Example endpoint returning a prediction of iris
    ---
    parameters:
      - name: s_length
        in: query
        type: number
        required: true
      - name: s_width
        in: query
        type: number
        required: true
      - name: p_length
        in: query
        type: number
        required: true
      - name: p_width
        in: query
        type: number
        required: true
    """
    input_payload = request.get_data()
    iris_j_data = json.loads(input_payload)
    s_length = iris_j_data["sepal_length"]
    s_width = iris_j_data["sepal_width"]
    p_length = iris_j_data["petal_length"]
    p_width = iris_j_data["petal_width"]

    input_params = request.get_data()
    #transformed_data = "[[" + s_length + "," + s_width + ", " + p_length + ", " + p_width + "]]"
    transformed_data = np.array([[s_length, s_width, p_length, p_width]])
    transformed_data = json.dumps(transformed_data.astype(float).tolist())
    print(transformed_data)
    iris_set = ['Iris-Setosa', 'Iris-Versicolour', 'Iris-Virginica']
    predict_url = "predict"
    bucket = "ml.bundles"
    obj = "rf.pkl"
    predict_url_prepared = url_for(predict_url, bucket_name=bucket, obj_key=obj)
    response = app.test_client().post(predict_url_prepared, data=transformed_data)
    iris_prediction_result = iris_set[json.loads(response.data.decode())[0]];
    print(iris_prediction_result)
    return iris_prediction_result

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=8080)

