import authorParse
import time
import pickle
import urllib2

st_time = time.time()
p_pro = pickle.HIGHEST_PROTOCOL
ffile = open('author_list_updated6','r')
all_authors = pickle.load(ffile)
ffile.close()
#screened_authors = all_authors[0:1084]
a = authorParse.get_authors_from_page_with_mechanize('lost')
new_authors = a.keys()
for aa in new_authors:
    if not aa in all_authors:
        all_authors.append(aa)

a_file = open('author_list_updated7','w')
pickle.dump(all_authors, a_file, p_pro)
a_file.close()
time_past = time.time()-st_time
print 'Has been running for: %s seconds' % str(time_past)
