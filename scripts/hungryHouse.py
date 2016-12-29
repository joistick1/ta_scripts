import urllib2
import re
import csv

urls = ['https://hungryhouse.co.uk/sitemap-postcodes-al.xml' , 'https://hungryhouse.co.uk/sitemap-postcodes-mz.xml']

""" function for converting values to proper format of body of POST request"""

def generate_body(data):
	gen_body = ''
	body_arr = []
	ids = data[0].split(',')
	res_num = len(ids)
	if res_num < 30:
		for i in range(0, len(ids)):
			gen_body += 'r%5B%5D=' + ids[i] + '&';
		return gen_body
	else:
		for i in range(0, len(ids)):
			gen_body += 'r%5B%5D=' + ids[i] + '&';
			if (i + 1) % 30 == 0:
				gen_body += 'rr=' + str(i + 1)
				body_arr.append(gen_body)
				gen_body = ''
		return body_arr

with open('hungryHouse_links.csv', 'wb') as outfile:
	writer = csv.writer(outfile)
	writer.writerow(['link'])
	""" gather links from sitemap.xml"""
	for i in urls:
		url = i
		htmlfile = urllib2.urlopen(url)
		htmltext = htmlfile.read()
		regex = '<loc>(.+?)</loc>'
		pattern = re.compile(regex)
		link = re.findall(pattern,htmltext)
		for idx in link:
			writer.writerow([idx])

""" reading links from sitemap.xml """

with open('hungryHouse_links.csv', 'r') as infile:
	with open('hungryHouse_pages.csv', 'wb') as outfile:
		reader = csv.reader(infile)
		writer = csv.writer(outfile)
		writer.writerow(['link'])
		for line_num, line in enumerate(reader):
			if line_num == 0:
				continue 
			else:
				print 'request num - ', line_num
				print 'requesting - ', line[0], '...'	
				url = urllib2.Request(line[0])

				""" read dynamic cookies and set them to header """

				response_headers = htmlfile.info()
				for info in response_headers:
					if info.find('set-cookie') > -1:
						cookies = response_headers[info]

				url.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36')
				url.add_header('Cookie', cookies)
				url.add_header('X-NewRelic-ID','UwIBU1dXGwcJUFJWAAk=')
				url.add_header('X-Requested-With','XMLHttpRequest')
				htmlfile = urllib2.urlopen(url)
				htmltext = htmlfile.read()
				
				ids = ' id=\"rids\" value=\"(.+?)\"\/>'
				pattern = re.compile(ids)
				query_param = re.findall(pattern,htmltext)
				if len(query_param) == 0:
					continue
				proper_body = generate_body(query_param)

				""" generate url with formatted body value """

				if isinstance(proper_body, list):
					body_array = proper_body
					for k in range(0, len(body_array)):
						link = line[0] + '#[!opt!]{"body":"'+body_array[k]+'","headers":{"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8","X-NewRelic-ID":"UwIBU1dXGwcJUFJWAAk=","X-Requested-With":"XMLHttpRequest"}}[/!opt!]'		
						writer.writerow([link])
				else:
					link = line[0] + '#[!opt!]{"body":"'+proper_body+'","headers":{"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8","X-NewRelic-ID":"UwIBU1dXGwcJUFJWAAk=","X-Requested-With":"XMLHttpRequest"}}[/!opt!]'
					writer.writerow([link])

