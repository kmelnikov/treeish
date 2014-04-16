from treeish import join_with

__author__ = 'kmelnikov'


def costruction_of_family_tree():
    jones = {
        'father': "Sergey",
        'mather': "Irina",
        'child': "Konstantin"
    }

    jones_second = {
        'father': "Konstantin",
        'mother': "Tanya",
        'child': None
    }

    print join_with(
        jones,
        lambda k, v: k == 'father' and isinstance(v, basestring),
        jones_second
    )


if __name__ == '__main__':
    costruction_of_family_tree()