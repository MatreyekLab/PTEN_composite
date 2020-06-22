import glob
import codecs
import sys
query_directory = "/Users/kmatreyek/Google_Drive/_Analysis_BLANK_SLATE_PTEN_FILLIN"  ### This should be whatever directory all of your fastq.gz files are in
query_files = glob.glob(query_directory + "/*.fastq.gz")

for x in range(0,len(query_files)):
	query_location = query_files[x]
	temp_name1 = query_files[x].split("/")[len(query_files[x].split("/"))-1]
	temp_name2 = temp_name1.split(".")[0]
	print(query_location)
	print(temp_name1)
	print(temp_name2)

	outfile_name = temp_name2 + ".json"
	outfile = codecs.open((query_directory + "/" + outfile_name), "w", "utf-8", "replace")
	outfile.write(
		"{" + "\n" +
		"  \"barcodes\": {}," + "\n" +
		"  \"fastq\": {" + "\n" +
		"    \"filters\": {" + "\n" +
		"      \"min quality\": 20" + "\n" +
		"    }," + "\n" +
		"    \"length\": 18," + "\n" +
		"    \"reads\": " + "\"" + temp_name1 + "\"" + ", " + "\n" +
		"    \"reverse\": false" + "\n" +
		"  },\n" + "\n" +
		"  \"name\": " + "\"" + temp_name2 + "\"" + ", " + "\n" +
		"  \"output directory\": \"Output\", " + "\n" +
		"  \"report filtered reads\": false, " + "\n" +
		"  \"timepoint\": 0 \n" + "\n" +
		"}")
	outfile.close()