# This script will take an XML file from a blastp run and parse it for relevant information


import codecs
import re
import sys

file_name = sys.argv[1]

accession = []
sciname = []
identity = []
align_length = []
qseq = []
hseq = []
midline = []
variant_number_list = []
variant_list = []
unique_list = []
right_region = 0
additional_marker = 0

with open(file_name, 'r') as datafile:
	for line in datafile:
		row = line.strip()
		if "</params>" in row:
			right_region = 1
		if right_region == 1:
			if "<accession>" in row:
				accession.append((row.split("<accession>")[1]).split("</accession>")[0])
			if "<sciname>" in row:
				sciname.append((row.split("<sciname>")[1]).split("</sciname>")[0])
				additional_marker = additional_marker + 1
			if "<identity>" in row:
				identity_temp = (row.split("<identity>")[1]).split("</identity>")[0]
				#identity.append(identity_temp)
			if "<align-len>" in row:
				align_length_temp = (row.split("<align-len>")[1]).split("</align-len>")[0]
				#align_length.append(align_length_temp)
			if "<qseq>" in row:
				qseq_temp = (row.split("<qseq>")[1]).split("</qseq>")[0]
				#qseq.append(qseq_temp)
			if "<hseq>" in row:
				hseq_temp = (row.split("<hseq>")[1]).split("</hseq>")[0]
				#hseq.append(hseq_temp)
			if "<midline>" in row:
				midline_temp = (row.split("<midline>")[1]).split("</midline>")[0]
				#midline.append(midline_temp)
				temp_variant_list = []
				position_counter = 0
				for x in range(0,len(qseq_temp)):
					if qseq_temp != "-":
						position_counter = position_counter + 1
					if midline_temp[x] in " +":
						position = str(position_counter)
						variant = (qseq_temp[x]+position+hseq_temp[x])
						temp_variant_list.append(variant)
				#variant_list.append(temp_variant_list)
				for x in range(0,additional_marker):
					identity.append(identity_temp)
					align_length.append(align_length_temp)
					qseq.append(qseq_temp)
					hseq.append(hseq_temp)
					midline.append(midline_temp)
					variant_number_list.append(len(temp_variant_list))
					variant_list.append(temp_variant_list)
					if x == 0:
						unique_list.append(1)
					else:
						unique_list.append(0)
				additional_marker = 0

outfilename = file_name[0:len(file_name)-4]+"_xml_blast_parsed_output.tsv"
outfile = codecs.open(outfilename, "w", "utf-8", "replace")
outfile.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format("accession","sciname","unique_list","identity","align_length","qseq","hseq","midline","variant_number","variant_list"))

print(len(identity))
print(len(align_length))
print(len(qseq))
print(len(hseq))
print(len(midline))
print(len(variant_list))
print(len(accession))
print(len(sciname))



for x in range(0,len(accession)):
	outfile.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(accession[x],sciname[x],unique_list[x],identity[x],align_length[x],qseq[x],hseq[x],midline[x],variant_number_list[x],variant_list[x]))
outfile.close()


		
			












'''
lastname = name.split("_")[0]
title_list = []
issn_list = []
journal_list = []
year_list = []
author_placement_list = []
author_total_list = []
first_list = []
second_list = []
third_list = []

toggle = 1
author_toggle = 1

#with open('Bruchez_A.txt', 'r') as datafile:
with open(name+'.txt', 'r') as datafile:
	for line in datafile:
		row = line.strip()
		## Figure out article title name
		if row[0:14] == "<ArticleTitle>":
			title_list.append(row[14:].split("</ArticleTitle>")[0])
		## This is figuring out ISSN and this is figuring out the publication year
		if row[0:14] == "<ISSN IssnType":
			issn_list.append((row.split(">")[1]).split("</ISSN>")[0][0:9])
			toggle = 0 ## To now get journal stuff
		if toggle == 0:
			if row.split(">")[0] == "<Year":
				year1 = (row.split(">")[1]).split("</Year")[0]
				year_list.append(year1)
				toggle = 1
        ## This is figuring out the journal
		journal1 = row.split(">")[0]
        #print(row)
		if journal1 == "<ISOAbbreviation":
			journal2 = (row.split("<ISOAbbreviation>")[1]).split("</ISOAbbreviation>")[0]
        	#print(row2)
			journal_list.append(journal2)
			author_toggle = 0
			temp_author_list = []
		## This is figuring out author order
		if author_toggle == 0:
			if row[0:10] == "<LastName>":
				temp_author_list.append(row[10:].split("</LastName>")[0])
		if row == "</AuthorList>":
			if lastname in temp_author_list:
				#print(temp_author_list.index(lastname))
				author_placement_list.append(str(temp_author_list.index(lastname) + 1))
				author_total_list.append(len(temp_author_list))
				if temp_author_list.index(lastname) == 0:
					first_list.append("yes")
				else:
					first_list.append("no")
				if temp_author_list.index(lastname) == 1:
					second_list.append("yes")
				else:
					second_list.append("no")
				if temp_author_list.index(lastname) == 2:
					third_list.append("yes")
				else:
					third_list.append("no")
				author_toggle = 1
			else:
				author_placement_list.append(len(temp_author_list))
				author_total_list.append(len(temp_author_list))
				first_list.append("no")
				second_list.append("no")
				third_list.append("no")

outfilename = name+"_output.tsv"
outfile = codecs.open(outfilename, "w", "utf-8", "replace")
outfile.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format("author","title","issn","journal","year","author_placement","author_total","first","second","third"))

print(len(title_list))
print(len(journal_list))
print(len(year_list))
print(len(author_placement_list))
print(len(author_total_list))
print(len(first_list))
print(len(second_list))
print(len(third_list))

print(title_list)
print(journal_list)
print(year_list)
print(author_placement_list)
print(author_total_list)
print(first_list)
print(second_list)
print(third_list)


for x in range(0,len(journal_list)):
	outfile.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(name,title_list[x],issn_list[x],journal_list[x],year_list[x],author_placement_list[x],author_total_list[x],first_list[x],second_list[x],third_list[x]))




#print(journal_list)
#print(year_list)
#print(temp_author_list)
'''