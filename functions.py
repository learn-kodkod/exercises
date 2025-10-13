def multiplication_table(t_size):
    for i in range(1,t_size + 1):
        for j in range(1, t_size +1):
            print(i * j, end=" " )
        print("")

multiplication_table(3)



def rectangle(height ):
    for i in range(1,height  + 1):
        for j in range(1, i + 1):
            print(j, end=" " )
        print("")

rectangle(5)


def star_rectangle(height ):
    for i in range(1,height  + 1):
        for j in range(1, i + 1):
            print("*", end=" " )
        print("")

star_rectangle(5)

def identical_matrix(size):
    for i in range(1,size  + 1):
        for j in range(1, size + 1):
           if i == j:
                print("1", end=" " )
           else:
               print("0", end=" ")
        print("")

identical_matrix(8)

def chess_table(size):
    line_char = "M"
    current_char = ""
    for i in range(1,size  + 1):
        if line_char == "M":
            line_char = "x"
        else:
            line_char = "M"
        current_char = line_char
        for j in range(1, size + 1):
           print(current_char , end=" " )
           if current_char == "M":
               current_char = "x"
           else:
               current_char = "M"
        print("")

chess_table(5)

def sum_table(t_size):
    sum = 0
    for i in range(1,t_size + 1):
        for j in range(1, t_size +1):
            mul = i * j
            sum += mul
            print(mul, end=" " )
        print("")
    print(f"metrix sum is {sum}")

sum_table(3)
