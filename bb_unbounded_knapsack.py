from memory_profiler import memory_usage
import time
import numpy as np
import math
"""
Airel Camilo Khairan
2106652581
Modified from: https://www.tandfonline.com/doi/pdf/10.1057/palgrave.jors.2601698?casa_token=EW35GGben2sAAAAA%3AVZt6DkysIcc7im289FIjHbV6Q3nZr2vYAH_HtWInlRnwryJnWsXKK87_g478Gof5mB_MDiz29IDO1eA
"""

# Branch and Bound
class UnboundedKnapsack:
    def __init__(self, W, v, w):
        self.W = W
        self.n = len(w)
        self.v = v
        self.w = w
        self.N = []

    def elim_dominated_items(self):
        # Kompleksitas: O(n^2)
        self.N = [i for i in range(self.n)]
        for j in range(0, len(self.N)-1):
            for k in range(j+1, len(self.N)):
                if math.floor(self.w[k] / self.w[j]) * self.v[j] >= self.v[k] and k in self.N:
                    self.N.remove(k)
                elif math.floor(self.w[j] / self.w[k]) * self.v[k] >= self.v[j] and j in self.N:
                    self.N.remove(j)
                    break

    def initialize(self):
        # STEP 1
        self.elim_dominated_items()
        self.N = self.sort_N()
        self.xhat, self.x, self.i, self.zhat = np.zeros(self.n), np.zeros(self.n), 0, 0
        self.M = np.zeros(shape=(len(self.N), self.W))
        Ni = self.N[self.i]
        self.x[Ni] = math.floor(self.W / self.w[Ni])
        self.V = self.v[Ni] * self.x[Ni]
        self.Wres = self.W - self.w[Ni] * self.x[Ni]
        self.U = self.upper_bound(self.i, self.W)
        self.m = self.find_mi()

    def sort_N(self):
        return sorted(self.N, key=lambda n: self.v[n]/self.w[n], reverse=True)

    def upper_bound(self, i, W):
        # Calculate upper bound
        j1 = self.N[i]
        w1, v1 = self.w[j1], self.v[j1]
        W1 = W - math.floor(W / w1) * w1
        U = math.floor(W / w1) * v1

        if i+1 < len(self.N):
            j2 = self.N[i+1]
            w2, v2 = self.w[j2], self.v[j2]
            z1 = math.floor(W / w1) * v1 + math.floor(W1 / w2) * v2
            W2 = W1 - math.floor(W1 / w2) * w2
            U1 = z1
            U21 = (W2 + math.ceil((w2 - W2) / w1) * w1) * v2 / w2
            U22 = math.ceil((w2 - W2) / w1) * v1
            U2 = z1 + math.floor(U21 - U22)
        
            if i+2 < len(self.N):
                j3 = self.N[i+2]
                w3, v3 = self.w[j3], self.v[j3]
                U1 = z1 + math.floor(W2 * v3 / w3)
            U = max(U1, U2)
        return U
    
    def find_mi(self):
        # Mencari w minimum untuk index j > i
        m = []
        mi_index = 0
        for i in range(len(self.N)):
            if i < mi_index:
                m.append(mi)
            mi = float("inf")
            mi_index = i
            for j in range(i+1, len(self.N)):
                if self.w[self.N[j]] < mi:
                    mi = self.w[self.N[j]]
                    mi_index = j
            m.append(mi)
        return m
    
    def develop(self):
        # STEP 2
        if self.Wres < self.m[self.i]:
            if self.zhat < self.V:
                self.zhat = self.V
                self.xhat = self.x

                if self.zhat == self.U:
                    # STEP 5
                    raise Exception("FINISH")
                
            # STEP 3
            self.backtrack()
            return
        else:
            j = self.find_min_j()
            U = self.upper_bound(j, self.Wres)

            # Nilai node dan upper bound lebih rendah dari solusi nilai terbaik
            if self.V + U <= self.zhat:
                # STEP 3
                self.backtrack()

            # Total maksimum value node sebelumnya lebih tinggi
            if self.M[self.i, int(self.Wres)] >= self.V:
                # STEP 3
                self.backtrack()

            # Tambahkan item ke-Nj
            Nj = self.N[j]
            self.x[Nj] = math.floor(self.Wres / self.w[Nj])
            self.V += self.v[Nj] * self.x[Nj]
            self.Wres -= self.w[Nj] * self.x[Nj]
            self.M[self.i, int(self.Wres)] = self.V
            self.i = j

            # STEP 2
            self.develop()

    def find_min_j(self):
        # Mencari item selanjutnya (j) yang dapat dimasukkan
        for n, j in enumerate(self.N[self.i+1:], start=self.i+1):
            if self.w[j] <= self.Wres:
                return n
            
        # Jika tidak ada item selanjutnya yang dapat dimasukkan
        if self.zhat < self.V:
            self.zhat = self.V
            self.xhat = self.x

        # STEP 3
        self.backtrack()

    def backtrack(self):
        # STEP 3
        j = self.find_max_j()

        # Tidak ada item sebelumnya untuk backtrack
        if j < 0:
            # STEP 5
            raise Exception("FINISH")

        # Mengurangi satu item j
        self.i = j
        Ni = self.N[self.i]
        self.x[Ni] -= 1
        self.V -= self.v[Ni]
        self.Wres += self.w[Ni]

        # Belum ada item selanjutnya yang dapat dimasukkan
        if self.Wres < self.m[self.i]:
            # STEP 3
            self.backtrack()

        if self.i+1 < len(self.N):
            Ni1 = self.N[self.i+1]
            # Memasukkan item selanjutnya, tetapi total nilai lebih rendah
            # daripada solusi nilai terbaik
            if self.V + math.floor(self.Wres * self.v[Ni1] / self.w[Ni1]) <= self.zhat:
                self.V -= self.v[Ni] * self.x[Ni]
                self.Wres += self.w[Ni] * self.x[Ni]
                self.x[Ni] = 0

                # STEP 3
                self.backtrack()

        # Selum kurang 1 item j, masih bisa develop
        if self.Wres - self.w[Ni] >= self.m[Ni]:
            # STEP 2
            self.develop()

        # STEP 4
        self.replace(self.i, self.i+1)

    def find_max_j(self):
        # Mencari item dengan index j terakhir yang dimasukkan
        for n, j in enumerate(reversed(self.N[:self.i+1]), start=self.i):
            if self.x[j] > 0:
                return n
        
        # STEP 5
        raise Exception("FINISH")

    def replace(self, j, h):
        # STEP 4
        if h >= len(self.N):
            # STEP 5
            raise Exception("Finish")
        Nj = self.N[j]
        Nh = self.N[h]
        
        if self.zhat >= self.V + math.floor(self.Wres * self.v[Nh] / self.w[Nh]):
            # STEP 3
            self.backtrack()
        if self.w[Nh] >= self.w[Nj]:
            if self.w[Nh] == self.w[Nj] or self.w[Nh] > self.Wres or self.zhat >= self.V + self.v[Nh]:
                h += 1
                # STEP 4
                self.replace(j, h)
            self.zhat = self.V + self.v[Nh]
            self.xhat = self.x
            self.x[Nh] = 1
            if self.zhat == self.U:
                # STEP 5
                raise Exception("FINISH")
            j = h
            h += 1

            # STEP 4
            self.replace(j, h)
        else:
            if self.Wres - self.w[Nh] < self.m[self.N[h-1]]:
                h += 1

                # STEP 4
                self.replace(j, h)
            self.i = h
            Ni = self.N[self.i]
            self.x[Ni] = math.floor(self.Wres / self.w[Ni])
            self.V += self.v[Ni] * self.x[Ni]
            self.Wres -= self.w[Ni] * self.x[Ni]

            # STEP 2
            self.develop()

    def start(self):
        try:
            # Kompleksitas: 
            # O(n^2) untuk menghapus item yang terdominasi
            # O(n'logn') untuk sorting array N
            #   O(2^n') untuk branch and bound 
            # Anggap n' konstan sehingga total kompleksitas: O(n^2) + O(1) + O(1) = O(n^2)
            self.initialize()
            self.develop()
        except:
            return (int(self.zhat), self.xhat)
        return (int(self.zhat), self.xhat)


if __name__ == '__main__':
    with open("dataset.txt", "r") as file:
        for _ in range(3):
            n, _ = file.readline().split(" ")
            w = [int(num) for num in file.readline().split(" ")]
            v = [int(num) for num in file.readline().split(" ")]
            W = int(0.1 * sum(w))
            print(f"Ukuran {n}")
            print(f"Weight knapsack : {W}")

            memory_before = memory_usage()[0]
            start_time = time.perf_counter()

            knapsack = UnboundedKnapsack(W, v, w)
            res, a = knapsack.start()
            print(f"Best value      : {res}")

            total_runtime = time.perf_counter() - start_time
            memory_used = memory_usage()[0] - memory_before
            
            print(f"Total runtime   : {(total_runtime):.4f}s")
            print(f"Memory usage    : {(memory_used * 1024):.4f}KiB\n")