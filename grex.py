from bs4 import BeautifulSoup
import requests
import re
import warnings
from datetime import datetime
import sys
import time
import concurrent.futures
import random
from termcolor import colored
import argparse
warnings.filterwarnings("ignore")


def dinoprint():
	print(" ")
	print(colored("                                              ████████      ",'yellow'))
	print(colored("   █████      █████  █████  █    █            ███▄███████   ",'yellow'))
	print(colored("   █          █   █  █       █  █             ███████████   ",'yellow'))
	print(colored("   █ ███  ██  █████  ████     ██              ██████        ",'yellow'))
	print(colored("   █   █      █  █   █       █  █             █████████     ",'yellow'))
	print(colored("   █████      █   █  █████  █    █  █       ███████         ",'yellow'))
	print(colored("                                    ██     ████████████     ",'yellow'))
	print(colored("                                    ███   ██████████  █     ",'yellow'))
	print(colored("                                      ██████████████        ",'yellow'))
	print(colored("                                       █████████████        ",'yellow'))
	print(colored("                                        ███████████         ",'yellow'))
	print(colored("                                         ███  ██            ",'yellow'))
	print(colored("                                         █    █             ",'yellow'))
	print(colored("                                         ██   ██            ",'yellow'))
	print(colored("                                                            ",'yellow'))

def mailScraper(url,rex_string,headers):
	extraction={}
	try:
		resp = requests.get(url, headers=headers,verify=False,timeout=3)
		if resp.status_code == 200:
			extraction=re.findall("([a-zA-Z0-9_.+-]+"+rex_string+")", resp.text)
			#print(url)
	except Exception as e:
		pass
		#print("[thread exception]\n"+str(e))
	res=[url,list(set(extraction))]
	return res

def getLinks(page):
	soup = BeautifulSoup(page.content)
	#print(soup)
	links = soup.findAll("a")
	res=[]
	for link in  soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
		for el in re.split(":(?=http)",link["href"].replace("/url?q=","")):
			el2=el.split("&sa")[0]
			if len(el2)>0:
				res.append(el2)
			else:
				append(el)
	#print(res)
	return res

def main():
	parser = argparse.ArgumentParser(
	prog='grex.py',
	formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument("domain")
	parser.add_argument("pages" , help="number of pages to scrape")
	args=parser.parse_args()
	dinoprint()
	domain=args.domain
	pages=int(args.pages)
	limit=pages*10
	search_string="@"+domain
	doc_title=search_string.replace(".","_")+".csv"
	rex_string=search_string.replace(".","\.").strip()
	query = "allintext:"+search_string
	query = query.replace(' ', '+')
	res_dict={}
	now=datetime.now()
	results=[]
	print ("["+str(now)+"] - Search started for domain "+colored(domain,'green')+"\n\n")
	i=0
	while i<limit:
		page=int(i/10)+1
		print(".....................................................Scanning Page "+str(page)+" of "+str(int(pages)),end='\r')
		current_page = requests.get("https://www.google.com/search?q="+query+"&start="+str(i))
		links=getLinks(current_page)
		for el in links:
			results.append(el)
		i+=10
		time.sleep(3)

	print("\n\n....................................................."+str(len(results))+" Results found\n")
	#for el in results:	
	# desktop user-agent
	USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
	# mobile user-agent
	MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"

	headers = {"user-agent" : USER_AGENT}

	for el in results:
		print(colored(el,'cyan'))
		
	with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:	
		future_to_mail_scrape = {executor.submit(mailScraper, el, rex_string, headers): el for el in results}
		for future in concurrent.futures.as_completed(future_to_mail_scrape):
			mail_scrape=future_to_mail_scrape[future]
			try:
				return_value = future.result()
				if return_value[0] not in res_dict:
					res_dict[return_value[0]]=return_value[1]
			except:
				pass
			
	print("\n.....................................................Mail found:\n")
	for el in res_dict:
		for mail in res_dict[el]:
			print(colored(mail,'red')+", "+colored(el,'cyan'))	
	
main()
