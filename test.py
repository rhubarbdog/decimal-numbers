import decimal

for f1 in ("-1234.567" , "-3.142", "-1.3", "-1", "0", "1", "1.3",\
           "3.142", "1234.567"):
    for f2 in ("-1234.567" , "-3.142", "-1.3", "-1", "0", "1", "1.3",\
               "3.142", "1234.567"):
        one = decimal.Number(f1)
        two = decimal.Number(f2)

        print(one, '\t+', two, '\t=', decimal.add(one, two))
        print(two, '\t+', one, '\t=', decimal.add(two, one))
        print(one, '\t-', two, '\t=', decimal.subtract(one, two))
        print(two, '\t-', one, '\t=', decimal.subtract(two, one))
        print(one, '\t*', two, '\t=', decimal.multiply(one, two))
        print(two, '\t*', one, '\t=', decimal.multiply(two, one))
        print(one, '\t/', two, '\t=', decimal.divide(one, two, 10))
        print(two, '\t/', one, '\t=', decimal.divide(two, one, 10))

        print('exp_10(', one, ", 0)\t=",decimal.exponent_10(one, 0))
        print('exp_10(', two, ", 0)\t=",decimal.exponent_10(two, 0))
        print('exp_10(', one, ", 5)\t=",decimal.exponent_10(one, 5))
        print('exp_10(', two, ", 5)\t=",decimal.exponent_10(two, 5))
        print('exp_10(', one, ",-5)\t=",decimal.exponent_10(one, -5))
        print('exp_10(', two, ",-5)\t=",decimal.exponent_10(two, -5))

        print('fraction(', one, ")\t=",decimal.fraction(one))
        print('integer(', one,")\t=",decimal.integer(one))
        print('round(', one, ", 2)\t=",decimal.round(one, 2))
