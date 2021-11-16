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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

index_by_id = {
    'video_id': 0,
    'trending_date': 1,
    'title': 2,
    'channel_title': 3,
    'category_id': 4,
    'publish_time': 5,
    'views': 6,
    'likes': 7,
    'dislikes': 8,
    'comment_count': 9,
    'thumbnail_link': 10,
    'comments_disabled': 11,
    'ratings_disabled': 12,
    'video_error_or_removed': 13,
    'description': 14,
    'country': 15
}

# Inicialización del Catálogo de libros

# Funciones para la carga de datos

def initCreate_videos():
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    videos = model.create_videos(filepath="Data/videos-all.csv")
    return videos

def initLista_tags():
    tags=model.lista_tags("Data/category-id.csv")
    return tags
# Funciones de ordenamiento
def order_by_Views(videos, size, algorithm = 'shell'):
    return model.inefficient_ordering(videos, size, algorithm)

def names_to_indexes(names):
    indexes = []
    for name in names:
        indexes.append(index_by_id[name])
    return indexes

def create_index_order(videos, *args):
    order_indexes = names_to_indexes(args)
    index_order = model.create_index_order(videos, order_indexes)
    return index_order

def most_days_tendency(videos, index_order, selection_parameters, print_parameters):
    floor = 0
    ceiling = len(index_order) - 1
    if selection_parameters:
        floor, ceiling = model.range_by_parameter(videos, index_order, selection_parameters)
    if ceiling < floor:
        return []
    i = floor
    imax = floor
    maxdays = 0
    days = 0
    title = model.element_videos_with_order(videos, index_order, i, 2)
    while i <= ceiling:
        cmp_title =  model.element_videos_with_order(videos, index_order, i, 2)
        if title == cmp_title:
            days += 1
        else:
            if days > maxdays:
                imax = i - days
                maxdays = days
            days = 1
            title = cmp_title
        i += 1
    if days > maxdays:
        maxdays = days
    print_indexes = names_to_indexes(print_parameters)
    result = [index_order['indexes'][imax]]
    for j in print_indexes:
        result.append(str(model.element_videos_with_order(videos, index_order, imax, j)))
    result.append(str(maxdays))
    return [result]


def top_videos_order(videos, index_order, selection_parameters, print_parameters, n=None, tag = None, top=True):
    floor = 0
    ceiling = len(index_order) - 1
    if selection_parameters:
        floor, ceiling = model.range_by_parameter(videos, index_order, selection_parameters)
    if ceiling < floor:
        return []
    print_indexes = names_to_indexes(print_parameters)
    if not n:
        n = ceiling - floor + 1
    result = []
    if top:
        i = ceiling
        while (i >= floor) and (len(result) < n):
            if (not tag) or model.has_tag_with_order(videos, index_order, i, tag):
                ithResult = [index_order['indexes'][i]]
                for j in print_indexes:
                    ithResult.append(str(model.element_videos_with_order(videos, index_order, i, j)))
                result.append(ithResult)
            i -= 1
    else:
        i = floor
        while (i <= ceiling) and (len(result) < n):
            if (not tag) or model.has_tag_with_order(videos, index_order, i, tag):
                ithResult = [index_order['indexes'][i]]
                for j in print_indexes:
                    ithResult.append(str(model.element_videos_with_order(videos, index_order, i, j)))
                result.append(ithResult)
            i += 1
    return result

def tag_index(tags, name):
    return int(model.tag_index(tags, name))

# Funciones de consulta sobre el catálogo
