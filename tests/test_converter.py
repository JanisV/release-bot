from unittest.mock import Mock

import pytest
from telegram._utils.defaultvalue import DEFAULT_NONE
from telegram.constants import ParseMode

from app.repo_engine import format_release_message

@pytest.fixture
def empty_repo():
    repo = Mock()
    repo.full_name = ""
    return repo

@pytest.fixture
def empty_release():
    release = Mock()
    release.tag_name = ""
    release.title = ""
    release.body = ""
    release.html_url = ""
    release.prerelease = False
    release.updated = False
    return release

def test_format_quote_empty_input(empty_repo, empty_release):
    release_note_format = "quote"

    message, parse_mode, entities = format_release_message(release_note_format, empty_repo, empty_release)

    assert parse_mode == ParseMode.HTML
    assert message == "<b></b>\n <a href=''></a>\n<blockquote></blockquote>"

def test_format_pre_empty_input(empty_repo, empty_release):
    release_note_format = "pre"

    message, parse_mode, entities = format_release_message(release_note_format, empty_repo, empty_release)

    assert parse_mode == ParseMode.HTML
    assert message == "<b></b>\n <a href=''></a>\n<pre></pre>"

def test_format_html_empty_input(empty_repo, empty_release):
    release_note_format = "html"

    message, parse_mode, entities = format_release_message(release_note_format, empty_repo, empty_release)

    assert parse_mode == DEFAULT_NONE
    assert message == "****\n\n"

def test_format_markdown_empty_input(empty_repo, empty_release):
    release_note_format = None

    message, parse_mode, entities = format_release_message(release_note_format, empty_repo, empty_release)

    assert parse_mode == ParseMode.MARKDOWN_V2
    assert message == "————————\n"

if __name__ == '__main__':
    pytest.main([__file__])
