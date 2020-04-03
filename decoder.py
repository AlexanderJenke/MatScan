import re

from pylibdmtx.pylibdmtx import decode as find_codes


def decode(image):
    return [parse(code.data) for code in find_codes(image, fnc1=True, max_count=1, timeout=200)]


def parse(code):
    fn = parse_unknown
    if code.startswith(b'01') or code.startswith(b'\x0101'):
        fn = parse_gs1

    elif code.startswith(b'[)'):
        fn = parse_asc

    return fn(code)


def parse_unknown(code):
    return {'type': 'unknown', 'content': code}


def parse_gs1(code):
    data = {'type': 'gs1'}
    pzn = re.findall(rb'\x01?0104150(\d{8})', code)
    exp = re.findall(rb'\x01?17(\d{6})', code)
    ch = re.findall(rb'\x01?10([\x21-\x22\x25-\x2F\x30-\x39\x3A-\x3F\x41-\x5A\x5F\x61-\x7A]{1,20})(\x01|\Z)', code)
    sn = re.findall(rb'\x01?21([\x21-\x22\x25-\x2F\x30-\x39\x3A-\x3F\x41-\x5A\x5F\x61-\x7A]{1,20})(\x01|\Z)', code)

    if len(pzn):
        data['PZN'] = pzn[0].decode('ascii')
    if len(sn):
        data['SN'] = sn[0][0].decode('ascii')
    if len(ch):
        data['Ch'] = ch[0][0].decode('ascii')
    if len(exp):
        data['Exp'] = exp[0].decode('ascii')

    return data


def parse_asc(code):
    data = {'type': 'asc'}

    for part in code[7:-2].split(b'\x1d'):
        if part[:4] == b'9N11':
            data['PZN'] = part[4:-2].decode("ascii")
        elif part[:7] == b'8P04150':
            data['PZN'] = part[7:-1].decode("ascii")
        elif part[:1] == b'S':
            data['SN'] = part[1:].decode("ascii")

        elif part[:2] == b'1T':
            data['Ch'] = part[2:].decode("ascii")

        elif part[:1] == b'D':
            data['Exp'] = part[1:].decode("ascii")

    return data
