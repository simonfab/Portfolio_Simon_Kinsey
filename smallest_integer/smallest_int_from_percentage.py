'''
Enter a percentage and the script will return the smallest integer
    where the supplied percentage delivers an integer...
eg 
    user inputs 88 for 88% and the smallest integer population is 25


this code has to routines in it sledge hammer which goes through all integers sequentially 
and computational 
at the moment the user entered percentage only goes through the sledgehammer method

the example numbers that print out after are for fixed example only

'''

import math
from fractions import Fraction

def get_valid_percentage():
    while True:
        try:
            user_input = input("Please enter percentage: ")
            user_perc = float(user_input)
            if 0 <= user_perc <= 100:
                return user_perc
            else:
                print("Please enter a number between 0 and 100.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


# slow sledge-hammer method:
def get_smallest_integer_for_percentage(percentage):
    # Convert the percentage to a fraction using string
    #   representation to handle floating point accurately
    percentage_fraction = Fraction(str(percentage)) / 100

    # Initialize a counter for the smallest integer
    smallest_integer = 1

    # Loop until the percentage of the integer is also an integer
    while (smallest_integer * percentage_fraction).denominator != 1:
        smallest_integer += 1

    return smallest_integer

# OR
# fast computational method

def get_smallest_integer_for_percentage_efficient(percentage):
    # Convert the percentage to a fraction using string representation
    percentage_fraction = Fraction(str(percentage)) / 100

    # The smallest integer is obtained by taking the least common multiple (LCM) of the denominators
    # after decomposing the fraction into its prime factors.
    # Mathematically, LCM of denominators of the fraction's prime factorization yields the result.
    prime_factors = decompose_to_prime_factors(percentage_fraction.denominator)
    lcm_denominator = calculate_lcm(prime_factors)

    return lcm_denominator

def decompose_to_prime_factors(n):
    """ Decompose a number into its prime factors. """
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors

def calculate_lcm(factors):
    """ Calculate the least common multiple (LCM) of a list of numbers. """
    lcm = 1
    for factor in set(factors):
        lcm *= factor ** factors.count(factor)
    return lcm

# Get required percentage
user_percentage = get_valid_percentage()

# Find the smallest integer for the given percentage
smallest_pop = get_smallest_integer_for_percentage(user_percentage)

# Display the result
print(f"The smallest integer for which {user_percentage}% "
      f"results in an integer is {smallest_pop}.")
print(f"{user_percentage}% of {smallest_pop} is "
      f"{(smallest_pop*user_percentage/100)}")

# example using fast
# Test the function with a high precision percentage
example_percentage = 16.1258
smallest_integer = get_smallest_integer_for_percentage_efficient(example_percentage)
rounded_result = round(smallest_integer * example_percentage / 100)

print(f"Example of fast method {example_percentage}% of "
      f"{smallest_integer} gives {rounded_result} population")
