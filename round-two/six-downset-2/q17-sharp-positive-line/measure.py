"""Unix child-resource receipt; no mathematical input or result comparison."""
import json
import resource
import runpy
import sys
import time
from pathlib import Path

target, script, *arguments = sys.argv[1:]
sys.argv = [script, *arguments]
sys.path.insert(0, str(Path(script).resolve().parent))
started = time.monotonic()
try:
    runpy.run_path(script, run_name='__main__')
finally:
    usage = resource.getrusage(resource.RUSAGE_SELF)
    Path(target).write_text(json.dumps({'seconds': time.monotonic() - started,
        'peak_rss_kib': usage.ru_maxrss, 'user_seconds': usage.ru_utime,
        'system_seconds': usage.ru_stime, 'python': sys.version,
        'optimize': sys.flags.optimize}) + '\n')
