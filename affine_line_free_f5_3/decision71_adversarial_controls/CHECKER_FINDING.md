# Signed negative dependency shift on geometric wrong-input controls

The explicit SAT controls expose undefined behaviour in pinned stock
DRAT-trim when a genuine UNSAT trace is checked against a formula with one
additional clause removed. This is a checker finding, not a demonstrated
false acceptance or a mathematical defect in the 71-point reduction.

## Concrete reproducer and mechanism

Take case 1634 with original line clause 532 omitted. Its formula is UNSAT
and its fresh trace verifies. Delete clause 546 as well: the explicit
71-point fixture satisfies the entire formula, so the same trace is invalid.
An ASan/UBSan build reports:

```text
drat-trim.c:145:48: runtime error: left shift of negative value -1485
```

The stack passes through `addDependency`, `checkRAT` and `redundancyCheck`.
In the pinned source, line 605 calls `addDependency(S, -id, 1)`, while line
145 evaluates `(dep << 1) + forced`. The observed negative operand reaches
the signed shift in proof-dependency processing. This is distinct from
the negative metadata read in the optional warning printer.

The valid CNF SHA256 is
`5c19c0a229ef97fad23b6cb47a0cb0aa867157d26e49c672dd01bd513b22b687`;
the SAT CNF SHA256 is
`2c753d6db15089e024936b164615121839c563848121737da2e7063f4c3db093`.
The recorded 165,798-byte trace has SHA256
`883a0e21d6a766fec711ed9c59f0396a37853293adeca83bffa6c0bed0ec4b56`.
Raw traces are regenerated from source, not included in Git.

## Scope of the instrumented checks

Ordinary stock DRAT-trim accepts all eight single-omission proofs and normally
rejects all eight checks against the corresponding SAT double-omission input.
With ASan/UBSan and default warnings, four valid inputs verify cleanly; four
stop at the known raw-buffer warning-printer read. Seven wrong inputs also
stop there, while the remaining wrong input exposes the dependency shift.
These diagnostic exits are not counted as normal rejection controls.

A second bounded diagnostic pass isolates the warning printer using official
`-w`, **after** every proof byte passes researcher 1's published binary-framing
guard. All eight traces have canonical framing and maximum variable 125.
The [handoff](../decision71_independent_proofs/HANDOFF.md) explains why this
format excludes the malformed-command branch where `-w` changes parser
control flow. It does not make `-w` a printing-only change on arbitrary input.

In this qualified mode, all eight valid inputs verify without ASan/UBSan
findings. Five wrong inputs reject normally; three reach negative shifts:

| Case | Originally omitted clause | Negative operand |
|---:|---:|---:|
| 1634 | 532 | -1485 |
| 9786 | 22 | -1359 |
| 17600 | 553 | -6129 |

The warning-printer call sites and the dependency shift are separate. This
experiment does not test or alter the reviewer's proposed diagnostic patch.
It supplies concrete negative controls for qualifying a checker's scope.

## Reproduce the findings

First run [the ordinary replay](README.md). Then:

```sh
gcc -std=gnu99 -O1 -g -fsanitize=address,undefined \
  -fno-omit-frame-pointer -no-pie "$R5_CONTROL_TMP/drat-trim.c" \
  -o "$R5_CONTROL_TMP/drat-trim-sanitized"
"$R5_CONTROL_TMP/venv/bin/python" -O sanitizer_probe.py \
  --corpus "$R5_CONTROL_TMP/proofs" --out "$R5_CONTROL_TMP/sanitizer-default" \
  --checker "$R5_CONTROL_TMP/drat-trim-sanitized" \
  --checker-source "$R5_CONTROL_TMP/drat-trim.c"
"$R5_CONTROL_TMP/venv/bin/python" -O sanitizer_probe.py \
  --corpus "$R5_CONTROL_TMP/proofs" --out "$R5_CONTROL_TMP/sanitizer-framed" \
  --checker "$R5_CONTROL_TMP/drat-trim-sanitized" \
  --checker-source "$R5_CONTROL_TMP/drat-trim.c" --warnings-off
```

The driver checks sanitizer runtime symbols, input/proof identities and the
pinned source. It sets `ASAN_OPTIONS=detect_leaks=0:halt_on_error=1` and
`UBSAN_OPTIONS=halt_on_error=1:print_stacktrace=1`, recording every outcome.
It reports findings rather than relabeling diagnostic exits as successful
rejections. The optional framing guard source is pinned to SHA256
`8ce3d45465a1b21ea4f028b27b9a9fb86d9bf0139730d6a26aa06c4b5f22cf08`.
The guard establishes syntax only; native derivation checks remain separate.

The initial sanitizer attempt with default leak detection stopped on 101,572
bytes in six unreleased exit-time allocations. That failed check is preserved
in the validation record. Subsequent probes explicitly disable leak detection;
no leak-free execution claim is made. Address and undefined-behaviour
instrumentation remain enabled and halt on their findings.

These are fresh modified-input traces, not an audit of the untouched global
author corpus. No result here implies false acceptance of a production proof.
No shift patch is supplied. Full independent acceptance remains a separate gate.
