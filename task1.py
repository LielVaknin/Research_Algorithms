import doctest
from typing import Any


def f(x: int, y: float, z):  # Helper function for the doctest of safe_call function
    return x + y + z


def safe_call(func, **kwargs):
    """
    Receives as an input a function and arguments with names and calls the function with the arguments
    if they exactly match the types specified in the function's annotation.
    If the types do not match, an exception will be thrown.
    :param func: Represents a given function
    :param kwargs: Used to pass a keyworded, variable-length argument list
    :return: The result of a given function on the given arguments

    >>> safe_call(f, x=5, y=7.0, z=3)
    15.0
    >>> safe_call(f, x=5, y="abc", z=3)
    Traceback (most recent call last):
    ...
    TypeError
    """
    annotations = func.__annotations__
    for argument_name, argument_value in kwargs.items():
        if argument_name in annotations and annotations[argument_name] != type(argument_value):
            raise TypeError()
    return f(**kwargs)


def four_neighbor_function(node: Any) -> list:  # Helper function for doctest of breadth_first_search function
    (x, y) = node
    return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]


def find_path(start, end, parent):
    """
    Helper function of breadth_first_search function which finds the path
    between a given source node and a given destination node
    :param start: Represents a source node
    :param end: Represents a destination node
    :param parent: A dictionary contains the parent of each node
    :return: The path between a given source node and a given destination node
    """
    path = []
    temp_node = end  # start with end node
    path.insert(0, end)
    while temp_node != start:
        path.insert(0, parent[temp_node])
        temp_node = parent[temp_node]
    return path


def breadth_first_search(start, end, neighbor_function):
    """
    Implementation of BFS algorithm.
    :param start: Represents a source node
    :param end: Represents a destination node
    :param neighbor_function: A function that finds neighbors of a given node
    :return: The path between a given source node and a given destination node

    >>> breadth_first_search(start=(0, 0), end=(2, 2), neighbor_function=four_neighbor_function)
    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]
    >>> breadth_first_search(start=(-5, -5), end=(-2, -2), neighbor_function=four_neighbor_function)
    [(-5, -5), (-4, -5), (-3, -5), (-2, -5), (-2, -4), (-2, -3), (-2, -2)]
    """
    queue = []
    visited = []
    parent = {}
    queue.append(start)
    visited.append(start)
    while queue:
        curr_node = queue.pop(0)
        if curr_node == end:
            return find_path(start, end, parent)
        else:
            curr_node_neighbors = neighbor_function(curr_node)
            for neighbor in curr_node_neighbors:
                if neighbor not in visited:
                    visited.append(neighbor)
                    parent[neighbor] = curr_node
                    queue.append(neighbor)


def sort_dict(x):
    """
    Helper function for sorting a dict for print_sorted function
    :param x: Represents a dict
    :return: Sorted dict
    """
    str_dict = {}
    for key, value in x.items():
        str_dict[str(key)] = value
    copy_dict = sorted(str_dict.items())
    new_dict = {}
    for item in copy_dict:
        if isinstance(item[1], dict):
            new_dict[item[0]] = sort_dict(item[1])
        elif isinstance(item[1], list):
            new_dict[item[0]] = sort_list(item[1])
        elif isinstance(item[1], set):
            new_dict[item[0]] = sort_set(item[1])
        elif isinstance(item[1], tuple):
            new_dict[item[0]] = sort_tuple(item[1])
        else:
            new_dict[item[0]] = item[1]
    return new_dict


def sort_list(x):
    """
    Helper function for sorting a list for print_sorted function
    :param x: Represents a list
    :return: Sorted list
    """
    new_list = []
    new_list2 = []
    for item in x:
        if isinstance(item, dict):
            new_list.append(sort_dict(item))
        elif isinstance(item, list):
            new_list.append(sort_list(item))
        elif isinstance(item, set):
            new_list.append(sort_set(item))
        elif isinstance(item, tuple):
            new_list.append(sort_tuple(item))
        else:
            new_list2.append(item)
    cpy = sorted(new_list2)
    return new_list + cpy


def sort_set(x):
    """
    Helper function for sorting a set for print_sorted function
    :param x: Represents a set
    :return: Sorted set
    """
    new_set = set()
    new_set2 = set()
    for item in x:
        if isinstance(item, dict):
            new_set.add(sort_dict(item))
        elif isinstance(item, list):
            new_set.add(sort_list(item))
        elif isinstance(item, set):
            new_set.add(sort_set(item))
        elif isinstance(item, tuple):
            new_set.add(sort_tuple(item))
        else:
            new_set2.add(item)
    cpy = sorted(new_set2)
    return new_set | set(cpy)


def sort_tuple(x):
    """
    Helper function for sorting a tuple for print_sorted function
    :param x: Represents a tuple
    :return: Sorted tuple
    """
    new_tuple = ()
    new_tuple2 = ()
    for item in x:
        if isinstance(item, dict):
            new_tuple = (*new_tuple, sort_dict(item))
        elif isinstance(item, list):
            new_tuple = (*new_tuple, sort_list(item))
        elif isinstance(item, set):
            new_tuple = (*new_tuple, sort_set(item))
        elif isinstance(item, tuple):
            new_tuple = (*new_tuple, sort_tuple(item))
        else:
            new_tuple2 = (*new_tuple2, item)
    cpy = sorted(new_tuple2)
    return new_tuple + tuple(cpy)


def print_sorted(x):
    """
    Receives as an input some deep data-structure and prints it when it is arranged in ascending order in all levels
    :param x: Represents the deep data-structure
    :return:
    >>> print_sorted({"c": (2, 1, 3), "a": {6, 5}, 10: ["d", "c", "a"], "b": 1, "d": {4: 2, 3: 4}})
    {'10': ['a', 'c', 'd'], 'a': {5, 6}, 'b': 1, 'c': (1, 2, 3), 'd': {'3': 4, '4': 2}}
    >>> print_sorted(((2, 1, 3), {6, 5}, ["d", "c", "a"], 1, {4: 2, 3: 4}))
    ((1, 2, 3), {5, 6}, ['a', 'c', 'd'], {'3': 4, '4': 2}, 1)
    >>> print_sorted([(2, 1, 3), {6, 5}, ["d", "c", "a"], 1, {4: 2, 3: 4}])
    [(1, 2, 3), {5, 6}, ['a', 'c', 'd'], {'3': 4, '4': 2}, 1]
    >>> print_sorted([(2, [6, 2, 9], {"b": 2, "a": 1}), {6, 5}, ["d", "c", "a"], 1, {4: (3, 2, 5, 1), 3: [8, 5, 2]}])
    [([2, 6, 9], {'a': 1, 'b': 2}, 2), {5, 6}, ['a', 'c', 'd'], {'3': [2, 5, 8], '4': (1, 2, 3, 5)}, 1]
    """
    if type(x) is dict:
        sorted_dict = sort_dict(x)
        print(sorted_dict)
    elif type(x) is list:
        sorted_list = sort_list(x)
        print(sorted_list)
    elif type(x) is set:
        sorted_set = sort_set(x)
        print(sorted_set)
    elif type(x) is tuple:
        sorted_tuple = sort_tuple(x)
        print(sorted_tuple)
    else:
        print(x)


if __name__ == '__main__':
    doctest.testmod()
