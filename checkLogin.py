from BeautifulSoup import BeautifulSoup
import time
import mechanize

br = mechanize.Browser()
br.open("https://eksisozluk.com/giris")
print br.title()

br.select_form(nr=2)
br['UserName'] = ''
br['Password'] = ''
br.submit()
page = br.open('https://eksisozluk.com/chinaski--100859')

soup = BeautifulSoup(page)

for i in range(100):
            value = str(i+1)
            entry = soup.body.find('li', attrs = {'value': value})
            if entry:
                author = entry.find('footer')['data-author']
                print value
                print author
            else:
                break