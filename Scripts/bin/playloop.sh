#This script is to play music from a directory one after the another

for file in $1/*
do
 while pgrep omxplayer > /dev/null; do sleep 1; done
 #Calling the play.sh script with a music file
 ./play.sh $file
done
