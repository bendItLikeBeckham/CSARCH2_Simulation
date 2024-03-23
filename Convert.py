import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

from decimal import Decimal, InvalidOperation

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
def normalize_decimal(decimal, rounding_method, sign_bit):
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
        if rounding_method == "Floor":
            if sign_bit == '1':
                ans = ans[:16]
                ans_int = int(ans) + 1
                ans = str(ans_int)
            elif sign_bit == '0':
                ans = ans[:16]
        elif rounding_method == "Ceiling":
            if sign_bit == '1':
                ans = ans[:16]
            elif sign_bit == '0':
                ans = ans[:16]
                ans_int = int(ans) + 1
                ans = str(ans_int)                
        elif rounding_method == "Truncate":
            ans = ans[:16]
        elif rounding_method == "RTN":
            extra_numbers = ans[16:]
            ans = ans[:16]
            ans_int = int(ans)
            right_zeroes = len(extra_numbers)
            check_num = '1' + '0' * right_zeroes
            check_num = int(check_num) / 2
            extra_numbers = int(extra_numbers)

            if extra_numbers < check_num:
                ans = str(ans_int)
            elif extra_numbers > check_num:
                ans = str(ans_int + 1)
            elif extra_numbers == check_num:
                if int(ans[15]) % 2 == 1:
                    ans = str(ans_int + 1)
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

class Decimal64ConverterApp:
    def __init__(self, root):
        self.root = root
        root.title("Decimal-64 Floating Point Converter")
        root.resizable(width=False, height=False)

        style = ttk.Style()
        style.theme_use('clam')

        # Frame for padding and better layout
        frame = ttk.Frame(root, padding="10 10 10 10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        # Input Label and Entry
        self.input_label = ttk.Label(frame, text="Enter Decimal Value:")
        self.input_label.grid(row=0, column=0, sticky="w", pady=5)
        
        self.input_entry = ttk.Entry(frame, width=50)
        self.input_entry.grid(row=0, column=1, sticky="ew", pady=5)

        self.input_label2 = ttk.Label(frame, text="Enter Base-10 Exponent:")
        self.input_label2.grid(row=1, column=0, sticky="w", pady=5)
        
        self.input_entry2 = ttk.Entry(frame, width=50)
        self.input_entry2.grid(row=1, column=1, sticky="ew", pady=5)

        # Rounding Method Selection
        self.rounding_label = ttk.Label(frame, text="Select Rounding Method:")
        self.rounding_label.grid(row=2, column=0, sticky="w", pady=5)
        
        self.rounding_var = tk.StringVar(root)
        self.rounding_var.set("Default")  # default value
        
        self.rounding_option = ttk.OptionMenu(frame, self.rounding_var, "Truncate", "Truncate", "Floor", "Ceiling", "RTN")
        self.rounding_option.grid(row=2, column=1, sticky="ew", pady=5)

        # Convert Button
        self.convert_button = ttk.Button(frame, text="Convert", command=self.convert, takefocus=False)
        self.convert_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Output Display
        self.output_label = ttk.Label(frame, text="Output:")
        self.output_label.grid(row=4, column=0, sticky="nw", pady=5)
        
        self.output_text = tk.Text(frame, height=10, width=50)
        self.output_text.grid(row=5, column=0, columnspan=2, sticky="ew", pady=5)
        self.output_text.config(state='disabled') # Disable editing at default to prevent user input
        
        # Save Button
        self.save_button = ttk.Button(frame, text="Save to File", command=self.save_to_file, takefocus=False)
        self.save_button.grid(row=6, column=0, columnspan=2, pady=10)

    def convert(self):
        # Placeholder for conversion logic
        try:
            decimal_input = Decimal(self.input_entry.get())
        except InvalidOperation:
            messagebox.showerror("Input Error", "Invalid decimal value. Please enter a valid decimal number.")
            return  # Exit the function early

        try:
            exponent_input = int(self.input_entry2.get())
        except ValueError:
            messagebox.showerror("Input Error", "Invalid exponent value. Please enter a valid integer.")
            return  # Exit the function early
        
        rounding_method = self.rounding_var.get()
        
        e_prime = get_e_prime(exponent_input, decimal_input)
        sign_bit = check_sign(decimal_input)

        normalized_input = normalize_decimal(decimal_input, rounding_method, sign_bit)

        grouped_decimal = get_grouped_decimal(normalized_input)

        if exponent_input <= 369 and exponent_input >= -398:
            valid_output = ("Sign: {}\n".format(sign_bit) + "Combination Field: {}\n".format(get_combination_field(e_prime, normalized_input)) + "Exponent Continuation: {}\n".format(get_exponent_field(e_prime)) + "Coefficient Continuation:\n" + get_BCD_values(grouped_decimal))

            # Temporarily enable text field to insert the output
            self.output_text.config(state='normal')
            self.output_text.delete("1.0", tk.END)  # Clear existing text
            self.output_text.insert(tk.END, f"Decimal Input: {decimal_input}\nExponent Input: {exponent_input}\nRounding Method: {rounding_method}\n\n --Results-- \n{valid_output}")

            complete_binary = sign_bit + get_combination_field(e_prime,normalized_input) + get_exponent_field(e_prime) + get_BCD_values(grouped_decimal)
            hexed = hex_to_binary(complete_binary)

            self.output_text.insert(tk.END, f"\n\nHexadecimal Result: {hexed.upper()}")
            self.output_text.config(state='disabled')  # disable editing to prevent user input

        elif exponent_input > 369 and decimal_input != 0:
            if sign_bit == '1':
                valid_output = "Negative Infinity"

                # Temporarily enable text field to insert the output
                self.output_text.config(state='normal')
                self.output_text.delete("1.0", tk.END)  # Clear existing text
                self.output_text.insert(tk.END, f"Decimal Input: {decimal_input}\nExponent Input: {exponent_input}\nRounding Method: {rounding_method}\n\n --Results-- \n{valid_output}")
  
                complete_binary = "1111111111110000000000000000000000000000000000000000000000000000"
                hexed = hex_to_binary(complete_binary)

                self.output_text.insert(tk.END, f"\n\nHexadecimal Result: {hexed.upper()}")
                self.output_text.config(state='disabled')  # Disable editing to prevent user input

            elif sign_bit == '0':
                valid_output = "Positive Infinity"

                # Temporarily enable text field to insert the output
                self.output_text.config(state='normal')
                self.output_text.delete("1.0", tk.END)  # Clear existing text
                self.output_text.insert(tk.END, f"Decimal Input: {decimal_input}\nExponent Input: {exponent_input}\nRounding Method: {rounding_method}\n\n --Results-- \n{valid_output}")

                complete_binary = "0111111111110000000000000000000000000000000000000000000000000000"
                hexed = hex_to_binary(complete_binary)

                self.output_text.insert(tk.END, f"\n\nHexadecimal Result: {hexed.upper()}")
                self.output_text.config(state='disabled')  # Disable editing to prevent user input

        elif  (exponent_input > 369 or exponent_input < -398) and decimal_input == 0:
                valid_output = "NaN"

                # Temporarily enable text field to insert the output
                self.output_text.config(state='normal')
                self.output_text.delete("1.0", tk.END)  # Clear existing text
                self.output_text.insert(tk.END, f"Decimal Input: {decimal_input}\nExponent Input: {exponent_input}\nRounding Method: {rounding_method}\n\n --Results-- \n{valid_output}")

                complete_binary = "0111111111111000000000000000000000000000000000000000000000000000"
                hexed = hex_to_binary(complete_binary)
                
                self.output_text.insert(tk.END, f"\n\nHexadecimal Result: {hexed.upper()}")
                self.output_text.config(state='disabled')  # Disable editing to prevent user input

    def save_to_file(self):
        script_directory = os.path.dirname(os.path.realpath(__file__))

        file_path = filedialog.asksaveasfilename(
            initialdir=script_directory,
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )

        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.output_text.get("1.0", tk.END))
            messagebox.showinfo("Save to File", "File saved successfully.")

# Create the app
root = tk.Tk()
app = Decimal64ConverterApp(root)
root.mainloop()