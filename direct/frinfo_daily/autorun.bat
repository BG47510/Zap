@echo off

echo Creating your playlist...
cd direct/frinfo_daily
python dailymotion_m3ugrabber.py > dailymotion.m3u

pause
