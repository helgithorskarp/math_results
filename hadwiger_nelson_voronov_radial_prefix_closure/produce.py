#!/usr/bin/env python3
import json
from pathlib import Path

from exact_model import exact_certificate


HERE = Path(__file__).resolve().parent
destination = HERE / "certificate.generated.json"
destination.write_text(json.dumps(exact_certificate(), indent=2) + "\n")
print(destination)
