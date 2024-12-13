# 将一条信息存储到变量中，再将其打印出来
simple = 'simple message'
print(simple)

simple = 'hello my girl'
print(simple.title())

age = 27
ina = 'Happy ' + str(age) + 'rd birthday'
print(ina)

foods = ['fruit', 'water', 'milk']
copyFoods = foods[:]
foods.insert(0, 'apple')

foods.pop()
print(foods)


cars = ['brand', 'model', 'year']
for car in cars:
    if car == 'brand':
        print(car.upper())
    else:
        print(car.title())


favorite_languages = {
    'jen': 'python',
    'sarah': 'c',
    'edward': 'ruby',
    'phil': 'python',
}
print(favorite_languages['edward'].title())
for language in favorite_languages.keys():
    print(language.title())