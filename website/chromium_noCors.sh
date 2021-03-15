
#!/bin/bash

cd 
mkdir -p cors
name=$(whoami)
chromium-browser --user-data-dir=/home/name/cors --disable-web-security --disable-site-isolation-trials /home/name/Airmeter/website/index.html

exit
