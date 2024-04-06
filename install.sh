#!/bin/bash

sudo docker run --name my-redis -d -p 6379:6379 redis

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
