import random
"""
Airel Camilo Khairan
2106652581
"""

class GenerateDataset:
    @staticmethod
    def generate(n):
        random.seed(n)
        w = [random.randint(10, 100) for _ in range(n)]
        v = [wi + 100 for wi in w]
        return (w, v)

if __name__ == '__main__':
    with open("dataset.txt", "w") as file:
        for n in [100, 1000, 10000]:
            w, v = GenerateDataset.generate(n)
            file.write(str(n))
            file.write(' \n')
            file.write(' '.join([str(i) for i in w]))
            file.write('\n')
            file.write(' '.join([str(i) for i in v]))
            file.write('\n')