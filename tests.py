from nose.tools import ok_, eq_
from treeish import join_right, join_left, substitute, treefy, construct_tree, join_with

__author__ = 'kmelnikov'


def test_empty():
    eq_(join_left([{}], [{}], 'a'), [{}], "2 empty dictionaries")


def test_one_empty():
    eq_(join_left([{}], [{'a': 1}], 'a'), [{}], "1 empty dictionary")


def test_second_empty():
    eq_(join_left([{'a': 1}], [{}], 'a'), [{'a': 1}], "1 empty dictionary")


def test_simple_join():
    eq_(
        join_left(
            [{'a': 1, 'b': 2}],
            [{'a': 1, 'c': 3}],
            'a'),
        [{'a': 1, 'b': 2, 'c': 3}],
        "1 empty dictionary"
    )


def test_simple_negative():
    eq_(
        join_left(
            [{'a': 1, 'b': 2}],
            [{'a': 2, 'b': 3}],
            'a'),
        [{'a': 1, 'b': 2}],
        "1 empty dictionary"
    )


def test_two_dict():
    eq_(
        join_left(
            [{'a': 1, 'b': 2}],
            [{'a': 1, 'c': 3}, {'a': 1, 'c': 4}],
            'a')
        ,
        [
            {'a': 1, 'b': 2, 'c': 3},
            {'a': 1, 'b': 2, 'c': 4}
        ],
        "1 empty dictionary"
    )


# #### Substitutions

def test_sub_empty_dict():
    eq_(
        substitute({'a': "{h}"}, {}),
        {'a': "{h}"},
        "Substitute empty dict doesn't change anything"
    )


def test_sub_simple_dict():
    eq_(
        substitute({'a': "{h}"}, {'h': "d"}),
        {'a': "d"},
        "Simple string substitution"
    )


def test_sub_several_in_one_val():
    eq_(
        substitute({'a': "{h}+{h}+{a}"}, {'a': 't', 'h': "d"}),
        {'a': "d+d+t"},
        "Several substitution in one value"
    )


def test_sub_two_inner_dict():
    eq_(
        substitute({'a': {'a': "{a}"}}, {'a': 't'}),
        {'a': {'a': "t"}},
        "Inner dict handled"
    )


def test_sub_self_dict():
    d = {'a': '{b}', 'b': 'c'}
    eq_(
        substitute(d, d),
        {'a': 'c', 'b': 'c'},
        "Self substitution"
    )


##### Treefy tests

def test_simple_tree():
    d1 = {'a': 'sub_tree'}
    d2 = {'sub_tree': {'d': 1}}
    eq_(
        treefy(d1, d2),
        {'a': {'d': 1}},
        "Make base tree"
    )


def test_simple_tree_from_list():
    d1 = {'a': 'sub_tree'}
    d2 = {'sub_tree': {'d': 1}}
    eq_(
        construct_tree(d1, d2, d2),
        {'a': {'d': 1}},
        "Make base tree"
    )


###### Test join with
def test_simple_join_with():
    d1 = {'a': 'sub_tree', 'b': 'hello'}
    d2 = {'b': 'sub_tree', 'c': 'hello'}
    eq_(
        join_with(d1, lambda x, y: isinstance(y, str), d2),
        {'a': d2, 'b': d2},
        "Make complex tree if has common keys"
    )


def test_simple_negative_join_with():
    d1 = {'a': 'sub_tree1', 'b': 'hello1'}
    d2 = {'b': 'sub_tree', 'c': 'hello'}
    eq_(
        join_with(d1, lambda x, y: isinstance(y, str), d2),
        d1,
        "Not join different trees"
    )


def test_simple_join_with_complex_condition():
    d1 = {'a': 'sub_tree', 'b': 'hello'}
    d2 = {'b': 'sub_tree', 'c': 'hello'}
    eq_(
        join_with(d1, lambda x, y: x == 'b' and isinstance(y, str), d2),
        {'a': d2, 'b': 'hello'},
        "Not join different trees"
    )
