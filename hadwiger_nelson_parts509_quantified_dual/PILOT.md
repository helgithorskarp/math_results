# Full-family native pilot: unknown at the declared limit

One run of the unchanged full D_134 formula completed at its declared
600-second solver limit. DepQBF printed

```text
User-given limit reached, exiting.
s cnf -1 3852 74956
```

The process returned 0 after 600.207586 seconds of wall time. Its measured
child usage was 593.904234 user seconds, 6.207005 system seconds and
125992 KiB maximum RSS. The 615-second external watchdog did not fire,
and no memory-limit failure was reported under the 4 GiB address-space cap.

This is a computational observation and continuation decision. It does
not prove either truth value, exclude any additional selected graph,
establish a new lower bound, or produce a five-chromatic graph. No
percentage of the family can be inferred from the restart or cube counts.
No QRP trace was requested and no candidate assignment was returned.

## Exact input and configuration

The instance has 3852 variables, 74956 clauses and a forall 303 / exists 3549
prefix, with the semantics proved in PROOF.md. QDIMACS SHA-256:

```text
20f03643727208fafbe960bea868e443ea6fb8e0788c5846c8fb93c8ef660e20
```

The producing binary was Debian DepQBF 5.01-3 amd64, SHA-256:

```text
15b19e5ce9f3e9a8dfa9503c72c336d92b26f59b0c1ce6f5cf59a68093e89378
```

Flags were `--qdo -v --max-secs=600`. There was one solver process, using
default dependency management and default solving/preprocessing options.
The input, solver and mathematical encoding were unchanged from the
successful fixed-instance calibration. The added verbosity records native
search diagnostics; it supplies no independent certificate.

## Reproduce the bounded experiment

Generate the input from the repository root:

```sh
python3 hadwiger_nelson_parts509_quantified_dual/encode_dual.py \
  --case pool508 --out /tmp/parts-dual508.qdimacs
```

Then run the following on a POSIX system with Python 3.11, replacing the
executable path. Use a fresh log path.

```sh
python3 - /path/to/depqbf /tmp/parts-dual508.qdimacs /tmp/parts-dual-pilot.log <<'PY'
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

Runtime-limited outcomes and verbose-log bytes may vary with the hardware
and execution conditions. The producing log had 144914 bytes and SHA-256
`7a0cd16cbae20f7368658cc9c4bbabee24353f4760e3d8f52c75003d996778c4`.
Its size and hash are provenance, not a proof or a required solver output.
The log and generated instance remain local; the compact measured record
is in pilot_summary.json.

## Handoff

The fixed 509-vertex success did not establish adequate full-family scaling for
this pilot. Do not automatically rerun the same configuration with a
larger limit. Before another family solve, assess an exact restriction
to inclusion-minimal selected sets and its necessary degree conditions.
That reduction is a proposed next milestone; no revised formula or proof
phase was started here.

The existing formula and all previously verified strata and colouring
cuts remain intact. No learned search state or partial strategy from
this invocation can be resumed: only its exact input, command and output
are preserved. No solver or proof checker remains running.
