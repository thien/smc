import util
import ot
import os
import time
# os.system('clear')

if __name__ == "__main__":
    print("Running Server")
    # set up alice class.
    alice = ot.Alice('hello','world')
    # set up server object
    server = util.ServerSocket()
    # print("Initiated Server Socket.")
    computed = False

    while not computed:
        # wait until bob is online
        ready = server.receive()
        print("Message:", ready, " - type:", type(ready))
        if ready:
            # send c
            c = alice.send_c()
            server.send(c)
            # wait for bob to send H0 so that we can receive it.
            h0 = server.receive()
            # compute c_1, E, length
            c_1, E, length = alice.sendMessage(h0)
            # send c_1, E, length to Bob.
            payload = (c_1, E, length)
            server.send(payload)
            print("Completed transaction of payload.")
        time.sleep(1)