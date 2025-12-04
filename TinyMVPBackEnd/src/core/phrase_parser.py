import json

class PhraseParser:
    """
    Extended parser:

    - Standard lines:   English / Spanish
    - Special lines:    ¿¿ Spanish phrase
    """

    def parse(self, raw_text: str, include_ids=True):
        lines = raw_text.replace("\ufeff", "").splitlines()

        parsed = []            # normal EN/ES phrases
        spanish_spoken = []    # special ¿¿ Spanish-only TTS phrases

        for i, line in enumerate(lines, start=1):
            line = line.strip()

            # Ignore empty or comment lines
            if not line or line.startswith("#") or line.startswith("//"):
                continue

            # --------------------------------------------
            # NEW FEATURE: lines starting with "¿¿"
            # --------------------------------------------
            if line.startswith("¿¿"):
                spanish = line[2:].strip()

                if not spanish:
                    print(f"[PhraseParser] Warning: line {i} has '¿¿' but no text")
                    continue

                entry = {"es": spanish}

                if include_ids:
                    entry["id"] = len(spanish_spoken) + 1

                spanish_spoken.append(entry)
                continue

            # --------------------------------------------
            # Normal lines must contain English / Spanish
            # --------------------------------------------
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

        # Return a structured JSON-ready dictionary
        return {
            "phrases": parsed,
            "spanish_spoken": spanish_spoken
        }

    def to_json(self, data):
        return json.dumps(data, ensure_ascii=False, indent=2)
