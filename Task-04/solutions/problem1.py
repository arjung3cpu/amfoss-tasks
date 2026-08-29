import sys


def generate_primes(count):
    limit = 200000
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False

    primes = []

    for number in range(2, limit + 1):
        if sieve[number]:
            primes.append(number)

            if len(primes) == count:
                return primes

            if number * number <= limit:
                for multiple in range(number * number, limit + 1, number):
                    sieve[multiple] = False

    return primes


def main():
    input = sys.stdin.readline

    t = int(input())

    ns = [int(input()) for _ in range(t)]
    max_n = max(ns)

    primes = generate_primes(max_n + 1)

    for n in ns:
        answer = [primes[i] * primes[i + 1] for i in range(n)]
        print(*answer)


if __name__ == "__main__":
    main()
