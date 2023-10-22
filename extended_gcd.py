def extended_gcd(a, m):
    x0, x1, y0, y1 = 1, 0, 0, 1
    og_a, og_m = a, m  #to print result 
    while m != 0:
        q, a, m = a // m, m, a % m
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1

    if a != 1:
        print("Inverse doesn't exist!")
    else:
        print(f"The multiplicative inverse of {og_a} mod {og_m} is {x0 % og_m}")

# Test
extended_gcd(1234,4321)
extended_gcd(550, 1769)
