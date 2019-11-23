#!/usr/bin/env python
# coding: utf-8

# In[1]:


def getMenu():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.implicitly_wait(10)

    url = input("Введите ссылку ресторана в формате [*delivery-club.ru/srv/*]: ")
    print("Загрузка...\n")

    driver.get(url)
    menu = driver.find_elements_by_class_name('menu-product')

    mealCost = {}
    
    for meal in menu:
        title = meal.find_element_by_class_name('menu-product__title').text   
        price = meal.find_element_by_class_name('menu-product__price').text
        mealCost[title] = int(price[:-1]);
    
    driver.close()
    return mealCost


# In[57]:


def printOrder():    
    if len(order) == 0: return
    totalForAll = 0
	
    for name in order:
        summary = 0
        print(name,"{")
        
        for meal in order[name]:
            cnt = order[name][meal]
            summary += mealCost[meal] * cnt
            
            if cnt == 1: print('   {}: {}'.format(meal, mealCost[meal]))
            else: print('   {}: {} x {} = {}'.format(meal,mealCost[meal],cnt, mealCost[meal]*cnt))
    
        total = summary * (100 - sale) / 100 + delivery / len(order)
        totalForAll += total
        print('}','Итого: {} - {}% + {} / {} = {}'.format(summary,sale,delivery,len(order), total))
        print('\n')
		
    print("Сумма общего заказа: {}".format(totalForAll))


# In[39]:


def parseMeal(comm):
    meal = ""
    
    for i in range(2,len(comm)):
        if i != 2: meal += " "
        meal += comm[i]
            
    return meal

def clear():  
    if name == 'nt': # win
        _ = system('cls') 
    else: #mac and linux
        _ = system('clear')

# In[2]:


from os import system, name
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

print("1. ПОЛУЧЕНИЕ МЕНЮ")
mealCost = getMenu()


# In[58]:


bill = {}
order = {}
delivery = 0
sale = 0
comm = ["Меню"]
output = ""

while(1):
    clear()
    print("2. СОСТАВЛЕНИЕ ЗАКАЗА")       
    
    if comm == ['Помощь']:
        print('+ [имя] [блюдо]')
        print('- [имя] [блюдо]')
        print('Доставка [стоимость]')
        print('Скидка [процент]')
        print('Меню')
        print('Завершить') 
        
    elif comm[0] == '+' and len(comm) >= 3:        
        meal = parseMeal(comm)
            
        if mealCost.get(meal) == None:
            output = "Неверное название блюда"            
        else:
            if order.get(comm[1]) == None: order[comm[1]] = {}
            if order[comm[1]].get(meal) == None: order[comm[1]][meal] = 0
                
            order[comm[1]][meal] += 1;
            
    elif comm[0] == '-' and len(comm) >= 3:
        meal = parseMeal(comm)
        
        if order.get(comm[1]) == None:
            output = "Неверное имя"
        elif order[comm[1]].get(meal) == None:
            output = "Неверное название блюда"        
        else:            
            order[comm[1]][meal] -= 1
            if order[comm[1]][meal] == 0: order[comm[1]].pop(meal)
            if len(order[comm[1]]) == 0: order.pop(comm[1])
            
    elif comm == ['Меню']:
        for meal in mealCost:
            print(meal,"-",mealCost[meal])  
    
    elif comm[0] == 'Доставка' and len(comm) == 2:
        delivery = int(comm[1])
    
    elif comm[0] == 'Скидка' and len(comm) == 2:
        sale = int(comm[1])
    
    elif comm == ['Завершить']:
        break    
        
    else:
        output = 'Неверная команда. Используйте [Помощь] для списка всех команд'
    
    print("\n")
    printOrder()
    
    if(output != ""):
        print("Ошибка:",output)
        output = ""
    
    comm = input("Введите команду: ")
    comm = comm.split()
    
clear()
print("3. ИТОГ\n")
printOrder()


# In[ ]:




