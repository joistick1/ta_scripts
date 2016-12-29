#Script for gathering pages from yahooUK web site, based on urls (yahooUK_seed.csv), which has long and lat pairs and are covering area of UK for this paricular website

# Steps:
# 1. Qeury eah link from the web site
# 2. Identify the number of results on each page
# 3. Generating pages. based on results from step 2 

import json
import urllib
import re
import csv
import time # if you want to pause between queries

e = open('foursquare_errors.txt','w') #file for errors
link_list = list()
link_counter = 0 # information, which receives user while running a script
error_page = 0 
row_count = 1876 # number of rows from seed file (yahooUK_seed.csv) always constant
with open("foursquare_seed.csv", "r") as infile: # reading seed file
    reader = csv.reader(infile)
    
    for line_num, line in enumerate(reader):
        link_counter += 1 
        try:
            print "Processing link ", link_counter, " from ", row_count
            url = line[0]
            data = urllib.urlopen(url).read()
            info = json.loads(data)
            for i in range(0, len(info['response']['group']['results'])):
                if  'venue' in info['response']['group']['results'][i]:
                    link = info['response']['group']['results'][i]['venue']['canonicalUrl'];
                    if link not in link_list:
                        link_list.append(link)
            
                

        except Exception as errors:   # handling errors    
            print "Page ", link_counter, " didn't responded"
            link_counter += 1
            error_page += 1
            e.write(str(error_page)+". "+str(errors.message) + '\n')
            pass

with open('foursquare_urls.csv','wb') as f: # writing output file with generated pages  
    writer = csv.writer(f)          
    for idx in range(0, len(link_list)):
        writer.writerow([link_list[idx]])

print "Processed ", link_counter - error_page, " pages from ", row_count, " in total"
infile.close()
f.close()

#now you can open YahooUK_urls.csv with generated urls and use all these links for the extractor in dash - JustEat 1 - yahooUK(rest list) d9e6a730-4fd8-4ca5-abff-352ee03892cc

        
         


