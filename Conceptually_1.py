import math
import time

# 1. Базис: 8 вершин куба (алгебраические объекты)
vertices = [
    [-1, -1, -1], [1, -1, -1],
    [1, 1, -1], [-1, 1, -1],
    [-1, -1, 1], [1, -1, 1],
    [1, 1, 1], [-1, 1, 1]
]

# Топология: ребра как пары индексов базиса (матрица связности)
edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

def rotate_x(points, angle):
    s, c = math.sin(angle), math.cos(angle)
    return [[x, y * c - z * s, y * s + z * c] for x, y, z in points]

def rotate_y(points, angle):
    s, c = math.sin(angle), math.cos(angle)
    return [[x * c + z * s, y, -x * s + z * c] for x, y, z in points]

def project(point, width, height, scale):
    # Проекция из 3D алгебраического пространства в 2D терминальное
    x, y, z = point
    # Увеличено смещение по Z (z + 6) и уменьшен множитель масштаба,
    # чтобы куб гарантированно помещался в область видимости 80x40
    factor = (scale / 2) / (z + 6)  
    sx = int(width / 2 + x * factor * width / 2)
    sy = int(height / 2 - y * factor * height / 2)
    return sx, sy

def draw_frame(angle_x, angle_y, width=80, height=40, scale=10):
    buffer = [[' ' for _ in range(width)] for _ in range(height)]
    
    # Блок 2: Применение матрицы вращения (схлопывание функции состояния)
    rotated = rotate_x(vertices, angle_x)
    rotated = rotate_y(rotated, angle_y)
    
    # Блок 3: Проектирование векторного пространства на экран
    projected_2d = []
    for v in rotated:
        projected_2d.append(project(v, width, height, scale))
        
    # Отрисовка ребер с проверкой выхода за границы буфера
    for start, end in edges:
        x0, y0 = projected_2d[start]
        x1, y1 = projected_2d[end]
        
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        
        while True:
            # Строгая проверка: символ ставится только внутри массива
            if 0 <= x0 < width and 0 <= y0 < height:
                buffer[y0][x0] = '#'
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy
                
    # Сборка финальной строки (обновление данных перед выводом)
    frame_str = '\n'.join([''.join(row) for row in buffer])
    return frame_str

width, height = 80, 40
angle_x, angle_y = 0, 0

try:
    while True:
        # Очистка экрана (ANSI-последовательность возврата каретки и очистки)
        print("\033[H\033[J", end="") 
        
        # Генерация обновленного кадра
        current_frame = draw_frame(angle_x, angle_y, width, height)
        
        # Вывод готового строкового представления
        print(current_frame)
        
        # Обновление углов для следующего "хлопка" (шага симуляции)
        angle_x += 0.04
        angle_y += 0.03
        time.sleep(0.05)
except KeyboardInterrupt:
    pass
