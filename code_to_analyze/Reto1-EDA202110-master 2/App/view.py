"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
import threading
from DISClib.ADT import list as lt
assert cf
from debugController import doSortingTests

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

debug = False

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Encontrar buenos videos por categoría y país (Grupal)")
    print("3- Encontrar video tendencia por país ")
    print("4- Encontrar video tendencia por categoría")
    print("5- Buscar los videos con más Likes")
    print("0- Salir")

def initCatalog():
    """
    Inicializa el catalogo de videos
    """
    return controller.initCreate_videos()

def initTags():
    tags=controller.initLista_tags()
    for a in tags["elements"]:
        print (a[0],"  ",a[1])
    return tags

def printMostViewed(ord_videos, sample= 10):
    size = lt.size(ord_videos)
    if size <= sample:
        sample = size
    print('\n\n\n Videos más vistos: ')
    print("trending date","title", "channel", "publish time", "views", "likes", "dislikes", sep="   ")
    i = 1
    while sample >= i:
        dir=ord_videos["elements"][-i][0]["elements"]
        print(dir[1],dir[2], dir[3], dir[5], dir[6], dir[7], dir[8], sep="   ")
        i+=1

def printResults(parameters,result):
    size = len(parameters)
    str_format = ''
    indexes = [str(i) for i in range(0, size)]
    str_format = '{'+':^20s}   {'.join(indexes) + ':^20s}'
    print(str_format.format(*tuple(parameters)))
    for line in result:
        line = line[1:]
        print(str_format.format(*tuple(line)))

def consoleSortingTests(catalog):
    # flag is a pointer that shares information between the threads
    flag = [True, True]
    testThread = threading.Thread(target=doSortingTests, args=(catalog, flag,))
    testThread.start()
    while flag[0]:
        change = int(input("0. Remain doing tests\n1. Stop when average has been computed\n2. Stop as soon as possible\n"))
        if (change == 1):
            flag[0] = False
        elif (change == 2):
            flag[0] = False
            flag[1] = False
    print("Wait for the testing to end.")
    testThread.join()
    print("Testing ended!")

catalog = None
req1_order = None
req2_order = None
req3_order = None
req4_order = None
tag_list = None
"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("\nCargando información de los archivos ....")
        catalog= initCatalog()
        print("Se han cargado " , lt.size(catalog), "registros de videos")
        if not debug:
            print("Optimizando requerimiento 1")
            req1_order = controller.create_index_order(catalog, 'country', 'category_id', 'views')
        print("Optimizando requerimiento 2")
        req2_order = controller.create_index_order(catalog, 'country', 'title')
        print("Optimizando requerimiento 3")
        req3_order = controller.create_index_order(catalog, 'category_id', 'title')
        print("Optimizando requerimiento 4")
        req4_order = controller.create_index_order(catalog, 'likes')
        print("Requerimientos optimizados")
        dir=catalog["elements"][0][0]["elements"]
        print("\nPrimer video: ",dir[2])
        print("Canal: ", dir[3])
        print("Fecha de tendencia: ",dir[1])
        print("País: ",dir[-1])
        print("vistas: ",dir[6])
        print("Likes: ",dir[7])
        print("Dislikes: ",dir[8],"\n")
        print("Id  Nombre")
        tag_list = initTags()
        
    elif int(inputs[0]) == 2:
        if debug:
            size = int(input("Introduzca el tamaño de la muestra que quiere ordenar: "))
            print("0. Serial experiments Sort")
            print("1. ShellSort\n2.InsertionSort\n3.SelectionSort\n4.QuickSort\n5.MergeSort")
            algorithm = int(input("Introduzca el índice del algoritmo que quiere usar: "))
            result = None
            if (algorithm == 0):
                consoleSortingTests(catalog)
            else:
                if(algorithm == 1):
                    algorithm = 'shell'
                elif(algorithm == 2):
                    algorithm = 'insertion'
                elif(algorithm == 3):
                    algorithm = 'selection'
                elif(algorithm == 4):
                    algorithm = 'quick'
                else:
                    algorithm = 'merge'
                sample = int(input("Introduzca el número de vídeos que quiere listar: "))
                time, result = controller.order_by_Views(catalog, size, algorithm)
                print("El tiempo de ordenamiento fue de",time,"ms.")
                printMostViewed(result, sample=sample)
        else:
            country = input("Introduzca el nombre del país que quiere consultar: ")
            category = input("Introduzca el nombre de la categoría que quiere consultar: ")
            category = controller.tag_index(tag_list, category)
            sample = int(input("Introduzca el número de vídeos que quiere listar: "))
            print_parameters = ['trending_date', 'title', 'channel_title', 'publish_time', 'views', 'likes', 'dislikes']
            result = controller.top_videos_order(catalog, req1_order, [country, category],
                print_parameters, n=sample)
            printResults(print_parameters, result)
        input("Presione cualquier tecla para continuar.")
    elif int(inputs[0]) == 3:
        country = input("Introduzca el país que quiere consultar: ")
        print_parameters = ['title', 'channel_title', 'country']
        result = controller.most_days_tendency(catalog, req2_order, [country], print_parameters)
        print_parameters.append('Días')
        printResults(print_parameters, result)
    elif int(inputs[0]) == 4:
        # TODO category name en vez de id
        category = input("Introduzca el id de la categoría que quiere consultar: ")
        category = controller.tag_index(tag_list, category)
        print_parameters = ['title', 'channel_title', 'category_id']
        result = controller.most_days_tendency(catalog, req3_order, [category], print_parameters)
        print_parameters.append('Días')
        printResults(print_parameters, result)
    elif int(inputs[0]) == 5:
        tag = input("Introduzca el tag que quiere consultar: ")
        print_parameters = ['title', 'channel_title', 'publish_time', 'views', 'likes', 'dislikes']
        result = controller.top_videos_order(catalog, req4_order, None, print_parameters, n=1, tag=tag)
        printResults(print_parameters, result)
        # TODO print tags (result[0][0] es el índice del elemento)
    else:
        sys.exit(0)
sys.exit(0)
