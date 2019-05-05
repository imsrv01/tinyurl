#!flask/bin/python
import json, random, string
from flask import Flask, Response, render_template, request, redirect
import boto3
from botocore.exceptions import ClientError
#from helloworld.flaskrun import flaskrun

application = Flask(__name__)

@application.route('/', methods=['GET', 'POST'])
def url():
    form = request.form
    if request.method == 'POST':
        longurl = request.form.get('url')
        print("longurl --> " + longurl)
        short_url = randomString()
        dynamodb =boto3.resource('dynamodb')
        table = dynamodb.Table('tiny_url')
        table.put_item(
        Item={
            'short_url': short_url,
            'longurl': longurl
            }
        )
        return render_template("home.html", short_url=short_url)
    return render_template("home.html")

@application.route('/<short_url>')
def redirect_short_url(short_url):
    try:
        dynamodb =boto3.resource('dynamodb')
        table = dynamodb.Table('tiny_url')
        response = table.get_item(
        Key={
            'short_url': short_url
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        
    else:
        longurl = response['Item']['longurl']
        #print("GetItem succeeded:" + longurl)
        print("redirecting to  --> " + longurl)
        return redirect(longurl)

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def createTable():

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.create_table(
    TableName='tinyurl',
    KeySchema=[
        {
            'AttributeName': 'short_url',
            'KeyType': 'HASH'  #Partition key
        },
        {
            'AttributeName': 'long_url',
            'KeyType': 'RANGE'  #Sort key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'long_url',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'title',
            'AttributeType': 'S'
        },

    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
    )
    


if __name__ == '__main__':
    #flaskrun(application)
    #application.run()
    #createTable()
    application.run(
        debug="false",
        host="127.0.0.1",
        port=8080
    )
