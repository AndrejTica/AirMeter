#!/bin/bash
#/home/pi/AirMeter/airMeter.sh
#dieses script wird EINMALIG beim systemstart gestartet und läuft endlos
#
#60s schlafen wegen zeitaktualisierung beim systemstart
sleep 60s
#
LOG_FILE="/home/pi/AirMeter/airMeter.log"
echo -n `date +"%Y.%m.%d;%T;"` >> $LOG_FILE
echo $SHELL >> $LOG_FILE
#
echo -n `date +"%Y.%m.%d;%T;"` >> $LOG_FILE
echo "/home/pi/AirMeter/airMeter.sh started" >> $LOG_FILE
#
#falls python abstürzt, wird es wieder gestartet
SCRIPT_FILE="/home/pi/AirMeter/02-airMeter.py"
STOP_FILE="/home/pi/AirMeter/stop"
STOP_FILE_="/home/pi/AirMeter/stop_"
while [ ! -f $STOP_FILE ];
do
    echo -n `date +"%Y.%m.%d;%T;"` >> $LOG_FILE
    echo "python3 $SCRIPT_FILE" >> $LOG_FILE
    python3 $SCRIPT_FILE
done
#
# da sollte das programm nur beim regulären Beenden hinkommen!
if [ -f $STOP_FILE ]; then
    mv $STOP_FILE $STOP_FILE_
fi
echo -n `date +"%Y.%m.%d;%T;"` >> $LOG_FILE
echo "/home/pi/Myon_detection/myon_detection.sh ended" >> $LOG_FILE
#