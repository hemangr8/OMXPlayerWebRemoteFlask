#This script is to start an OMXPlayer instance in the PIPE with a music file sent as an argument from the playloop.sh script

omxplayer $* < ~/bin/omfifo &
#To synchronise the playspeed of the running OMXPlayer instance
./dspeed.sh &
./ispeed.sh &
echo -n . > ~/bin/omfifo
