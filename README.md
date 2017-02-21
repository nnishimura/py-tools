# python program README

This is a collection directory of python program.  
You may find some of them useful.


## Sorting.py

Example script for sorting files in directories.  
Sorting rules can be customized by tweaking codes.

## delete-facebook-cache.py

Original program at https://github.com/jshaw/fb-cache-flush/    
Same usage, only updated for the current API system (2017).  
Sending POST request to Graph API to force scrape new og information.

### Usage
1. Generate sitemap at http://www.xml-sitemaps.com/ or create sitemap.xml by yourself
2. Place the sitemap on ./sitemaps/sitemap.xml
3. (If necessary) ```pip install json```
4. get your access token on https://developers.facebook.com/tools/explorer/ and insert it to this script
5. Place the script on your current directory and run ```python delete-facebook-cache.py```

## resize_psd.py

Save psd as jpg with resizing function.

### Usage
1. mkdir ./psd & ./jpg
2. run ```python resize_psd.py```



