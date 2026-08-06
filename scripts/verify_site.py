#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
HTML_FILES = sorted(ROOT.rglob("*.html"))
PRIVATE_PATTERNS = [
    re.compile(r"/root/"),
    re.compile(r"agent_token", re.I),
    re.compile(r"github[_-]?token", re.I),
    re.compile(r"private[_-]?key", re.I),
    re.compile(r"seed phrase", re.I),
]


class Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag not in {"a", "link"}:
            return
        data = dict(attrs)
        value = data.get("href")
        if value:
            self.links.append(value)


def assert_local_links(path: Path, links: list[str]) -> None:
    for link in links:
        parsed = urlparse(link)
        if parsed.scheme or parsed.netloc or link.startswith("#"):
            continue
        target = (path.parent / parsed.path).resolve()
        assert ROOT in target.parents or target == ROOT, (path, link, "escape")
        assert target.exists(), (path, link, "missing")


def main() -> None:
    assert len(HTML_FILES) == 5, HTML_FILES
    all_text = ""
    for path in HTML_FILES:
        text = path.read_text(encoding="utf-8")
        all_text += text
        parser = Links()
        parser.feed(text)
        assert_local_links(path, parser.links)
        assert '<meta name="viewport"' in text
        assert "<title>" in text
        for pattern in PRIVATE_PATTERNS:
            assert not pattern.search(text), (path, pattern.pattern)

    runx = json.loads((ROOT / "evidence/runx-love-evidence.json").read_text())
    assert runx["claim_type"] == "public_runx_walkthrough"
    assert runx["runx_link_found"] is True
    assert runx["run_evidence"]["verified_valid"] is True
    assert runx["run_evidence"]["signature_mode"] == "local-development"
    assert runx["run_evidence"]["production_notary_claimed"] is False

    frantic = json.loads((ROOT / "evidence/frantic-writeup-evidence.json").read_text())
    assert frantic["claim_type"] == "public_post"
    assert frantic["receipt_link_found"] is True
    assert frantic["receipt_url"] == "https://gofrantic.com/r/b3aad156"
    assert frantic["duplicate_reward"] is False

    assert "https://github.com/runxhq/runx" in all_text
    assert "https://gofrantic.com/r/b3aad156" in all_text
    assert "accepted_awaiting_payout" in all_text
    assert "$0 realized income" in all_text
    print(json.dumps({"status": "pass", "html_files": len(HTML_FILES), "runx_evidence": "pass", "frantic_evidence": "pass"}, sort_keys=True))


if __name__ == "__main__":
    main()
