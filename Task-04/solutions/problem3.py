import sys


def solve():
    input = sys.stdin.readline

    t = int(input())

    for _ in range(t):
        n, c = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))

        
        if all(a[i] >= b[i] for i in range(n)):
            ans = sum(a[i] - b[i] for i in range(n))
        else:
            ans = float('inf')

        a.sort()
        b.sort()

        if all(a[i] >= b[i] for i in range(n)):
            ans = min(ans, c + sum(a[i] - b[i] for i in range(n)))

        print(-1 if ans == float('inf') else ans)


if __name__ == "__main__":
    solve()
