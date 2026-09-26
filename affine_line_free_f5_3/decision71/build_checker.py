"""Build the documented allocation-only DRAT-trim configuration locally."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

UPSTREAM_COMMIT = "2e3b2dc0ecf938addbd779d42877b6ed69d9a985"
BASE_SHA256 = "d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee"
PATCHED_SHA256 = "9c8dfa3e02fe7ab6102ee799165f04188d6738c1dbe5ba249b1cb86a1dd2b288"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--sanitize", action="store_true")
    args = parser.parse_args()
    original = args.source.read_bytes()
    if hashlib.sha256(original).hexdigest() != BASE_SHA256:
        raise ValueError("unexpected upstream DRAT-trim source")
    replacements = [
        (b"#define BIGINIT     1000000", b"#define BIGINIT     65536"),
        (b"if (S->mem_used + size + EXTRA >= DBsize)",
         b"while (S->mem_used + size + EXTRA >= DBsize)"),
    ]
    patched = original
    for before, after in replacements:
        if patched.count(before) != 1:
            raise ValueError("checker patch context is not unique")
        patched = patched.replace(before, after)
    if hashlib.sha256(patched).hexdigest() != PATCHED_SHA256:
        raise ValueError("checker patch does not match the validated source")
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    source, binary = out / "drat-trim-65536.c", out / "drat-trim-65536"
    source.write_bytes(patched)
    flags = (["-O1", "-g", "-fsanitize=address,undefined", "-fno-omit-frame-pointer"]
             if args.sanitize else ["-O2"])
    subprocess.run(["gcc", "-std=gnu99", *flags, str(source), "-o", str(binary)], check=True)
    result = {"upstream_commit": UPSTREAM_COMMIT, "upstream_source_sha256": BASE_SHA256,
              "modified_source_sha256": PATCHED_SHA256,
              "binary_sha256": hashlib.sha256(binary.read_bytes()).hexdigest(),
              "flags": ["-std=gnu99", *flags]}
    (out / "build.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
