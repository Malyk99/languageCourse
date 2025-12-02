import json

class PhraseParser:
    """
    Parses lesson text files where each line follows:
        English phrase / Spanish phrase

    Improvements:
    - Ignores empty lines
    - Ignores comments (# or //)
    - Warns about invalid lines
    - Handles extra slashes gracefully
    - Strips BOM characters
    - Adds phrase IDs optionally
    """

    def parse(self, raw_text: str, include_ids=True):
        lines = raw_text.replace("\ufeff", "").splitlines()
        parsed = []

        for i, line in enumerate(lines, start=1):
            line = line.strip()

            # Skip empty lines
            if not line:
                continue

            # Skip comment lines
            if line.startswith("#") or line.startswith("//"):
                continue

            # Must contain a separator
            if "/" not in line:
                print(f"[PhraseParser] Warning: line {i} missing '/', skipping -> {line}")
                continue

            en, es = line.split("/", 1)
            en = en.strip()
            es = es.strip()

            if not en or not es:
                print(f"[PhraseParser] Warning: line {i} missing English or Spanish, skipping -> {line}")
                continue

            entry = {"en": en, "es": es}
            if include_ids:
                entry["id"] = len(parsed) + 1

            parsed.append(entry)

        return parsed

    def to_json(self, data):
        return json.dumps(data, ensure_ascii=False, indent=2)
