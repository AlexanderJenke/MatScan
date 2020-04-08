from pylibdmtx.pylibdmtx import decode as find_codes


def parse(code: bytes) -> dict:
    """ Parse bytes in ASC or GS1 Format
    :param code: bytes to parse
    :return: dict containing data
    """
    content = {'RAW': code}
    if code[:7] == b'\x5B\x29\x3E\x1E06\x1D':  # Mac06 -> ASC
        content['dfi'] = "IFA"
        for part in code.split(b'\x1E')[1][2:].split(b'\x1D'):  # split along group separators
            if part[:4] == b'9N11':  # PPN-DE
                content['PPN'] = part[2:].decode("ascii")
                content['PZN'] = part[4:-2].decode("ascii")
            elif part[:7] == b'8P04150':  # GTIN/NTIN-DE
                content['GTIN'] = part[2:].decode("ascii")
                content['PZN'] = part[7:-1].decode("ascii")
            elif part[:1] == b'S':  # SN
                content['SN'] = part[1:].decode("ascii")
            elif part[:2] == b'1T':  # LOT
                content['LOT'] = part[2:].decode("ascii")
            elif part[:1] == b'D':  # EXP
                content['EXP'] = part[1:].decode("ascii")

    elif code[:1] == b'\x01':  # FNC1 -> GS1
        content['dfi'] = "GS1"
        while len(code):
            if code[:7] == b'0104150':  # GTIN/NTIN-DE
                content['GTIN'] = code[2:16].decode("ascii")
                content['PZN'] = code[7:15].decode("ascii")
                code = code[16:]
            elif code[:5] == b'04150':  # GTIN/NTIN-DE without AI (possibly wrong but shown in SecuPharm documentation)
                content['GTIN'] = code[:14].decode("ascii")
                content['PZN'] = code[5:13].decode("ascii")
                code = code[14:]
            elif code[:2] == b'21':  # SN
                content['SN'] = code[2:].split(b'\x01')[0].decode("ascii")
                code = code[2 + len(content['SN']) + 1:]
            elif code[:2] == b'10':  # LOT
                content['LOT'] = code[2:].split(b'\x01')[0].decode("ascii")
                code = code[2 + len(content['LOT']) + 1:]
            elif code[:2] == b'17':  # EXP
                content['EXP'] = code[2:8].decode("ascii")
                code = code[8:]
            elif code[:1] == b'\x01':  # starts with FNC1 -> look at next bit
                code = code[1:]
            else:
                raise LookupError(f"Remaining Code '{code}' can not be parsed.")

    else:  # Unknown format
        content['dfi'] = "UNKONWN"

    return content


def decode(image, max_count=1, timeout=200):
    return [parse(code.data) for code in find_codes(image, fnc1=True, max_count=max_count, timeout=timeout)]


if __name__ == '__main__':
    """ Regex to parse GS1
    pzn = re.findall(rb'\x01?0104150(\d{8})', code)
    exp = re.findall(rb'\x01?17(\d{6})', code)
    ch = re.findall(rb'\x01?10([\x21-\x22\x25-\x2F\x30-\x39\x3A-\x3F\x41-\x5A\x5F\x61-\x7A]{1,20})(\x01|\Z)', code)
    sn = re.findall(rb'\x01?21([\x21-\x22\x25-\x2F\x30-\x39\x3A-\x3F\x41-\x5A\x5F\x61-\x7A]{1,20})(\x01|\Z)', code)
    """

    print(parse(b'\x0110031325\x0117220731010415014272133521NX7KHP32W6CXW4'))
