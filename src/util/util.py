import re


def html_to_md(inp):
    out = re.sub(r'<i>|</i>', '_', inp)
    out = re.sub(r'<b>|</b>', '**', out)
    out = re.sub(r'<u>|</u>', '__', out)
    out = re.sub(r'<br>', '\n', out)
    return out

if __name__ == '__main__':
    print(html_to_md('Whenever this minion takes damage, add a <b>Spare Part</b> card to your hand.'))