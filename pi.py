#
# Calculate pi
# Author  - Phil Hall, October 2022
# License - MIT
#

import decimal
import random
import time

square = decimal.Number(0)
circle = decimal.Number(0)
two_one = decimal.Number(2.1)
one_05 = decimal.Number(1.05)
one = decimal.Number(1)

begin = time.time()
loops = 0
end = time.time()

while end - begin < 60.0 * 60.0 * 72.0:
    x_coordinate = decimal.Number(random.random())
    y_coordinate = decimal.Number(random.random())

    x_coordinate = decimal.multiply(x_coordinate, two_one)
    y_coordinate = decimal.multiply(y_coordinate, two_one)

    x_coordinate = decimal.subtract(x_coordinate, one_05)
    y_coordinate = decimal.subtract(y_coordinate, one_05)

    x_coordinate = decimal.absolute(x_coordinate)
    y_coordinate = decimal.absolute(y_coordinate)

    if x_coordinate <= one and y_coordinate <= one:
        x_coordinate = decimal.multiply(x_coordinate, x_coordinate)
        y_coordinate = decimal.multiply(y_coordinate, y_coordinate)

        if decimal.add(x_coordinate, y_coordinate) <= one:
            circle = decimal.add(circle, one)

        square = decimal.add(square, one)

    end = time.time()
    loops += 1
    
    if loops % 1000 == 0:
        print(circle, square , end - begin, end = '        \r')

    if loops > 100000000000:
        loops = 0

print("")
print("dividing")
pi = decimal.divide(circle, square, 45)
pi = decimal.multiply(pi, decimal.Number(4))
print(pi)
