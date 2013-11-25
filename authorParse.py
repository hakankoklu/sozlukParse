import urllib2
from BeautifulSoup import BeautifulSoup
from datetime import datetime

author_base_url = 'https://eksisozluk.com/biri/'

def get_number_of_pages(author):

    entry_list_url = author_base_url + author + '/son-entryleri?p=1'
    page = urllib2.urlopen(entry_list_url)
    soup = BeautifulSoup(page)

    x = soup.body.find('div', attrs={'class' : 'pager'})['data-pagecount']

    print x
    return int(x)

def get_entry_count_random_date(author, year1, month1, day1, year2, month2, day2):
    year2, month2, day2 = correct_to_date(year2, month2, day2)
    url_part1 = 'https://eksisozluk.com/ara?searchform.keywords=&searchform.author='
    url_part2 = '&searchform.when.from='+str(year1)+'-'+str(month1)+'-'+str(day1)+'&searchform.when.to='
    url_part3 = str(year2)+'-'+str(month2)+'-'+str(day2)+'&searchform.sortorder=date'
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
    date = str(today).split(' ')[0]
    dateBroken = date.split('-')
    cYear = int(dateBroken[0])
    cMonth = int(dateBroken[1])
    cDay = int(dateBroken[2])
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
    
if __name__ == "__main__":
    a = get_entry_count_for_year('chinaski',2002)
    print str(a)
