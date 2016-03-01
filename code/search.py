#!/usr/bin/env python
import pickle
import linecache
import unicodedata
from nltk.stem import PorterStemmer
import sys
import re
import os
import operator
reload(sys)
sys.setdefaultencoding("utf-8")
config_details = pickle.load(open("config_details.p","rb"))
curr_dir = os.getcwd()
extra = re.compile('[<>~!@#_$%?^&:;*\.,/()\"\[\]\|\+{}\=\-]')
extra_br = re.compile(r'<.*?>')
stemmer=PorterStemmer()

def perform_search(text,typeq,typer,start,end):
	global config_details
	global curr_dir

	if typeq=="t":
		file_name = "title_file"
	elif typeq=="b":
		file_name = "text_file"
	elif typeq=="r":
		file_name = "reference_file"
	elif typeq=="e":
		file_name = "external_file"
	elif typeq=="c":
		file_name = "category_file"
	elif typeq=="i":
		file_name = "info_box_file"

	if typer=="s":
		file_name = file_name + "_sec"
		req_index = bsearch(file_name,text,0,config_details[file_name]-1,typer)
	else:
		if start==end:
			return linecache.getline(curr_dir + "/" + file_name,start+1).strip() 
		req_index = bsearch(file_name,text,start,min(end,config_details[file_name]-1),typer)
		if(req_index[1]==-1):
			return None
		else:
			return linecache.getline(file_name,req_index[0]+1).strip()
	if typer=="s":
		if req_index[1] == 0:
			return linecache.getline(file_name[:-4],req_index[0]*1000+1).strip()
		elif req_index[1] == 1:
			return perform_search(text,typeq,"p",(req_index[0]-1)*1000,(req_index[0])*1000-1)
		else:
			return perform_search(text,typeq,"p",(req_index[0])*1000,(req_index[0]+1)*1000-1)


def bsearch(filename,text,start,end,typer):
	global curr_dir
	mid = int((start+end)/2)
	line_req = linecache.getline(curr_dir + "/" + filename,mid+1).strip()
	if(typer=="p"):
		req_text = line_req.split("=")[0].strip()
	else:
		req_text = line_req.strip()
	if start >= end:
		if text == req_text:
			return [start,0]
		else:
			if typer == "p":
				return [start,-1]
			else:
				if text < req_text:
					return [start,1]
				else:
					return [start,2]
	else:
		if text == req_text:
			return [mid,0]
		elif text < req_text:
			return bsearch(filename,text,start,mid-1,typer)
		else:
			return bsearch(filename,text,mid+1,end,typer)



def handlegaps(textinput):
	pattern = re.compile(r"\s+")
	textinput = re.sub(pattern, " ", textinput)
	textinput = textinput.replace("  "," ")
	return textinput

def tokenise(text):
	global stemmer
	#text = unicodedata.normalize('NFKD', text).encode('ascii','ignore').strip()
	text = extra.sub("",text)
	text = handlegaps(text)
	texts = text.split(" ")
	for i in range(0,len(texts)):
		texts[i] = stemmer.stem(texts[i])
	return texts


def parse_query(text):
	query = text.split(":")
	query = [i.strip() for i in query]
	query_tags = []
	query_values = []
	query_new = []
	if len(query) > 1:
		i=0
		query_tags.append(query[0])
		for i in range(1,len(query)):
			if i!=len(query)-1:
				query_values.append(query[i][:-1].strip())
				query_tags.append(query[i][-1].strip())
			else:
				query_values.append(query[i].strip())
	else:
		query_tags.append("a")
		query_values = [query[0].strip()]
	return [query_tags, query_values]

def process_query(tags, values):
	doc_weights = dict()
	weights = {"t":10, "i":8, "b":6, "c": 5, "r": 4, "e":2}

	if len(tags) == 1 and tags[0] == "a":
		tags = ["t", "b", "r", "e", "i", "c"]
		values = values*6
	for i in range(0,len(tags)):
		temp = list(set(tokenise(values[i])))
		for j in range(0,len(temp)):
			a = perform_search(temp[j],tags[i],"s",0,0)
			if a != None:
				a = a.split("=")[1].strip()
				a = a.split("$$")
				for k in a[:30]:
					try:
						temp1 = doc_weights[k.split("|")[0]]
						doc_weights[k.split("|")[0]] = doc_weights[k.split("|")[0]] + weights[tags[i]] * float(k.split("|")[1])
					except KeyError:
						doc_weights[k.split("|")[0]] = weights[tags[i]] * float(k.split("|")[1])

	doc_weights = sorted(doc_weights.items(), key=operator.itemgetter(1))
	doc_weights.reverse()
	doc_weights=[i[0] for i in doc_weights]
	return doc_weights[:10]

def fbsearch(filename,text,start,end):
	global curr_dir
	mid = int((start+end)/2)
	line_req = linecache.getline(curr_dir + "/" + filename,mid+1).strip()
	req_text = line_req.split("=")[0].strip()
	if start >= end:
		if int(text) == int(req_text):
			return linecache.getline(curr_dir + "/" + filename,start+1).strip()
		else:
			print start
			return "2=0"
	else:
		if int(text) == int(req_text):
			return linecache.getline(curr_dir + "/" + filename,mid+1).strip()
		elif int(text) < int(req_text):
			return fbsearch(filename,text,start,mid-1)
		else:
			return fbsearch(filename,text,mid+1,end)

if __name__ == "__main__":
	query = raw_input()
	query_parts = parse_query(query)
	results = process_query(query_parts[0], query_parts[1])
	for i in results:
		print i, fbsearch("title_record",i,0,config_details["title_record"]-1).split("=")[1]

