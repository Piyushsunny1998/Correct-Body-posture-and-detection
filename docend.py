import numpy as np
n=np.load('doctor.npy')
print(n[0])
print(n[1])
print(n[2])
print(n[3])
print(n[4])
print(n[5])

import sqlite3

conn=sqlite3.connect(':memory:')

c=conn.cursor()

c.execute("""CREATE TABLE doctor(
            Head_to_Right_leg integer,
            Head_to_Right_leg1 integer,
            Head_to_Rigth_Arm integer,
            Head_to_Rigth_Arm1 integer,
            Head_to_both_shoulder integer,
            Head_to_both_shoulder1 integer)""")


c.execute("INSERT INTO doctor VALUES (:Head_to_Right_leg, :Head_to_Right_leg1, :Head_to_Rigth_Arm, :Head_to_Rigth_Arm1, :Head_to_both_shoulder, :Head_to_both_shoulder1)",
          {'Head_to_Right_leg':n[0] ,'Head_to_Right_leg1':n[1],'Head_to_Rigth_Arm':n[2], 'Head_to_Rigth_Arm1':n[3] ,'Head_to_both_shoulder':n[4],'Head_to_both_shoulder1':n[5]})





c.execute("""SELECT Head_to_Right_leg,Head_to_Right_leg1,Head_to_Rigth_Arm,Head_to_Rigth_Arm1,Head_to_both_shoulder,Head_to_both_shoulder1 FROM doctor""")
p=c.fetchone()
l=list(p)
ar=np.array([l[0],l[1],l[2],l[3],l[4],l[5]])
np.save('arm.npy',ar)       
           
conn.close()
