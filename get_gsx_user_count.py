import os
import random
import requests
from SequenceNumber import SequenceNumber

from bs4 import BeautifulSoup
from datetime import datetime


headers = {
    'user-agent': 'Mozilla/5.0',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
}
fname = 'gsx_user_count.txt'

incremental = [100, 400, 1000, 5000, 10000, 50000, 10000000]

sn = SequenceNumber()

def is_user_id_real(id, doPrint=True):
    a = sn.encode_user_number(id)
    url = 'https://m.genshuixue.com/x/'+str(a)
    if doPrint:
        print('Checking id ', id, ' -> encoded url', url)
    response = requests.get(url, headers=headers)
    s = BeautifulSoup(response.content, features="html.parser")
    e = s.select('span.item-info')
    if e[0].string != '****':
        print('\t\t\t\t\t^^^ Above is a fake profile just created \n')
        return True
    else:
        return False


def cond(m):
    return is_user_id_real(m)


def binary(a, b):
    if a < b - 1 :    
        m = int((a + b)/2)
        return True, m
    return False, None


def search(a, b):
    s = a
    e = b
    m = int((s + e) / 2)
    print("\tSearching fake profiles between [", s, "  and  ", e, "]\n")

    more = True
    while more:
        if cond(m):
            s = m
        else:
            e = m
        more, m = binary(s, e)
    return s

def get_last_id():
    if not os.path.exists(fname):
        return 33129013
    with open(fname, "r") as f:
        last_id = f.readlines()[-1]
        return int(last_id.split()[0])

def update_last_id():
    last_id = get_last_id()
    # Skip to a future number that is large enough
    further = last_id + 10000 + random.randint(1, 40)
    i = 0
    while is_user_id_real(further, doPrint=False):
        further += incremental[i] + random.randint(1, 20)
        i += 1
    last_user_id = search(last_id, further)
    
    now = datetime.now()
    print("At " + now.strftime("%m/%d %H:%M:%S") + " there are " + str(last_user_id) + " users in GSX.  " + str (last_user_id - last_id) + " new users created since last run.")
    with open(fname, "a+") as f:
        f.write(str(last_user_id) +  '\t' +  str(now) + '\n')

    for i in range(1, 20):
        future_id = last_user_id + 10 + i
        url_not_exist = 'https://m.genshuixue.com/x/'+str(sn.encode_user_number(future_id))
        print("User id " + str(future_id) + "-> encoded url " + url_not_exist + " is expect to be created in the next few minutes.")

if __name__ == "__main__":
    print("""
    This program uses binary search to locate the last user id on genshuixue.com.
    It probes a range of user ids and their encoded profile URLs.
    
    It will print out a list of fake profiles as it is probing.

    At the end, it will print out a list of profile URLs that is expected to create.

    You can catch the fraud in real time.
    """)
    update_last_id()