#Script for gathering pages from yahooUK web site, based on urls (yahooUK_seed.csv), which has long and lat pairs and are covering area of UK for this paricular website

# Steps:
# 1. Qeury eah link from the web site
# 2. Identify the number of results on each page
# 3. Generating pages. based on results from step 2 

import json
import urllib
import re
import csv
import math
import time # if you want to pause between queries

e = open('YahooUk_errors.txt','w') #file for errors
link_counter = 0 # information, which receives user while running a script
error_page = 0 
row_count = 1876 # number of rows from seed file (yahooUK_seed.csv) always constant
with open("yahooUK_seed.csv", "r") as infile: # reading seed file
    with open('YahooUK_urls.csv','wb') as f: # writing output file with generated pages
        reader = csv.reader(infile)
        writer = csv.writer(f)

        for line_num, line in enumerate(reader): 
            try:
                link_counter += 1
                print "Processing link ", link_counter, " from ", row_count
                url = line[0]
                htmlfile = urllib.urlopen(url)
                htmltext = htmlfile.read()

                match = re.search(r'(\d+) results', htmltext)
                results = match.group(1)
                offset = int(math.floor(int(results)/15) * 15) # pagination has structure: link + '&offset=' + (0, 15, 30, 45 etc)
               
                for idx in range(0, offset):
                  if((idx == 0 or idx%15 == 0) and idx <= 990): # if offset > 990 - websites returns no data, idx has values from 0 to 975 with step 15
                    
                    final_url = url + '&offset=' + str(idx);
                    writer.writerow([final_url])
                    

            except Exception as errors:   # handling errors    
                print "Page ", link_counter, " didn't responded"
                link_counter += 1
                error_page += 1
                e.write(str(error_page)+". "+str(errors.message) + '\n')
                pass

print "Processed ", link_counter - error_page, " pages from ", row_count, " in total"
infile.close()
f.close()

#now you can open YahooUK_urls.csv with generated urls and use all these links for the extractor in dash - JustEat 1 - yahooUK(rest list) d9e6a730-4fd8-4ca5-abff-352ee03892cc

        
         


