"""Read-only deterministic checker, including under python -O."""
import json
import signal
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from core import build, digest, same_typed

signal.alarm(45)
record = build()
fixture = Path(sys.argv[1]) if len(sys.argv) == 2 else Path(__file__).with_name('expected.json')
same_typed(record, json.loads(fixture.read_text()))
print(json.dumps({'status': 'PASS', 'record_sha256': digest(record),
                  'cyclic_rows': len(record['symbolic']['cyclic_rows']),
                  'literal_weight_controls': len(record['physical_weight_controls']),
                  'energy_thresholds': [record['original30']['H'], record['refined32']['H']]}))
