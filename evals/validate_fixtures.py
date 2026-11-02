"""Validate fixture structure, not model behavior or design quality."""

from html.parser import HTMLParser
from pathlib import Path
import sys


class FixtureParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.lang = None
        self.scripts = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "html":
            self.lang = attrs.get("lang")
        if tag == "script" and attrs.get("src"):
            self.scripts.append(attrs["src"])


def main():
    fixtures = Path(__file__).resolve().parent / "fixtures"
    required_ids = {f"c{i:02}" for i in range(1, 15)} | {
        "release-preview", "outside-scope", "shared-preview", "shared-example", "search"
    }
    for suffix, language in (("zh", "zh-CN"), ("en", "en")):
        html_path = fixtures / f"exhibition.{suffix}.html"
        script_path = fixtures / f"shared.{suffix}.js"
        parser = FixtureParser()
        parser.feed(html_path.read_text(encoding="utf-8"))
        ids = set(parser.ids)
        missing = required_ids - ids
        if parser.lang != language or missing or len(ids) != len(parser.ids):
            raise ValueError(f"Invalid {html_path.name}: language, missing IDs, or duplicate IDs: {sorted(missing)}")
        if parser.scripts != [script_path.name] or not script_path.is_file():
            raise ValueError(f"Invalid shared script for {html_path.name}")
        script = script_path.read_text(encoding="utf-8")
        if 'querySelector("#shared-preview")' not in script or 'querySelector("#shared-example")' not in script:
            raise ValueError(f"Shared mounts missing in {script_path.name}")
        print(f"OK: {html_path.name} fixture structure")
    print("Fixture structure only; no agent or browser behavior was evaluated.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as error:
        print(f"Fixture validation failed: {error}", file=sys.stderr)
        sys.exit(1)
