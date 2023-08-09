class Operations(object):
    def __init__(self,x,y,op,num):
        self.x=x
        self.y=y
        self.op=op
        self.num=num
    def operation(self):
        if(self.op=='+'):
           sum=self.x+self.y
           print(f"Sum is {sum}")
        elif(self.op=='-'):
           diff=self.x-self.y
           print(f"Difference is {diff}")
        elif(self.op=='x'):
           prod=self.x*self.y
           print(f"Product is {prod}")
        elif(self.op=='/'):
           quo=self.x/self.y
           print(f"Quotient is {quo}")
    def sum_even(self):
        i=100
        sum=0
        while(i<=200):
            if(i%2==0):
                sum=sum+i
            i=i+2
        print(f"sum is {sum}")
    def prime(self):
        flag=True
        for i in range(2,self.num//2+1):
            if(self.num%i==0):
                flag=False
                break
        if(flag):
            print(f"{self.num} is a prime")
        else:
            print(f"{self.num} is not prime")
    def leap(self,year):
        if(year%4==0):
            if(year%100==0):
                if(year%400==0):
                    print(f"{year} is a leap year")
                else:
                    print(f"{year} is not a leap year")
            else:
                print(f"{year} is a leap year")
        else:
            print(f"{year} is not a leap year")

if __name__=="__main__":
    try:
        x=int(input("Enter a number :"))
        y=int(input("Enter another a number :"))
        op=input("Enter an operation to perform")
        num=int(input("Enter number to check prime: "))
        year=int(input("Enter a year to check if leap year:"))
        obj=Operations(x,y,op,num)
        obj.operation()
        obj.sum_even()
        obj.prime()
        obj.leap(year)
    except ZeroDivisionError:
        print("Division by zero")
    else:
        print('Execution fine')
    finally:
        print("Finally block executed")


