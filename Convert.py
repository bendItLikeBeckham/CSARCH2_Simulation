
# Gets Sign Bit
def check_sign(decimal):
    if decimal < 0:
        return 1
    else:
        return 0
    
# Gets e' value
def get_e_prime(exponent, decimal):
    dec_string = str(decimal)
    left, _, right = dec_string.partition('.')

    if int(right) > 0:
         exponent =  exponent - len(right)
    return exponent + 398

# Returns Normalized 16 digit of the decimal
def normalize_decimal(decimal, e_prime):

    dec_string = str(decimal)
    if(dec_string[0] == '-'):
        dec_string = dec_string[1:]
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

#Get group of 3 decimals for densely packed BCD
def get_grouped_decimal(normalized_input):
    coefficient_string = normalized_input[1:]

    groups = []
    for i in range(0, 15, 3):
        group = coefficient_string[i:i+3]
        groups.append(group)   
    return groups

#Converts A E I numbers of the current group to densely packed BCD equivalent

def convert_AEI_to_String(a_binary_string,e_binary_string,i_binary_string):
    if len(a_binary_string) < 3:
            num_zeroes = 3 - len(a_binary_string)
            a_binary_string = '0' * num_zeroes + a_binary_string
    if len(e_binary_string) < 3:
            num_zeroes = 3 - len(e_binary_string)
            e_binary_string = '0' * num_zeroes + e_binary_string
    if len(i_binary_string) < 3:
            num_zeroes = 3 - len(i_binary_string)
            i_binary_string = '0' * num_zeroes + i_binary_string
    
    return a_binary_string + " " + e_binary_string + " " + '0' + " " + i_binary_string + "  "

#Get the whole string of all A,E,I numbers in densely packed BCD Form
def get_BCD_values(grouped_decimal):

    major_count = 0

    BCD_string = ""

    for group in grouped_decimal:
        a = int(group[0])
        e = int(group[1])
        i = int(group[2])
        if (a > 7):
            major_count = major_count + 1
        if (e > 7):
            major_count = major_count + 1
        if (i > 7):
            major_count = major_count + 1

        if major_count == 0:
            a_binary = bin(a)
            e_binary = bin(e)
            i_binary = bin(i)

            a_binary_string = str(a_binary)
            e_binary_string = str(e_binary)
            i_binary_string = str(i_binary)

            a_binary_string = remove_0b(a_binary_string)
            e_binary_string = remove_0b(e_binary_string)
            i_binary_string = remove_0b(i_binary_string)

            BCD_string = BCD_string + convert_AEI_to_String(a_binary_string, e_binary_string,i_binary_string) + " "

    return BCD_string


decimal = float(input("Input Decimal: "))
exponent = int(input("Input Exponent: "))

e_prime = get_e_prime(exponent, decimal)
sign_bit = check_sign(decimal)

normalized_input = normalize_decimal(decimal, e_prime)
print(normalized_input)

grouped_decimal = get_grouped_decimal(normalized_input)

print("Sign","     ","Combination Field","     ","Exponent Continuation","     ","Coefficient Continuation","     ") 
print(sign_bit,"     ", get_combination_field(e_prime,normalized_input),"     ", get_exponent_field(e_prime))

print(get_BCD_values(grouped_decimal))


