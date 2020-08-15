import re

# negates a string, i.e.
# if string is '123'/'+123' then it gives '-123'
# if string is '-123' then it gives '+123'
def negate(s: str) -> str:
    if s[0] == '-':
        return '+' + s[1:]
    if s[0] == '+':
        return '-' + s[1:]
    return '-' + s # for no sign

# it takes input as a string
# and returns the equivalent simple expression
# for e.g:
# '--+123+-+---+2' returns '1+2' 
def equi_simp_exp(exp: str) -> str:
    signs = re.compile(r'[-+]+')
    # this function helps in getting the equivalent sign
    # for e.g: '++---+' returns '-'
    def get_equivalent_sign(s: str) ->str:
        non = 0 # number of negative sign
        for ch in s:
            if ch == '-':
                non += 1
        if non % 2 == 0:
            return '+'
        return '-'
    # now subtitute in the string
    exp = signs.sub(lambda m: get_equivalent_sign(m[0]), exp)
    return exp

# this function does binary operation based on strings
def _cal(exp: str) -> str:
    exp_re = re.compile(r'([-+]?\d+)([-+/*%])([-+]?\d+)')
    result = 0
    match = exp_re.search(exp)
    if match[2] == '-':
        result = int(match[1]) - int(match[3])
    elif match[2] == '+':
        result = int(match[1]) + int(match[3])
    elif match[2] == '/':
        result = int(int(match[1]) / int(match[3]))
    elif match[2] == '*':
        result = int(match[1]) * int(match[3])
    else:
        result = int(match[1]) % int(match[3])
    return str(result)

# deals with operations regarding + and -
def expression(exp: str) -> str:
    # first remove all white spaces
    exp = re.sub(r'\s', '', exp)
    # and then 
    exp = equi_simp_exp(exp)
    exp = term(exp)
    # find all + or - operators
    e_re = re.compile(r'([-+]?\d+)([-+])(\d+)')

    while re.search(r'.[+-]', exp):
        # execute the calculation
        exp = e_re.sub(lambda m: _cal(m[0]), exp, count=1)
        exp = equi_simp_exp(exp)
    return exp

#deals with operations regarding * and /
def term(exp: str) -> str:
    exp = primary(exp)
    # find all * or / operators
    e_re = re.compile(r'([-+]?\d+)([/*%])([-+]?\d+)')

    while re.search(r'.[*/%]', exp):
        # execute the calculation
        exp = e_re.sub(lambda m: _cal(m[0]), exp, count=1)
        exp = equi_simp_exp(exp)

    if re.search(r'[*/%]', exp):
        raise Exception('wrong syntax')
    return equi_simp_exp(exp)

# deals with parenthesis
def primary(exp: str) -> str:
    # find all parenthesis
    p_re = re.compile(r'\(([^(]+?)\)')

    while p_re.search(exp):
        exp = p_re.sub(lambda m: expression(m[1]), exp)
    
    if re.search(r'[()]', exp):
        raise Exception('wrong syntax')

    return equi_simp_exp(exp)

print(expression('75%7*12/6'))