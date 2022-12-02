import pandas as pd
import lxml.etree as ET
import datetime
import re
import numpy as np


def informe_calidad_datos (fichero, name):
    #Print name of the file, nans, nulls and data types
    print('Nombre del fichero:', name)
    print (fichero.isnull().sum()) 
    print (fichero.dtypes)
    print (fichero.isna().sum())
    #escribir en un datatype_dictionary, como key el nombre de la columna y como value el tipo de dato
    datatype_dictionary = {}
    for i in range(len(fichero.columns)):
        datatype_dictionary[fichero.columns[i]] = fichero.dtypes[i]
    
    return datatype_dictionary

def limpiar_fichero_order_details(fichero):
    print(fichero)
    print('Limpiando fichero order_details')
    #we change nan values to 1
    fichero['quantity'].fillna(1, inplace=True)
    fichero['quantity'] = fichero['quantity'].apply(lambda quantity: change_quantity(quantity))
    #we change the nan values of the column pizza_id to the value above
    fichero['pizza_id'].fillna(method='ffill', inplace=True)
    fichero['pizza_id'] = fichero['pizza_id'].apply(lambda pizza_id: change_pizza_id(pizza_id))
    print('Fichero order_details limpio')
    return fichero  

def change_quantity(quantity):
    #change in the column quantity the values that are not numbers to their numbers and if they are less than 1 we change them to 1
    try:
        quantity = int(quantity)
        if quantity < 1:
            quantity = 1
        return quantity
    except:
        quantity = re.sub(r'one', '1', quantity, flags=re.IGNORECASE)
        quantity = re.sub(r'two', '2', quantity, flags=re.IGNORECASE)
        return quantity

def change_pizza_id(pizza_id):
    #convert some characters to others 
    pizza_id = re.sub('@', 'a', pizza_id)
    pizza_id = re.sub('0', 'o', pizza_id)
    pizza_id = re.sub('1', 'i', pizza_id)
    pizza_id = re.sub('3', 'e', pizza_id)
    pizza_id = re.sub('-', '_', pizza_id)
    pizza_id = re.sub(' ', '_', pizza_id)
    return pizza_id


def limpieza_datos_orders(fichero):
    fichero = fichero.sort_values(by=['order_id'])
    #fichero fillna with values above
    print(fichero)
    print('Limpiando fichero orders')
    fichero.fillna(method='ffill', inplace=True) # we fill the nan values with the value above
    #change column date to datetime
    fichero['date'] = fichero['date'].apply(lambda x: change_date(x))    
    print('Fichero orders limpio') 
    return fichero

def change_date(date):
    try:
        #change the date to datetime
        date = pd.to_datetime(date)
        return date
    except:
        #change the date (written in seconds) to the correct format
        date = datetime.datetime.fromtimestamp(int(float(date)))
        return date

def create_dictionary(pizza_types):
    #create a dictionary with the pizza type id as key and the ingredients as value 
    dictionary_pizza_type = {}
    for i in range(len(pizza_types)):
        dictionary_pizza_type [pizza_types ['pizza_type_id'][i]] = pizza_types ['ingredients'] [i]
    return dictionary_pizza_type

def cargar_datos (order_details, pizzas, pizza_types, orders):
    dictionary_pizza_type = create_dictionary(pizza_types) #create a dictionary with the pizza type id as key and the ingredients as value
    semanas, dias_semana = organizar_por_semanas(orders) #organize the orders by weeks
    pedidos = organizar_por_pedidos(semanas, order_details, dictionary_pizza_type, pizzas) #organize the orders by pizzas
    ingredients_dictionary = {} 
    for i in range(len(pedidos)):
        #get the ingredients of each week
        ingredients_week = transform_pizza_into_ingredients(pedidos[i], dias_semana[i], pizza_types, {})
        ingredients_dictionary [i+1] = ingredients_week
        print('Cargado los ingredientes de la semana', i+1)
    return ingredients_dictionary

def organizar_por_semanas(orders):
    diccionario_weekdays = {}
    diccionario_pedidos = {}
    #we create a dictionary with the week number as key and the days of the week as value being all 0 and empty
    for i in range (53):
        diccionario_weekdays [i] = [0, 0, 0, 0, 0, 0, 0]
        diccionario_pedidos [i] = [] 

    for order in orders['order_id']:
        #we get the day of the week and the week of the year and we add the order id to the dictionary of the orders
        try:
            fecha = orders['date'][order]
            numero_semana = fecha.isocalendar().week
            numero_dia = fecha.isocalendar().weekday
            diccionario_weekdays [numero_semana-1][numero_dia-1] += 1
            diccionario_pedidos [numero_semana-1].append(orders['order_id'][order])
        except:
            pass
    for i in range(len(diccionario_weekdays)):
        #We calculate the number of days of the week that have orders
        dias_semana = 0
        for j in range(len(diccionario_weekdays[i])):
            if diccionario_weekdays[i][j] != 0:
                dias_semana += 1
        diccionario_weekdays[i] = dias_semana
    return diccionario_pedidos, diccionario_weekdays

def organizar_por_pedidos(semanas, order_details, dictionary_pizza_type, pizzas):
    tamanos = {'S': 1, 'M': 2, 'L': 3, 'XL': 4, 'XXL': 5}
    pedidos_semana = []
    for i in range(len(semanas)):
        pedidos_semana.append({})
        #we create a dictionary with the order id as key and 0 as value
        for key, value in dictionary_pizza_type.items():
            pedidos_semana[i][key] = 0
        

        for j in range(len(semanas[i])):
            #we get the order id and the pizza id of every week and we add all the quantities (multiplied by size) of the pizza to the dictionary
            order_id_buscado = semanas[i][j]
            lista_pizzas = order_details.loc[order_details['order_id'] == order_id_buscado]
            for pizza in lista_pizzas['pizza_id']:
                pizza_searched = pizzas.loc[pizzas['pizza_id'] == pizza]
                quantity = lista_pizzas.loc[lista_pizzas['pizza_id'] == pizza]['quantity'].values[0]
                pizza_type = pizza_searched['pizza_type_id'].values[0]
                pizza_size = pizza_searched['size'].values[0]
                pedidos_semana[i][pizza_type] += int(quantity) * int(tamanos[pizza_size])
        print('Cargado el pedido de la semana', i+1)
    return pedidos_semana

def transform_pizza_into_ingredients(pizzas_semana, dias_semana, pizza_types, ingredients_dictionary):    
    #get all the possible ingredients and add them to a dictionary
    for i in range(len(pizza_types)):
        ingredients = pizza_types['ingredients'][i]
        ingredients = ingredients.split(', ')
        for ingredient in ingredients:
            ingredients_dictionary[ingredient] = 0
    #add the ingredients of each pizza to the dictionary
    for key, value in pizzas_semana.items():
        ingredients = pizza_types.loc[pizza_types['pizza_type_id'] == key]['ingredients'].values[0]
        ingredients = ingredients.split(', ')
        for ingredient in ingredients:
            ingredients_dictionary[ingredient] += value
    for key, value in ingredients_dictionary.items():
        ingredients_dictionary[key] = int(np.ceil(value/dias_semana*7))
    return ingredients_dictionary

def extract_data():
    #extract the data from the database
    datatype_dictionary = {'datatype_order_details': {}, 'datatype_pizzas': {}, 'datatype_pizza_types': {}, 'datatype_orders': {}}	
    order_details = pd.read_csv('order_details.csv',sep=';')
    datatype_od = informe_calidad_datos(order_details, 'order_details.csv')
    datatype_dictionary['datatype_order_details'] = datatype_od
    order_details = limpiar_fichero_order_details(order_details)
    pizzas = pd.read_csv('pizzas.csv',sep = ',')
    datatype_p = informe_calidad_datos(pizzas, 'pizzas.csv')
    datatype_dictionary['datatype_pizzas'] = datatype_p
    pizza_types = pd.read_csv('pizza_types.csv', sep = ',', encoding='latin-1')
    datatype_pt = informe_calidad_datos(pizza_types, 'pizza_types.csv')
    datatype_dictionary['datatype_pizza_types'] = datatype_pt
    orders = pd.read_csv('orders.csv', sep = ';')
    datatype_o = informe_calidad_datos(orders, 'orders.csv')
    datatype_dictionary['datatype_orders'] = datatype_o
    orders = limpieza_datos_orders(orders)
    return order_details, pizzas, pizza_types, orders, datatype_dictionary

def load_data(ingredients, datatype_dictionary):   
    #We create the root of the xml file
    root = ET.Element('Informe')
    diccionario_datatype = ET.SubElement(root, 'Datatype') #we create the datatype dictionary and add it to the root
    for fichero in datatype_dictionary: 
        fichero_data = ET.SubElement(diccionario_datatype, fichero) #
        for elemento in datatype_dictionary[fichero]:
            subelemento = ET.SubElement(fichero_data, elemento)
            subelemento.text = str(datatype_dictionary[fichero][elemento])
    diccionario_ingrediente = ET.SubElement(root, 'Ingredients') #we create a dictionary with the ingredients per week and add it to the root
    for week in ingredients:
        number_week = ET.SubElement(diccionario_ingrediente, 'Week_'+str(week))
        for key, value in ingredients[week].items():
            key = re.sub(' ', '_', key)
            ingrediente = ET.SubElement(number_week, key)
            ingrediente.text = str(value)
    tree = ET.ElementTree(root) #add the root to the tree
    tree.write('pizzas.xml') #write the tree in the xml file
    print('Cargado el archivo xml pizzas.xml')
        
    
if __name__ == '__main__':
    order_details, pizzas, pizza_types, orders, datatype_dictionary = extract_data() #ETL process
    ingredients = cargar_datos(order_details, pizzas, pizza_types, orders)
    load_data(ingredients, datatype_dictionary)
