from BeautifulSoup import BeautifulSoup
import time
import mechanize
import cookielib

br = mechanize.Browser()
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_robots(False)
#br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
br.addheaders = [('User-agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36')]

page = br.open("http://www.eksistats.com/index.php?page=tek&nick=blindman&sd=15&sm=2&sy=1999&ed=22&em=12&ey=2013&listele=Listele")
print br.title()
soup = BeautifulSoup(page)
graph_div = soup.body.contents[34]#find_all('div')
script_soup = BeautifulSoup(str(graph_div))
main_script = script_soup.div.contents
main_script_soup = BeautifulSoup(str(main_script[7]))
entry_count_txt = main_script_soup.text
entry_count_txt = str(entry_count_txt)
value_start = entry_count_txt.find('"values":') + 10
value_end = entry_count_txt.find(']',value_start + 10)
values = entry_count_txt[value_start:value_end + 1]
label_start = entry_count_txt.find('"labels":') + 28
label_end = entry_count_txt.find(']', label_start + 10)
labels = entry_count_txt[label_start:label_end + 1]
#print values
ffile = open('eksiStatsValues.txt','w')
ffile.write(values)
ffile.close()
ffile = open('eksiStatsLabels.txt','w')
ffile.write(labels)
ffile.close()