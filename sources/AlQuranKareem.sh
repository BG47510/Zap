#!/bin/bash

echo $(dirname $0)

python3 -m pip install requests

cd $(dirname $0)/sources/

python3 AlQuranKareem.py > AlQuranKareem.m3u8

echo m3u grabbed
