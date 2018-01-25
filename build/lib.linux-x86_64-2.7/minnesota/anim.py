import sys
import time

data = ["c","&","c"," ","s","e","r","v","e","r"," ","f","o","r"," ", "t","c","p"," ","n","e","t","w","o","r","k"," ","|"]


# display with one upper char

for x in range(len(data)):
    # remeber lower char
    old = data[x]

    # replace with upper char
    data[x] = old.upper()

    # create full text
    text = "".join(data)

    # display full text
    sys.stdout.write("\r")
    sys.stdout.write(text)
    sys.stdout.flush()

    # put back lower char
    data[x] = old

    time.sleep(1)

# display without upper chars at the end 

text = "".join(data)

sys.stdout.write("\r")
sys.stdout.write(text)
sys.stdout.flush()