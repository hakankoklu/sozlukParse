import authorParse
import pickle

p_pro = pickle.HIGHEST_PROTOCOL
ffile = open('author_list_3640','r')
all_authors = pickle.load(ffile)
ffile.close()
#screened_authors = all_authors[0:1084]

ffile = open('author_baslik_4096','r')
new_authors = pickle.load(ffile)
ffile.close()

for aa in new_authors:
    if not aa in all_authors:
    	all_authors.append(aa)

a_file = open('author_list_with_baslik','w')
pickle.dump(all_authors, a_file, p_pro)
a_file.close()