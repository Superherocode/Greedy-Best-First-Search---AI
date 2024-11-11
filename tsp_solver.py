# Chứa thuật toán GBFS cho TSP

import pandas as pd
import numpy as np

def load_cities(file_path):
    return pd.read_csv(file_path)

def distance(city1, city2):
    return np.sqrt((city1['x'] - city2['x'])**2 + (city1['y'] - city2['y'])**2)

def greedy_best_first_search(cities):
    start_city = cities.iloc[0]  # Bắt đầu từ thành phố đầu tiên trong danh sách
    visited = [start_city]
    total_distance = 0

    current_city = start_city
    remaining_cities = cities.iloc[1:].copy()  # Các thành phố chưa ghé thăm

    while not remaining_cities.empty:
        # Tìm thành phố gần nhất
        next_city = remaining_cities.iloc[
            np.argmin(remaining_cities.apply(lambda city: distance(current_city, city), axis=1))
        ]
        total_distance += distance(current_city, next_city)
        visited.append(next_city)
        remaining_cities = remaining_cities[remaining_cities['city'] != next_city['city']]
        current_city = next_city

    # Trở về thành phố bắt đầu
    total_distance += distance(current_city, start_city)
    visited.append(start_city)

    return visited, total_distance
