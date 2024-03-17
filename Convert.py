
# Gets Sign Bit
def check_sign(decimal):
    if decimal < 0:
        return 1
    else:
        return 0
    
# Gets e' value
def get_e_prime(exponent):
    return exponent + 398

# Returns Normalized 16 digit of the decimal
def normalize_decimal(decimal):
    dec_string = str(decimal)
    left, _, right = dec_string.partition('.')

    ans = left + right
    if ans[-1] == '0':
            ans = ans[:-1]
            
    if len(ans) < 16:
        num_zeros = 16 - len(ans)
        ans = '0' * num_zeros + left
        if right:
            ans += right
        else:
            ans += '0' * num_zeros
        if ans[-1] == '0':
            ans = ans[:-1]
            ans = '0' + ans

    return ans

# Removes the "0b" at the start of a binary string after it is converted
def remove_0b(string):
    ans = string[2:]
    return ans

# Get combination field
def get_combination_field(e_prime, normalized_input):
    e_prime_binary = bin(e_prime)
    string_e_prime_binary = str(e_prime_binary)
    string_e_prime_binary = remove_0b(string_e_prime_binary)

    if len(string_e_prime_binary) < 10:
        num_zeros = 10 - len(string_e_prime_binary)
        string_e_prime_binary = '0' * num_zeros  + string_e_prime_binary

    first_2_combi = string_e_prime_binary[:2]

    last_three_digits = bin(int(normalized_input[0]))
    string_three_digits = str(last_three_digits)
    string_three_digits = remove_0b(string_three_digits)

    if len(string_three_digits) < 3:
        num_zeros = 3 - len(string_three_digits)
        string_three_digits = '0' * num_zeros  + string_three_digits 
    return first_2_combi + string_three_digits

#Get Exponent Continuation
def get_exponent_field(e_prime):
    e_prime_binary = bin(e_prime)
    string_e_prime_binary = str(e_prime_binary)
    string_e_prime_binary = remove_0b(string_e_prime_binary)

    if len(string_e_prime_binary) < 10:
        num_zeros = 10 - len(string_e_prime_binary)
        string_e_prime_binary = '0' * num_zeros  + string_e_prime_binary

    last_8_exponent = string_e_prime_binary[2:]

    return last_8_exponent



decimal = float(input("Input Decimal: "))
exponent = int(input("Input Exponent: "))

e_prime = get_e_prime(exponent)
sign_bit = check_sign(decimal)

normalized_input = normalize_decimal(decimal)
print(normalized_input)



print("Sign","     ","Combination Field","     ","Exponent Continuation","     ","Coefficient Continuation","     ") 
print(sign_bit,"     ", get_combination_field(e_prime,normalized_input),"     ", get_exponent_field(e_prime))