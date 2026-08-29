import sys


def solve():
    input = sys.stdin.readline
    t = int(input())

    for _ in range(t):
        s = input().strip()
        n = len(s)

        pref1 = [0] * (n + 1)
        pref2 = [0] * (n + 1)
        pref3 = [0] * (n + 1)

        for i, ch in enumerate(s):
            pref1[i + 1] = pref1[i] + (ch == '1')
            pref2[i + 1] = pref2[i] + (ch == '2')
            pref3[i + 1] = pref3[i] + (ch == '3')
        best = 0

        for split in range(n + 1):
            left_2 = pref2[split]
            right_13 = (pref1[n] - pref1[split]) + (pref3[n] - pref3[split])
            best = max(best, left_2 + right_13)

        print(n - best)


if __name__ == "__main__":
    solve()
