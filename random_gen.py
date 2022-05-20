from typing import Generator

def lcg(modulus: int, a: int, c: int, seed: int) -> Generator[int, None, None]:
    """Linear congruential generator."""
    while True:
        seed = (a * seed + c) % modulus
        yield seed

class RandomGen:
    
    def __init__(self, seed: int = 0) -> None:
        self.seed = seed


    def randint(self, k: int) -> int:
        num = []
        res = ""
        it = lcg(pow(2,32), 1347758132132, 1, self.seed)
        it.__next__()
        for i in range(5):
            ran = it.__next__()
            ran = ran >> 16
            num.append(format(ran, '016b'))
        for j in range(16):
            count = 0
            for h in range(5):
                if num[h][j] == "1":
                    count += 1
            res += str(count)
        res1 = ""
        for l in res:
            if int(l) >= 3:
                res1 += "1"
            else:
                res1 += "0"
        return int(res1, 2) % k + 1

if __name__ == "__main__":
    Random_gen = lcg(pow(2,32), 134775813, 1, 0)
