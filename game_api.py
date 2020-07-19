#!/usr/bin/env python
import json
from kafka import KafkaProducer
from flask import Flask, request
from datetime import datetime


app = Flask(__name__)
producer = KafkaProducer(bootstrap_servers='kafka:29092')


def log_to_kafka(topic, event):
    #Get the values passed in the POST
    #form_values = request.form.to_dict()
    #event.update(form_values)
    
    #Get the JSON posted in the body
    body_json = request.get_json()
    event.update(body_json)
    
    
    #Save the headers in the schema
    event['request_headers'] = dict(request.headers)
    event['timestamp'] = str(datetime.now())
    
    producer.send(topic, json.dumps(event).encode())
    return str(event)


@app.route("/", methods=['GET', 'POST'])
def default_response():
    default_event = {'event_type': 'default'}
    log = log_to_kafka('events', default_event)
    return " This is the default response!\n" + log


@app.route("/purchase_a_sword/", methods=['GET', 'POST'])
def purchase_a_sword():
    purchase_sword_event = {'event_type': 'purchase_sword'}
    log = log_to_kafka('events', purchase_sword_event)
    return "Sword Purchased!\n" + log

@app.route("/sell_a_sword/", methods=['GET', 'POST'])
def sell_a_sword():
    purchase_sword_event = {'event_type': 'sell_a_sword'}
    log = log_to_kafka('events', purchase_sword_event)
    return "Sword Sold!\n" + log