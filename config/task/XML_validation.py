# -*- coding: utf-8 -*-
a = '<?xml version="1.0" encoding="windows-1251"?>ValCurs Date="08.02.2022" name="Foreign Currency Market"><Valute ID="R01010"><NumCode>036</NumCode><CharCode>AUD</CharCode><Nominal>1</Nominal><Name>Австралийский доллар</Name><Value>53,6954</Value></Valute><Valute ID="R01020A"><NumCode>944</NumCode><CharCode>AZN</CharCode>'


def xml_valid(content):
    stack = []
    verify = True

    for lt in content:
        if lt in "<([{":
            stack.append(lt)
        elif lt in ")]}>":
            if len(stack) == 0:
                verify = False
                break

            br = stack.pop()
            if br == '(' and lt == ')':
                continue
            if br == '[' and lt == ']':
                continue
            if br == '{' and lt == '}':
                continue
            if br == '<' and lt == '>':
                continue

            verify = False
            break

    """По итогу проверки стен должен быть пустым"""
    if verify and len(stack) == 0:
        return True
    else:
        return False


if __name__ == '__main__':
    xml_valid(a)
