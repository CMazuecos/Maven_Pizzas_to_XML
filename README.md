# Maven_Pizzas_to_XML
Este programa hará un informe sobre los ficheros de la pizzería Maven, limpiará los datos y hará una recomendación de compra de ingredientes para cada semana.
### Archivos necesitados
- 'data_dictionary.csv': archivo csv que explican cada columna de los diferentes csvs.
- 'pizzas_to_xml.py': programa python que hace el informe de datos y la recomendación.
- 'order_details.csv': archivo con los detalles de los pedidos, habrá que limipiarlo.
- 'orders.csv': archivo que registra cuando se hace cada pedido, este fichero tampoco tiene todos sus datos limpios.
- 'pizza_types.csv': archivo con los detalles de cada pizza.
- 'pizzas.csv': archivo que registra detalles sobre cada pizza id.
- 'requirements.txt': contiene todos las librerías necesarias para el correcto funcionamiento del programa.
### Outputs
- Fichero 'Informe_Calidad_Datos.txt': fichero txt con un informe con el número de Nulls, tipología de datos y número de Nans en cada columna de cada fichero.
- Fichero 'ingredients_per_week.csv': fichero csv con la compra de los ingredientes necesarios para cada semana.
### Forma de ejecución
- Descargamos los archivos csv, el requirements.txt y el archivo python en una misma carpeta.
- Ejecutar en la terminal 'pip install requirements.txt'.
- Ejecutar 'pizzas_to_xml.py' y automáticamente se ejecutará el programa. 
- En primer lugar, se leen los datos de cada csv y se realizará el informe de datos. Se mostrará por pantalla y se escribirá en un fichero xml.
- Posteriormente, se limpian los datos.
- Después, con los datos ya extraídos y limpios se organizarán los pedidos por semanas.
- Cuando se organizan los pedidos por semanas, se ve que pizza contiene cada pedido.
- De cada pizza, se sacan los ingredientes de cada pizza y se van añadiendo a los pedidos de cada semana.
- Cuando ya se tiene la recomendación hecha, se escirbe en un archivo xml y se muestra por pantalla la compra recomendada para cada semana.  
### Archivo xml
- En primer lugar, devuelve un informe de los datasets. Cada rama es un fichero y las ramas de estos las columnas con su tipología de datos.
- La siguiente rama que sale de la raíz es con la recomendación. Cada rama que sale de estas, es una semana con cada uno de sus ingredientes.
### Limpieza ficheros
#### Fichero order_details
- Columna quantity: cambiamos nans y valores inferiores a 1 por 1. Los valores que no son numéricos (one, two) se cambian por su correspondiente número.
- Columna pizza_id: cambiamos nans por el pizza_id de la fila superior y convertimos algunos caracteres a los correctos. 
#### Fichero orders
- Columna fecha: hacemos un change to date time o cambiamos los segundos a fecha dependiendo de como esté escrita la fecha. 
- Rellenamos los nans con los valores de la fila superior
Para más aclaraciones, código explicado en el texto.

