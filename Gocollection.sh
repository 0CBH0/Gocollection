#!/bin/bash
cd ~/work/Gocollection/
wget http://geneontology.org/gene-associations/goa_human.gaf.gz
gzip -df goa_human.gaf.gz
rm -f Gocollection.log
rm -f goTerms.db
cp -f goTerms_ori.db goTerms.db
nohup scrapy crawl basic > run.log 2>&1 &
