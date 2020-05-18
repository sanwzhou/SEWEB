#! -*-conding:utf-8 -*-
#@Time: 2019/3/27 0027 11:28
#@swzhou
'''
功能说明
'''

# alien_color = 'green'
# alien_color = 'yellow'
# alien_color = 'red'
#
# if alien_color == 'green':
#     print('kill green , get 5 fen')
# elif alien_color == 'yellow':
#     print('get 10 fen')
# elif alien_color == 'red':
#     print('get 15 fen')

# peoples = {
#     'z':{
#         'age':'20',
#         'sex':'nan'
#         },
#     'l':{
#         'age':'18',
#         'sex':'nv'
#         }
#     }
#
# for name,info in peoples.items():
#     print('\nname is',name)
#     infoo = info['age'] + info['sex']
#     for info1,info2 in info.items():
#         print(infoo)
#         print(info1,':',info2)

# wang = {'type' : 'dog', 'master' : 'z'}
# miao = {'type' : 'cat','master' : 'l'}
# pets = [wang,miao]
#
# for x in pets:
#     print('name :',x,'\ttype:',x['type'],'\tmaster:',x['master'])

# aa = ('\ninput what your want')
# aa += ('\ninput "quit" to break')
#
# while b != 'quit':
#     b = input(aa)
#     # if b == 'quit':
#     #     break
#     if int(b) < 3:
#         print('free')
#     elif 3 <= int(b) <=12 :
#         print('10')
#     elif int(b) > 12:
#         print('15')

# ttt = True
# while ttt:
#     b = input(aa)
#     if b == 'quit':
#         ttt = False
#     else:
#         print('add', b)

# while True:
#     b = input(aa)
#     if b == 'quit':
#         break
#     elif int(b) < 3:
#         print('free')
#     elif 3 <= int(b) <=12 :
#         print('10')
#     elif int(b) > 12:
#         print('15')

# sandwich_orders = ['pastrami','a','pastrami','b','pastrami','c']
# finished_sandwiches = []
#
# print('pastrami is over')
# while 'pastrami' in sandwich_orders:
#     sandwich_orders.remove('pastrami')
#
# while sandwich_orders:
#     aa = sandwich_orders.pop()
#     print('I made your tuna sandwich',aa)
#     finished_sandwiches.append(aa)
# for y in finished_sandwiches:
#     print('f',y)

# lists = {}
# goon = True
# while goon:
#
#     name = input('your name:')
#     an = input('If you could visit one place in the world, where would you go?')
#     lists[name] = an
#
#     ann = input('继续 "y" or "n"')
#     if ann == 'n':
#         goon =False
#
# for name2,an2 in lists.items():
#     print(name2,'would go',an2)

# def display_message(me):
#     me = input('your')
#     print('l',me)
# display_message('123')

# def make_shirt(num = 'big',zi = 'I love Python'):
#     print('num:',num,'zi:',zi)
#
# make_shirt()
# make_shirt('2')
# make_shirt(zi='123')

# def describe_city(city,country = 'china'):
#     print(city, 'in' ,country)
#
# describe_city('beijing')
# describe_city('sh')
# describe_city('dong','je')

# def name(fir,la,mi=''):
#     if mi:
#         full = fir + mi + la
#     else:
#         full = fir + la
#     return full
#
# name1 = name('a','b','c')
# print(name1)
# name1=name('a','b')
# print(name1)

# lists = {}
# def city_country(city,country):
#
#     lists[city] = country
#
#
# while True:
#     print('"q" over')
#     city = input('your city')
#     if city == 'q':
#         break
#
#     country = input('country')
#     if country == 'q':
#         break
#     city_country(city, country)
#     for city1, country1 in lists.items():
#         print(city1, country1)
#
# lists={}
# def make_album(name,songs,num=''):
#     lists['name'] = name
#     lists['songs'] = songs
#     if num:
#         lists['num']=num
#     print(lists)
#
# # make_album('qili','qili')
# # make_album('shiyi','shiyi')
# # make_album('aizai','aizai','9')
#
# cc = True
# while cc:
#     print('enter"q" to over')
#     name = input('name:')
#     if name == 'q':
#         break
#     lists['name'] = name
#
#     songs = input('songs:')
#     if songs == 'q':
#         break
#     lists['songs'] = songs

# print(lists)


# magicians = ['a','b','c']
#
# def show_magicians(magicians):
#     for x in magicians:
#         print (x)
#
# show_magicians(magicians)

# magicians = ['a','b','c']
# greatlists = []
# def make_great(magicians):
#     while magicians:
#         great = magicians.pop()
#         greatlists.append('the great '+great)
#         # print(great)
#
#
# def show_magicians(magicians):
#     for x in magicians:
#         print (x)
#
# make_great(magicians[:])
# show_magicians(greatlists)
# show_magicians(magicians)

# def sanmingzhi(*foods):
#     lists = []
#     for x in foods:
#         lists.append(x)
#     print(lists)
#
# sanmingzhi('1')
# sanmingzhi('1','2')
# sanmingzhi('1','2','3')

# def build_profile(first, last, **user_info):
#     """创建一个字典㼿其中包含㼿㼿㼿㼿的有关用户的一切"""
#     profile = {}
#     profile['first_name'] = first
#     profile['last_name'] = last
#
#     for key, value in user_info.items():
#
#         profile[key] = value
#     return profile
#
# user_profile = build_profile('z', 'sw',
#                              location='hf',
#                              field='IT',
#                              sex = 'n')
# print(user_profile)

# def cars(user,model,**info):
#     lists = {}
#     lists[user] = user
#     lists[model] = model
#
#     for key,value in info.items():
#         lists[key] = value
#
#     return lists
#
# car = cars('subaru', 'outback', color='blue', tow_package=True)
#
# print(car)

# class Restaurant():
#     def __init__(self,restaurant_name,cuisine_type):
#         self.restaurant_name = restaurant_name
#         self.cuisine_type = cuisine_type
#
#     def describe_restaurant(self):
#         print(self.restaurant_name)
#         print(self.cuisine_type)
#
#     def open_restaurant(self):
#         print('Restaurant is run')
#
# restaurant = Restaurant('c','ch')
# print(restaurant.restaurant_name)
# print(restaurant.cuisine_type)
# restaurant.describe_restaurant()
# restaurant.open_restaurant()

# class User():
#     def __init__(self,first_name,last_name):
#         self.first_name =  first_name
#         self.last_name =last_name
#
#     def describe_user(self):
#         print(self.first_name)
#         print(self.last_name)
#
#     def get_uesr(self):
#         print(self.first_name + self.last_name + 'con')
#
# user1 = User('z','sw')
# user1.describe_user()
# user1.get_uesr()
#
# user2 = User('z','yl')
# user2.describe_user()
# user2.get_uesr()


# class Restaurant():
#     def __init__(self,restaurant_name,cuisine_type):
#         self.restaurant_name = restaurant_name
#         self.cuisine_type = cuisine_type
#         self.number_served = 0
#
#     def describe_restaurant(self):
#         print(self.restaurant_name)
#         print(self.cuisine_type)
#
#     def open_restaurant(self):
#         print('Restaurant is run')
#
#     def set_number_served(self,number_served):
#         self.number_served = number_served
#
#     def increment_number_served(self,number):
#         self.number_served += number
#
# restaurant = Restaurant('c','ch')
# print(restaurant.number_served)
# restaurant.set_number_served(3)
# print(restaurant.number_served)
# restaurant.increment_number_served(3)
# print(restaurant.number_served)


class User():
    def __init__(self,first_name,last_name):
        self.first_name =  first_name
        self.last_name =last_name
        self.login_attempts = 0

    def describe_user(self):
        print(self.first_name)
        print(self.last_name)

    def get_uesr(self):
        print(self.first_name + self.last_name + 'con')

    def increment_login_attempts(self):
        self.login_attempts +=1

    def reset_login_attempts(self):
        self.login_attempts = 0

#
# user1 = User('z','sw')
# user1.increment_login_attempts()
# print(user1 .login_attempts)
# user1.increment_login_attempts()
# print(user1 .login_attempts)
# user1.increment_login_attempts()
# print(user1 .login_attempts)
# user1.reset_login_attempts()
# print(user1 .login_attempts)


# class IceCreamStand(Restaurant):
#
#     def __init__(self,restaurant_name,cuisine_type):
#         super().__init__(restaurant_name,cuisine_type)
#         self.flavors = ''
#
#     def get_flavors(self,*flavors):
#         self.flavors = flavors
#         print(flavors)
#
# aa = IceCreamStand('a','b')
# aa.get_flavors('1')
# aa.get_flavors('2')
# aa.get_flavors('1','2')


# class Admin(User):
#     def __init__(self,first_name,last_name):
#         super().__init__(first_name,last_name)
#         self.privileges = ''
#
#     def show_privileges(self,*privileges):
#         self.privileges = privileges
#         print(privileges)
#
# aa = Admin('z','sw')
# aa.show_privileges('hf','n')

# from random import randint
#
# class Die():
#     def __init__(self,sides):
#         self.sides = 6
#
#     def roll_die(self):
#         x = randint(1,6)
#         return x
#
#
# D = Die('1')
# print(D.sides)
# print(D.roll_die())

# with open('tmp/test.txt') as file:
#     contents = file.read()
#     print(contents.rstrip())

# with open('test.txt') as file_o:
#     for line in file_o:
#         print(line.rstrip())

# with open('test.txt') as file_o:
#     aa = file_o.readlines()
#
# print(aa)
# # for b in aa:
# #     print(b)
#
# b = ''
# for i in aa:
#     b +=i.strip()
# print(b)

# while True:
#     aa = input('your name:')
#     print(aa,'Welcome!')
#
#     with open('t.txt','a') as f:
#         f.write(aa+'Visit \n')

# while True:
#     print('输入两个数字：')
#     try:
#         a = int(input('one:'))
#         b = int(input('two:'))
#     except ValueError:
#         print('请输入数字')
#     else:
#         print('sum:',a + b)
#
# filet = ['cats.txt','dogs.txt']
#
# def p(file):
#     try:
#         with open(file) as cat:
#             cc = cat.read()
#     except FileNotFoundError:
#         print(file ,'not existence')
#     else:
#         print(cc)
#         print(type(cc))
#
# for i in filet:
#     p(i)
#
# print(i.count('cat'))

# a =  ['1',2,3,4]
#
# import json
# file = 'test.json'
# with open(file,'w') as file_o:
#     json.dump(a,file_o)
#
# with open(file) as file2_o:
#     s = json.load(file2_o)
#
# print(s)

# import json
# file = 'test.json'
# def numj():
#     try:
#         with open(file) as file2_o:
#             aa = json.load(file2_o)
#     except FileNotFoundError:
#         num = input('your num:')
#         with open(file, 'w') as file_o:
#             json.dump(num, file_o)
#             print('I know your favorite number! It’s', num)
#     else:
#          print('I know your favorite number! It’s', aa)
#
# numj()


# import json
#
# def get_username():
#     file = 'test.json'
#     try:
#         with open(file) as file_o:
#             user = json.load(file_o)
#     except FileNotFoundError:
#         return None
#     else:
#         return user
#
# def stor_username():
#     file = 'test.json'
#     user = input('input your name:')
#     with open(file,'w') as file_o:
#         json.dump(user,file_o)
#     return user
#
# def welcome():
#     user1 = get_username()
#     if user1:
#         print('your name is',user1,'?')
#         j = input('Y or N:')
#         if j.lower() =='y':
#             print(user1,'welcome back')
#         else:
#             user1 = stor_username()
#             print(user1, 'welcome')
#     else:
#         user1 = stor_username()
#         print(user1,'welcome')
#
# welcome()

# 11-1\11-2
# def city_functions(city,country,population=''):
#     if population:
#         cc = city + ',' + country + ' - population ' + population
#     else:
#         cc = city + ',' + country
#     return cc
#
# import unittest
#
# class test_cities(unittest.TestCase):
#     def test_city_functions(self):
#         ccc = city_functions('sh','china')
#         self.assertEqual(ccc,'sh,china')
#     def test_city_country_population(self):
#         ccc = city_functions('sh','china','1000000')
#         self.assertEqual(ccc,'sh,china - population 1000000')
#
# unittest.main()































