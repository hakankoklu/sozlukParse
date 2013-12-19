import urllib2
from BeautifulSoup import BeautifulSoup
from datetime import datetime
import time
import sys
import Queue
import threading


author_base_url = 'https://eksisozluk.com/biri/'

def get_number_of_pages(author):

    entry_list_url = author_base_url + author + '/son-entryleri?p=1'
    page = urllib2.urlopen(entry_list_url)
    soup = BeautifulSoup(page)

    x = soup.body.find('div', attrs={'class' : 'pager'})['data-pagecount']

    print x
    return int(x)

def author_name_dash(author):
    author_words = author.split(' ')
    author_new = '-'.join(author_words)
    if len(author_words) > 1:
        author = author_new
    return author

def get_entry_count_random_date(author, year1, month1, day1, year2, month2, day2):
    year2, month2, day2 = correct_to_date(year2, month2, day2)
    url_part1 = 'https://eksisozluk.com/ara?searchform.keywords=&searchform.author='
    url_part2 = '&searchform.when.from='+str(year1)+'-'+str(month1)+'-'+str(day1)+'&searchform.when.to='
    url_part3 = str(year2)+'-'+str(month2)+'-'+str(day2)+'&searchform.sortorder=date'
    author_words = author.split(' ')
    author_new = '%20'.join(author_words)
    if len(author_words) > 1:
        author = author_new
    search_url = url_part1 + author + url_part2 + url_part3
    page = urllib2.urlopen(search_url)
    soup = BeautifulSoup(page)

    x = soup.body.find('p', attrs={'class' : 'topic-list-description'}).text
    words = x.split(' ')
    title = words[2]
    no_results = int(title[1:len(x)-1])
    return no_results


def correct_to_date(year, month, day):
    today = datetime.now()
    cYear = int(today.strftime('%Y'))
    cMonth = int(today.strftime('%m'))
    cDay = int(today.strftime('%d'))
    if year > cYear:
        year = cYear
        month = cMonth
        day = cDay
    elif year == cYear and month > cMonth:
        month = cMonth
        day = cDay
    elif year == cYear and month == cMonth and day > cDay:
        day = cDay
    return [year, month, day]


def get_entry_count_for_year(author,year):
    no_results = get_entry_count_random_date(author, year, 1, 1, year, 12, 31)
    if not no_results == 1000:
        print 'not so hard'
        return no_results
    
    no_results_half1 = get_entry_count_random_date(author, year, 1, 1, year, 6, 30)
    no_results_half2 = get_entry_count_random_date(author, year, 7, 1, year, 12, 31)
    if not (no_results_half1 == 1000 or no_results_half2 == 1000):
        print 'kind of hard'
        no_results = no_results_half1 + no_results_half2
        return no_results
    
    if no_results_half1 == 1000:
        no_results_q1 = get_entry_count_random_date(author, year, 1, 1, year, 3, 31)
        no_results_q2 = get_entry_count_random_date(author, year, 4, 1, year, 6, 30)
    else:
        no_results_q1, no_results_q2 = no_results_half1, 0
    
    if no_results_half2 == 1000:
        no_results_q3 = get_entry_count_random_date(author, year, 7, 1, year, 9, 30)
        no_results_q4 = get_entry_count_random_date(author, year, 10, 1, year, 12, 31)
    else:
        no_results_q3, no_results_q4 = no_results_half2, 0
    if not (no_results_q3 == 1000 or no_results_q4 == 1000 or no_results_q1 == 1000 or no_results_q2 == 1000):
        print 'pretty hard'
        no_results = no_results_q1 + no_results_q2 + no_results_q3 + no_results_q4
        return no_results
    no_results_arr = []
    no_results_arr.append(get_entry_count_random_date(author, year, 1, 1, year, 1, 31))
    no_results_arr.append(get_entry_count_random_date(author, year, 2, 1, year, 2, 28))
    for mo in range(3,13):
        no_results_arr.append(get_entry_count_random_date(author, year, mo, 1, year, mo, 30))
    no_results = sum(no_results_arr)
    print str(no_results_arr)
    print 'really hard'
    return no_results


def get_entry_count_for_year_per_month(author, year):
    def get_entry_counts(author, month, q):
        days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        day = days_in_month[month-1]
        no_results = get_entry_count_random_date(author, year, month, 1, year, month, day)
        q.put([month, no_results])

    q = Queue.Queue()
    thread_list = []
    months = range(1,13)
    for m in months:
        t = threading.Thread(target=get_entry_counts, args = (author, m, q))
        thread_list.append(t)

    for t in thread_list:
        t.start()

    for t in thread_list:
        t.join()
    result = []
    while not q.empty():
        result.append(q.get())
    result_sorted = range(1,13)
    for res in result:
        result_sorted[res[0]-1] = res[1]
    return result_sorted, sum(result_sorted)

def get_entry_count_all_per_month(author):
    def get_entry_counts(author, month, year, q):
        days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        day = days_in_month[month-1]
        no_results = get_entry_count_random_date(author, year, month, 1, year, month, day)
        q.put([year, month, no_results])

    cYear = int(datetime.now().strftime('%Y'))
    q = Queue.Queue()
    thread_list = []
    months = range(1,13)
    years = range(1999, cYear + 1)
    for y in years:
        for m in months:
            t = threading.Thread(target=get_entry_counts, args = (author, m, y, q))
            thread_list.append(t)

    for t in thread_list:
        t.start()

    for t in thread_list:
        t.join()
    result = []
    while not q.empty():
        result.append(q.get())
    result_year_sorted = [[] for x in range(15)]
    result_sorted = [range(12) for x in range(15)]
    for res in result:
        result_year_sorted[res[0]-1999].append(res[1:])
    for res in range(len(result_year_sorted)):
        for r in result_year_sorted[res]:
            result_sorted[res][r[0]-1] = r[1]
    return result_sorted


def get_entry_count_all_years(author):
    cYear = int(datetime.now().strftime('%Y'))
    entry_count = []
    for year in range(1999,cYear+1):
        entry_count.append(get_entry_count_for_year(author,year))
    return entry_count

def get_entry_count_all_years_per_month(author):
    cYear = int(datetime.now().strftime('%Y'))
    entry_count = []
    for year in range(1999,cYear+1):
        entry_count.append(get_entry_count_for_year_per_month(author,year)[0])
    return entry_count

def get_karma(author):
    author = author_name_dash(author)
    url_author = 'https://eksisozluk.com/biri/%s' % author
    page = urllib2.urlopen(url_author)
    soup = BeautifulSoup(page)

    x = soup.body.find('h1', attrs={'id' : 'user-profile-title'}).small.text
    xx = x.split(' ')
    karma_desc = ' '.join(xx[:len(xx)-12])
    karma = int(xx[len(xx)-1].strip('()'))
    return karma, karma_desc

def get_page_count_of_author_page(author):
    author = author_name_dash(author)
    url_page = 'https://eksisozluk.com/%s' % author
    page = urllib2.urlopen(url_page)
    soup = BeautifulSoup(page)

    x = soup.body.find('div', attrs = {'class': 'pager'})['data-pagecount']
    return int(x)

def get_authors_from_page(author):
    author = author_name_dash(author)
    page_count = get_page_count_of_author_page(author)
    print page_count
    url_page = 'https://eksisozluk.com/%s' % author
    page = urllib2.urlopen(url_page)
    soup = BeautifulSoup(page)

    url_page = soup.head.find('meta', attrs = {'property': 'og:url'})['content']
    print url_page
    authors = {}
    for p in range(page_count):
        new_url_page = url_page + '?p=%s' % str(p+1)
        print new_url_page
        page = urllib2.urlopen(new_url_page)
        soup = BeautifulSoup(page)
        #Not finished, looping over all the pages.
        for i in range(10):
            value = str(p*10+i+1)
            print value
            entry = soup.body.find('li', attrs = {'value': value})
            if entry:
                author = entry.find('footer')['data-author']
                if authors.get(author):
                    authors[author] += 1
                else:
                    authors[author] = 1
            else:
                break
    return authors

if __name__ == "__main__":
    author = sys.argv[1]
    #year = sys.argv[2]
    st_time = time.time()
    a = get_authors_from_page(author)
    #a = get_entry_count_random_date('madonnanin yagli zencisi 2',2013,12,1,2013,12,16)
    #a = get_entry_count_all_per_month(author)
    #a = get_entry_count_all_years_per_month(author)
    print a
    print str(time.time()-st_time)
    #print str(sum(a))