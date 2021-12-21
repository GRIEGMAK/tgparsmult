import os, sys
file = sys.argv[1]
file_results = sys.argv[2]
if not os.path.exists(file):
    file_name = open(file, "w")
    file_name.close()
file_name_search = open(file_results, "a")
f = open(file)
for line in f:
    if line[0] != ',':
        file_name_search.write(line)
f.close()