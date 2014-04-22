from treeish import join_with, substitute

__author__ = 'kmelnikov'


def construction_of_family_tree():
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


def latter_description():
    latter = {
        "Name": "Konstantin",
        "Later": "Hello {Name},\n"
                 "I'm a test latter for you.\n\n"
                 "Kind Regards,\n"
                 "{Name}\n"
    }
    print substitute(latter, latter)['Later']


if __name__ == '__main__':
    construction_of_family_tree()
    latter_description()