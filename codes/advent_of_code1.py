with open("input.txt") as f:
    inp=f.readlines()
    sum=0
    ind=1
    for i in inp:
        #print(i)
        mapp={'one':'1','two':'2','three':'3','four':'4','five':'5','six':'6','seven':'7','eight':'8','nine':'9'}
        
        #i=list(i)
        
        for k in mapp:
            
            poss=[j for j in range(len(i)-1) if i.startswith(k,j)]
            for j in poss:
                i=list(i)
                i.insert(j+(len(k)//2)+1,mapp[k])
                i=''.join(i)
                
        print(poss)
        numb=[]
        print(i)
        for j in range(len(i)):
            if i[j].isdigit()==True:
                numb.append(int(i[j]))
        print(numb)
        ind+=1
        sum+=numb[0]*10+numb[len(numb)-1]
        
        # print(sum)
        # numb.clear()
        
        
    print(ind)
    print(sum)