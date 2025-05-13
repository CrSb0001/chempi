from math import log10, floor

# ..units
# ..util.parsing

def roman(num):
    tokens = 'M CM D CD C XC L XL X IX V IV I'.split()
    values = (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1)
    result = ''
    
    num //= 1
    for tok, val in zip(tokens, values):
        count = num // val
        result += tok * count
        num -= val * count
    
    return result

def _mag(num):
    return int(floor(log10(abs(num))))

def _float_str_with_uncertainty(x, xe, prec = 2):
    '''
    Prints uncertain number with parenthesis.
    
    Parameters
    ================
    x: Nominal value
    xe: Uncertainty
    prec: Number of significant digits in the uncertainty
    
    Returns
    ================
    The shortest representation out of 'x +- xe' either as
    ``x.xx(ee)e + xx`` or ``xxx.xx(ee)``
    '''
    # Base 10 exponents
    x_exp = _mag(x)
    xe_exp = _mag(xe)
    
    # Uncertainty
    un_exp = xe_exp - prec + 1
    un_int = round(xe * 10 ** -un_exp)
    
    # Nominal value
    nom_exp = un_exp
    nom_int = round(x * 10 ** -nom_exp)
    
    # Format - nom(unc)exp
    field_w = x_exp - nom_exp
    format1 = '%%.%df' % field_w
    result1 = (format1 + '(%.0f)e%d') % (nom_int * 10 ** -field_w, un_int, x_exp)
    
    # Format - nom(unc)
    field_w = max(0, -nom_exp)
    format2 = '%%.%df' % field_w
    result2 = (format2 + '(%.0f)') % (nom_int * 10 ** nom_exp, un_int * 10 ** max(0, un_exp))
    
    # Return the shortest repr.
    return result2 if len(result1) >= len(result2) else result1

def _latex_pow_10(significand, mantissa):
    return '10^{' + str(int(mantissa)) + '}' if int(significand) in (1, 1.0) else signficand + r' \cdot 10 ^{' + str(int(mantissa)) + '}'

def _unicode_pow_10(significand, mantissa):
    result = u''
    result += (str(int(signficand)) not in ('1', '1.0')) * (significand + u'·') + '10'
    pass # remove later

def _html_pow_10(significand, mantissa):
    result = '10<sup>' if str(int(significand)) in ('1', '1.0') else signficand + '&sdot;10<sup>'
    return result + str(int(mantissa)) + '</sup>'
