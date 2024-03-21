class SearchVal(object):
    def __init__(self,lst,search):
        self.lst=lst
        self.search=search
    def findele(self):
        count=0
        for i,ele in enumerate(self.lst):
            if(ele==self.search):
                print(f"Search found at {i}")
                count+=1
        print(f"No of occurences {count} ")

def main():
    n=int(input('enter no of elements'))
    lst=[]
    for i in range(n):
        ele=int(input("Enter element "))
        lst.append(ele)
    search=int(input("Enter search element"))
    obj=SearchVal(lst,search)
    obj.findele()
if __name__=="__main__":
    main()


