from bs4 import BeautifulSoup
import requests
import re
import warnings
from datetime import datetime
import sys
import time
from threading import Thread
import random
warnings.filterwarnings("ignore")

limit=100

class mailScraper (Thread):
	def __init__(self, url,rex_string,headers):
		Thread.__init__(self)
		self.url= url
		self.rex_string = rex_string
		self.headers = headers
	def run(self):
		#print ("Thread '" + self.url + "' avviato")
		tmp_dict=[]
		res_dict={}
		try:
			#print(self.url)
			resp = requests.get(self.url, headers=self.headers,verify=False,timeout=10)
			if resp.status_code == 200:
				tmp_dict=re.findall("([a-zA-Z0-9_.+-]+"+self.rex_string+")", resp.text)
				if len(tmp_dict)>0:
					print("\n___________________________________________________________________________")
					print("site: "+self.url)
					
					res_dict[self.url]=set(tmp_dict)
					for item in res_dict[self.url]:
						print ("\t - "+item)
		except Exception as e:
			print("[thread exception]\n"+str(e))
		return 0
		#print ("Thread '" + self.url + "' terminato")



def dinoprint():
	print(" ")
	print("                                              ████████      ")
	print("   █████      █████  █████  █    █            ███▄███████   ")
	print("   █          █   █  █       █  █             ███████████   ")
	print("   █ ███  ██  █████  ████     ██              ██████        ")
	print("   █   █      █  █   █       █  █             █████████     ")
	print("   █████      █   █  █████  █    █  █       ███████         ")
	print("                                    ██     ████████████     ")
	print("                                    ███   ██████████  █     ")
	print("                                     ███ ███████████        ")
	print("                                      ███████████████       ")
	print("                                       █████████████        ")
	print("                                        ███████████         ")
	print("                                         ███  ██            ")
	print("                                         █    █             ")
	print("                                         ██   ██            ")
	print("                                                            ")

def getLinks(page):
	soup = BeautifulSoup(page.content)
	#print(soup)
	links = soup.findAll("a")
	res=[]
	for link in  soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
		for el in re.split(":(?=http)",link["href"].replace("/url?q=","")):
			#print (el)
			el2=el.split("&sa")[0]
			if len(el2)>0:
				res.append(el2)
			else:
				append(el)
	return res


def main():
	dinoprint()
	search_string=sys.argv[1]
	rex_string=search_string.replace(".","\.").strip()
	query = "allintext:"+search_string
	query = query.replace(' ', '+')
	
	now=datetime.now()
	print ("["+str(now)+"] - Searching for '"+search_string+"' ...")
	i=0
	while i<=limit:
		page=int(i/10)+1
		print("\n\t\t\t\t\t[ Scanning Page "+str(page)+"/10 ]")
		current_page = requests.get("https://www.google.com/search?q="+query+"&start="+str(i))
		gsearch=getLinks(current_page)
		#search_string="@email.it"

		# desktop user-agent
		USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
		# mobile user-agent
		MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"

		headers = {"user-agent" : USER_AGENT}
		res_dict={}
		
		jobs = []
		for el in gsearch:
			out_list = list()
			thread = mailScraper(el, rex_string, headers)
			jobs.append(thread)
			thread.start()


		# Ensure all of the threads have finished
		for j in jobs:
			j.join()

		i+=10
		time.sleep(3)

main()
