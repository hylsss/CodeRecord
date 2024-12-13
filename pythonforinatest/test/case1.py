# n = int(input("请输入一个大于0的整数："))
# mysun = 0
# num = 1
# while num <= n:
#     mysun = mysun + num
#     num = num + 1
# print("1加到%d的和为：%d"%(n,mysun))


def changeme (mylist):
    mylist.append([1,2,3,4])
    print("函数内取值：",mylist)
    return

mylist = [10]
changeme(mylist)
print("函数外取值：", mylist)

def fun1(name, age,sex="女"):
    print(name)
    print(age)
    print(sex)
    return

fun1(name="ina.h",age=21)

mylamb = lambda arg1, arg2, arg3: arg1 + arg2 - arg3
print("调用匿名函数，并返回值：",mylamb(10,20,5))

def outer():
    num = 10
    def inner():
        nonlocal  num
        print("nonlocal关键字声明，在嵌套函数中调用num的值，其值为",num)
        num = 100
        print("重新为num赋值后，其值为",num)
    inner()
    print("调用嵌套函数后，num的值为",num)
outer()