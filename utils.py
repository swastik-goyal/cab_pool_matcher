from readchar import readchar, key

def custom_input(text=None):
    if text:
        print(text, end='')
    s = ""
    while True:
        c = readchar()
        if c==key.ESC:
            return False
        if c==key.ENTER:
            return s
        s += c
        print(c, end='')