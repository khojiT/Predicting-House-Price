#It's khoji <a.khoji2001@gmail.com>
# * in this code means that you should put your individual information

#pip install mysql.connector,scikit-learn
import mysql.connector

#extract data from database
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
#convert data from string to separated list in one main list
l_t =[]
for item in l_org:
    item = item.replace('(', '')
    item = item.replace(')', '')
    item = list(item.split(','))
    l_t += [[int(item[0]), int(item[2]), float(item[3]), int(item[4]), int(item[5])]]
#input list
l_in = []
for item in l_t:
    l_in += [[item[0],item[2],item[3],item[4]]]
#output list
l_out =[]
for item in l_t:
    l_out += [item[1]]
#linear regression
from sklearn import linear_model
regr = linear_model.LinearRegression()
regr.fit(l_in, l_out)
#Enter your input data for predicting
z = ([[*1,*300,*0,*4]])
print(regr.predict(z))
