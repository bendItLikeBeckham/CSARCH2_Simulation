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

    if right == "":
        right = '0'
    if int(right) > 0:
         exponent =  exponent - len(right)
    return exponent + 398

def GRS(non_normalized, sign):
    temp = ""
    grs = 0
    sticky = 0
    rounded = 0
    #Check if Greater than Less than, or Equal to 19 digits
    if(len(non_normalized) == 19):
        #get digits 17-19 and make them the GRS
        grs = int(non_normalized[16:19], 10)
    elif(len(non_normalized) < 19):
        #fill up remaining digits
        while len(non_normalized) != 19:
            non_normalized = non_normalized + '0'
        grs = int(non_normalized[16:19], 10)
    elif(len(non_normalized) > 19):
        temp = non_normalized[16:18]
        #19 onwards will need to be checked
        sticky = int(non_normalized[18:], 10)
        if (sticky > 0):
            sticky = '1'
        else :
            sticky = '0'
        temp = temp + sticky
        grs = int(temp, 10)

    #GRS is always 3 digits long, meaning the basis will always be 500
    #different cases based on sign
    if (grs > 500):
        #print(sign)
        #print(grs)
        if (sign == '0'):
            #print("Addition")
            rounded = int(non_normalized[:16], 10) + 1
        else:
            #print("Subtraction")
            rounded = int(non_normalized[:16], 10) - 1
    elif(grs == 500):
        #check if even
        temp = int(non_normalized[15], 10)
        if (temp % 2 != 0):
            #change
            if (sign == '0'):
                rounded = int(non_normalized[:16], 10) + 1
            else:
                rounded = int(non_normalized[:16], 10) - 1
        else:
            rounded = int(non_normalized[:16], 10)
    elif(grs < 500):
        rounded = int(non_normalized[:16], 10)
    rounded = str(rounded)
    print(rounded)
    return rounded

def RTE(non_normalized, sign):
    temp = 0
    exponent = 0
    basis = 0
    rounded = int(non_normalized[:16], 10)
    #Check if the extra starts with a 5 or not
    temp = int(non_normalized[16], 10)
    if(temp > 5):
        rounded = rounded + 1
    elif(temp == 5):
        #check if the extra part is greater than the halfpoint
        exponent = len(non_normalized[16:])
        basis = (10**exponent)/2
        temp = int(non_normalized[16:], 10)
        if(temp > basis):
            rounded = rounded + 1
        elif (temp == basis):
            if(int(non_normalized[16], 10) % 2 != 0):
                if (sign == '0'):
                    rounded = rounded + 1
                else:
                    rounded = rounded - 1
        else:
            #stay
            rounded = rounded
    rounded = str(rounded)
    print(rounded)
    return rounded


        

    

# Returns Normalized 16 digit of the decimal
def normalize_decimal(decimal, rounding, sign):
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
    if len(ans) > 16:
        if(rounding == 0):
            ans = GRS(ans, sign)
        else:
            ans = RTE(ans, sign)
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
    for x in range(16):
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
rounding = int(input("Rounding Method (0=GRS | 1=RTE):"))

e_prime = get_e_prime(exponent, decimal)
sign_bit = check_sign(decimal)


#Split fractional and whole part into two strings
dec_string = str(decimal)
left, _, right = dec_string.partition('.')
print(left)
print(right)

normalized_input = normalize_decimal(decimal, rounding, sign_bit)
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
