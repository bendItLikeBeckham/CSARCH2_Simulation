from decimal import Decimal

# Define rounding methods
def round_towards_negative_infinity(value):
    if value >= 0:
        return int(value)
    else:
        return int(value) - 1

def round_towards_positive_infinity(value):
    if value >= 0:
        return int(value) + 1
    else:
        return int(value)

def truncate_towards_zero(value):
    return int(value)

def round_to_nearest(value):
    integer_part = int(value)
    fractional_part = value - integer_part
    
    # If the fractional part is exactly 0.5, round towards the nearest even integer
    if fractional_part == 0.5:
        # If the integer part is even, round towards it
        if integer_part % 2 == 0:
            return integer_part
        # If the integer part is odd, round away from it
        else:
            return integer_part + 1
    # Otherwise, round as usual
    else:
        return int(value + 0.5) if value >= 0 else int(value - 0.5)


# Round the decimal value based on the chosen rounding method
def round_decimal(decimal, rounding_method):
    if rounding_method == "floor":
        return round_towards_negative_infinity(decimal)
    elif rounding_method == "ceiling":
        return round_towards_positive_infinity(decimal)
    elif rounding_method == "truncate":
        return truncate_towards_zero(decimal)
    elif rounding_method == "round":
        return round_to_nearest(decimal)
    else:
        print("Invalid rounding method specified.")
        return None

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

    if right == "":
        right = '0'
    if int(right) > 0:
         exponent =  exponent - len(right)
    return exponent + 398

# Returns Normalized 16 digit of the decimal
def normalize_decimal(decimal):

    #Splits up the whole number and fractional to left and right respectively (Removes '-' as well)
    dec_string = str(decimal)
    if(dec_string[0] == '-'):
        dec_string = dec_string[1:]
    left, _, right = dec_string.partition('.')


    #Get the combined string and removes last bit if it is 0
    ans = left + right
    if right == "":
        right = '0'
    if int(right) == 0:
            ans = left

    #If kulang ung decimal       
    if len(ans) < 16:
        num_zeros = 16 - len(ans)
        ans = '0' * num_zeros + left
        if int(right) != 0:
            ans += right
        else:
            ans += '0'
        if ans[-1] == '0':
            ans = ans[:-1]
    
    #Put round up here

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


    if (normalized_input[0] != '8' and normalized_input[0] !='9'):
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

        whole_combi = first_2_combi + string_three_digits
    else:
        if len(string_e_prime_binary) < 10:
            num_zeros = 10 - len(string_e_prime_binary)
            string_e_prime_binary = '0' * num_zeros  + string_e_prime_binary

        first_2_combi = string_e_prime_binary[:2]
        if (normalized_input[0] == '8'):
            last_digit = '0'
        elif (normalized_input[0] == '9'):
            last_digit = '1'
        whole_combi =  '11' + first_2_combi + last_digit

    return whole_combi

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
    
    #return a_binary_string + " " + e_binary_string + " " + '0' + " " + i_binary_string + "  "
    return a_binary_string + e_binary_string + '0' + i_binary_string



# Gets binary value of a digit and converts it to binary string equivalent

def get_binary_digit_to_string(num):
    binary_num = bin(num)
    binary_num_string = str(binary_num)
    binary_num_string = remove_0b(binary_num_string)

    return binary_num_string

# Gets binary value of the 2 bits for the BCD
def get_binary_byte_to_string(byte):
    byte_string = remove_0b(byte)

    if len(byte_string) == 1:
        byte_string = "0" + byte_string
                
    if len(byte_string) == 3:
        byte_string = byte_string[:2]
    
    return byte_string

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

            #BCD_string = BCD_string + convert_AEI_to_String(a_binary_string, e_binary_string,i_binary_string) + " "
            BCD_string = BCD_string + convert_AEI_to_String(a_binary_string, e_binary_string,i_binary_string)


        elif major_count == 1:
            if a > 7:
                col_bit = "10"
                third_byte = bin(a)
            elif e > 7:
                col_bit = "01"
                third_byte = bin(e)
            elif i > 7:
                col_bit = "00"
                third_byte = bin(i)

            d_string = get_binary_digit_to_string(a)
            h_string = get_binary_digit_to_string(e)
            m_string = get_binary_digit_to_string(i)

            if len(d_string) > 1:
                d_string = d_string[-1]
            if len(h_string) > 1:
                h_string = h_string[-1]
            if len(m_string) > 1:
                m_string = m_string[-1]
            
            if e < 8 and i < 8:
                first_byte_string = get_binary_byte_to_string(str(bin(i)))
                second_byte_string = get_binary_byte_to_string(str(bin(e)))           
            if e < 8 and a < 8:
                first_byte_string = get_binary_byte_to_string(str(bin(a)))
                second_byte_string = get_binary_byte_to_string(str(bin(e)))
            if  a < 8 and i < 8:
                first_byte_string = get_binary_byte_to_string(str(bin(a)))
                second_byte_string = get_binary_byte_to_string(str(bin(i)))
                    
            #BCD_string = BCD_string + first_byte_string + d_string +" "+ second_byte_string + h_string + " " + "1" +" "+ col_bit + m_string + " "
            BCD_string = BCD_string + first_byte_string + d_string + second_byte_string + h_string + "1" + col_bit + m_string

        
        elif major_count == 2:
             
            if a < 8:
                col_bit = "10"
                first_byte = bin(a)
            elif e < 8:
                col_bit = "01"
                first_byte = bin(e)
            elif i < 8:
                col_bit = "00"
                first_byte = bin(i)

            first_byte_string = get_binary_byte_to_string(str(first_byte))
    
            d_string = get_binary_digit_to_string(a)
            h_string = get_binary_digit_to_string(e)
            m_string = get_binary_digit_to_string(i)

            if len(d_string) > 1:
                d_string = d_string[-1]
            if len(h_string) > 1:
                h_string = h_string[-1]
            if len(m_string) > 1:
                m_string = m_string[-1]
             

            #BCD_string = BCD_string + first_byte_string + d_string +" "+ col_bit + h_string + " " + "1" +" "+ "11" + m_string + " "
            BCD_string = BCD_string + first_byte_string + d_string + col_bit + h_string + "1" +"11" + m_string

    return BCD_string

def hex_to_binary (complete_binary):
    #Hex to binary
    binary = ""
    full_Hex = ""
    binary = complete_binary

    start = 0
    end = 4

    #Every binary is 64 bits long
    for x in range(11):
        #4 bits at a time
        sub = binary[start:end]
        decimal = int(sub, 2) #decinal
        temp = hex(decimal)
        full_Hex = full_Hex + temp[2]

        #increment
        start = start + 4
        end = end + 4

    return full_Hex

decimal = Decimal(input("Input Decimal: "))
exponent = int(input("Input Exponent: "))

e_prime = get_e_prime(exponent, decimal)
sign_bit = check_sign(decimal)


#Split fractional and whole part into two strings
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


print("Full Binary Representation not split")
complete_binary = sign_bit + get_combination_field(e_prime,normalized_input) + get_exponent_field(e_prime) + get_BCD_values(grouped_decimal)
print("-------------------------------------------")
print(complete_binary)
print("-------------------------------------------")
hexed = hex_to_binary(complete_binary)
print(hexed.upper())
