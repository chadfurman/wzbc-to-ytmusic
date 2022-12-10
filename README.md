
Basically you need to follow the instructions [here](https://ytmusicapi.readthedocs.io/en/stable/setup.html#copy-authentication-headers)  to copy your authentication headers from ytmusic to a file called "headers_raw", then you need to put the wzbc playlist url in the "start_urls" array at the start of the file

you also need to use python3 and pip install:
pip install scrapy
pip install ytmusicapi

from there, if you just run the script:
python w2y.py

it will make a playlist in ytmusic for you.

Should work for any spintronic site.  If it stops working lmk I'll update it.