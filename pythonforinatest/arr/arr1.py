print("----列表-----")
class1 = ["丁一","王二","张三","李五","jojo","ina"]
a = class1[1:4]
print(a)
c = class1[-2:]
print(c)
d = class1[:-4]
print(d)
class1.append("joe")
print(class1)
e = ";".join(class1)
print(e)
f = "hi hello world"
print(f.split(' '))

print("-----------")


print("----字典-----")
class1 = {"丁一":80,"王二":70,"张三":61,"李五":52,"jojo":90,"ina":100}
print("丁一：",class1["丁一"])

for k in class1:
    print(k + ":" + str(class1[k]))
    ### 这里的str函数是因为分数是number格式的，拼接的时候需要用str()函数转换

print("items()：",class1.items())
print("keys()：",class1.keys())
print("values()：",class1.values())
print("-----------")

score = 10
year = 2024
if (score < 0 ) and (year < 100):
    print("录入数据库")
else:
    print("不录入数据库")
print("------while循环-----")
g = 5
while g > 1:
    # print(g)
    g -= 1
    print(g)
print("------try/catch----------")

try:
    # a = 10
    print(1+a)
except:
    print("error")

print("------def()函数-----")
def fun1(u):
    a = 10 + u
    print(a)
    return a

fun1(20)
print("------fun1---------")

def fun2():
    x = 2
    print(x + 2)
    return x + 2

fun2()
print("------fun2---------")
x=1
def fun3(z):
    z=z+1
    print(z)
fun3(3)

print(x)


print("----------常用函数介绍----------")
#str()函数
name = 'ina'
score = 100
print( name+ "的成绩是:" + str(score))
#len()函数
title = ["标题1","标题2","标题3"]
print(len(title))