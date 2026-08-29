import sys


def solve():
    input = sys.stdin.readline

    t = int(input())

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        ans = 0

        for x in a:
            if ans > x:
                ans += x
            else:
                ans = x

        print(ans)


if __name__ == "__main__":
    solve()
