#!/usr/bin/ python3

# Random Forest Classifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
import boto3
import paramiko
from sqlalchemy import create_engine
from flask import Flask, request, jsonify
import pandas as pd
import os


app = Flask(__name__)
awsAccessKey =os.environ.get('AWS_ACCESS_KEY')
awsSecretKey =os.environ.get('AWS_SECRET_KEY')



def download_s3(bucketname):
  object_key="iris.csv"
  #BUCKET_NAME="javadownload"
  BUCKET_NAME=bucketname
  client = boto3.client('s3', aws_access_key_id=awsAccessKey, aws_secret_access_key=awsSecretKey)
  client.download_file(BUCKET_NAME, object_key, object_key)

def upload_to_bucket(bucketname):
  s3 = boto3.client('s3', aws_access_key_id=awsAccessKey, aws_secret_access_key=awsSecretKey)
  s3.upload_file(Filename = 'trainedmodel.pkl', Bucket = bucketname, Key = 'trainedmodel.pkl')


def tptexecution():
  ssh_connect('1.1.1.1')

def load_datafrom_td():
  user, pasw, host = 'dbc','TD', '1.1.1.1'
  td_engine = create_engine('teradatasql://{}:{}@{}'.format(user,pasw,host))
  query = 'select * from iris_db.IRIS'
  result = td_engine.execute(query)
  iris = pd.read_sql(query,td_engine)
  print (iris)
  print (type(iris))
  print (iris.columns.values)
  X_train, X_test, y_train, y_test = train_test_split(iris[iris.columns[1:-1]], iris[iris.columns[-1]], random_state=42, test_size=0.7)
  # Build the model
  clf = RandomForestClassifier(n_estimators=10)
  # Train the classifier
  clf.fit(X_train, y_train)
  # Predictions
  predicted = clf.predict(X_test)
  # Check accuracy
  print(accuracy_score(predicted, y_test))
  import pickle
  with open('trainedmodel.pkl', 'wb') as model_pkl:
    pickle.dump(clf, model_pkl, protocol=2)
  return accuracy_score(predicted, y_test)

def ssh_connect(host):
  try:
    ssh = paramiko.SSHClient()
    print('Calling paramiko')
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host)
    ssh_command(ssh)
  except Exception as e:
    print('Connection Failed')
    print(e)

def ssh_command(ssh):
  command = 'sh /opt/iris_load_data.sh'
  ssh.invoke_shell()
  stdin, stdout, stderr = ssh.exec_command(command)
  print(stdout.read())


@app.route("/ingest", methods=['POST'])
def ingestdata():
  bucketname = request.json['bucketname']
  download_s3(bucketname)
  tptexecution()
  return jsonify({'Message': 'Ingestion Completed'}), 200

@app.route("/train", methods=['POST'])
def savemodel():
  bucketname = request.json['bucketname']
  accuracy_score = load_datafrom_td()
  upload_to_bucket(bucketname)
  return jsonify({'Message': 'Model Uploaded', 'Accuracy_Score': accuracy_score}), 200

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
