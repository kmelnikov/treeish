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
                        d1[k] = d1[k].replace('{' + match_key + '}', d2[match_key])
    return d1


def treefy(d1, d2):
    """
    Construct complex dict from base @d1 by adding value from @d2
    """
    keys = set(d2)
    for k, v in d1.items():
        if isinstance(v, dict):
            d1[k] = treefy(v, d2)
            continue
        if hasattr(v, '__hash__') and v in keys:
            d1[k] = d2[v]
            continue
    return d1


def construct_tree(*karg):
    """
    Get list of dictionaries and fold it with treefy function.
    :param karg: list of dictionaries.
    :return: complex dict with all values expanded
    """
    res = karg[0]
    for d in karg[1:]:
        res = treefy(res, d)
    return res


def join_with(d1, tp, *karg):
    """
    Construct tree using d1 as a base. If tp(key,value) of some later dict in list returns true it was considered as a
     candidate to join.

    :param d1: base dict
    :param tp: predicate to consider if the parir in dict should be considered as candidate to join. Usually some check
    on type of value.
    :param karg: list of dicts to get subtrees from

    :return: Tree based on d1 dictionary
    """
    vals = list()

    for d2 in karg:
        vals.append((d2, [v for k, v in d2.items() if tp(k, v)]))

    for k, v in d1.items():
        for d2, values_in_dict in vals:
            if v in values_in_dict:
                d1[k] = d2
    return d1


def invert(d1):
    """
    Turn keys to values and visa versa.

    :param d1: base dictionary
    :return: inverted dictionary
    """
    return dict({(v, k) for k, v in d1.items()})


def covert_with_schema(data, schema):
    """
    Get arbitrary dictionary and rename its keys according to schema.

    @param data: data to convert
    @param schema: contains info on how to form result dictionary
    """
    result = dict()
    for key, value in data.items():
        if schema.has_key(key):
            # not checked
            if '.' in schema[key]:
                v = result
                keys_list = schema[key].split('.')
                for sub_key in keys_list[:-1]:
                    if not v.has_key(sub_key):
                        v[sub_key] = dict()
                    v = v[sub_key]
                v[keys_list[-1]] = data[key]
            else:
                result[schema[key]] = data[key]
        else:
            if key in result:
                raise SchemaCleanData()
            result[key] = data[key]
    return result


def only_with_keys(d, key_list):
    """
    Remove all keys from @d that are not in @key_list
    """
    result = d()
    for key, value in d.items():
        if key in key_list:
            result[key] = d[key]
    return result


def make_d(d):
    """
    Make simple one level dict from the one of depth n

    :param d: dict which contains
    :return: dict with only one level. all keys are folded to 'key1.key2.key3' notation
    """
    def add_key(dd, key):
        return dict([(key + '.' + k, v) for k, v in dd.items()])

    if not isinstance(d, dict):
        return d
    for k, v in d.items():
        if isinstance(v, dict):
            dd = make_d(v)
            dd = add_key(dd, k)
            del d[k]
            d.update(dd)
    return d


def unfold_d(d):
    """
    Opposite to make_d function. Unfold dotted notation to initial complex dict.

    :param d: dict with dotted notation
    :return: complex dict
    """
    def unfold(key_list, v):
        if len(key_list) > 1:
            return {key_list[0]: unfold(key_list[1:], v)}
        else:
            return {key_list[0]: v}

    def recursive_update(d1, d2):
        for k, v in d2.items():
            if isinstance(v, dict) and k in d1 and isinstance(d1[k], dict):
                recursive_update(d1[k], v)
                continue
            d1[k] = v

    res = dict()
    for k, v in d.items():
        if '.' in k:
            recursive_update(res, unfold(k.split('.'), v))
        else:
            res[k] = v

    return res


if __name__ == "__main__":
    d = {'t.t.d': 'a.b', 't.t.c': 'a.b.c'}
    print unfold_d(d)
