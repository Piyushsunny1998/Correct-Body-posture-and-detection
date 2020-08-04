import numpy as np
n=np.load('loginend.npy')
print(n[0])
print(n[1])
k=0
username="piyush"
password="dubey"

import sqlite3

conn=sqlite3.connect(':memory:')

c=conn.cursor()

c.execute("""CREATE TABLE login(
            name string,
            password string)""")


c.execute("INSERT INTO login values(:name,:password)",{'name':n[0],'password':n[1]})



c.execute("""SELECT name,password from login""")
p=c.fetchone()
l=list(p)
if(l[0]==username and l[1]==password):
    k=1
    arr=np.array([k])
    np.save('logins.npy',arr)
else:
    k=0
    arr=np.array([k])
    np.save('logins.npy',arr)
     
