import sys
from collections import deque, defaultdict


prune_n = 16777216


def get_next(n):
    n = ((n*64) ^ n) % prune_n
    n = ((n // 32) ^ n) % prune_n
    n = ((n*2048) ^ n) % prune_n
    return n


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = tuple(ln.strip() for ln in f.readlines())

        r1 = 0
        all_prices = defaultdict(int)
        for ln in lines:
            prev_n = int(ln)
            deltas = deque([], 4)
            prices = defaultdict(int)
            prev_price = prev_n % 10
            for _ in range(2000):
                n = get_next(prev_n)
                price = n % 10
                delta = price - prev_price
                deltas.append(delta)
                if len(deltas) == 4 and tuple(deltas) not in prices:
                    prices[tuple(deltas)] = price
                prev_n, prev_price = n, price
            for k, v in prices.items():
                all_prices[k] += v
            r1 += prev_n

        r2 = max(all_prices.values())

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
