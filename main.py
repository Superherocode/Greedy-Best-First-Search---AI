# Tệp chính để chạy dự án

import time
from tsp_solver import load_cities, greedy_best_first_search
from visualizer import plot_path

def main():
    cities = load_cities('data/cities.csv')
    start_time = time.time()
    
    visited, total_distance = greedy_best_first_search(cities)
    end_time = time.time()
    execution_time = end_time - start_time

    print(f"Total distance: {total_distance}")
    print(f"Execution time: {execution_time:.4f} seconds")

    plot_path(visited)

if __name__ == "__main__":
    main()
