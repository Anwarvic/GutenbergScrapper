import requests
import multiprocessing as mp
from time import strftime, gmtime
from bs4 import BeautifulSoup, SoupStrainer




class Scraper():
	"""
	This Scraper should scrape the whole website (56,920) in less than 5 hours
	"""
	def __init__(self):
		#the file where data will be saved
		running_date = strftime("%B%Y", gmtime()) #date at which this script was run (April2018)
		self.filename = 'gutenberg{}.txt'.format(running_date)
		#the book attributes we want to get
		self.INCLUDE = set(['Title', 'Author', 'EBook-No.', 'Language'])
		#the book no. at which we want to start scraping
		self.START = 1
		#the book no. at which we want to end scraping
		self.END = 56920 #no. of books till April 2018
		#number of processes to run concurrently
		self.proc = 7
		"""
		NOTE:
		=====
		This scraper is a multi-threading scraping. One of the most important thing to 
		know about it is that the no. of processes is the perfect number for our case
		and these are the time taken to parse 50 pages in respect of different processes number:
		No. Processes: 2 ---> Time: 53.88681674003601
		No. Processes: 3 ---> Time: 32.92372012138367
		No. Processes: 4 ---> Time: 23.577651977539062
		No. Processes: 5 ---> Time: 22.71523427963257
		No. Processes: 6 ---> Time: 23.9236478805542
		No. Processes: 7 ---> Time: 17.64547371864319
		No. Processes: 8 ---> Time: 20.18887066841125
		No. Processes: 9 ---> Time: 20.49740481376648
		No. Processes: 10---> Time: 18.402575254440308

		7.. I think it's a magical number after all
		If the scraper was blocked a few times in a row, reduce the number to 5

		"""


	def scrape_page(self, _id):
		"""
		Takes book id
		Return a list of all wanted attribues (INCLUDE) and their values
		"""
		url = "http://www.gutenberg.org/ebooks/"
		#Will try a few times to request the page
		GOT = False
		while(not GOT):
			try:
				page = requests.get(url + str(_id), timeout=5) #5 seconds
				GOT = True
			except:
				print("Trying one more time ...")
				page = requests.get(url + str(_id), timeout=5)
				if page.status_code == 200:
					GOT = True

		#parse only the 'bibrec tables', that's why I've used SoupStrainer
		table = BeautifulSoup(page.content, 'lxml', \
								parse_only= SoupStrainer('table', {'class': 'bibrec'}))

		if table == None:
			print('Book no. {} not found'.format(_id))
		else:
			book = []
			#find all rows
			table_rows = table.find_all("tr")
			for tr in table_rows:
				key = tr.find('th').get_text()
				if key in self.INCLUDE:
					value = tr.find('td').get_text()
					value = value.replace('\n', ' ')
					if key == 'EBook-No.':
						book.insert(0, 'ID: {}'.format(value)) #put ID first
					else:
						book.append( '{}: {}'.format(key.strip(), value.strip()) )
		print(book)
		if book:
			return book
		else:
			return ['ID: {}'.format(_id)]


	def scrape(self, start, end):
		"""
		Takes two arguments (start) and (end)
		Uses Multi-threading to scrape the whole website starting with (start) and ending at (end)
		Returns a list of lists, each list represents a book info.
		"""
		# Setup a list of processes
		pool = mp.Pool(processes= self.proc)
		results = [pool.apply_async(self.scrape_page, args= (x,)) for x in range(start, end)]
		output = [res.get() for res in results]
		#to close the processes
		pool.close()
		pool.join()
		return output


	def save(self, size=56):
		"""
		Takes a size as an argument which is the number of pages after which the output is saved
		 (default: 56 pages)
		It runs the 'scrape' method and saves the list in the filename
		Returns nothin'
		"""
		for i in range(self.START, self.END+1, size):
			if i+size > self.END:
				output = self.scrape(i, self.END+1)
			else:	
				output = self.scrape(i, i+size)
			if output:
				#sort the output based on the id
				output = sorted(output, key=lambda x: x[0])
				#saves the output
				with open(self.filename, 'a') as fout:
					for book in output:
						if book:
							fout.write('\n'.join(book))
							fout.write('\n\n')




if __name__ == "__main__":
	sc = Scraper()
	# -------------------- THIS PART TO GET THE LAST 'ID' FROM THE DATA FILE --------------------
	# import subprocess
	# few_lines = subprocess.run(['tail', '-10', sc.filename], stdout=subprocess.PIPE).stdout
	# few_lines = few_lines.decode('utf-8').split('\n')

	# for i in range(len(few_lines)-1, 0, -1):
	# 	line = few_lines[i].strip()
	# 	if line and 'ID' in line:
	# 		_, idx = line.split(' ')
	# print(idx)
	# sc.START = int(idx)+1
	#------------------------------------------------------------------------------------------
	sc.save()
	
