def read_sensor():
    import random
    return random.randint(5, 52)


def listen():
    import usocket
    # accept connections from anyone, else supply IP address of client.
    HOST = ''
    PORT = 65000

    s = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(7)

    print(" Socket Server is : 'Listening' ")

    while True:
        # 41 -->
        # Get socket object and client IP and port addresses ************ Line # 41 *******************
        c, addr = s.accept()
        print('Accepted connection from ', addr)
        cmd = c.recv(255)
        if not cmd:
            break
        if cmd == 'get_temp':
            print('Decoded the get_temp cmd.')
            temp_C = read_sensor()
            print("function returned temp is : " + temp_C)
            c.send(str(temp_C))
            print("Sent to client : " + str(temp_C) + " Degrees C. ")
            c.close()
