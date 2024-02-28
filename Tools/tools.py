def sum(a,b):
    return a+b

def prime_fib_sum(n):
    def is_prime(num):
        if num <= 1:
            return False
        for i in range(2, int(num**0.5) + 1):
            if num % i == 0:
                return False
        return True

    count, num, sum_primes = 0, 2, 0
    while count < n:
        if is_prime(num):
            sum_primes += num
            count += 1
        num += 1

    if n <= 0:
        sum_fibs = 0
    else:
        fib1, fib2 = 0, 1
        sum_fibs = fib1 + fib2
        for _ in range(2, n):
            fib_next = fib1 + fib2
            sum_fibs += fib_next
            fib1, fib2 = fib2, fib_next

    return sum_primes + sum_fibs
