import usocket

sockaddr = usocket.getaddrinfo('www.micropython.org', 80)[0][-1]
print(usocket.getaddrinfo('www.micropython.org', 80))
print(usocket.getaddrinfo('www.micropython.org', 80)[0][-1])
sock.connect(addr)
