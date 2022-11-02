from microbit import *
import decimal, music, random, time

square = decimal.Number(0)
circle = decimal.Number(0)
number2_1 = decimal.Number(2.1)
number1_05 = decimal.Number(1.05)
number1 = decimal.Number(1)

begin = time.ticks_ms()
loops = 0
end = time.ticks_ms()

images = [Image.SQUARE, Image.SQUARE_SMALL , Image("00000:00000:00900:" \
                                                   "00000:00000") ]

while time.ticks_diff(end ,begin) < 60000 * 60 * 72:
    xxx = decimal.Number(random.random())
    yyy = decimal.Number(random.random())

    xxx = decimal.multiply(xxx, number2_1)
    yyy = decimal.multiply(yyy, number2_1)

    xxx = decimal.subtract(xxx, number1_05)
    yyy = decimal.subtract(yyy, number1_05)

    xxx = decimal.absolute(xxx)
    yyy = decimal.absolute(yyy)

    if xxx <= number1 and yyy <= number1:
        xxx = decimal.multiply(xxx, xxx)
        yyy = decimal.multiply(yyy, yyy)

        if decimal.add(xxx, yyy) <= number1:
            circle = decimal.add(circle, number1)

        square = decimal.add(square, number1)

    end = time.ticks_ms()
    loops += 1
    
    if loops % 10 == 1:
        display.show(images[(loops // 10 ) % 3])

    if loops > 90:
        loops = 0

display.show('D')
print('square', square)
with open("square.txt", 'w') as file:
    file.write(str(square))

print('circle', circle)    
with open("cirle.txt", 'w') as file:
    file.write(str(circle))

pi = decimal.divide(circle, square, 45)
pi = decimal.multiply(pi, decimal.Number(4))

print('pi', pi)
with open("pi.txt", 'w') as file:
    file.write(str(pi))
music.play(['c4:4'])
sleep(3000)
display.scroll(str(pi) + '  ', wait = True, loop =True)

