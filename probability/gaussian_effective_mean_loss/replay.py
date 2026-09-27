#!/usr/bin/env python3
"""Replay the frozen original packet from its source commit, without checkout."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import subprocess
import sys
import tempfile

SOURCE_COMMIT = "f171c499bc0ed272d1b6fd5f78d57968d1578b62"
PACKET = "probability/gaussian_effective_mean_loss"
FILES = [".gitignore", "EXPECTED.json", "HANDOFF.md", "INPUTS.json", "PROOF.md",
         "README.md", "SHA256SUMS", "SOURCES.md", "certificate.py", "verify.py"]
EXPECTED_SHA = "1fed1586ae3915c7410387cbd68551c26dd9479d17b922092f02563b37a79e31"
REPO = Path(__file__).resolve().parents[2]


def need(ok, message):
    if not ok:
        raise ValueError(message)


def historical(path):
    p = PurePosixPath(path)
    need(not p.is_absolute() and ".." not in p.parts, "invalid repository path")
    return subprocess.check_output(
        ["git", "-C", str(REPO), "show", SOURCE_COMMIT+":"+str(p)])


def main():
    need(sys.argv[1:] in ([], ["--optimized"]), "usage: replay.py [--optimized]")
    blobs = {PACKET+"/"+name: historical(PACKET+"/"+name) for name in FILES}
    expected = blobs[PACKET+"/EXPECTED.json"]
    need(hashlib.sha256(expected).hexdigest() == EXPECTED_SHA, "expected record")
    for line in blobs[PACKET+"/SHA256SUMS"].decode().splitlines():
        digest, name = line.split(maxsplit=1)
        need(name in FILES and name != "SHA256SUMS", "manifest file")
        need(hashlib.sha256(blobs[PACKET+"/"+name]).hexdigest() == digest,
             "original packet hash: "+name)
    pins = json.loads(blobs[PACKET+"/INPUTS.json"])["files"]
    for pin in pins:
        data = historical(pin["path"])
        need(hashlib.sha256(data).hexdigest() == pin["sha256"],
             "original dependency hash: "+pin["path"])
        blobs[pin["path"]] = data
    with tempfile.TemporaryDirectory(prefix="gaussian-mean-loss-replay-") as temp:
        root = Path(temp)
        for path, data in blobs.items():
            destination = root/path
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
        command = [sys.executable]
        if sys.argv[1:]:
            command.append("-O")
        command.append(str(root/PACKET/"verify.py"))
        subprocess.run(command, cwd=root, check=True)
    print("HISTORICAL_REPLAY_PASS")
    print("source_commit="+SOURCE_COMMIT)
    print("packet_files=10 dependency_pins="+str(len(pins)))


if __name__ == "__main__":
    main()
