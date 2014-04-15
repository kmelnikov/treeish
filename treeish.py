import copy
import re


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
    """
    :param dl1: list of dictionaries with default values
    :param dl2: list of dictionaries to join
    :param key: key to join
    :return: list of result dictionaries
    """
    dll = [d for d in dl1 if d.has_key(key)]
    dlr = [d for d in dl2 if d.has_key(key)]
    if not dll or not dlr:
        return dl1

    res = list()
    for rd in dll:
        for ld in dlr:
            res.append(join(rd, ld, key))
    return res


def join_right(dl1, dl2, key):
    return join_left(dl2, dl1, key)


def substitute(d1, d2):
    """
    If some key has no reference it remains. it gives ability to chain substitutions.

    :param d1: dict to put params
    :param d2: dict with values
    :return: dict with string expanded according to d2
    """
    if not d2:
        return d1
    params = d2.keys()
    for k, v in d1.items():
        if isinstance(v, dict):
            d1[k] = substitute(v, d2)
        if isinstance(v, basestring):
            s = set(re.findall(r'{(.+?)}', v))
            if s:
                for match_key in s:
                    if match_key in params:
                        d1[k] = d1[k].replace('{'+ match_key + '}', d2[match_key])
    return d1


def treefy(d1, d2):
    keys = set(d2)
    for k, v in d1.items():
        if v in keys:
            d1[k] = d2[v]
            continue
        if isinstance(v, dict):
            d1[k] = treefy(v, d2)
    return d1


def construct_tree(*karg):
    res = karg[0]
    for d in karg[1:]:
        res = treefy(res, d)
    return res


if __name__ == "__main__":
    d1 = {{'a'}: 'sub_tree'}
    d2 = {'sub_tree': {'d': 1}}
    print treefy(d1, d2),

