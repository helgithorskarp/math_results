# Degree-restricted family pilot: unknown at 600 seconds

One bounded run of the changed, degree-restricted full-family formula
completed at the declared solver limit. DepQBF printed

```text
User-given limit reached, exiting.
s cnf -1 11843 92468
```

The process returned 0 after 600.244834 seconds of wall time.
Child usage was 596.247317 user seconds, 3.902860 system seconds and
117488 KiB maximum RSS. The 615-second external watchdog did not fire.
The address-space cap was 4 GiB, with one solver process.

This is a computational observation and a continuation decision. No
candidate assignment, quantified certificate, additional family closure,
graph-order bound or five-chromatic graph was obtained. No QRP trace
was requested. Search counters do not measure a fraction of the family
covered. The degree-restriction proof and preceding finite checks retain
their stated scope.

## Exact input and configuration

The input has 11843 variables and 92468 clauses, with 303 universal
selectors followed by 11540 existential variables. Its family semantics
are proved in [PROOF.md](PROOF.md). QDIMACS SHA-256:

```text
08e5a931743148cb50534d0d5e4d8cd5687137d229844148215a0a080c77c9d6
```

The producing binary was Debian DepQBF 5.01-3 amd64, SHA-256:

```text
15b19e5ce9f3e9a8dfa9503c72c336d92b26f59b0c1ce6f5cf59a68093e89378
```

Flags were `--qdo -v --max-secs=600`, with default dependency management
and solving/preprocessing options. The input and executable hashes and
the complete quantifier prefix were checked before launch. This was the
first full-family pilot of the degree-restricted formula; the earlier
unfiltered formula was not rerun.

## Reproduce the bounded experiment

From the repository root, generate the exact input:

```sh
python3 hadwiger_nelson_parts509_quantified_mindegree/encode_degree.py --out /tmp/parts-degree508.qdimacs
```

Then run on a POSIX system with Python 3.11, replacing the executable
path and using a fresh log path:

```sh
python3 - /path/to/depqbf /tmp/parts-degree508.qdimacs /tmp/parts-degree-pilot.log <<'PY'
import resource
import subprocess
import sys
import time

def limits():
    resource.setrlimit(resource.RLIMIT_AS, (4 * 1024**3, 4 * 1024**3))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))

start = time.monotonic()
with open(sys.argv[3], 'xb') as log:
    process = subprocess.Popen(
        [sys.argv[1], '--qdo', '-v', '--max-secs=600', sys.argv[2]],
        stdout=log, stderr=subprocess.STDOUT, preexec_fn=limits)
    try:
        code = process.wait(timeout=615)
    except subprocess.TimeoutExpired:
        process.terminate()
        try:
            code = process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            code = process.wait()
        print('external watchdog fired')
print('returncode', code, 'wall_seconds', time.monotonic() - start)
PY
```

Runtime-limited outcomes and log bytes depend on execution conditions.
The producing log has 79370 bytes and SHA-256
`5553c561aed9131ce219231a6449595c83298520a464ae45ef1ec51b06209277`.
These are provenance, not a proof or required output. Generated input,
raw log and live-job state remain local; [pilot_summary.json](pilot_summary.json)
contains the compact measured record.

## Comparison and handoff

The earlier unfiltered pilot also returned UNKNOWN at 600 seconds. Its
maximum child RSS was 125992 KiB, compared with 117488 KiB here. These
two bounded observations establish neither runtime superiority nor a
family-coverage fraction. The change did not yield a decided family
result within this pilot.

Decision: do not automatically rerun this configuration with a longer
limit. Both tested full-family DepQBF configurations and the earlier
isolated cut/shrink loop remain paused. Before another full-family run,
assess a materially different certificate mechanism, such as a
proof-producing decomposition using the existing exact interface and
colouring evidence. Require a bounded calibration that gives a reason
to proceed. This is a proposed assessment, not a new proof or solver
phase started in this pass.

The exact input, command and output are preserved. Internal learned
state or a partial strategy was not exported, so the native search
cannot be resumed from the log. No solver, proof checker or background
job remains active. The mathematical family and the record target
remain open.
