import sys


def solve():
    input = sys.stdin.readline
    t = int(input())

    for _ in range(t):
        x = int(input())

        d = len(str(x))
        y = 10 ** d + 1

        print(y)


if __name__ == "__main__":
    solve()
