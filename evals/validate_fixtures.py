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
        self.elements = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.elements.append((tag, attrs))
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

    # Each category site is independently usable; it must not require the other language.
    for suffix, language in (("zh", "zh-CN"), ("en", "en")):
        site = fixtures / f"category.{suffix}"
        for page_name in ("index.html", "collection.html"):
            page = site / page_name
            parser = FixtureParser()
            parser.feed(page.read_text(encoding="utf-8"))
            ids = set(parser.ids)
            required = {"work-title", "caption-a", "caption-b", "source", "search", "search-help"}
            if parser.lang != language or required - ids or len(ids) != len(parser.ids):
                raise ValueError(f"Invalid category fixture: {page}")
            captions = {attrs.get("id") for tag, attrs in parser.elements if tag == "figcaption"}
            links = {attrs.get("href") for tag, attrs in parser.elements if tag == "a"}
            inputs = [attrs for tag, attrs in parser.elements if tag == "input" and attrs.get("id") == "search"]
            labels = [attrs for tag, attrs in parser.elements if tag == "label" and attrs.get("for") == "search"]
            if not {"caption-a", "caption-b"}.issubset(captions):
                raise ValueError(f"Missing caption elements: {page}")
            if not {"index.html", "collection.html"}.issubset(links):
                raise ValueError(f"Missing local site navigation: {page}")
            if len(inputs) != 1 or inputs[0].get("aria-describedby") != "search-help" or len(labels) != 1:
                raise ValueError(f"Missing search label or help association: {page}")
        print(f"OK: category.{suffix} two-page fixture structure")
    print("Fixture structure only; no agent or browser behavior was evaluated.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as error:
        print(f"Fixture validation failed: {error}", file=sys.stderr)
        sys.exit(1)
