

def read_txt(file_name: str):
    with open(file_name) as f:
        ret = f.read().splitlines()
    return ret


def read_and_parse_text(file_name: str):
    text = read_txt(file_name)
    ret = {}
    for line in text[1:]:
        split_text = line.split(',')
        ret[split_text[0]] = [float(x) for x in split_text[1:]]
    return ret