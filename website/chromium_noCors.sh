
#!/bin/bash

cd 
mkdir -p cors
name=$(whoami)
chromium --user-data-dir=/home/name/cors --disable-web-security --disable-site-isolation-trials


exit
