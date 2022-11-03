#
# Decimal Numbers
# Author  - Phil Hall, October 2022
# License - MIT
#
import sys
_max_10_exp = sys.float_info.max_10_exp
class Number:

    ERROR = 'e'
    MINUS = '-'
    POINT = '.'
        
    def __init__(self, value):
        self._minus = False
        self._error = False
        self._digits = 0
        self._places = 0
        self._number = None

        if isinstance(value, str):
            self._atod(value)
        elif isinstance(value, int):
            self._itod(value)
        elif isinstance(value, float):
            self._gtod(value)
        else:
            raise TypeError

        self._squeeze()
        

    def __str__(self):
        if self._number is None:
            return str(None)
        
        output = ""
        if self._error:
            output += Number.ERROR

        if self._minus:
            output += Number.MINUS
        
        if self._digits == 0:
            output += "0"
        else:
            for digit in range(self._digits):
                output += str(int(self._number[digit]))

        if self._places != 0:
            output += Number.POINT

            for digit in range(self._digits, self._bytes()):
                output += str(int(self._number[digit]))

        return output

    
    def __lt__(self, factor):
        return self._compare(factor) < 0
    
    def __gt__(self, factor):
        return self._compare(factor) > 0

    def __eq__(self, factor):
        return self._compare(factor) == 0

    def __ne__(self, factor):
        return self._compare(factor) != 0

    def __le__(self, factor):
        return self._compare(factor) < 1

    def __ge__(self, factor):
        return self._compare(factor) > -1

    
    def digits(self):
        return self._digits


    def places(self):
        return self._places
    

    def is_zero(self):
        return self._digits == 1 and self._places == 0 and self._number[0] == 0


    def is_negative(self):
        return self._minus
    

    def is_error(self):
        return self._error


    def flip_sign(self):
        if not self.is_zero():
            self._minus = not self._minus

            
    def set_error(self):
        self._error = True


    def clear_error(self):
        self._error = False


    def _squeeze(self):
        digits = 0
        places = 0

        for i in range(self._digits):
            if self._number[i] != 0:
                break
            digits += 1

        for i in reversed(range(self._digits, self._bytes())):
            if self._number[i] != 0:
                break
            places += 1

        if self._digits == digits and self._places == places:
            self._minus = False
            self._digits = 1
            self._places = 0
            del self._number
            self._number = bytearray(1)
            self._number[0] = 0
                
        elif digits != 0 or places != 0:
            temp = bytearray(self._bytes() - digits - places)
            
            j = 0
            for i in range(digits, self._bytes() - places):
                temp[j] = self._number[i]
                j += 1

            self._digits -= digits
            self._places -= places
            del self._number
            self._number = temp

    def _abs_comp(self, factor):
        for pow in reversed(range(-max(self._places, factor._places), \
                                  max(self._digits, factor._digits))):
        
            digit1 = self._get_digit(pow)
            digit2 = factor._get_digit(pow)

            if digit1 > digit2:
                return 1
            if digit1 < digit2:
                return -1

        return 0


    def _bytes(self):
        return self._digits + self._places

    
    def _compare(self, factor):
        if not isinstance(factor, Number):
            raise TypeError

        if self._minus and not factor._minus:
            return -1
        if factor._minus and not self._minus:
            return 1

        comp = self._abs_comp(factor)
        if(self._minus):
            return -comp

        return comp


    def _recreate(self, digits, places):
        del self._number
        self._number = bytearray(digits + places)
        self._digits = digits
        self._places = places

        
    def _atod(self, value):
        error = False
        minus = False
        got_digit = False
        point = False
        digits = 0
        places = 0

        if value[:1] == Number.ERROR:
            error = True
            value = value[1:]

        if value[:1] == Number.MINUS:
            minus = True
            value = value[1:]

        for char in value:
            if char == Number.POINT:
                if point:
                    raise ValueError
                point = True
            elif char in "0123456789":
                got_digit = True
                if point:
                    places += 1
                else:
                    digits += 1
            else:
                raise ValueError

        if not got_digit:
            raise ValueError
        
        self._digits = digits
        self._places = places
        self._error = error
        self._number = bytearray(self._bytes())

        i = 0
        for char in value:
            if char in "0123456789":
                self._number[i] =  int(char)
                i += 1

        self._squeeze()
        if not self.is_zero():
            self._minus = minus

        
    def _gtod(self, value):
        if value < 0.0:
            value =-value
            minus = True
        else:
            minus = False

        if value == 0.0:
            result = Number(0)
            self._places = result._places
            self._digits = result._digits
            self._minus = result._minus
            self._error = result._error
            del self._number
            self._number = result._number
            del result
             
        else:
            exp = _max_10_exp
            for _ in range(-exp, exp + 1):
                if 10.0 ** exp <= value:
                    break
                exp -= 1

            if exp != 0:
                value /= 10.0 ** exp

            self._recreate(1, 20)
            self._zadd0()
            
            calc = int(value) % 10
            last = calc
            self._number[0] = calc
            temp = value - float(calc)
            pow = 1
            while pow <= 40 and temp > 0.0:
                tens = 10.0**pow
                calc = int(value * tens)
                if calc > last * 10 + 9:
                    calc -=1
                last = calc
                self._number[pow] = calc % 10
                temp = value - float(calc) / tens
                pow += 1
                
            answer = self._number

            places = self._places
            digits = self._digits
            
            self._places -= exp
            self._digits += exp
            
            if self._places < 0:
                temp = self._places
                self._places = 0
            else:
                temp = 0
        
            if self._digits < 0:
                self._places -= self._digits
                self._digits = 0
                
            self._digits -= temp
            self._recreate(self._digits, self._places)

            if exp > 0:
                for temp in range(-self._places, -self._places - exp):
                    self._set_digit(temp, 0)
            else:
                for temp in range(self._digits + exp, self._digits):
                    self._set_digit(temp, 0)
            
            for temp in range(digits + places):
                self._set_digit(-places + temp + exp, \
                                answer[digits + places - 1 - temp])

        self._minus = minus

        
    def _itod(self, value):

        if value == 0:
            self._minus = False
            self._digits = 1
            self._places = 0
            self._number = bytearray(1)
            self._number[0] = 0
        else:
            if value < 0:
                self._minus = True
                value = -value

            work = value
            i = 0
            
            while work != 0:
                work //= 10
                i += 1

            self._digits = i
            self._number = bytearray(i)
        
            while value != 0:
                i -= 1
                self._number[i] = value % 10
                value //= 10


    def _get_digit(self, power):
        if power >= self._digits or power < -self._places:
            return 0

        if self._digits == 0 and power == 0:
            return 0

        i = self._digits - power - 1

        return int(self._number[i])

    def _set_digit(self, power, value):
        if power >= self._digits or power < -self._places:
            return

        if self._digits == 0 and power == 0:
            return

        i = self._digits - power - 1

        self._number[i] = value


    def  _shift_left(self):
        for pow in reversed(range(-self._places,self._digits)):
            self._set_digit(pow + 1, self._get_digit(pow))

        self._set_digit(-self._places, 0)


    def _zadd0(self):
        for index in range(self._bytes()):
            self._number[index] = 0

        self._error = 0
        self._minus = 0
#######################################################################
def _mini_add(factor_one, factor_two, carry):
    result = factor_one + factor_two + carry

    return (result % 10, result // 10)

def _mini_sub(factor_one, factor_two, carry):
    factor_two += carry

    if factor_one >= factor_two:
        result = factor_one - factor_two
        carry = 0
    else:
        result = (10 + factor_one) - factor_two
        carry = 1

    return (result, carry)


def _mini_mult(factor_one, factor_two):
    result = factor_one * factor_two

    return (result % 10, result // 10)


def _mini_half(factor, modulus):
    result = (10 * modulus) + factor

    return (result // 2, result % 2)


def _abs_add_sub(adding, big_factor, small_factor):
    digits = max(big_factor._digits, small_factor._digits)
    places = max(big_factor._places, small_factor._places)

    if adding:
        digits +=1

    result = Number(0)
    result._recreate(digits, places)
    result._zadd0()
    
    carry = 0
    for pow in range(-places, digits):
        if adding:
            value, carry = _mini_add(big_factor._get_digit(pow), \
                                             small_factor._get_digit(pow),
                                             carry)
        else:
            value, carry = _mini_sub(big_factor._get_digit(pow), \
                                             small_factor._get_digit(pow),
                                             carry)
        result._set_digit(pow, value)

    result._squeeze()

    result._error = big_factor._error or small_factor._error
        
    return result


def copy(factor):
    if not isinstance(factor, Number):
        raise TypeError
    
    new = Number(0)
    new._recreate(factor._digits, factor._places)
    for pow in range(-factor._places, factor._digits):
        new._set_digit(pow, factor._get_digit(pow))

    new._minus = factor._minus
    new._error = factor._error
    return new


def absolute(factor):
    if not isinstance(factor, Number):
        raise TypeError

    new = copy(factor)
    new._minus = False

    return new


def integer(factor):
    if not isinstance(factor, Number):
        raise TypeError

    new = copy(factor)
    for pow in range(-new._places, 0):
        new._set_digit(pow, 0)

    new._squeeze()

    return new


def fraction(factor):
    if not isinstance(factor, Number):
        raise TypeError

    new = copy(factor)
    for pow in range(new._digits):
        new._set_digit(pow, 0)

    new._squeeze()

    return new


def round(factor, places):
    if not isinstance(factor, Number) or not isinstance(places, int):
        raise TypeError

    if places < 0:
        raise ValueError

    if places > factor._places:
        return copy(factor)

    result = Number(0)
    result._recreate(factor._digits + 1, places)
    result._zadd0()
    
    for pow in range(-places, factor._digits):
        result._set_digit(pow, factor._get_digit(pow))

    if factor._get_digit(-places - 1) >= 5:
        carry = 1
        for pow in range(-places, result._digits):
            sum, carry = _mini_add(result._get_digit(pow), 0, carry)
            result._set_digit(pow, sum)

            if carry == 0:
                break
            
    result._squeeze()
    result._minus = factor._minus
    result._error = factor._error
    return result


def add(factor_one, factor_two):
    if not isinstance(factor_one, Number) or \
       not isinstance(factor_two, Number):
        raise TypeError

    # a + b & -a + -b
    if factor_one._minus == factor_two._minus:
        result = _abs_add_sub(True, factor_one, factor_two)

        if factor_one._minus:
            result._minus = True

        return result

    comp = factor_two._abs_comp(factor_one)

    # -a + b
    if factor_one._minus:
        # b < a
        if comp == -1:
            result = _abs_add_sub(False,factor_one, factor_two)

            if not result.is_zero():
                result._minus = True

            return result

        return _abs_add_sub(False, factor_two, factor_one)

    # a + -b & b >= a
    if(comp > -1):
        result = _abs_add_sub(False, factor_two, factor_one)

        if not result.is_zero():
            result._minus = True

        return result

    # a + -b & b < a
    return _abs_add_sub(False, factor_one, factor_two)
    

def subtract(factor_one, factor_two):
    if not isinstance(factor_one, Number) or \
       not isinstance(factor_two, Number):
        raise TypeError

    comp = factor_one._abs_comp(factor_two)

    # a > b
    if comp > -1:
        # a - b  and  -a - -b
        if factor_one._minus == factor_two._minus:
            if comp == 0: # the same
                result = Number(0)

                if factor_one._error or factor_two._error:
                    result._error = True

                return result

            result = _abs_add_sub(False, factor_one, factor_two)
            
            if factor_one._minus and not result.is_zero():
                result._minus = True

            return result
        # -a - -b  and  a - -b 
        result = _abs_add_sub(True, factor_one, factor_two)
        if factor_one._minus:
            result._minus = True

        return result

    # a - b  and  -a - -b
    if factor_one._minus == factor_two._minus:
        result = _abs_add_sub(False,factor_two, factor_one)
        
        if not factor_one._minus:
            result._minus = True

        return result

    # -a - b  and  a - -b
    result = _abs_add_sub(True, factor_two, factor_one)

    if not factor_one._minus and factor_two._minus:
        return result

    result._minus = True

    return result


def multiply(factor_one, factor_two):
    if not isinstance(factor_one, Number) or \
       not isinstance(factor_two, Number):
        raise TypeError
    
    r_carry = 0
    break_on = False

    # multiply by zero equals zero
    if factor_one.is_zero() or factor_two.is_zero():
        result = Number(0)
        if factor_one._error or factor_two._error:
            result._error = True

        return result

    result = Number(0)
    result._recreate(factor_one._digits + factor_two._digits, \
                     factor_one._places + factor_two._places)

    
    # do multiplication
    for pow_1 in range(-factor_one._places, factor_one._digits):
        digit_one = factor_one._get_digit(pow_1)

        for pow_2 in range(-factor_two._places, factor_two._digits):
            put = pow_1 + pow_2
            digit = factor_two._get_digit(pow_2)
            answer, m_carry = _mini_mult(digit_one, digit)

            digit = result._get_digit(put)
            answer, r_carry = _mini_add(answer, digit, r_carry)
            result._set_digit(put, answer)

            while True:
                put += 1
                if put >= result._digits:
                    break_on = True
                    break

                digit = result._get_digit(put)
                answer, r_carry = _mini_add(m_carry, digit, r_carry)
                result._set_digit(put, answer)
                m_carry = 0

                if r_carry == 0:
                    break

            if break_on:
                break

        if break_on:
            break

    result._squeeze()

    result._error = break_on or factor_one._error or factor_two._error
        
    result._minus = factor_one._minus != factor_two._minus and \
        not result.is_zero()

    return result


def divide(numerator, denominator, precision):
    if not isinstance(precision, int) or \
       not isinstance(numerator, Number) or \
       not isinstance(denominator, Number):
        raise TypeError

    if precision < 0:
        raise ValueError
    
    # divide by zero error
    if denominator.is_zero():
        result = copy(numerator)
        result._error = True

        return result

    # zero divided by a non-zero equals zero
    if numerator.is_zero():
        result = Number(0)

        if numerator._error or denominator._error:
            result._error = True

        return result

    divisor = None
    #create work numbers
    if denominator._digits > 0:
        get = numerator._digits - denominator._digits + 1
        put = get - 1
        places = denominator._places
        zeros = 0
        
        if get <= 0:
            if denominator._places == 0:
                for pow in range(denominator._digits):
                    if denominator._get_digit(pow) != 0:
                        break
                    zeros += 1

            get = max(0, numerator._digits + 1 - denominator._digits)

        digits = denominator._digits + 1 - zeros

        if denominator._places == 0 and zeros != 0:
            divisor = Number(0)
            divisor._recreate(digits, places)
            divisor._zadd0()

    else:
        zeros = -1
        for pow in reversed(range(-denominator._places,0)):
            if denominator._get_digit(pow) != 0:
                break
            
            zeros -= 1

        get = numerator._digits - zeros
        put = get - 1
        digits = 2
        places = denominator._places + zeros

        divisor = Number(0)
        divisor._recreate(digits, places)
        divisor._zadd0()
                    
    result = Number(0)
    result._recreate(get, precision)
    result._zadd0()
    
    work = Number(0)
    work._recreate(digits, places)
    work._zadd0()

    # set work
    total = numerator._digits - 1

    if denominator._digits == 0:
        maximum = total - digits
        id = digits - 2
    elif not divisor is None:
        maximum = total - digits
        id = digits - 2
    else:
        maximum = total - denominator._digits - denominator._places
        id = denominator._digits - 1

    for get in reversed(range(maximum + 1, numerator._digits)):
        work._set_digit(id, numerator._get_digit(get))
        id -= 1
        
    # set denominator
    if denominator._digits == 0:
        id =0;
        for get in reversed(range(-denominator._places, zeros + 1)):
            divisor._set_digit(id, denominator._get_digit(get))
            id -= 1
    elif not divisor is None:
        id = digits - 2
        for get in reversed(range(zeros, denominator._digits)):
            divisor._set_digit(id, denominator._get_digit(get))
            id -= 1
    
    # create look up
    temp = None
    if divisor is None:
        compare = copy(denominator)
        if denominator._minus:
            compare = absolute(compare)
            temp = absolute(denominator)
    else:
        compare = copy(divisor)

    lookup = [compare]

    for _ in range(9):
        if divisor is None:
            if denominator._minus:
                compare = add(compare, temp)
            else:
                compare = add(compare, denominator)
        else:
            compare = add(compare, divisor)

        lookup.append(compare)

    del temp
    
    # begin division
    if denominator._digits == 0:
        get = total - places - 1
    elif not divisor is None:
        get = total - digits + 1
    else:
        get = total - (denominator._digits + places)

    if put >= -precision:
        while True:
            while work._abs_comp(lookup[0]) < 0:
                result._set_digit(put, 0)
                put -= 1
                if put < -precision:
                    break

                work._shift_left()
                work._set_digit(-places, numerator._get_digit(get))
                get -= 1

            if put < -precision:
                break

            value = 1
            comp = work._abs_comp(lookup[0])
            while comp > 0:
                comp = work._abs_comp(lookup[value])
                value += 1

            if comp == 0:
                work._zadd0()
            else:
                value -= 1

                if value != 0:
                    carry = 0
                    for pow in range(-work._places,work._digits):
                        temp, carry = \
                            _mini_sub(work._get_digit(pow), \
                                      lookup[value - 1]. _get_digit(pow),
                                             carry)

                        work._set_digit(pow, temp)          

            result._set_digit(put, value)
            put -= 1

            if put < -precision:
                break
            
            if comp !=0:
                work._shift_left()

            work._set_digit(-places, numerator._get_digit(get))
            get -= 1

    del lookup
    del work
    if not divisor is None:
        del divisor

    result._squeeze()

    result._minus = not result.is_zero() and \
        denominator._minus != numerator._minus

    result._error = denominator._error or numerator._error

    return result
                    

def exponent_10(factor, power_of_ten):
    if not isinstance(factor, Number):
        raise TypeError

    if not isinstance(power_of_ten, int):
        raise TypeError
    
    if power_of_ten == 0:
        return copy(factor)

    places = factor._places - power_of_ten
    digits = factor._digits + power_of_ten
    
    if places < 0:
        temp = places
        places = 0
    else:
        temp = 0
        
        if digits < 0:
            places -= digits
            digits = 0

    result = Number(0)
    result._recreate(digits - temp, places)
    
    if power_of_ten > 0:##bug
        for temp in range(-result._places, -result._places - power_of_ten):
            result._set_digit(temp, 0)
    else:
        for temp in range(result._digits + power_of_ten, result._digits):
            result._set_digit(temp, 0)
            
    for pow in range(-factor._places, factor._digits):
        result._set_digit(pow + power_of_ten, factor._get_digit(pow))

    result._minus = factor._minus;
    result._error = factor._error;
    result._squeeze()
    
    return result


def half(factor):
    if not isinstance(factor, Number):
        raise TypeError

    result = Number(0)
    result._recreate(factor._digits, factor._places + 1)
    result._error = factor._error
    result._minus = factor._minus
        
    modulus = 0
    for index in range(factor._bytes()):
        divide, modulus = _mini_half(factor._number[index], modulus)
        result._number[index] = divide

    if modulus != 0:
        result._set_digit(-result._places, 5)
    else:
        result._set_digit(-result._places, 0)
        
    result._squeeze()
    return result

