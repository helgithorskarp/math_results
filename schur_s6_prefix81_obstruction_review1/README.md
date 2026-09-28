# Independent review of the Fredricksen--Sweet 81-entry prefix obstruction

This directory audits the certificate in the sibling
[`schur_s6_prefix81_obstruction`](../schur_s6_prefix81_obstruction)
directory. The exact claim is conditional: a classical six-colouring of
`[1,537]` cannot agree with the specified Fredricksen--Sweet 536-colouring
on **all** of `1,...,81`. Every later colour, including the colour of 537,
is unrestricted. The statement also holds after any global relabelling of
the six colours. It is a fixed-prefix exclusion, not a bound on unrestricted
`S(6)`.

## Verdict and proof scope

**Accepted with high confidence as a finite deduction certificate.**
Initially, the first 81 colour domains are fixed to the baseline digits;
the remaining 456 domains contain all six colours. A certificate row
`[target,colour,x,y]` means that `target` cannot have `colour`: in the
Schur triple `(x,y,x+y)`, every *other distinct vertex* has already been
forced to that colour. Induction shows every hypothetical colouring that
extends the prefix remains within the current domains. The checked 351st
deletion empties the domain of 537. There are 23 doubling steps with `x=y`;
the distinct-vertex rule handles them correctly.

`audit.py` independently replays all 351 rows using six-bit integer domain
masks. It imports no author checker or generator. It checks the baseline
by direct colour-class sumsets, verifies every triple and singleton premise,
rejects an absent-colour deletion or an early contradiction, and requires
the final empty domain to be exactly 537. The original `check.py` reports
the same values. Its four positive and negative tests pass, and
`generate.py` regenerates the committed 7,021-byte certificate
byte-for-byte. The generator is not a premise of the proof.

The baseline bytes equal those in the separately reviewed 51-edit project.
That earlier review compared all 536 entries to the 269 printed source
entries and reflection rule in [Fredricksen and Sweet (2000)](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32),
including the exceptional pair `179,358`. The finite obstruction depends
only on the explicitly supplied first 81 digits, not historical attribution.

## Reproduce

CPython 3.11 or later, standard library only. From this directory:

```sh
python3 -B audit.py
python3 -B -O audit.py
```

Both commands print:

```text
PASS independent_prefix81 baseline=536 certificate_steps=351 doubling_steps=23 contradiction_at=537
baseline_sha256=2fdf85110de782426dd5deccfa7244f182441fda9870db64ba8e4eea7e3d600d
proof_sha256=0fddc52d3193648237e26bf0353331f70a86bb7c5e141c3f800b18aaeee84324
```

The independent checker uses explicit exception checks, which remain active
under `python3 -O`. The author checker also verifies all 71,824 unordered
Schur triples on the baseline. Its exact reproduction commands and expected
JSON fields are in the sibling directory.

## Novelty and limits

Targeted searches found no prior publication of this exact 81-entry
extension obstruction. The [July 2026 shifted S-templates preprint](https://arxiv.org/abs/2607.15034)
still uses `S(6)>=536`. The local certificate appears ready to report in
its stated scope; this is a search-relative novelty assessment, not a
historical priority claim. Its direct consequence is that any hypothetical
537-colouring must change at least one of the first 81 baseline entries.
Together with the separately certified 51-edit distance theorem, it must
also change at least 51 baseline entries overall.

The generator's lack of contradiction when only the first 80 entries are
fixed does **not** establish that such a colouring exists, or that 81 is
the shortest nonextendible prefix. No global upper or lower bound on
classical `S(6)` follows.

## Strengthening and improvement opportunities

1. Seek a shorter fixed prefix with a finite branching or SAT proof whose
   deductions can be checked independently. An unbranched propagation
   threshold at 81 does not settle the true minimum.
2. Apply the same checked-domain method to other verified 536-colourings
   and justified scalar-equivalent baselines. The equivalence maps and
   transformed colourings must themselves be checked before transferring
   an obstruction.
3. Combine the prefix restriction with the 51-edit exclusion in a complete
   certified search of the remaining 537-colourings. A global search
   certificate and an audited encoding of doubling triples are the missing
   bridge to an upper bound for `S(6)`.

## Trust boundary

The theorem rests on the explicit 81-digit prefix, the 351-row certificate,
the sound domain-deletion rule, and exact Python integer operations. The
independent audit is a separate code path, not a proof-assistant
formalization. It proves neither the shortest nonextendible prefix nor
the existence or nonexistence of an unrestricted 537-colouring.
