import qisge
import numpy as np

from qiskit import QuantumCircuit, QuantumRegister, transpile, IBMQ
import math, random, time
from qiskit.test.mock import FakeSantiago


# load images
images = qisge.ImageList([
    'background.png',
    'cmap1.png',
    'cmap2.png',
    'cmgame1.png',
    'A.png',
    'B.png',
    'C.png',
    'D.png',
    'E.png',
    'HA.png',
    'HB.png',
    'HC.png',
    'HD.png',
    'HE.png',
    'reset.png'
    ])

#setting background
#bg=qisge.Sprite(0,x=14,y=8,z=0,size=30)
choosetext=qisge.Text('Choose a Coupling Map to continue', width=8, height=2, x=10, y=10, font_size=20, font=2)
algotext=qisge.Text('List of operations: A-B, A-C, D-E, A-E', width=0, height=3, x=11, y=12, font_size=20, font=2)
congratstext=qisge.Text('Congratulations! You did a perfect mapping!!', width=0, height=5, x=10,y=10, font_size=30,font=2)
tryagaintext=qisge.Text('Oops! Click play to try again',width=0, height=5, x=10,y=10, font_size=30,font=2)
cmap1=qisge.Sprite(1,x=8,y=5,z=1,size=4)
cmap2=qisge.Sprite(2,x=18,y=5,z=1,size=4)
cmgame1=qisge.Sprite(3,x=14,y=10,z=1,size=0)
a=qisge.Sprite(4,x=9.5,y=7,z=2,size=0)
b=qisge.Sprite(5,x=11.5,y=7,z=2,size=0)
c=qisge.Sprite(6,x=13.5,y=7,z=2,size=0)
d=qisge.Sprite(7,x=15.5,y=7,z=2,size=0)
e=qisge.Sprite(8,x=17.5,y=7,z=2,size=0)
reset=qisge.Sprite(14,x=14,y=3,z=1,size=0)
pressed=0
select=0
pos=0
qr=QuantumRegister(5)
qc=QuantumCircuit(qr)
qc.cx(qr[0],qr[1])
qc.cx(qr[0],qr[2])
qc.cx(qr[3],qr[4])
qc.cx(qr[0],qr[4])
Ar=[a.x,b.x,c.x,d.x,e.x]
dict={1: 9.5, 2: 11.5, 3: 13.5, 4: 15.5, 5: 17.5}
layout={}
layout2=[]
result=0




def next_frame(input):
    global pressed,select,pos,dict,layout,Ar,layout2,result
    if pressed==0: 
        for entry in input['clicks']: #selection
            if entry['X']>=7 and entry['X']<=13 and entry['Y']>=4 and entry['Y']<=10:
                pressed=1
            if entry['X']>=17 and entry['X']<=23 and entry['Y']>=4 and entry['Y']<=10:
                pressed=2

    if pressed==1: #cmap1
        choosetext.width=0
        algotext.width=6
        cmgame1.size=10
        a.size=1
        b.size=1
        c.size=1
        d.size=1
        e.size=1
        reset.size=3
        cmap1.size=0
        cmap2.size=0
        if select==0:
            for entry in input['clicks']:
                if entry['X']>=9 and entry['X']<=10 and entry['Y']>=6.5 and entry['Y']<=7.5: #whenclickedA
                    a.image_id=9
                    select=1
                if entry['X']>=11 and entry['X']<=12 and entry['Y']>=6.5 and entry['Y']<=7.5: #whenclickedB
                    b.image_id=10
                    select=2
                if entry['X']>=13 and entry['X']<=14 and entry['Y']>=6.5 and entry['Y']<=7.5: #whenclickedC
                    c.image_id=11
                    select=3                    
                if entry['X']>=15 and entry['X']<=16 and entry['Y']>=6.5 and entry['Y']<=7.5: #whenclickedD
                    d.image_id=12
                    select=4                    
                if entry['X']>=17 and entry['X']<=18 and entry['Y']>=6.5 and entry['Y']<=7.5: #whenclickedE
                    e.image_id=13
                    select=5
                    
        if select:
            for entry in input['clicks']:
                if entry['X']>=9 and entry['X']<=10 and entry['Y']>=9.5 and entry['Y']<=10.5:
                    pos=1
                if entry['X']>=11 and entry['X']<=12 and entry['Y']>=9.5 and entry['Y']<=10.5: 
                    pos=2
                if entry['X']>=13 and entry['X']<=14 and entry['Y']>=9.5 and entry['Y']<=10.5: 
                    pos=3
                if entry['X']>=15 and entry['X']<=16 and entry['Y']>=9.5 and entry['Y']<=10.5: 
                    pos=4
                if entry['X']>=17 and entry['X']<=18 and entry['Y']>=9.5 and entry['Y']<=10.5: 
                    pos=5  
            
        if pos!=0:    
            if select==1:
                a.x=dict[pos]
                a.y=10
                a.image_id=4
                select=0
                pos=0
            if select==2:
                b.x=dict[pos]
                b.y=10
                b.image_id=5
                select=0
                pos=0
            if select==3:
                c.x=dict[pos]
                c.y=10
                c.image_id=6
                select=0
                pos=0
            if select==4:
                d.x=dict[pos]
                d.y=10
                d.image_id=7
                select=0
                pos=0
            if select==5:
                e.x=dict[pos]
                e.y=10
                e.image_id=8
                select=0
                pos=0
        for entry in input['clicks']:
            if entry['X']>=12 and entry['X']<=15.5 and entry['Y']>=2 and entry['Y']<=4:
                select=0
                pos=0
                a.x=9.5
                a.y=7
                b.x=11.5
                b.y=7
                c.x=13.5
                c.y=7
                d.x=15.5
                d.y=7
                e.x=17.5
                e.y=7
        if 4 in input['key_presses']:
            layout=np.argsort(Ar)
            #provider = IBMQ.load_account()
            #backend= IBMQ.load_account().get_backend('ibmq_santiago')
            #backend=FakeSantiago
            for i in layout:
               layout2.append(qr[i])
            qc_transpile=transpile(qc,coupling_map=[[0,1],[1,2],[2,3],[3,4]],initial_layout= layout2,optimization_level=0)
            if qc_transpile.count_ops().get('swap')==2:
                result=1
            if qc_transpile.count_ops().get('swap')>2:
                result=2
            if result==1:
                algotext.width=0
                cmgame1.size=0
                a.size=0
                b.size=0
                c.size=0
                d.size=0
                e.size=0
                reset.size=0
                congratstext.width=10
            elif result==2:
                algotext.width=0
                cmgame1.size=0
                a.size=0
                b.size=0
                c.size=0
                d.size=0
                e.size=0
                reset.size=0
                tryagaintext.width=10


            





    if pressed==2:
        choosetext.width=0
        cmap2.x=15
        cmap2.size=8
        cmap1.size=0

    


#if pos==1:
#                    b.x=9.5
 #               if pos==2:
  #                  b.x=11.5
   #             if pos==3:
    #                b.x=13.5
     #           if pos==4:
      #              b.x=15.5
       #         if pos==5:
        #            b.x=17.5
