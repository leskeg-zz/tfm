# IT Master Thesis

Project name: 
"Web Crawling and data analysis with Python"

Description:
This project extract data from a turistic webpage using Scrapy. Output are 2 files: 'result.json' and 'region.json'. Then files are imported to MongoDB database called 'tfm'. Finally different gramatical analysis and clustering are made.


Technologies:
- Scrapy Framework
- MongoDB
- Scikit-Learn

Dependencies:
- python-virtualenv
- mongodb 
- mongodb-tools 
- robomongo
- lapack 
- blas 
- gcc-fortran

Setup:
- virtualenv -p /usr/bin/python2.7 env
- source env/bin/activate
- pip install -r req.txt
- In python console: import nltk; nltk.download('stopwords'); nltk.download('punkt')

Deployment:

cd groupon_parser

rm result.json; scrapy crawl grouponScrapy -o result.json -t json

rm region.json; scrapy crawl grouponRegionScrapy -o region.json -t json


Import Result to db:

mongoimport --db tfm --collection result --type json --file result.json --jsonArray --upsertFields url

python update_regions_db.py result.json


Analysis:
- cd ../clustering/
- python clus.py

Results are showed in console and clustering.html is created.
