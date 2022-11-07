# decimal-numbers

**decimal.py**

Numbers can be compared with relational operators <, <=, ==, !=, >= and >.
They also can be printed with the print() function as they have the `__str__`
magic method.

*Examples*

```
import decimal

# initialise with an integer
one = decimal.Number(1)
two = decimal.Number(2)
# initialise with a floating point number
three = decimal.Number(3.0)
pi = decimal.Number(3.1415)
# initialise with a simple string, can be more accurate than floating
# point numbers
number102_57 = decimal.Number("102.57")

# add and subtract them
print(decimal.add(one, two))
print(decimal.subtract(one, two))

# calculate the area of a circle radius 2
area = decimal.multiply(pi, decimal.multiply(two, two))

# divide to a greater precision than flaoting point numbers
third = decimal.divide(one, three, 50)

# get the integer or faction portion of the number
print(decimal.integer(number102_57))
print(decimal.fraction(number102_57))

# round the number up
print(decimal.round(number102_57, 1))

# truncate it to 'z' decimal place with this code fragment
z = 3
truncated = decimal.exponent_10(pi, z)
truncated = decimal.integer(truncated)
truncated = decimal.exponent_10(truncated, -z)

print(truncated)
```


*Methods*
<table>
<tr><td><code>is_zero()</code></td><td>A boolean, returns true if the number
is 0.</td></tr>
<tr><td><code>is_negative()</code></td><td>A boolean, returns true if the number
is less than 0 (a negative number).</td></tr>
<tr><td><code>is_error()</code></td><td>A boolean, returns True if the number is
in error.</td></tr>
<tr><td><code>flip_sign()</code></td><td>Makes positive numbers into negative ones and negeative into poitive.</td></tr>
<tr><td><code>set_error()</code></td><td>Sets the error flag.</td></tr>
<tr><td><code>clear_error()</code></td><td>Resets the error flag.</td></tr>
<tr><td><code>digits()</code></td><td>An indication of the number of digits in
the number. Zero has one digit the 0, where as 0.1 has no digits the printed
leading zero is implied.</td></tr>
<tr><td><code>places()</code></td><td>The number of fractional digits in the
number.</td></tr>
</table>

*Functions*

`copy(factor)`

returns a copy of factor. `a = copy(b)` is the correct way to express `a = b`

`absolue(factor)`

returns a positive copy of the number

`integer(factor)`

returns a new number the integer portion of the factor

`fraction(factor)`

returns a new number the fractional portion of the factor

`round(factor, places)`

returns a new number rounded to the prescribed number of decimal places

`add(factor_one, factor_two)`

returns a new number the sum of the factors

`subtract(factor_one, factor_two)`

returns a new number the difference of the factor one and factor two

`multiply(factor_one, factor_two)`

returns a new number the product of the factors

`divide(numerator, denominator, precision)`

returns a new number the division of the factors. if the denominator is 0 then
a copy of the numerator is returned with the error flag set

`exponent_10(factor, power_of_ten)`

returns a new number `factor * 10 ^ power_of_ten`

`half(factor)`

returns new a number quickly, half of the factor. Faster then divide by 2,
useful for search by interval division

**decimal_math.py**

*functions*

`root(factor, power, iterations)`

calculates the square, cubed, fourth etc. root of a number.  Negative factors
with even results in `-root(absolue(factor), power, iterations)` with the error
flag set

**microbit.py**

The same as `decimal.py` except all variable names have been shortened as have
internal function and method names.  It only works with command
To use this you currently need to have a freshly `uflash`ed microbit and have
to `uflash` it again to use it again.

To use enter:

```
uflash
```

Wait until the yellow light on the microbit stops flashing, then enter:
```
ufs put microbit.py decimal.py
ufs put microbit_root.py main.py
```

The `root` in file `microbit_root.py` function is the same as the function in
`decimal_math.py`

Or Try:
```
uflash
```
Wait until the yellow light on the microbit stops flashing, then enter:
```
ufs put microbit.py decimal.py
ufs put microbit_pi.py main.py
```

To calculate the number pi.

Remember to reset you microbit to start the functions running.