import os
from unittest.mock import Mock

import pytest
from telegram._utils.defaultvalue import DEFAULT_NONE
from telegram.constants import ParseMode

from app.repo_engine import format_release_message

FORMATTING_PARAMS = {
    "quote": {"format": "quote", "mode": ParseMode.HTML},
    "pre": {"format": "pre", "mode": ParseMode.HTML},
    "html": {"format": "html", "mode": DEFAULT_NONE},
    "markdown": {"format": None, "mode": ParseMode.MARKDOWN_V2},
}

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
    release_note_format = FORMATTING_PARAMS["quote"]["format"]

    message, parse_mode, entities = format_release_message(release_note_format, empty_repo, empty_release)

    assert parse_mode == FORMATTING_PARAMS["quote"]["mode"]
    assert message == "<b></b>\n <a href=''></a>\n<blockquote></blockquote>"

def test_format_pre_empty_input(empty_repo, empty_release):
    release_note_format = FORMATTING_PARAMS["pre"]["format"]

    message, parse_mode, entities = format_release_message(release_note_format, empty_repo, empty_release)

    assert parse_mode == FORMATTING_PARAMS["pre"]["mode"]
    assert message == "<b></b>\n <a href=''></a>\n<pre></pre>"

def test_format_html_empty_input(empty_repo, empty_release):
    release_note_format = FORMATTING_PARAMS["html"]["format"]

    message, parse_mode, entities = format_release_message(release_note_format, empty_repo, empty_release)

    assert parse_mode == FORMATTING_PARAMS["html"]["mode"]
    assert message == "****\n\n"

def test_format_markdown_empty_input(empty_repo, empty_release):
    release_note_format = FORMATTING_PARAMS["markdown"]["format"]

    message, parse_mode, entities = format_release_message(release_note_format, empty_repo, empty_release)

    assert parse_mode == FORMATTING_PARAMS["markdown"]["mode"]
    assert message == "————————\n"

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

def get_test_cases():
    files = [f[:-5] for f in os.listdir(DATA_DIR) if f.endswith('.orig')]
    return files

@pytest.mark.parametrize("case_name", get_test_cases())
def test_format_quote_input(empty_repo, empty_release, case_name):
    release_note_format = FORMATTING_PARAMS["quote"]["format"]

    orig_path = os.path.join(DATA_DIR, f"{case_name}.orig")
    dst_path = os.path.join(DATA_DIR, f"{case_name}.quote")
    with open(orig_path, 'r', encoding='utf-8', newline="") as f:
        orig_content = f.read()
    with open(dst_path, 'r', encoding='utf-8', newline="") as f:
        dst_content = f.read()

    empty_release.body = orig_content

    message, parse_mode, entities = format_release_message(release_note_format, empty_repo, empty_release)

    assert parse_mode == FORMATTING_PARAMS["quote"]["mode"]
    assert message == dst_content

@pytest.mark.parametrize("case_name", get_test_cases())
def test_format_pre_input(empty_repo, empty_release, case_name):
    release_note_format = FORMATTING_PARAMS["pre"]["format"]

    orig_path = os.path.join(DATA_DIR, f"{case_name}.orig")
    dst_path = os.path.join(DATA_DIR, f"{case_name}.pre")
    with open(orig_path, 'r', encoding='utf-8', newline="") as f:
        orig_content = f.read()
    with open(dst_path, 'r', encoding='utf-8', newline="") as f:
        dst_content = f.read()

    empty_release.body = orig_content

    message, parse_mode, entities = format_release_message(release_note_format, empty_repo, empty_release)

    assert parse_mode == FORMATTING_PARAMS["pre"]["mode"]
    assert message == dst_content

@pytest.mark.parametrize("case_name", get_test_cases())
def test_format_html_input(empty_repo, empty_release, case_name):
    release_note_format = FORMATTING_PARAMS["html"]["format"]

    orig_path = os.path.join(DATA_DIR, f"{case_name}.orig")
    dst_path = os.path.join(DATA_DIR, f"{case_name}.html")
    with open(orig_path, 'r', encoding='utf-8', newline="") as f:
        orig_content = f.read()
    with open(dst_path, 'r', encoding='utf-8', newline="") as f:
        dst_content = f.read()

    empty_release.body = orig_content

    message, parse_mode, entities = format_release_message(release_note_format, empty_repo, empty_release)

    assert parse_mode in (FORMATTING_PARAMS["html"]["mode"], FORMATTING_PARAMS["markdown"]["mode"])
    assert message == dst_content

@pytest.mark.parametrize("case_name", get_test_cases())
def test_format_markdown_input(empty_repo, empty_release, case_name):
    release_note_format = FORMATTING_PARAMS["markdown"]["format"]

    orig_path = os.path.join(DATA_DIR, f"{case_name}.orig")
    dst_path = os.path.join(DATA_DIR, f"{case_name}.md")
    with open(orig_path, 'r', encoding='utf-8', newline="") as f:
        orig_content = f.read()
    with open(dst_path, 'r', encoding='utf-8', newline="") as f:
        dst_content = f.read()

    empty_release.body = orig_content

    message, parse_mode, entities = format_release_message(release_note_format, empty_repo, empty_release)

    assert parse_mode == FORMATTING_PARAMS["markdown"]["mode"]
    assert message == dst_content

if __name__ == '__main__':
    pytest.main([__file__])
