"""Late-only native row observer; preserves every native arithmetic statement."""
from pathlib import Path
import sys

target, certificate, stage, output, rows = sys.argv[1:]
target = Path(target).resolve()
source = target.read_text()
anchor = "            digest.update(struct.pack('<38H', *row))\n"
if source.count(anchor) != 1:
    raise ValueError("native observer insertion site changed")
observed = source.replace(anchor, anchor +
    "            _audit_sink.write(struct.pack('<38H', *row))\n")
sys.argv = [str(target), "--certificate", certificate, "--stage", stage, "--output", output]
with Path(rows).open("wb") as sink:
    scope = {"__name__": "__main__", "__file__": str(target), "_audit_sink": sink}
    exec(compile(observed, str(target), "exec"), scope)
