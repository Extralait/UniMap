from math import sqrt

with open('f') as file:
    first = True
    counter = 0
    def square_counter(line):
        global counter
        global first
        if first==True:
            a,b=map(int,line.split())
            first=False
            counter+=1
        else:
            c,d=map(int,line.split())
            first=True
            counter+=1
        if counter==2:
            left=a/b
            right=c/d
            left_sqrt=int(sqrt(left))
            right_sqrt = int(sqrt(right))
            all_square=[range(left,right,left^2+left+right)]
            answer=len(all_square)
            return
    for line in file:
        square_counter(line)


