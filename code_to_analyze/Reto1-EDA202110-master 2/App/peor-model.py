"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """

import config as cf
import csv
import time
from DISClib.ADT import list as lt
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import selectionsort as se
from DISClib.Algorithms.Sorting import insertionsort as ie
from DISClib.Algorithms.Sorting import quicksort as qk
from DISClib.Algorithms.Sorting import mergesort as mr

assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def create_videos(filepath: str):
    """
    Complexity time O(nt), space O(nt), where n stands for number of videos and t stands for tags in the videos.
    Args:
        filepath: path to the file to be read from
    Returns:
        Arraylist that represents videos with a tuple of:
            arraylist with video_id,trending_date,title,channel_title,category_id,publish_time,views,likes,dislikes,comment_count,
                thumbnail_link,comments_disabled,ratings_disabled,video_error_or_removed,description,country
            linkedlist with tags
    """
    videos = lt.newList(datastructure='ARRAY_LIST')
    if filepath is not None:
        input_file = csv.DictReader(open(filepath, encoding="utf-8"),
                                    delimiter=',')
        for line in input_file:
            add_video(videos, line)
    return videos


# Funciones para agregar informacion al catalogo
def add_video(videos, line):
    """
    Auxiliary function to create_videos which adds to videos an arraylist with most parameters and a linked list
    with the information of the tags of the videos. Complexity time O(t), space O(t) where t stands for tags in the
    videos.
    Args:
        videos: arraylist of videos
        line: OrderedDict with information of the videos
    Returns:
        None
    """
    categories = lt.newList(datastructure='ARRAY_LIST')
    tags = lt.newList()
    for element in line.items():
        if element[0] in ['likes','dislikes','views','comment_count','category_id']:
            lt.addLast(categories, int(element[1]))
        elif element[0] != 'tags':
            lt.addLast(categories, element[1])
        else:
            tagl = element[1].replace('"', '').split('|')
            for tag in tagl:
                lt.addLast(tags, tag)
    lt.addLast(videos, (categories, tags))

# Funciones para creacion de datos
def lista_tags(filepath,type="ARRAY_LIST"):
    tags=lt.newList(type)
    data= open(filepath)
    data.readline()
    linea= data.readline().replace("\n","").split("\t")
    while len(linea)>1:
        lt.addLast(tags,linea)
        linea=data.readline().replace("\n","").split("\t")
    return tags

# Funciones de consulta
def element_videos(videos, i, j):
    """
    Complexity time O(1), space O(1).
    Args:
        videos:
        i: index of the video
        j: index of the parameter
    Returns:
    Parameter of the video.
    """
    if j < 16:
        return videos['elements'][i][0]['elements'][j]
    else:
        return 'error'

def element_videos_with_order(videos, index_order, i, j):
    return element_videos(videos, index_order['indexes'][i], j)


def parameter_minimum(videos, index_order, index_parameter, parameter, floor, ceiling):
    """
    Works correctly only if index_parameter is equal to the first index parameter with which index_order was made.
    Args:
        videos: arraylist of videos
        index_order: custom index_order of videos
        index_parameter: index of parameter to be evaluated
        parameter: search parameter
    Returns:
    Index of the minimum element (in the index_order) which contains a certain parameter.
    """
    f = floor - 1
    c = len(index_order) - 1
    if ceiling is not None:
        c = ceiling
    m = (c + f) // 2 + (c + f) % 2
    while f != c:
        if element_videos(videos, index_order[m], index_parameter) >= parameter:
            c = m - 1
        else:
            f = m
        m = (c + f) // 2 + (c + f) % 2
    return f + 1


def parameter_maximum(videos, index_order, index_parameter, parameter, floor, ceiling):
    """
    Works correctly only if index_parameter is equal to the first index parameter with which index_order was made.
    Args:
        videos: arraylist of videos
        index_order: custom index_order of videos
        index_parameter: index of parameter to be evaluated
        parameter: search parameter
    Returns:
    Index of the maximum element (in the index_order) which contains a certain parameter.
    """
    f = floor
    c = len(index_order)
    if ceiling is not None:
        c = ceiling + 1
    m = (c + f) // 2
    while f != c:
        if element_videos(videos, index_order[m], index_parameter) <= parameter:
            f= m + 1
        else:
            c = m
        m = (c + f) // 2
    return c - 1


def range_by_parameter(videos, order, parameters):
    """
    Note that the function can be used to find how many elements share a number of characteristics.
    Args:
        videos: arraylist of videos
        order: custom index_order of videos
        parameters: parameters in the same order of the parameters_ids of order
    Returns:
    Index of the minimum element (in the index_order) which contains a certain parameter.
    """
    floor = 0
    ceiling = None
    for parameter, index_parameter in zip(parameters, order['parameters']):
        f = parameter_minimum(videos, order['indexes'], index_parameter, parameter, floor, ceiling)
        c = parameter_maximum(videos, order['indexes'], index_parameter, parameter, floor, ceiling)
        floor = f
        ceiling = c
    return f, c


def has_tag(videos, i, tag):
    return lt.isPresent(videos['elements'][i][1], tag)

def has_tag_with_order(videos, index_order, i, tag):
    return has_tag(videos, index_order[i], tag)

def tag_index(tags, name):
    result = -1
    for a in tags['elements']:
        if name in a[1]:
            if result == -1:
                result = a[0]
            else:
                result =-1
                break
    return result

# Funciones utilizadas para comparar elementos dentro de una lista
def base_sort_function(videos, i, parameter_indexes):
    """
    Auxiliary function to createIndexOrder. Complexity time O(p), space O(p), where p stands for number of parameters,
    (p <= 16).
    Args:
        videos: arraylist of videos
        i: index of the video
        parameter_indexes: list of indexes of parameters
    Returns:
    A tuple with the values that correspond to the parameter_indexes in the index i of videos.
    """
    return tuple([element_videos(videos, i, x) for x in parameter_indexes if x < 16])


def cmpVideosByViews(video1, video2):
    """
    Devuelve verdadero si los views de video1 son menores que los del video 2
    Args:
        video1: informacion del primer video que incluye su valor views
        video2: informacion del primer video que incluye su valor views
    """
    return (video1[0]['elements'][6] < video2[0]['elements'][6])


# Funciones de ordenamiento
def create_index_order(videos, order_indexes):
    """
    'Tags' parameter not supported. Complexity time O(nlog(n)p), space O(np), where n stands for number of videos and
    p stands for number of parameters (p <= 16).
    Args:
        videos: arraylist of videos
        order_indexes: list of indexes of parameters
    Returns:
    A list of indexes that indicate an order of videos based on the referenced parameters.
    """
    indexes = [i for i in range(0, len(videos['elements']))]
    sort_key = lambda a: base_sort_function(videos, a, order_indexes)
    indexes.sort(key=sort_key)
    order = {
        'indexes': indexes,
        'parameters': order_indexes
    }
    return order


def inefficient_ordering(videos, size, algorithm = 'shell'):
    if(size > lt.size(videos)):
        size = lt.size(videos)
    temp_list = lt.subList(videos, 0, size)
    temp_list = temp_list.copy()
    start_time = time.process_time()
    if (algorithm == 'shell'):
        temp_list = sa.sort(temp_list, cmpVideosByViews)
    elif(algorithm == 'insertion'):
        temp_list = ie.sort(temp_list, cmpVideosByViews)
    elif(algorithm == 'selection'):
        temp_list = se.sort(temp_list, cmpVideosByViews)
    elif(algorithm == 'quick'):
        temp_list = qk.sort(temp_list, cmpVideosByViews)
    else:
        temp_list = mr.sort(temp_list, cmpVideosByViews)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    return elapsed_time_mseg, temp_list


#usage example
if __name__ == '__main__':
    import time
    print("Loading vidios", time.asctime(time.gmtime()))
    vidios = create_videos(cf.data_dir+'videos-small.csv')
    print("Videos loaded! Size: ", lt.size(vidios), "\n")

    print("Creating order", time.asctime(time.gmtime()), "\n")
    order = create_index_order(vidios, [15,4,6])
    
    print("Finding range for country Canada category_id 10", time.asctime(time.gmtime()),"\n")
    floor, ceiling = range_by_parameter(vidios, order, ['canada', '10'])
    selection = list(reversed(order['indexes'][floor:(ceiling+1)]))
    n = 10
    print("The "+str(n)+" most viewed videos of Canada in category_id 10 are")
    for x in selection[:n]:
        name = element_videos(vidios, x, 2)
        views = element_videos(vidios, x, 6)
        country = element_videos(vidios, x, 15)
        category = element_videos(vidios, x, 4)
        print("    ",name, ":", views, country, category)
    print("Finish", time.asctime(time.gmtime()))