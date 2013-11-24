import urllib2
from BeautifulSoup import BeautifulSoup

author_base_url = 'https://eksisozluk.com/biri/'

def get_number_of_pages(author):

    entry_list_url = author_base_url + author + '/son-entryleri?p=1'
    page = urllib2.urlopen(entry_list_url)
    soup = BeautifulSoup(page)

    x = soup.body.find('div', attrs={'class' : 'pager'})['data-pagecount']

    print x
    return int(x)

def get_entry_number_for_year(author,year):
    url_part1 = 'https://eksisozluk.com/ara?searchform.keywords=&searchform.author='
    url_part2 = '&searchform.when.from='
    url_part3 = '-01-01&searchform.when.to='
    url_part4 = '-12-31&searchform.sortorder=date'
    if year == 2013:
        url_part4 = '-11-22&searchform.sortorder=date'
    search_url = url_part1 + author + url_part2 + str(year) + url_part3 + str(year) + url_part4
    page = urllib2.urlopen(search_url)
    soup = BeautifulSoup(page)

    x = soup.body.find('p', attrs={'class' : 'topic-list-description'}).text
    words = x.split(' ')
    title = words[2]
    no_results = int(title[1:len(x)-1])
    print str(no_results)
    return no_results
if __name__ == "__main__":
    get_entry_number_for_year('chinaski',2000)
