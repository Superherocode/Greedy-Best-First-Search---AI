import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


# Tạo ma trận khoảng cách ngẫu nhiên dựa trên số lượng thành phố
def create_distance_matrix(num_cities):
    distance_matrix = []
    for i in range(num_cities):
        row = []
        for j in range(num_cities):
            if i == j:
                row.append(0)
            elif j > i:
                row.append(random.randint(1, 300))
            else:
                row.append(distance_matrix[j][i])
        distance_matrix.append(row)
    return distance_matrix


# Tính độ dài quãng đường
def routeLength(tsp, solution):
    total_length = 0
    for i in range(len(solution) - 1):
        total_length += tsp[solution[i]][solution[i + 1]]
    return total_length


class GreedyTSP():
    def __init__(self, num_cities):
        self.num_cities = num_cities
        self.matrix = create_distance_matrix(num_cities)  # Tạo ma trận khoảng cách chỉ một lần
        self.result = None
        self.path = []  # Đường đi theo thứ tự các thành phố
        self.total_distance = 0  # Tổng độ dài của hành trình
        self.steps = 0  # Số bước thực hiện


    def create_plot(self):
        # Vẽ tất cả các thành phố và khoảng cách giữa các thành phố
        distance = np.array(self.matrix)
        G = nx.from_numpy_array(distance)
        pos = nx.spring_layout(G)
       
        # Vẽ tất cả các đỉnh (thành phố)
        nx.draw_networkx_nodes(G, pos, node_color='r', node_size=500)
        nx.draw_networkx_labels(G, pos)
       
        # Vẽ tất cả các cạnh với trọng số
        all_edges = [(i, j) for i in range(self.num_cities) for j in range(i + 1, self.num_cities)]
        nx.draw_networkx_edges(G, pos, edgelist=all_edges, edge_color='blue', style='dotted')
       
        # Hiển thị trọng số của các cạnh
        edge_labels = {(i, j): self.matrix[i][j] for i in range(self.num_cities) for j in range(i + 1, self.num_cities)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, font_color="blue")


        # Vẽ hành trình Greedy
        edges = [(self.path[i], self.path[i + 1]) for i in range(len(self.path) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color='green', style='solid', width=2)
       
        # Hiển thị đồ thị
        plt.show()
   
    def solve(self):
        # In ma trận khoảng cách để kiểm tra các giá trị
        print("Ma trận khoảng cách giữa các thành phố:")
        for row in self.matrix:
            print(row)
       
        current_city = 0
        unvisited = set(range(1, self.num_cities))  # Tập các thành phố chưa thăm
        self.path = [current_city]
       
        while unvisited:
            # Tìm thành phố gần nhất chưa thăm
            nearest_city = min(unvisited, key=lambda city: self.matrix[current_city][city])
            # In chi tiết thành phố gần nhất được chọn và khoảng cách tới nó
            print(f"Từ thành phố {current_city} đến thành phố {nearest_city} với khoảng cách {self.matrix[current_city][nearest_city]}")
            self.path.append(nearest_city)
            unvisited.remove(nearest_city)
            current_city = nearest_city
            self.steps += 1  # Tăng số bước mỗi lần chọn thành phố
       
        # Quay lại điểm xuất phát
        self.path.append(0)
        print(f"Từ thành phố {current_city} quay lại thành phố 0 với khoảng cách {self.matrix[current_city][0]}")


        # Tính tổng độ dài quãng đường
        self.total_distance = routeLength(self.matrix, self.path)
       
        # Lưu kết quả vào self.result
        self.result = f"Đường đi theo Greedy: {self.path}\nTổng độ dài: {self.total_distance}\nSố bước thực hiện: {self.steps}\n"
        return self.path


# Hàm main để chạy GreedyTSP và kiểm tra kết quả
def main():
    # Nhập vào số lượng thành phố
    num_cities = int(input("Số lượng thành phố cần đi qua: "))


    if num_cities >= 2:
        tsp = GreedyTSP(num_cities)
        tsp.solve()
        print(tsp.result)
        tsp.create_plot()
    else:
        print("Hãy nhập số lượng thành phố >= 2 !!!")


if __name__ == "__main__":
    main()
