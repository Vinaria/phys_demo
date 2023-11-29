

def temp_diap(x):
    start = 0
    end = 5000
    if x.isdigit():
        if start < int(x) <= end:
            return ''
        return 'Диапазон значений температуры: (' + str(start) + '; ' + str(end) + '].'
    return 'Вы можете вводить только целые числа'

def width_diap(x):
    start = 0
    end = 150
    if x.isdigit():
        if start < int(x) <= end:
            return ''
        return 'Диапазон значений ширины ямы: (' + str(start) + '; ' + str(end) + '].'
    return 'Вы можете вводить только целые числа'


def depth_diap(x):
    start = 0
    end = 500
    if x.isdigit():
        if start < int(x) <= end:
            return ''
        return 'Диапазон значений глубины ямы: (' + str(start) + '; ' + str(end) + '].'
    return 'Вы можете вводить только целые числа'


def size_diap(x):
    start = 0
    end = 25
    if x.isdigit():
        if start < int(x) <= end:
            return ''
        return 'Диапазон размеров частицы: (' + str(start) + '; ' + str(end) + '].'
    return 'Вы можете вводить только целые числа'


def jump_diap(x):
    start = 0
    end = 50
    if x.isdigit():
        if start <= int(x) <= end:
            return ''
        return 'Диапазон значений расстояния между ямами: (' + str(start) + '; ' + str(end) + '].'
    return 'Вы можете вводить только целые числа'