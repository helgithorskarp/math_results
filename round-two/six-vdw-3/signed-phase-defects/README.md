# One-exception period-618 exclusion and signed phase-defect transport

**six-vdw-3, researcher.** A checked exact refutation excludes every
period-618 seven-AP-free coloring whose ternary phase skeleton has exactly
one exceptional column: all 618 such skeletons and all 2^102 normalized
orientations in each. The model has 5253 variables and 35394 clauses.

The same work proves an elementary transport bound for any valid nearest-phase
word: its separable comparison has at most
`16*(C(d_+,2)+C(d_-,2))+5*d_+*d_-` bad pair-parity ladders. A single phase
exception therefore cannot create an orientation outside the valid separable
family. See [PROOF.md](PROOF.md), [expected.json](expected.json), and
[VALIDATION.md](VALIDATION.md).

No unrestricted length-3704 coloring, new W(2,7) bound, or full period-618
exclusion is established. The constant ternary skeleton remains open. The
written proof is unformalized and independent peer review is pending.

Reproduce from a repository checkout, using CPython 3.11.2 and GCC 12.2 as
tested, standard libraries plus the pinned untrusted discovery solver:

```sh
python3 -m venv /tmp/vdw-phase-env
/tmp/vdw-phase-env/bin/pip install --no-cache-dir -r round-two/six-vdw-3/signed-phase-defects/requirements.txt
/tmp/vdw-phase-env/bin/python round-two/six-vdw-3/signed-phase-defects/reproduce.py --workdir /tmp/vdw-phase-proof
```

Success ends with
`VERIFIED_ONE_EXCEPTION_EXCLUSION_AND_SIGNED_DEFECT_REDUCTION` in the JSON
summary. All computations are sequential and one-thread, with 45-second
child timeouts and bounded solver/converter budgets. The source audit and
proof replay run in normal and optimized Python. SAT/UNKNOWN/timeout or failed
conversion/replay cannot substitute for the checked refutation.

The wrapper fetches three checksum-pinned sources into the work directory:
the previously published cut generator by six-vdw-3, the separate positive-RUP
checker by six-vdw-1, and the untrusted DRAT converter. All URLs, commits and
hashes are in expected.json. Existing cached source is accepted only if its
hash matches. Generated models, binaries and 22 MB of proof corpora remain
in the work directory; none is published here.

For a solver-free local/incidence/model audit, run `generate.py` with the
published sibling `parity-ladders/generate.py` present, then run `check.py` on
its output. These checks establish the model equivalence and transport lemma;
the one-exception exclusion additionally needs the exact refutation replay.
