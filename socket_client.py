import util
import os
import ot

# This is Bob.
if __name__ == "__main__":
    # setup bob class.
    # zero for the first item, 1 for the second item.
    bob = ot.Bob(0)
    # set up client object
    client = util.ClientSocket()
    # set up ready.
    client.send(True)
    # wait to receive c value
    c = client.receive()
    # generate H0
    H0 = bob.send_h0(c)
    # send H0 to alice
    client.send(H0)
    # wait for Alice to send h0, E, length as a payload
    (c_1, E, length) = client.receive()
    # compute response
    message = bob.getMessage(c_1, E, length).decode()
    print(message)