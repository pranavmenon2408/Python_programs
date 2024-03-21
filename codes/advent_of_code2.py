with open("input.txt") as f:
    inp=f.readlines()
    sum=0
    ind=1
    for i in inp:
        game=i.split(':')
        games=game[1].split(';')
        flag=0
        temp=''
        max_red=0
        max_green=0
        max_blue=0
        for j in games:
            temp=j.split(' ')
            
            if('red,' in temp):
               
                if(int(temp[temp.index('red,')-1])>max_red):
                    max_red=int(temp[temp.index('red,')-1])

            if('green,' in temp):
               
                if(int(temp[temp.index('green,')-1])>max_green):
                    max_green=int(temp[temp.index('green,')-1])
            if('blue,' in temp):
                
                if(int(temp[temp.index('blue,')-1])>max_blue):
                    max_blue=int(temp[temp.index('blue,')-1])
            if('red\n' in temp):
                
                if(int(temp[temp.index('red\n')-1])>max_red):
                    max_red=int(temp[temp.index('red\n')-1])
            if('green\n' in temp):
                
                if(int(temp[temp.index('green\n')-1])>max_green):
                    max_green=int(temp[temp.index('green\n')-1])
            if('blue\n' in temp):
                
                if(int(temp[temp.index('blue\n')-1])>max_blue):
                    max_blue=int(temp[temp.index('blue\n')-1])
            if('red' in temp):
                
                if(int(temp[temp.index('red')-1])>max_red):
                    max_red=int(temp[temp.index('red')-1])
            if('green' in temp):
                
                if(int(temp[temp.index('green')-1])>max_green):
                    max_green=int(temp[temp.index('green')-1])
            if('blue' in temp):
                
                if(int(temp[temp.index('blue')-1])>max_blue):
                    max_blue=int(temp[temp.index('blue')-1])
        if flag==0:
            sum+=max_blue*max_green*max_red
            print(max_blue*max_green*max_red)
            print(games)
        
        

    print(sum)