from multiprocessing import Queue, Pool
from time import sleep
from random import randint

class Adder:

    def __init__(self, number_one, number_two):
        self.number_one = number_one
        self.number_two = number_two
        self.result = None
        self.queue = None

    def run(self):
        self.result = self.number_two + self.number_one
        sleep(randint(0,4))
        print("Result: {}".format(self.result))
        return self.result

    def _set_output_queue(self, queue):
        self.queue = queue


if __name__ == "__main__":
    tasks = [Adder(4, 2), Adder(1, 2), Adder(6, 10), Adder(60, 9), Adder(75, -5)]
    pool = Pool(4)


    results = [pool.apply_async(x.run) for x in tasks]
    output = [p.get() for p in results]
