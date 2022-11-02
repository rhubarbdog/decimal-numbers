import decimal


def root(factor, power, iterations):
    if not isinstance(factor, decimal.Number) or not isinstance(power, int) or \
       not isinstance(iterations, int):
        raise TypeError

    if power < 1 or iterations < 0:
        raise ValueError

    if power == 1 or factor.is_zero():
        result = decimal.copy(factor)
        return result

    minus = factor.is_negative()
    abs_factor = decimal.absolute(factor)
    if abs_factor.digits() == 0:
        upper = decimal.Number(1)
        lower = decimal.copy(abs_factor)
    else:
        upper = decimal.copy(abs_factor)
        lower = decimal.Number(1)

    test = decimal.add(lower, decimal.half(decimal.subtract(upper, lower)))
      
    while iterations > 0:
        iterations -= 1
        product = decimal.multiply(test, test)
        for _ in range(2, power):
            product = decimal.multiply(product, test)
            
        
        if product == abs_factor:
            break

        if product < abs_factor:
            del lower
            lower = decimal.copy(test)
            test = decimal.add(test, \
                               decimal.half(decimal.subtract(upper, test)))
        else:
            del upper
            upper = decimal.copy(test)
            test = decimal.add(lower, \
                               decimal.half(decimal.subtract(test, lower)))

        del product

    del lower
    del upper

    if factor._error:
        test.set_error()

    if minus:
        test.flip_sign()

    if power % 2 == 0 and minus:
        test.set_error()

    return test

