import pytest

from semantic_release.errors import UnknownCommitMessageStyleError
from semantic_release.history import hc_parser

text = 'This is an long explanatory part of a commit message. It should give ' \
       'some insight to the fix this commit adds to the codebase.'
footer = 'Closes #400'


def test_parser_raises_unknown_message_style():
    pytest.raises(UnknownCommitMessageStyleError, hc_parser, '')
    pytest.raises(UnknownCommitMessageStyleError, hc_parser,
                  '[docs] Some wrong commit')
    pytest.raises(UnknownCommitMessageStyleError, hc_parser,
                  'Some wrong commit')


def test_parser_return_correct_bump_level():
    assert(
        hc_parser('[major]: Add new parser pattern')[0] == 3
    )
    assert(
        hc_parser('[minor] Add new parser pattern')[0] == 2
    )
    assert(
        hc_parser('[patch] Add new parser pattern')[0] == 1
    )


def test_parser_return_subject_from_commit_message():
    assert(
        hc_parser('[Minor]: Add emoji parser')[3][0] ==
        'Add emoji parser'
    )
    assert(
        hc_parser('[Major] Fix regex in angular parser')[3][0] ==
        'Fix regex in angular parser'
    )
    assert(
        hc_parser('[patch]: Add a test for angular parser')[3][0] ==
        'Add a test for angular parser'
    )


def test_parser_return_text_from_commit_message():
    assert(
        hc_parser('[patch]: Fix regex in an parser\n\n{}'.format(text))[3][1] ==
        text
    )


def test_parser_return_footer_from_commit_message():
    commit = '[patch]: Fix env \n\n{t[text]}\n\n{t[footer]}'.format(t=globals())
    assert(
        hc_parser(commit)[3][2] == footer
    )


# def test_parser_should_accept_message_without_scope():
#     assert hc_parser('fix: superfix')[0] == 1
#     assert hc_parser('fix: superfix')[3][0] == 'superfix'
