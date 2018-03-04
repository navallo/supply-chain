from math import *
import argparse


class Chain():
    def __init__(self, capacity, batch_size, ship, order_point):
        self.in_produce_num = 0
        self.on_ship_num = 0
        self.inventory_num = 1000
        self.cash = 10000000
        self.capacity = capacity
        self.batch_size = batch_size
        self.ship = ship
        self.order_point = order_point

        self.produce_day = ceil(self.batch_size / self.capacity)
        self.trucks_need = ceil(self.batch_size / 200)

        self.sell_history = []
        self.lost_history = []

        self.product_queue = {}

    def order(self, day):
        if self.ship == 'mail':
            self.product_queue[day] = [self.produce_day, -1]
            self.cash -= self.batch_size * 150
            if babble: print('[Order] cash -', self.batch_size * 150)
        else:
            self.product_queue[day] = [self.produce_day, -1]
            self.cash -= self.trucks_need * 15000
            if babble: print('[Order] cash -', self.trucks_need * 15000)

        cost = (self.batch_size * 1000) + 1500
        self.cash -= cost
        if babble: print('[Facotry] cash -', cost)
        self.in_produce_num += self.batch_size

    def produce(self):
        delete_list = []
        for day, clock_read in self.product_queue.items():
            if clock_read[1] > 0:
                clock_read[1] -= 1
                if clock_read[1] == 0:
                    self.inventory_num += self.batch_size
                    self.on_ship_num -= self.batch_size
                    delete_list.append(day)

        for day, clock_read in self.product_queue.items():
            if clock_read[0] > 0:
                clock_read[0] -= 1
                if clock_read[0] == 0:
                    clock_read[0] = -1
                    if self.ship == 'mail':
                        clock_read[1] = 1
                    elif self.ship == 'truck':
                        clock_read[1] = 7
                    self.on_ship_num += self.batch_size
                    self.in_produce_num -= self.batch_size
                    continue
                else:
                    break

        for key in delete_list:
            del self.product_queue[key]

    def gain_to_customer(self, num):
        gain = num * (1450 - 150)
        self.cash += gain
        if babble: print('[sell] cash +', gain)

    def gain_daily_interest(self):
        gain = int(self.cash * 0.000261)
        self.cash += gain
        if babble: print('[interest] cash +', gain)

    def cost_holding(self):
        cost = ceil((self.inventory_num + self.on_ship_num) * 0.274)
        self.cash -= cost
        if babble: print('[Hold] cash -', cost)

    def next_day(self, demand, day):
        self.produce()
        if demand > self.inventory_num:
            self.lost_history.append(demand - self.inventory_num)
            self.sell_history.append(self.inventory_num)
            self.gain_to_customer(self.inventory_num)
            self.inventory_num = 0
        else:
            self.lost_history.append(0)
            self.sell_history.append(demand)
            self.gain_to_customer(demand)
            self.inventory_num -= demand

        if (self.inventory_num + self.on_ship_num) <= self.order_point:
            idle = True
            for _, clock_read in self.product_queue.items():
                if clock_read[0] > 0:
                    idle = False
            if idle:
                self.order(day)

        self.cost_holding()
        self.gain_daily_interest()

        if self.cash <= 0:
            print('dao bi la')
            exit(-1)


def main(babble_level, capacity, batch_size, ship, order_point):
    global babble
    babble = babble_level
    c = Chain(
        capacity=capacity,
        batch_size=batch_size,
        ship=ship,
        order_point=order_point)

    count_day = 0
    print('capacity=', capacity, '\nbatch_size=', batch_size, '\nship=', ship,
          '\norder_point=', order_point)
    print('\n')
    with open('./data/data_all.txt', 'r') as data:
        for demand in data:
            count_day += 1
            demand = int(demand)
            c.next_day(demand, day=count_day)
            print('(Day:', count_day, ')Demand:', demand, '\tCash:', int(
                c.cash), '\tInventory:', c.inventory_num, '\tOn ship:',
                  c.on_ship_num, '\tInproduce:', c.in_produce_num, ' Queue:',
                  c.product_queue)
            if babble: print('\n')
    print('Final gain=', c.cash / 10000000)


if __name__ == '__main__':
    CAPACITY = 50
    BATCH_SIZE = 200
    SHIP = 'truck'
    #SHIP = 'mail'
    ORDER_POINT = 1000

    parser = argparse.ArgumentParser()
    parser.add_argument('-b', help='babble level')
    args = parser.parse_args()

    main(
        babble_level=args.b,
        capacity=CAPACITY,
        batch_size=BATCH_SIZE,
        ship=SHIP,
        order_point=ORDER_POINT)
