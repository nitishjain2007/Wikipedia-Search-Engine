#!/usr/bin/env python
import os
import pickle
import math

global total_f
def sortitems(reqstring):
	global total_f
	req_elements = reqstring.split("$$")
	to_sort1 = [req_elements[i].split("|")[0] for i in range(0,len(req_elements))]
	#print req_elements
	to_sort = [int(req_elements[i].split("|")[1]) for i in range(0,len(req_elements))]
	to_sort = [round(float(float(math.log(1+to_sort[i]))/float(math.log(10)))*float(float(math.log(total_f/len(to_sort)))/float(math.log(10))),4) for i in range(0,len(req_elements))]
	sorted_list = [i[0] for i in sorted(enumerate(to_sort), key=lambda x:x[1])]
	sorted_list.reverse()
	to_return = ""
	for i in sorted_list[:-1]:
		to_return = to_return + str(to_sort1[i]) + "|" + str(to_sort[i]) + "$$"
	to_return = to_return + str(to_sort1[sorted_list[-1]]) + "|" + str(to_sort[sorted_list[-1]])
	return to_return

def sortitems1(reqstring):
	req_elements = reqstring.split("$$")
	to_sort1 = [req_elements[i].split("|")[0] for i in range(0,len(req_elements))]
	to_sort = [int(req_elements[i].split("|")[1]) for i in range(0,len(req_elements))]
	sorted_list = [i[0] for i in sorted(enumerate(to_sort), key=lambda x:x[1])]
	sorted_list.reverse()
	to_return = ""
	for i in sorted_list[:-1]:
		to_return = to_return + str(to_sort1[i]) + "|" + str(to_sort[i]) + "$$"
	to_return = to_return + str(to_sort1[sorted_list[-1]]) + "|" + str(to_sort[sorted_list[-1]])
	return to_return

def sec_merge(start_file,end_file,total_count):
	global total_f
	total_f = total_count
	curr_dir = os.getcwd()
	titles = []
	info_box = []
	text = []
	category = []
	reference = []
	external = []
	for i in range(start_file,end_file):
		titles.append(open(curr_dir + "/titles/file" + str(i), "r+"))
		info_box.append(open(curr_dir + "/info_box/file" + str(i), "r+"))
		text.append(open(curr_dir + "/text/file" + str(i), "r+"))
		category.append(open(curr_dir + "/category/file" + str(i), "r+"))
		reference.append(open(curr_dir + "/reference/file" + str(i), "r+"))
		external.append(open(curr_dir + "/external/file" + str(i), "r+"))
	current = []
	current_mat = []
	to_remove1 = []
	for i in range(0,end_file-start_file):
		f = titles[i].readline()
		f = f.strip()
		f = f.split("=")
		try:
			current_mat.append(f[1])
			current.append(f[0])
		except IndexError:
			to_remove1.append(i)
	titles = [titles[i] for i in range(0,len(titles)) if i not in to_remove1]
	write_file = open(curr_dir + "/titles/title_file_temp" + str(start_file/2),"w")
	while(len(titles)):
		smallest_elements = [j for j in range(0,len(current)) if current[j] == min(current)]
		curr = ""
		for i in smallest_elements[:-1]:
			curr = curr + current_mat[i] + "$$"
		curr = curr + current_mat[smallest_elements[-1]]
		curr = sortitems1(curr)
		curr = current[smallest_elements[0]] + "=" + curr
		write_file.write(curr + "\n")
		to_remove = []
		for i in smallest_elements:
			line = titles[i].readline()
			if line=="":
				to_remove.append(i)
			else:
				line = line.strip()
				line = line.split("=")
				current[i] = line[0]
				current_mat[i] = line[1]
		titles = [titles[i] for i in range(0,len(titles)) if i not in to_remove]
		current = [current[i] for i in range(0,len(current)) if i not in to_remove]
		current_mat = [current_mat[i] for i in range(0,len(current_mat)) if i not in to_remove]
		
	write_file.close()
	current = []
	current_mat = []
	to_remove1 = []
	for i in range(0,end_file-start_file):
		f = info_box[i].readline()
		f = f.strip()
		f = f.split("=")
		try:
			current_mat.append(f[1])
			current.append(f[0])
		except IndexError:
			to_remove1.append(i)
	info_box = [info_box[i] for i in range(0,len(info_box)) if i not in to_remove1]

	write_file = open(curr_dir + "/info_box/info_box_file_temp" + str(start_file/2),"w")
	while(len(info_box)):
		smallest_elements = [j for j in range(0,len(current)) if current[j] == min(current)]
		curr = ""
		for i in smallest_elements[:-1]:
			curr = curr + current_mat[i] + "$$"
		curr = curr + current_mat[smallest_elements[-1]]
		curr = sortitems1(curr)
		curr = current[smallest_elements[0]] + "=" + curr
		write_file.write(curr + "\n")
		to_remove = []
		for i in smallest_elements:
			line = info_box[i].readline()
			if line=="":
				to_remove.append(i)
			else:
				line = line.strip()
				line = line.split("=")
				current[i] = line[0]
				current_mat[i] = line[1]
		info_box = [info_box[i] for i in range(0,len(info_box)) if i not in to_remove]
		current = [current[i] for i in range(0,len(current)) if i not in to_remove]
		current_mat = [current_mat[i] for i in range(0,len(current_mat)) if i not in to_remove]
		
	write_file.close()
	current = []
	current_mat = []
	to_remove1 = []
	for i in range(0,end_file-start_file):
		f = category[i].readline()
		f = f.strip()
		f = f.split("=")
		try:
			current_mat.append(f[1])
			current.append(f[0])
		except IndexError:
			to_remove1.append[i]
	category = [category[i] for i in range(0,len(category)) if i not in to_remove1]

	write_file = open(curr_dir + "/category/category_file_temp" + str(start_file/2),"w")
	while(len(category)):
		smallest_elements = [j for j in range(0,len(current)) if current[j] == min(current)]
		curr = ""
		for i in smallest_elements[:-1]:
			curr = curr + current_mat[i] + "$$"
		curr = curr + current_mat[smallest_elements[-1]]
		curr = sortitems1(curr)
		curr = current[smallest_elements[0]] + "=" + curr
		write_file.write(curr + "\n")
		to_remove = []
		for i in smallest_elements:
			line = category[i].readline()
			if line=="":
				to_remove.append(i)
			else:
				line = line.strip()
				line = line.split("=")
				current[i] = line[0]
				current_mat[i] = line[1]
		category = [category[i] for i in range(0,len(category)) if i not in to_remove]
		current = [current[i] for i in range(0,len(current)) if i not in to_remove]
		current_mat = [current_mat[i] for i in range(0,len(current_mat)) if i not in to_remove]
	write_file.close()
	current = []
	current_mat = []
	to_remove1 = []
	for i in range(0,end_file-start_file):
		f = text[i].readline()
		f = f.strip()
		f = f.split("=")
		try:
			current_mat.append(f[1])
			current.append(f[0])
		except IndexError:
			to_remove1.append(i)
	text = [text[i] for i in range(0,len(text)) if i not in to_remove1]

	write_file = open(curr_dir + "/text/text_file_temp" + str(start_file/2),"w")
	while(len(text)):
		smallest_elements = [j for j in range(0,len(current)) if current[j] == min(current)]
		curr = ""
		#print current_mat
		for i in smallest_elements[:-1]:
			curr = curr + current_mat[i] + "$$"
		curr = curr + current_mat[smallest_elements[-1]]
		curr = sortitems1(curr)
		curr = current[smallest_elements[0]] + "=" + curr
		write_file.write(curr + "\n")
		to_remove = []
		for i in smallest_elements:
			line = text[i].readline()
			if line=="":
				to_remove.append(i)
			else:
				line = line.strip()
				line = line.split("=")
				current[i] = line[0]
				current_mat[i] = line[1]
		#print to_remove
		#print len(text)
		text = [text[i] for i in range(0,len(text)) if i not in to_remove]
		current = [current[i] for i in range(0,len(current)) if i not in to_remove]
		current_mat = [current_mat[i] for i in range(0,len(current_mat)) if i not in to_remove]
	write_file.close()
	current = []
	current_mat = []
	to_remove1 = []
	for i in range(0,end_file-start_file):
		f = reference[i].readline()
		f = f.strip()
		f = f.split("=")
		try:
			current_mat.append(f[1])
			current.append(f[0])
		except IndexError:
			to_remove1.append(i)
	reference = [reference[i] for i in range(0,len(reference)) if i not in to_remove1]
	write_file = open(curr_dir + "/reference/reference_file_temp" + str(start_file/2),"w")
	while(len(reference)):
		smallest_elements = [j for j in range(0,len(current)) if current[j] == min(current)]
		curr = ""
		for i in smallest_elements[:-1]:
			curr = curr + current_mat[i] + "$$"
		curr = curr + current_mat[smallest_elements[-1]]
		curr = sortitems1(curr)
		curr = current[smallest_elements[0]] + "=" + curr
		write_file.write(curr + "\n")
		to_remove = []
		for i in smallest_elements:
			line = reference[i].readline()
			if line=="":
				to_remove.append(i)
			else:
				line = line.strip()
				line = line.split("=")
				current[i] = line[0]
				current_mat[i] = line[1]
		reference = [reference[i] for i in range(0,len(reference)) if i not in to_remove]
		current = [current[i] for i in range(0,len(current)) if i not in to_remove]
		current_mat = [current_mat[i] for i in range(0,len(current_mat)) if i not in to_remove]	
	write_file.close()
	current = []
	current_mat = []
	to_remove1 = []
	for i in range(0,end_file-start_file):
		f = external[i].readline()
		f = f.strip()
		f = f.split("=")
		try:
			current_mat.append(f[1])
			current.append(f[0])
		except IndexError:
			to_remove1.append(i)
	external = [external[i] for i in range(0,len(external)) if i not in to_remove1]
	write_file = open(curr_dir + "/external/external_file_temp" + str(start_file/2),"w")
	while(len(external)):
		smallest_elements = [j for j in range(0,len(current)) if current[j] == min(current)]
		curr = ""
		for i in smallest_elements[:-1]:
			curr = curr + current_mat[i] + "$$"
		curr = curr + current_mat[smallest_elements[-1]]
		curr = sortitems1(curr)
		curr = current[smallest_elements[0]] + "=" + curr
		write_file.write(curr + "\n")
		to_remove = []
		for i in smallest_elements:
			line = external[i].readline()
			if line=="":
				to_remove.append(i)
			else:
				line = line.strip()
				line = line.split("=")
				current[i] = line[0]
				current_mat[i] = line[1]
		external = [external[i] for i in range(0,len(external)) if i not in to_remove]
		current = [current[i] for i in range(0,len(current)) if i not in to_remove]
		current_mat = [current_mat[i] for i in range(0,len(current_mat)) if i not in to_remove]
	write_file.close()
	'''for i in range(start_file,end_file):
		os.remove(curr_dir + "/titles/file" + str(i))
		os.remove(curr_dir + "/info_box/file" + str(i))
		os.remove(curr_dir + "/text/file" + str(i))
		os.remove(curr_dir + "/category/file" + str(i))
		os.remove(curr_dir + "/reference/file" + str(i))
		os.remove(curr_dir + "/external/file" + str(i))'''

























































def merge(filecount,total_count):
	global total_f
	total_f = total_count
	curr_dir = os.getcwd()
	titles = []
	info_box = []
	text = []
	category = []
	reference = []
	external = []
	config_details = dict()
	for i in range(0,filecount):
		'''titles.append(open(curr_dir + "/titles/file" + str(i), "r+"))
		info_box.append(open(curr_dir + "/info_box/file" + str(i), "r+"))
		text.append(open(curr_dir + "/text/file" + str(i), "r+"))
		category.append(open(curr_dir + "/category/file" + str(i), "r+"))
		reference.append(open(curr_dir + "/reference/file" + str(i), "r+"))
		external.append(open(curr_dir + "/external/file" + str(i), "r+"))'''
		titles.append(open(curr_dir + "/titles/title_file_temp" + str(i), "r+"))
		info_box.append(open(curr_dir + "/info_box/info_box_file_temp" + str(i), "r+"))
		text.append(open(curr_dir + "/text/text_file_temp" + str(i), "r+"))
		category.append(open(curr_dir + "/category/category_file_temp" + str(i), "r+"))
		reference.append(open(curr_dir + "/reference/reference_file_temp" + str(i), "r+"))
		external.append(open(curr_dir + "/external/external_file_temp" + str(i), "r+"))
	current = []
	current_mat = []
	to_remove1 = []
	for i in range(0,filecount):
		f = titles[i].readline()
		f = f.strip()
		f = f.split("=")
		try:
			current_mat.append(f[1])
			current.append(f[0])
		except IndexError:
			to_remove1.append(i)
	titles = [titles[i] for i in range(0,len(titles)) if i not in to_remove1]

	write_file = open(curr_dir + "/title_file","w")
	write_file1 = open(curr_dir + "/title_file_sec","w")
	sec_count=0
	sec_count1=0
	while(len(titles)):
		smallest_elements = [j for j in range(0,len(current)) if current[j] == min(current)]
		curr = ""
		if min(current) == "abraham":
			print "hi"
			print smallest_elements
			print current
			print current_mat
		for i in smallest_elements[:-1]:
			curr = curr + current_mat[i] + "$$"
			if min(current) == "abraham":
				print curr
		curr = curr + current_mat[smallest_elements[-1]]
		if min(current) == "abraham":
			print curr
		curr = sortitems(curr)
		if min(current) == "abraham":
			print curr
		curr = current[smallest_elements[0]] + "=" + curr
		write_file.write(curr + "\n")
		if sec_count%1000==0:
			write_file1.write(current[smallest_elements[0]] + "\n")
			sec_count1=sec_count1+1
		sec_count = sec_count+1
		to_remove = []
		for i in smallest_elements:
			line = titles[i].readline()
			if line=="":
				to_remove.append(i)
			else:
				line = line.strip()
				line = line.split("=")
				current[i] = line[0]
				current_mat[i] = line[1]
		titles = [titles[i] for i in range(0,len(titles)) if i not in to_remove]
		current = [current[i] for i in range(0,len(current)) if i not in to_remove]
		current_mat = [current_mat[i] for i in range(0,len(current_mat)) if i not in to_remove]
		
	write_file.close()
	write_file1.close()
	config_details["title_file"] = sec_count
	config_details["title_file_sec"] = sec_count1
	current = []
	current_mat = []
	to_remove1 = []
	for i in range(0,filecount):
		f = info_box[i].readline()
		f = f.strip()
		f = f.split("=")
		try:
			current_mat.append(f[1])
			current.append(f[0])
		except IndexError:
			to_remove1.append(i)
	info_box = [info_box[i] for i in range(0,len(info_box)) if i not in to_remove1]

	write_file = open(curr_dir + "/info_box_file","w")
	write_file1 = open(curr_dir + "/info_box_file_sec","w")
	sec_count=0
	sec_count1=0
	while(len(info_box)):
		smallest_elements = [j for j in range(0,len(current)) if current[j] == min(current)]
		curr = ""
		for i in smallest_elements[:-1]:
			curr = curr + current_mat[i] + "$$"
		curr = curr + current_mat[smallest_elements[-1]]
		curr = sortitems(curr)
		curr = current[smallest_elements[0]] + "=" + curr
		write_file.write(curr + "\n")
		if sec_count%1000 == 0:
			write_file1.write(current[smallest_elements[0]] + "\n")
			sec_count1=sec_count1+1
		sec_count=sec_count+1
		to_remove = []
		for i in smallest_elements:
			line = info_box[i].readline()
			if line=="":
				to_remove.append(i)
			else:
				line = line.strip()
				line = line.split("=")
				current[i] = line[0]
				current_mat[i] = line[1]
		info_box = [info_box[i] for i in range(0,len(info_box)) if i not in to_remove]
		current = [current[i] for i in range(0,len(current)) if i not in to_remove]
		current_mat = [current_mat[i] for i in range(0,len(current_mat)) if i not in to_remove]
		
	write_file.close()
	write_file1.close()
	config_details["info_box_file"] = sec_count
	config_details["info_box_file_sec"] = sec_count1
	current = []
	current_mat = []
	to_remove1 = []
	for i in range(0,filecount):
		f = category[i].readline()
		f = f.strip()
		f = f.split("=")
		try:
			current_mat.append(f[1])
			current.append(f[0])
		except IndexError:
			to_remove1.append[i]
	category = [category[i] for i in range(0,len(category)) if i not in to_remove1]

	write_file = open(curr_dir + "/category_file","w")
	write_file1 = open(curr_dir + "/category_file_sec","w")
	sec_count=0
	sec_count1=0
	while(len(category)):
		smallest_elements = [j for j in range(0,len(current)) if current[j] == min(current)]
		curr = ""
		for i in smallest_elements[:-1]:
			curr = curr + current_mat[i] + "$$"
		curr = curr + current_mat[smallest_elements[-1]]
		curr = sortitems(curr)
		curr = current[smallest_elements[0]] + "=" + curr
		write_file.write(curr + "\n")
		if sec_count%1000 == 0:
			write_file1.write(current[smallest_elements[0]] + "\n")
			sec_count1=sec_count1+1
		sec_count=sec_count+1
		to_remove = []
		for i in smallest_elements:
			line = category[i].readline()
			if line=="":
				to_remove.append(i)
			else:
				line = line.strip()
				line = line.split("=")
				current[i] = line[0]
				current_mat[i] = line[1]
		category = [category[i] for i in range(0,len(category)) if i not in to_remove]
		current = [current[i] for i in range(0,len(current)) if i not in to_remove]
		current_mat = [current_mat[i] for i in range(0,len(current_mat)) if i not in to_remove]
	write_file1.close()
	write_file.close()
	config_details["category_file"] = sec_count
	config_details["category_file_sec"] = sec_count1
	current = []
	current_mat = []
	to_remove1 = []
	for i in range(0,filecount):
		f = text[i].readline()
		f = f.strip()
		f = f.split("=")
		try:
			current_mat.append(f[1])
			current.append(f[0])
		except IndexError:
			to_remove1.append(i)
	text = [text[i] for i in range(0,len(text)) if i not in to_remove1]

	write_file = open(curr_dir + "/text_file","w")
	write_file1 = open(curr_dir + "/text_file_sec","w")
	sec_count=0
	sec_count1=0
	while(len(text)):
		smallest_elements = [j for j in range(0,len(current)) if current[j] == min(current)]
		curr = ""
		#print current_mat
		for i in smallest_elements[:-1]:
			curr = curr + current_mat[i] + "$$"
		curr = curr + current_mat[smallest_elements[-1]]
		curr = sortitems(curr)
		curr = current[smallest_elements[0]] + "=" + curr
		write_file.write(curr + "\n")
		if sec_count%1000==0:
			write_file1.write(current[smallest_elements[0]]+"\n")
			sec_count1=sec_count1+1
		sec_count=sec_count+1
		to_remove = []
		for i in smallest_elements:
			line = text[i].readline()
			if line=="":
				to_remove.append(i)
			else:
				line = line.strip()
				line = line.split("=")
				current[i] = line[0]
				current_mat[i] = line[1]
		#print to_remove
		#print len(text)
		text = [text[i] for i in range(0,len(text)) if i not in to_remove]
		current = [current[i] for i in range(0,len(current)) if i not in to_remove]
		current_mat = [current_mat[i] for i in range(0,len(current_mat)) if i not in to_remove]
	write_file1.close()
	write_file.close()
	config_details["text_file"]=sec_count
	config_details["text_file_sec"]=sec_count1
	current = []
	current_mat = []
	to_remove1 = []
	for i in range(0,filecount):
		f = reference[i].readline()
		f = f.strip()
		f = f.split("=")
		try:
			current_mat.append(f[1])
			current.append(f[0])
		except IndexError:
			to_remove1.append(i)
	reference = [reference[i] for i in range(0,len(reference)) if i not in to_remove1]
	sec_count=0
	sec_count1=0
	write_file = open(curr_dir + "/reference_file","w")
	write_file1 = open(curr_dir + "/reference_file_sec","w")
	while(len(reference)):
		smallest_elements = [j for j in range(0,len(current)) if current[j] == min(current)]
		curr = ""
		for i in smallest_elements[:-1]:
			curr = curr + current_mat[i] + "$$"
		curr = curr + current_mat[smallest_elements[-1]]
		curr = sortitems(curr)
		curr = current[smallest_elements[0]] + "=" + curr
		write_file.write(curr + "\n")
		if sec_count%1000 == 0:
			write_file1.write(current[smallest_elements[0]] + "\n")
			sec_count1 = sec_count1+1
		sec_count=sec_count+1
		to_remove = []
		for i in smallest_elements:
			line = reference[i].readline()
			if line=="":
				to_remove.append(i)
			else:
				line = line.strip()
				line = line.split("=")
				current[i] = line[0]
				current_mat[i] = line[1]
		reference = [reference[i] for i in range(0,len(reference)) if i not in to_remove]
		current = [current[i] for i in range(0,len(current)) if i not in to_remove]
		current_mat = [current_mat[i] for i in range(0,len(current_mat)) if i not in to_remove]
	config_details["reference_file"]=sec_count
	config_details["reference_file_sec"]=sec_count1	
	write_file.close()
	write_file1.close()
	current = []
	current_mat = []
	to_remove1 = []
	for i in range(0,filecount):
		f = external[i].readline()
		f = f.strip()
		f = f.split("=")
		try:
			current_mat.append(f[1])
			current.append(f[0])
		except IndexError:
			to_remove1.append(i)
	external = [external[i] for i in range(0,len(external)) if i not in to_remove1]
	sec_count=0
	sec_count1=0
	write_file = open(curr_dir + "/external_file","w")
	write_file1 = open(curr_dir + "/external_file_sec","w")
	while(len(external)):
		smallest_elements = [j for j in range(0,len(current)) if current[j] == min(current)]
		curr = ""
		for i in smallest_elements[:-1]:
			curr = curr + current_mat[i] + "$$"
		curr = curr + current_mat[smallest_elements[-1]]
		curr = sortitems(curr)
		curr = current[smallest_elements[0]] + "=" + curr
		write_file.write(curr + "\n")
		if sec_count%1000==0:
			write_file1.write(current[smallest_elements[0]] + "\n")
			sec_count1=sec_count1+1
		sec_count=sec_count+1
		to_remove = []
		for i in smallest_elements:
			line = external[i].readline()
			if line=="":
				to_remove.append(i)
			else:
				line = line.strip()
				line = line.split("=")
				current[i] = line[0]
				current_mat[i] = line[1]
		external = [external[i] for i in range(0,len(external)) if i not in to_remove]
		current = [current[i] for i in range(0,len(current)) if i not in to_remove]
		current_mat = [current_mat[i] for i in range(0,len(current_mat)) if i not in to_remove]
	write_file1.close()
	write_file.close()
	config_details["external_file"]=sec_count
	config_details["external_file_sec"]=sec_count1
	'''for i in range(0,filecount):
		titles.append(open(curr_dir + "/titles/file" + str(i), "r+"))
		info_box.append(open(curr_dir + "/info_box/file" + str(i), "r+"))
		text.append(open(curr_dir + "/text/file" + str(i), "r+"))
		category.append(open(curr_dir + "/category/file" + str(i), "r+"))
		reference.append(open(curr_dir + "/reference/file" + str(i), "r+"))
		external.append(open(curr_dir + "/external/file" + str(i), "r+"))
		os.remove(curr_dir + "/titles/title_file_temp" + str(i))
		os.remove(curr_dir + "/info_box/info_box_file_temp" + str(i))
		os.remove(curr_dir + "/text/text_file_temp" + str(i))
		os.remove(curr_dir + "/category/category_file_temp" + str(i))
		os.remove(curr_dir + "/reference/reference_file_temp" + str(i))
		os.remove(curr_dir + "/external/external_file_temp" + str(i))'''

	pickle.dump( config_details, open( "config_details.p", "wb" ) )