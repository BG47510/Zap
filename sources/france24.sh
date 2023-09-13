#!/bin/bash

echo $(dirname $0)

python3 -m pip install requests

cd $(dirname $0)/sources/

python3 france24.py > ./france24.m3u8

echo m3u grabbed
