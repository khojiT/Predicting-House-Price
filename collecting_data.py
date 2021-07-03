#It's khoji <a.khoji2001@gmail.com>
# * in this code means that you should put your individual information

#pip install requests,mysqlconnector,bs4
import requests
import mysql.connector
from bs4 import BeautifulSoup
import re
from numpy import array_split
import mysql.connector
#first you should create a database(for example in MYSQL) then create a table that you will write data in it. 

#after running this code you will have some data in your table, save that data to checking new data is same or not.
def show_table( table_name):
    cnx = mysql.connector.connect(user='root', password='1234',
                                  host='127.0.0.1',
                                  database='*home')
    cur = cnx.cursor()
    cur.execute(f"select * from {table_name};")
    res = cur.fetchall()
    l = []
    for item in res:
        item = str(item)
        item = item.replace('(\'','')
        item = item.replace('\',)','')
        l = l +[item]
    return (l)
    cnx.commit()
    cnx.close()

l_org = show_table('*homis')
#converting from string to separated list in main list
l_t =[]
for item in l_org:
    item = item.replace('(','')
    item = item.replace(')', '')
    item = list(item.split(','))
    l_t += [[int(item[0]),int(item[2]),float(item[3]),int(item[4]),int(item[5])]]
#In Tehran we have 22 residential area so: range(1,23)
#res in this part is the max number of homes in one residential area
count =[]
for i in range(1,23):
    url=f'https://ihome.ir/sell-residential-apartment/th-tehran/district{i}'
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'html.parser')
    res = soup.find('*span',{'class':'*filters__count'})
    count += [(int(res.text)//30)+1]
l=[]
l1 =[]
l3 = []
l_nei = []

for i in range(1,23):
    for c in range(1,(count[i-1])+1):
        url = f'https://ihome.ir/sell-residential-apartment/th-tehran/district{i}?locations=iran.th.tehran.district{i}&property_type=residential-apartment&paginate=30&page={c}&is_sale=1&source=website'
        site = requests.get(url)
        soup = BeautifulSoup(site.text,'html.parser')
        #go to site and [ctrl + shift + I] then select 
        #neighborhood
        r = soup.find_all('*span',{'class':"*sub-title"})
        for item in r:
            item = item.text.strip()
            item = item.replace('*تهران - ' , '')
            l += [item]
            l_nei += [i]

        #price
        r2 = soup.find_all('*div',{'class':'*sell-value'})
        for item in r2:
            item = item.text.strip()
            item = item.replace('*  تومان' , '')
            item = item.replace('* میلیارد','b')
            item = item.replace('* و ','')
            item = item.replace('* میلیون', 'm')
            item = item.replace('* هزار','k')
            try:
                b = float(''.join(re.findall(r'(\d+)b',item)))* 1000000000
            except:
                b = 0
            try:
                m = float(''.join(re.findall(r'(\d+)m',item))) * 1000000
            except:
                m = 0
            try:
                k = float(re.findall('(\d+)k',item))*1000
            except:
                k = 0
            l1 += [int(b+m+k)]

        #House Area , Year Built , Bedrooms
        r3 =soup.find_all('*span',{'class':'*property-detail__icons-item__value'})
        for item in r3:
            item =item.text.strip()
            if item == '*نوساز':
                item = 0
            l3 += [float(item)]
l3_final = array_split(l3,len(l3)/3)
l_meter = []
l_room = []
l_time = []
for i in range(int(len(l3)/3)):
    l_meter += [l3_final[i][0]]
    l_room += [l3_final[i][1]]
    l_time += [l3_final[i][2]]
print(len(l_meter))
#connect to database
cnx = mysql.connector.connect(user='root', password='1234',
                                  host='127.0.0.1',
                                  database='*home')
cur = cnx.cursor()
#avoid repetition
for i in range(len(l)):
    if not [l_nei[i],l[i],l1[i],l_meter[i],l_room[i],l_time[i]] in l_t:
        cur.execute(f"INSERT INTO *homis (*man,*nei,*price,*met,*room,*time) VALUES('{l_nei[i]}','{l[i]}','{l1[i]}','{l_meter[i]}','{l_room[i]}','{l_time[i]}');")
cnx.commit()
cnx.close()
