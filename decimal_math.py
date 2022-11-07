import decimal

pi = decimal.Number("3.1415926535897932384626433832795028842")

def root(factor, power, iterations):
    if not isinstance(factor, decimal.Number) or \
       not isinstance(power, int) or not isinstance(iterations, int):
        raise TypeError

    if power <= 0 or iterations < 0:
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


def radians(degrees, precision):
    if not isinstance(degrees, decimal.Number):
        raise TypeError

    return decimal.divide(decimal.multiply(decimal.multiply(decimal.Number(2), \
                                                            pi), degrees), \
                          decimal.Number(360), precision)


def sine(factor, iterations, precision):
    if not isinstance(factor, decimal.Number) or \
       not isinstance(iterations, int) or not isinstance(precision, int):
        raise TypeError

    if iterations < 1 or precision < 0:
        raise ValueError
    
    one = decimal.Number(1)
    two = decimal.Number(2)
    denominator = decimal.Number(1)
    term = decimal.Number(1)
    work = decimal.copy(factor)

    two_pi = decimal.multiply(two, pi)
    if not work.is_negative():
        while work > two_pi:
            work = decimal.subtract(work, two_pi)
    else:
        two_pi.flip_sign()
        while work < two_pi:
            work = decimal.subtract(work, two_pi)
        two_pi.flip_sign()
        work = decimal.add(work, two_pi)

    half_pi = decimal.divide(pi, two, precision)
    pi_and_a_half = decimal.add(pi, half_pi)

    minus = False
    if work > pi_and_a_half:
        work = decimal.add(decimal.subtract(half_pi, work), pi_and_a_half)
        minus = True
    elif work > half_pi:
        work = decimal.subtract(work, pi)
        minus = True
        
    numerator = decimal.copy(work)
    work = decimal.multiply(work, work)
    sigma = decimal.copy(numerator)
    for i in range(1,iterations):
        numerator = decimal.multiply(numerator, work)
        term = decimal.add(term, one)
        denominator = decimal.multiply(denominator, term)
        term = decimal.add(term, one)
        denominator = decimal.multiply(denominator, term)

        if i % 2 == 1:
            sigma = decimal.subtract(sigma, decimal.divide(numerator, \
                                                           denominator, \
                                                           precision))
        else:
            sigma = decimal.add(sigma, decimal.divide(numerator, \
                                                           denominator, \
                                                           precision))

    if minus:
        sigma.flip_sign()

    return sigma


def cosine(factor, iterations, precision):
    if not isinstance(factor, decimal.Number) or \
       not isinstance(iterations, int) or not isinstance(precision, int):
        raise TypeError

    if iterations < 1 or precision < 0:
        raise ValueError
    
    one = decimal.Number(1)
    two = decimal.Number(2)
    denominator = decimal.Number(1)
    term = decimal.Number(2)
    work = decimal.copy(factor)

    two_pi = decimal.multiply(two, pi)
    if not work.is_negative():
        while work > two_pi:
            work = decimal.subtract(work, two_pi)
    else:
        two_pi.flip_sign()
        while work < two_pi:
            work = decimal.subtract(work, two_pi)
        two_pi.flip_sign()
        work = decimal.add(work, two_pi)

    half_pi = decimal.divide(pi, two, precision)
    pi_and_a_half = decimal.add(pi, half_pi)

    minus = False
    if work > pi_and_a_half:
        work = decimal.subtract(work, two_pi)
    elif work > half_pi:
        work = decimal.subtract(work, pi)
        minus = True
        
    numerator = decimal.Number(1)
    work = decimal.multiply(work, work)
    sigma = decimal.copy(numerator)
    for i in range(1,iterations):
        numerator = decimal.multiply(numerator, work)
        denominator = decimal.multiply(denominator, term)

        if i % 2 == 1:
            sigma = decimal.subtract(sigma, decimal.divide(numerator, \
                                                           denominator, \
                                                           precision))
        else:
            sigma = decimal.add(sigma, decimal.divide(numerator, \
                                                           denominator, \
                                                           precision))

        term = decimal.add(term, one)
        denominator = decimal.multiply(denominator, term)
        term = decimal.add(term, one)

    if minus:
        sigma.flip_sign()

    return sigma
                                

def _to_the_power(factor, power):
    product = decimal.Number(1)

    for _ in range(power):
        product = decimal.multiply(product, factor)

    return product


def y_to_the_x(factor_one, factor_two, iterations):
    product = decimal.Number(1)
    root_pow = 10
    one = decimal.Number(1)

    work = decimal.integer(factor_two)

    while work >= one:
        product = decimal.multiply(product, factor_one)
        work = decimal.subtract(work, one)
        
    if factor_two.places() != 0:
        work = decimal.fraction(factor_two)
        work = decimal.exponent_10(work, factor_two.places())
        root_pow = 10 ** factor_two.places()
        temp = decimal.Number(1)
        while work >= one:
            temp = decimal.multiply(temp, factor_one)
            work = decimal.subtract(work, one)

        product = decimal.multiply(product, root(temp, root_pow, iterations))

    return product
