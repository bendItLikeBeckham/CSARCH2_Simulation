from decimal import Decimal


# Gets Sign Bit
def check_sign(decimal):
    if decimal < 0:
        return '1'
    else:
        return '0'
    
# Gets e' value
def get_e_prime(exponent, decimal):
    dec_string = str(decimal)
    left, _, right = dec_string.partition('.')

    if int(right) > 0:
         exponent =  exponent - len(right)
    return exponent + 398

# Returns Normalized 16 digit of the decimal
def normalize_decimal(decimal):

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
            ans += '0'
        if ans[-1] == '0':
            ans = ans[:-1]

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
    if len(string_three_digits) == 4:
         string_three_digits = string_three_digits[1:]

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


# Gets binary value of a digit and converts it to binary string equivalent

def get_binary_digit_to_string(num):
    binary_num = bin(num)
    binary_num_string = str(binary_num)
    binary_num_string = remove_0b(binary_num_string)

    return binary_num_string

#Get the whole string of all A,E,I numbers in densely packed BCD Form
def get_BCD_values(grouped_decimal):

    major_count = 0

    BCD_string = ""

    for group in grouped_decimal:
        major_count = 0
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
            a_binary_string = get_binary_digit_to_string(a)
            e_binary_string = get_binary_digit_to_string(e)
            i_binary_string = get_binary_digit_to_string(i)

            BCD_string = BCD_string + convert_AEI_to_String(a_binary_string, e_binary_string,i_binary_string) + " "
        
        if major_count == 2:
             
            if a < 8:
                col_bit = "10"
                first_byte = bin(a)
            elif e < 8:
                col_bit = "01"
                first_byte = bin(e)
            elif i < 8:
                col_bit = "00"
                first_byte = bin(i)

            first_byte_string = str(first_byte)
            first_byte_string = remove_0b(first_byte_string)

            if len(first_byte_string) == 1:
                first_byte_string = "0" + first_byte_string
            
            if len(first_byte_string) == 3:
                first_byte_string = first_byte_string[:2]

            d_string = get_binary_digit_to_string(a)
            h_string = get_binary_digit_to_string(e)
            m_string = get_binary_digit_to_string(i)

            if len(d_string) > 1:
                d_string = d_string[-1]
            if len(h_string) > 1:
                h_string = h_string[-1]
            if len(m_string) > 1:
                m_string = m_string[-1]
             

            BCD_string = BCD_string + first_byte_string + d_string +" "+ col_bit + h_string + " " + "1" +" "+ "11" + m_string + " "

    return BCD_string


decimal = Decimal(input("Input Decimal: "))
exponent = int(input("Input Exponent: "))

e_prime = get_e_prime(exponent, decimal)
sign_bit = check_sign(decimal)

dec_string = str(decimal)
left, _, right = dec_string.partition('.')

print(left)
print(right)

normalized_input = normalize_decimal(decimal)
print("Normalized Input: " + normalized_input)

grouped_decimal = get_grouped_decimal(normalized_input)

print("Sign","     ","Combination Field","     ","Exponent Continuation") 
print(sign_bit,"        ", get_combination_field(e_prime,normalized_input),"                 ", get_exponent_field(e_prime))
print("Coefficient Continuation","     ")
print(get_BCD_values(grouped_decimal))


