# Decimal Numbers
# Author  - Phil Hall, October 2022
# License - MIT
_R = range
_B = reversed
_I = isinstance
_A = bytearray

_F = False
_T = True
_N = None

_Ve = ValueError
_Te = TypeError

class Number:
    EE = 'e'
    MM = '-'
    PP = '.'
    def __init__(self, vv):
        _S = self
        _S._m = _F
        _S._e = _F
        _S._d = 0
        _S._p = 0
        _S._n = _N
        if _I(vv, str):
            _S._atod(vv)
        elif _I(vv, int):
            _S._itod(vv)
        elif _I(vv, float):
            _S._gtod(vv)
        else:
            raise _Te
        _S._sqz()

    def __str__(self):
        _S = self
        if _S._n is _N:
            return str(_N)
        out = ""
        if _S._e:
            out += Number.EE
        if _S._m:
            out += Number.MM
        if _S._d == 0:
            out += "0"
        else:
            for dig in _R(_S._d):
                out += str(int(_S._n[dig]))
        if _S._p != 0:
            out += Number.PP
            for dig in _R(_S._d, _S._byt()):
                out += str(int(_S._n[dig]))
        return out       

    def __lt__(self, ff):
        return self._comp(ff) < 0
    def __gt__(self, ff):
        return self._comp(ff) > 0
    def __eq__(self, ff):
        return self._comp(ff) == 0
    def __ne__(self, ff):
        return self._comp(ff) != 0
    def __le__(self, ff):
        return self._comp(ff) < 1
    def __ge__(self, ff):
        return self._comp(ff) > -1

    def digits(self):
        return self._d

    def places(self):
        return self._p
    
    def is_zero(self):
        _S = self        
        return _S._d == 1 and _S._p == 0 and _S._n[0] == 0

    def is_negative(self):
        return self._m
    
    def is_error(self):
        return self._e

    def flip_sign(self):
        _S = self
        if not _S.is_zero():
            _S._m = not _S._m

    def set_error(self):
        self._e = _T

    def clear_error(self):
        self._e = _F

    def _byt(self):
        return self._d + self._p
        
    def _sqz(self):
        _S = self
        digs = 0
        pla = 0
        for i in _R(_S._d):
            if _S._n[i] != 0:
                break
            digs += 1
        for i in _B(_R(_S._d, _S._byt())):
            if _S._n[i] != 0:
                break
            pla += 1
        if _S._d == digs and _S._p == pla:
            _S._m = _F
            _S._d = 1
            _S._p = 0
            del _S._n
            _S._n = _A(1)
            _S._n[0] = 0
        elif digs != 0 or pla != 0:
            tmp = _A(_S._byt() - digs - pla)
            j = 0
            for i in _R(digs, _S._byt() - pla):
                tmp[j] = _S._n[i]
                j += 1
            _S._d -= digs
            _S._p -= pla
            del _S._n
            _S._n = tmp

    def _abs_cmp(self, ff):
        _S = self
        for pow in _B(_R(-max(_S._p, ff._p), \
                         max(_S._d, ff._d))):
            d1 = _S._get(pow)
            d2 = ff._get(pow)
            if d1 > d2:
                return 1
            if d1 < d2:
                return -1
        return 0

    def _comp(self, ff):
        _S = self
        if not isinstance(ff, Number):
            raise TypeError
        if _S._m and not ff._m:
            return -1
        if ff._m and not _S._m:
            return 1
        cmp = _S._abs_cmp(ff)
        if(_S._m):
            return -cmp
        return cmp

    def _rec(self, dig, pla):
        _S = self
        del _S._n
        _S._n = _A(dig + pla)
        _S._d = dig
        _S._p = pla

    def _atod(self, vv):
        _S = self
        eee = _F
        mns = _F
        g_d = _F
        ppp = _F
        digs = 0
        pla = 0
        if vv[:1] == Number.EE:
            eee = _T
            vv = vv[1:]
        if vv[:1] == Number.MM:
            mns = _T
            vv = vv[1:]
        for ch in vv:
            if ch == Number.PP:
                if ppp:
                    raise _Ve
                ppp = _T
            elif ch in "0123456789":
                g_d = _T
                if ppp:
                    pla += 1
                else:
                    digs += 1
            else:
                raise _Ve
        if not g_d:
            raise _Ve
        _S._d = digs
        _S._p = pla
        _S._e = eee
        _S._n = _A(_S._byt())
        i = 0
        for ch in vv:
            if ch in "0123456789":
                _S._n[i] =  int(ch)
                i += 1
        _S._sqz()
        if not _S.is_zero():
            _S._m = mns

    def _gtod(self, vv):
        _S = self
        if vv < 0.0:
            vv =-vv
            mns = _T
        else:
            mns = _F
        if vv == 0.0:
            res = Number(0)
            _S._p = res._p
            _S._d = res._d
            _S._m = res._m
            _S._e = res._e
            del _S._n
            _S._n = res._n
            del res
        else:
            exp = 38
            for _ in _R(-exp, exp + 1):
                if 10.0**exp <= vv:
                    break
                exp -= 1
            if exp != 0:
                vv /= 10.0 ** exp
            self._rec(1, 20)
            self._zad0()
            calc = int(vv) % 10
            last = calc
            self._n[0] = calc
            tmp = vv - float(calc)
            pow = 1
            while pow <= 20 and tmp > 0.0:
                tens = 10.0**pow
                calc = int(vv * tens)
                if calc > last * 10 + 9:
                    calc -= 1
                lest = calc
                self._n[pow] = calc % 10
                tmp = vv - float(calc) / tens
                pow += 1
            flt = _S._n
            pla = _S._p
            digs = _S._d
            _S._p -= exp
            _S._d += exp
            if _S._p < 0:
                tmp = _S._p
                _S._p = 0
            else:
                tmp = 0
            if _S._d < 0:
                _S._p -= _S._d
                _S._d = 0
            _S._d -= tmp
            _S._rec(_S._d, _S._p)
            if exp > 0:
                for tmp in _R(-_S._p, -_S._p - exp):
                    _S._set(tmp, 0)
            else:
                for tmp in _R(_S._d + exp, _S._d):
                    _S._set(tmp, 0)
            
            for tmp in _R(digs + pla):
                _S._set(-pla + tmp + exp, \
                                flt[digs + pla - 1 - tmp])
        _S._m = mns

    def _itod(self, vv):
        _S = self
        if vv == 0:
            _S._m = _F
            _S._d = 1
            _S._p = 0
            _S._n = _A(1)
            _S._n[0] = 0
        else:
            if vv < 0:
                _S._m = _T
                vv = -vv
            wrk = vv
            i = 0
            while wrk != 0:
                wrk //= 10
                i += 1
            _S._d = i
            _S._n = _A(i)
            while vv != 0:
                i -= 1
                _S._n[i] = vv % 10
                vv //= 10

    def _get(self, power):
        _S = self
        if power >= _S._d or power < -_S._p:
            return 0
        if _S._d == 0 and power == 0:
            return 0
        i = _S._d - power - 1
        return int(_S._n[i])

    def _set(self, power, vv):
        _S = self
        if power >= _S._d or power < -_S._p:
            return
        if _S._d == 0 and power == 0:
            return
        i = _S._d - power - 1
        _S._n[i] = vv

    def  _left(self):
        _S = self
        for p in _B(_R(-_S._p,_S._d)):
            _S._set(p + 1, _S._get(p))
        _S._set(-_S._p, 0)

    def _zad0(self):
        _S = self
        for iii in _R(_S._byt()):
            _S._n[iii] = 0
        _S._e = _F
        _S._m = _F
###########
_n = Number
def _add(f1, f2, cry):
    res = f1 + f2 + cry
    return (res % 10, res // 10)

def _sub(f1, f2, cry):
    f2 += cry
    if f1 >= f2:
        res = f1 - f2
        cry = 0
    else:
        res = (10 + f1) - f2
        cry = 1
    return (res, cry)

def _mult(f1, f2):
    res = f1 * f2
    return (res % 10, res // 10)

def _half(ff, mod):
    res = (10 * mod) + ff
    return (res // 2, res % 2)

def _abs_math(add, big, tiny):
    digs = max(big._d, tiny._d)
    pla = max(big._p, tiny._p)
    if add:
        digs +=1
    res = _n(0)
    res._rec(digs, pla)
    res._zad0()
    cry = 0
    for p in _R(-pla, digs):
        if add:
            vv, cry = _add(big._get(p), tiny._get(p), cry)
        else:
            vv, cry = _sub(big._get(p), tiny._get(p), cry)
        res._set(p, vv)
    res._sqz()
    res._e = big._e or tiny._e
    return res

def copy(ff):
    if not _I(ff, _n):
        raise _Te
    new = _n(0)
    new._rec(ff._d, ff._p)
    for pow in range(-ff._p, ff._d):
        new._set(pow, ff._get(pow))
    new._m = ff._m
    new._e = ff._e
    return new

def absolute(ff):
    if not _I(ff, _n):
        raise _Te
    new = copy(ff)
    new._m = _F
    return new

def integer(ff):
    if not _I(ff, _n):
        raise _Te
    new = copy(ff)
    for pow in _R(-new._p, 0):
        new._set(pow, 0)
    new._sqz()
    return new

def fraction(ff):
    if not _I(ff, _n):
        raise _Te
    new = copy(ff)
    for pow in _R(new._d):
        new._set(pow, 0)
    new._sqz()
    return new

def round(ff, pla):
    if not _I(ff, _n) or not _I(pla, int):
        raise _Te
    if pla < 0:
        raise _Ve
    if pla > ff._p:
        return copy(ff)
    res = _n(0)
    res._rec(ff._d + 1, pla)
    res._zad0()
    for pow in range(-pla, ff._d):
        res._set(pow, ff._get(pow))
    if ff._get(-pla - 1) >= 5:
        cry = 1
        for pow in range(-pla, res._d):
            sum, cry = _add(res._get(pow), 0, cry)
            res._set(pow, sum)
            if cry == 0:
                break
    res._sqz()
    res._m = ff._m
    res._e = ff._e 
    return res

def add(f1, f2):
    if not _I(f1, _n) or \
       not _I(f2, _n):
        raise _Te
    if f1._m == f2._m:
        res = _abs_math(_T, f1, f2)
        if f1._m:
            res._m = _T
        return res
    cmp = f2._abs_cmp(f1)
    if f1._m:
        if cmp == -1:
            res = _abs_math(_F,f1, f2)
            if not res.is_zero():
                res._m = _T
            return res
        return _abs_math(_F, f2, f1)
    if cmp > -1:
        res = _abs_math(_F, f2, f1)
        if not res.is_zero():
            res._m = _T
        return res
    return _abs_math(_F, f1, f2)
    
def subtract(f1, f2):
    if not _I(f1, _n) or not _I(f2, _n):
        raise _Te
    cmp = f1._abs_cmp(f2)
    if cmp > -1:
        if f1._m == f2._m:
            if cmp == 0:
                res = _n(0)
                if f1._e or f2._e:
                    res._e = _T
                return res
            res = _abs_math(_F, f1, f2)
            if f1._m and not res.is_zero():
                res._m = _T
            return res
        res = _abs_math(_T, f1, f2)
        if f1._m:
            res._m = _T
        return res
    if f1._m == f2._m:
        res = _abs_math(_F,f2, f1)
        if not f1._m:
            res._m = _T
        return res
    res = _abs_math(_T, f2, f1)
    if not f1._m and f2._m:
        return res
    res._m = _T
    return res

def multiply(f1, f2):
    if not _I(f1, _n) or not _I(f2, _n):
        raise _Te
    r_c = 0
    brk = _F
    if f1.is_zero() or f2.is_zero():
        res = _n(0)
        if f1._e or f2._e:
            res._e = _T
        return res
    res = _n(0)
    res._rec(f1._d + f2._d,f1._p + f2._p)
    for p1 in _R(-f1._p, f1._d):
        d1 = f1._get(p1)
        for p2 in _R(-f2._p, f2._d):
            put = p1 + p2
            tot, m_c = _mult(d1, f2._get(p2))
            tot, r_c = _add(tot, res._get(put), r_c)
            res._set(put, tot)
            while _T:
                put += 1
                if put >= res._d:
                    brk = _T
                    break
                tot, r_c = _add(m_c, res._get(put), r_c)
                res._set(put, tot)
                m_c = 0
                if r_c == 0:
                    break
            if brk:
                break
        if brk:
            break
    res._sqz()
    res._e = brk or f1._e or f2._e
    res._m = f1._m != f2._m and not res.is_zero()
    return res

def divide(num, den, ppp):
    if not _I(ppp, int) or not _I(num, _n) or not _I(den, _n):
        raise _Te
    if ppp < 0:
        raise _Ve
    if den.is_zero():
        res = copy(num)
        res._e = _T
        return res
    if num.is_zero():
        res = _n(0)
        if num._e or den._e:
            res._e = _T
        return res
    div = _N
    if den._d > 0:
        get = num._d - den._d + 1
        put = get - 1
        pla = den._p
        zz = 0
        if get <= 0:
            if den._p == 0:
                for p in _R(den._d):
                    if den._get(p) != 0:
                        break
                    zz += 1
            get = max(0, num._d + 1 - den._d)
        digs = den._d + 1 - zz
        if den._p == 0 and zz != 0:
            div = _n(0)
            div._rec(digs, pla)
            div._zad0()
    else:
        zz = -1
        for p in _B(_R(-den._p,0)):
            if den._get(p) != 0:
                break
            zz -= 1
        get = num._d - zz
        put = get - 1
        digs = 2
        pla = den._p + zz
        div = _n(0)
        div._rec(digs, pla)
        div._zad0()
    res = _n(0)
    res._rec(get, ppp)
    res._zad0()
    wrk = _n(0)
    wrk._rec(digs, pla)
    wrk._zad0()
    tot = num._d - 1
    if den._d == 0:
        mmm = tot - digs
        id = digs - 2
    elif not div is _N:
        mmm = tot - digs
        id = digs - 2
    else:
        mmm = tot - den._d - den._p
        id = den._d - 1
    for get in _B(_R(mmm + 1, num._d)):
        wrk._set(id, num._get(get))
        id -= 1
    if den._d == 0:
        id =0;
        for get in _B(_R(-den._p, zz + 1)):
            div._set(id, den._get(get))
            id -= 1
    elif not div is _N:
        id = digs - 2
        for get in _B(_R(zz, den._d)):
            div._set(id, den._get_d(get))
            id -= 1
    tmp = _N
    if div is _N:
        cmpr = copy(den)
        if den._m:
            cmpr = absolute(cmpr)
            tmp = absolute(den)
    else:
        cmpr = copy(div)
    luk = [cmpr]
    for _ in _R(9):
        if div is _N:
            if den._m:
                cmpr = add(cmpr, tmp)
            else:
                cmpr = add(cmpr, den)
        else:
            cmpr = add(cmpr, div)
        luk.append(cmpr)
    del tmp
    if den._d == 0:
        get = tot - pla - 1
    elif not div is _N:
        get = tot - digs + 1
    else:
        get = tot - (den._d + pla)
    if put >= -ppp:
        while _T:
            while wrk._abs_cmp(luk[0]) < 0:
                res._set(put, 0)
                put -= 1
                if put < -ppp:
                    break
                wrk._left()
                wrk._set(-pla, num._get(get))
                get -= 1
            if put < -ppp:
                break
            vv = 1
            cmp  = wrk._abs_cmp(luk[0])
            while cmp > 0:
                cmp = wrk._abs_cmp(luk[vv])
                vv += 1
            if cmp == 0:
                wrk._zad0()
            else:
                vv -= 1
                if vv != 0:
                    cry = 0
                    for p in _R(-wrk._p,wrk._d):
                        tmp, cry = _sub(wrk._get(p), \
                                        luk[vv - 1]._get(p),
                                        cry)
                        wrk._set(p, tmp)
            res._set(put, vv)
            put -= 1
            if put < -ppp:
                break
            if cmp !=0:
                wrk._left()
            wrk._set(-pla, num._get(get))
            get -= 1
    del luk
    del wrk
    if not div is _N:
        del div
    res._sqz()
    res._m = not res.is_zero() and den._m != num._m
    res._e = den._e or num._e
    return res
                    
def exponent_10(ff, pow):
    if not (_I(ff, _n) and _I(pow, int)):
        raise _Te
    if pow == 0:
        return copy(ff)
    ppp = ff._p - pow
    ddd = ff._d + pow
    if ppp < 0:
        tmp = ppp
        ppp = 0
    else:
        tmp = 0
        if ddd < 0:
            ppp -= ddd
            ddd = 0
    res = _n(0)
    res._rec(ddd - tmp, ppp)
    if pow > 0:
        for tmp in _R(-res._p, -res._p - pow):
            res._set(tmp, 0)
    else:
        for tmp in _R(res._d + pow, res._d):
            res._set(tmp, 0)
            
    for tmp in _R(-ff._p, ff._d):
        res._set(tmp + pow, ff._get(tmp))
    res._m = ff._m;
    res._e = ff._e;
    res._sqz()
    return res

def half(ff):
    if not _I(ff, _n):
        raise _Te
    res = _n(0)
    res._rec(ff._d, ff._p + 1)
    mod = 0
    for i in _R(ff._p + ff._d):
        div , mod = _half(ff._n[i], mod)
        res._n[i] = div
    if mod != 0:
        res._set(-res._p, 5)
    else:
        res._set(-res._p, 0)
    res._sqz()
    return res
