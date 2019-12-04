"""Angular commit style commit parser
"""
import re
from typing import Tuple

import ndebug

from ..errors import UnknownCommitMessageStyleError
from .parser_helpers import parse_text_block

debug = ndebug.create(__name__)

TYPES = {
    'major': 'major',
    'minor': 'minor',
    'patch': 'patch',
}

re_parser = re.compile(
    r'(\[(?P<type>' + '|'.join(TYPES.keys()) + r')\]?:? )'
    r'(?P<subject>[^\n]+)'
    r'(:?\n\n(?P<text>.+))?',
    re.DOTALL | re.IGNORECASE
)

MINOR_TYPES = [
    'minor',
]

PATCH_TYPES = [
    'patch',
]

MAJOR_TYPES = [
    'major',
]


def parse_commit_message(message: str) -> Tuple[int, str, str, Tuple[str, str, str]]:
    """
    Parses a commit message according to the angular commit guidelines specification.

    :param message: A string of a commit message.
    :return: A tuple of (level to bump, type of change, scope of change, a tuple with descriptions)
    :raises UnknownCommitMessageStyleError: if regular expression matching fails
    """
    parsed = re_parser.match(message)
    if not parsed:
        raise UnknownCommitMessageStyleError(
            'Unable to parse the given commit message: {}'.format(message)
        )

    level_bump = 0

    if parsed.group('type').lower() in MAJOR_TYPES:
        level_bump = max([level_bump, 3])

    if parsed.group('type').lower() in MINOR_TYPES:
        level_bump = max([level_bump, 2])

    if parsed.group('type').lower() in PATCH_TYPES:
        level_bump = max([level_bump, 1])

    body, footer = parse_text_block(parsed.group('text'))
    if debug.enabled:
        debug('parse_commit_message -> ({}, {}, {}, {})'.format(
            level_bump,
            TYPES[parsed.group('type').lower()],
            '',
            (parsed.group('subject'), body, footer)
        ))
    return (
        level_bump,
        TYPES[parsed.group('type').lower()],
        '',
        (parsed.group('subject'), body, footer)
    )
