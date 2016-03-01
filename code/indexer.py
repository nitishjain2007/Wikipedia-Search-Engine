#!/usr/bin/python
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import time
import pickle
from tokenise import tokenise
from merge import merge,sec_merge
import unicodedata
import sys
import re
import os
reload(sys)
sys.setdefaultencoding("utf-8")
dict_titles = dict()
dict_info_box = dict()
dict_text = dict()
dict_categories = dict()
dict_references = dict()
dict_external = dict()
extra = re.compile('[<>~!@#_$%?^&:;*\.,/()\"\[\]\|\+{}\=\-]')
extra_br = re.compile(r'<.*?>')
url_handler = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
current_dir = os.getcwd()
count = 0
filecount = 0
title_record = open(current_dir + "/title_record","w")

class wikiobject:
	def __init__(self):
		self.start = None
		self.end = None
		self.id = None
		self.title = None
		self.text = None
		self.info_box = ""
		self.tags = []
		self.categories = ""
		self.references = ""
		self.external_links = ""
		self.text_body = ""
		self.rest = ""

	def parse(self):
		info_case = 0
		lines = self.text.split("\n")
		info_flag = 0
		reference_flag = 0
		external_flag = 0
		in_func_flag = 0
		for line in lines:
			line = line.lower()
			if in_func_flag == 0:
				if line.startswith("{{infobox"):
					info_flag = info_flag + 1
					in_func_flag = in_func_flag + 1
					self.info_box = self.info_box + line + "\n"
				elif line.startswith("==references") or line.startswith("== references"):
					#print "hi"
					reference_flag = reference_flag + 1
					in_func_flag = in_func_flag + 1
				elif line.startswith("==external links") or line.startswith("== external links"):
					#print "hi"
					external_flag = external_flag + 1
					in_func_flag = in_func_flag + 1
				elif line.startswith("[[category"):
					self.categories = self.categories + line[11:-2] + "\n"
				else:
					self.rest = self.rest + line

			else:
				if info_flag > 0:
					self.info_box = self.info_box + line
					if line.startswith("}}"):
						self.info_box = self.info_box[:-1]
						info_flag = info_flag - 1
						in_func_flag = in_func_flag - 1

				elif reference_flag > 0:
					if line == "":
						self.references = self.references[:-1]
						reference_flag = 0
						in_func_flag = in_func_flag -1
					else:
						self.references = self.references + line + "\n"
						#print self.references

				elif external_flag > 0:
					if line == "":
						self.external_links = self.external_links[:-1]
						external_flag = 0
						in_func_flag = in_func_flag -1
					else:
						self.external_links = self.external_links + line + "\n"



class TestHandler(ContentHandler):
	global extra_br
	global extra
	global url_handler
	def __init__(self):
		ContentHandler.__init__(self)
		self.curr = None
		self.content = ""

	def startElement(self, name, attrs):
		self.tag = name
		if name == "page":
			self.curr = wikiobject()
			self.curr.start = self._locator.getLineNumber()
		if self.curr:
			self.curr.tags.append(name)

	def characters(self, content):
		to_add=unicodedata.normalize('NFKD', content).encode('ascii','ignore').strip()
		#to_add = content.encode("utf-8").strip()
		to_add = extra_br.sub("",to_add)
		self.content = self.content + to_add + "\n"

	def endElement(self, name):
		global dict_titles
		global dict_info_box
		global dict_text
		global dict_categories
		global dict_references
		global dict_external
		global filecount
		global count
		global title_record
		if self.curr:
			te = self.curr.tags.pop()
		if name == "id":
			if self.curr.tags[-1] == "page":
				self.curr.id = self.content[:-1].replace("\n","").strip()
		if name == "title":
			self.curr.title = self.content[:-1].replace("\n","")
		if name == "text":
			self.curr.text = self.content[:-1].replace("\n\n\n","!@#$%^&*()").replace("\n\n","\n").replace("!@#$%^&*()","\n\n")
		if name == "page":
			count=count+1
			title_record.write(self.curr.id + "=" + self.curr.title + "\n")
			self.curr.end = self._locator.getLineNumber()
			self.curr.parse()
			self.curr.categories = extra.sub(" ",self.curr.categories)
			self.curr.references = extra.sub(" ",self.curr.references)
			self.curr.title = extra.sub(" ",self.curr.title)
			self.curr.references = url_handler.sub(" ",self.curr.references)
			self.curr.info_box = extra.sub(" ",self.curr.info_box)
			self.curr.info_box = url_handler.sub(" ",self.curr.info_box)
			self.curr.external_links = extra.sub(" ",self.curr.external_links)
			self.curr.external_links = url_handler.sub(" ",self.curr.external_links)
			self.curr.rest = extra.sub(" ",self.curr.rest)
			self.curr.rest = url_handler.sub(" ",self.curr.rest)
			dict_titles = tokenise(self.curr.title,dict_titles,self.curr.id)
			dict_info_box = tokenise(self.curr.info_box,dict_info_box,self.curr.id)
			dict_text = tokenise(self.curr.rest,dict_text,self.curr.id)
			dict_categories = tokenise(self.curr.categories,dict_categories,self.curr.id)
			dict_references = tokenise(self.curr.references,dict_references,self.curr.id)
			dict_external = tokenise(self.curr.external_links,dict_external,self.curr.id)
			#print dict_info_box
			self.curr = None
			if count%1000==0:
				print count
				flush_files()
		self.content = ""

def flush_files():
	global filecount
	global current_dir
	global dict_titles
	global dict_info_box
	global dict_text
	global dict_categories
	global dict_references
	global dict_external
	f_title = open(current_dir + "/titles/file" + str(filecount),"w")
	for key in sorted(dict_titles.iterkeys()):
		f_title.write(key + "=" + dict_titles[key] + "\n")
	f_title.close()
	f_info_box = open(current_dir + "/info_box/file" + str(filecount), "w")
	for key in sorted(dict_info_box.iterkeys()):
		f_info_box.write(key + "=" + dict_info_box[key] + "\n")
	f_info_box.close()
	f_text = open(current_dir + "/text/file" + str(filecount), "w")
	for key in sorted(dict_text.iterkeys()):
		f_text.write(key + "=" + dict_text[key] + "\n")
	f_text.close()
	f_categories = open(current_dir + "/category/file" + str(filecount), "w")
	for key in sorted(dict_categories.iterkeys()):
		f_categories.write(key + "=" + dict_categories[key] + "\n")
	f_categories.close()
	f_references = open(current_dir + "/reference/file" + str(filecount), "w")
	for key in sorted(dict_references.iterkeys()):
		f_references.write(key + "=" + dict_references[key] + "\n")
	f_references.close()
	f_external = open(current_dir + "/external/file" + str(filecount), "w")
	for key in sorted(dict_external.iterkeys()):
		f_external.write(key + "=" + dict_external[key] + "\n")
	f_external.close()
	dict_titles.clear()
	dict_info_box.clear()
	dict_text.clear()
	dict_categories.clear()
	dict_references.clear()
	dict_external.clear()
	filecount = filecount + 1

def main(filename):
	parser = make_parser()
	handler = TestHandler()
	parser.setContentHandler(handler)
	parser.parse(filename)

if __name__ == "__main__":
	main("wiki-search-small.xml")
	flush_files()
	count1 = 0
	last = 0
	title_record.close()
	for i in range(0,filecount):
		if (i+1)%2 == 0:
			sec_merge(i-1,i+1,count)
			count1=count1+1
			last = i+1
	if last%2 != 0:
		sec_merge(last,i+1,count)
		count1=count1+1
	merge(count1,count)
	'''pickle.dump( dict_info_box, open( "dict_info_box.p", "wb" ) )
	pickle.dump( dict_titles, open( "dict_titles.p", "wb" ) )
	pickle.dump( dict_categories, open( "dict_categories.p", "wb" ))
	pickle.dump( dict_references, open("dict_references.p", "wb" ))
	pickle.dump( dict_external, open("dict_external.p", "wb" ))
	pickle.dump( dict_text, open("dict_text.p", "wb" ))'''