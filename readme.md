# SMC

This repository contains example code of running secure multi-party computation of boolean circuits with two participants. 

## Install

You may want to install `zmq` and `sympy` via `pip3` prior to running the `makefile`.

## Run

Hopefully we have managed to write our code such that it remains faithful to the setup in the `makefile`. 

initiate bob first (which will always run.)
```
make bob
```

Then, on a seperate terminal, run alice using the predefined calls in the makefile.
```
make alice
```

I did not include the evaluation of the millionaires problem within the primary call to make it more `diff` friendly but this can be computed with `make million`.

The program should work whichever way the execution is performed (i.e it should work if alice is called first and then bob).

alternatively you can use `local` which will compute the
garbled circuit and the oblivious transfer within the same
thread.

```
make local
```
