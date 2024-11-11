# Thư viện trực quan hóa từng bước đi

import matplotlib.pyplot as plt

def plot_path(visited):
    x = [city['x'] for city in visited]
    y = [city['y'] for city in visited]
    city_names = [city['city'] for city in visited]

    plt.figure(figsize=(10, 8))
    plt.plot(x, y, marker='o')
    
    # Hiển thị tên thành phố
    for i, city in enumerate(city_names):
        plt.text(x[i], y[i], city, fontsize=12, ha='right')
    
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title('Travelling Salesman Path (Greedy Best-First Search)')
    plt.show()
