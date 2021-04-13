import time

from Pinterest import Pinterest

with open('links.txt', 'r') as f:
    links = f.read().strip().split('\n')

pinterest = Pinterest(linux=True)
login = pinterest.login()
time.sleep(2)
# print('login', login)
if login:
    for link in links:
        try:
            pinterest.get_pin_info_by_short_link(link)
        except Exception as e:
            print(e)
