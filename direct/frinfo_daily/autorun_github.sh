#!/bin/bash

python3 direct/frinfo_daily/dailymotion_m3ugrabber.py > direct/frinfo_daily/dailymotion-US.m3u

exit 0
#echo $(dirname $0)
#cd $(dirname $0)/direct/frinfo_daily/
#python3 dailymotion_m3ugrabber.py > dailymotion-US.m3u

#echo m3u grabbed
