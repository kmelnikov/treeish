import copy

def f_join(d1, d2, criteria):
    """
    @param d1, d2: two dictionaries
    @param key: key to join

    @return the result key consisted of two values of two dictionaries
    """
    if not d1 or not d2:
        return {}

    if not criteria(d1) or not criteria(d2):
        raise KeyError

    res = copy.deepcopy(d1)
    if criteria(d1) == criteria(d2):
        res.update(d2)
    return res

def join(d1, d2, key):
    """
    @param d1, d2: two dictionaries
    @param key: key to join

    @return the result key consisted of two values of two dictionaries
    """
    if not d1 or not d2:
        return {}

    if not d1.has_key(key) or not d1.has_key(key):
        raise KeyError

    res = copy.deepcopy(d1)
    if res[key] == d2[key]:
        res.update(d2)
    return res


def join_left(dl1, dl2, key):
    dll = [d for d in dl1 if d.has_key(key)]
    dlr = [d for d in dl2 if d.has_key(key)]
    res = list()
    for rd in dll:
        for ld in dlr:
            res.append(join(rd, ld, key))
    return res


def f_join_left(dl1, dl2, criteria):
    dll = [d for d in dl1 if criteria(d)]
    dlr = [d for d in dl2 if criteria(d)]
    res = list()
    for rd in dll:
        for ld in dlr:
            res.append(f_join_left(rd, ld, criteria))
    return res


def join_right(dl1, dl2, key):
    return join_left(dl2, dl1, key)


if __name__ == "__main__":
    d1 = dict(a=1, b=2, d=2)
    d2 = dict(a=1, c=2, r=2)
    d3 = dict(a=1, d=2, e=1)
    # print join_left([d1], [d2, d3], 'd')
    print f_join_left([d1], [d2, d3], lambda x: x.has_key())
    # print join_right([d1], [d2, d3], 'a')