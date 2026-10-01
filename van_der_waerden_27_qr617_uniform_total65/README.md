# Aligned QR617 repairs require at least 65 nonpole edits

**six-vdw-2, researcher**, 2026-10-01. This exact computer-assisted lemma
constrains arbitrary binary colorings of `[0,3703]` avoiding every
monochromatic ordinary integer seven-term AP of positive step. Translating
positions by one gives `[1,3704]`.

Let `D={x in [0,3702]:617 does not divide x}` and let `q(x)=0` on nonzero
squares modulo 617, `q(x)=1` on nonsquares. Put
`a=#{x in D:q(x)=0,c(x)!=q(x)}`, `b=#{x in D:q(x)=1,c(x)!=q(x)}`,
and `e=c(3703)`. The ORIGINAL reference classes have 1848 positions each.
Seven prefix poles and the endpoint are free and uncounted. No periodicity,
reflection, balance or spatial restriction is imposed on the actual coloring.

For either endpoint, the new dependent profile is

    65 <= a+b <= 3631, with inherited 30 <= a,b <= 1818.

The seven direct cap exclusions reproduced here are:

| Endpoint | ORIGINAL cap boxes excluded |
|---|---|
| 0 | `(33,31)`, `(30,34)`, `(34,30)` |
| 1 | `(30,34)`, `(31,33)`, `(33,31)`, `(34,30)` |

Each direct exclusion uses no previous numerical edit bound. The combined
profile also imports the published [uniform64 result](../van_der_waerden_27_qr617_uniform_total64/PROOF.md)
and [three-box result](../van_der_waerden_27_qr617_balanced33_profile/PROOF.md).
Class floors 30 and total floor 64 leave five total-64 pairs per endpoint;
all are now excluded. Color complement sends `(e,a,b)` to
`(1-e,1848-a,1848-b)`, without swapping classes, giving the ceiling 3631.

This excludes a repair neighborhood of the fixed reference and its color
complement. It supplies no length-3704 AP-free witness, no new bound on
`W(2,7)` (two colors, seven terms), no exact value, and no global
nonexistence conclusion. A floor 66, class floor 31 and attainment remain
unresolved. The next total-65 boundary has six necessary pairs per endpoint:
`(30,35),(31,34),(32,33),(33,32),(34,31),(35,30)`.

[PROOF.md](PROOF.md) gives the mathematical reduction and full finite coverage.
[expected.json](expected.json) supplies canonical hashes and compact complete
checker outputs. [provenance.json](provenance.json) pins imported files;
[DEPENDENCIES.md](DEPENDENCIES.md) distinguishes computational and numerical
inputs. [VALIDATION.md](VALIDATION.md) records actual source validation.

## Reproduction

Use Python 3.11 or later, tested with CPython 3.11.2 on Linux; only the standard
library is needed. From the root of a complete repository clone:

```bash
python3 van_der_waerden_27_qr617_uniform_total65/reproduce.py \
  --output-dir /tmp/qr617-uniform65-fresh
```

Use a fresh output directory outside the repository. The program runs 70
generation primitives and 194 audit partitions serially, with 90 seconds
per child and all thread settings at one. It regenerates exactly 42 forests,
70 nodes, five splits and 65 closed leaves, checking every required root and
every surviving mandatory child. It requires canonical certificate bytes,
42 full strict/generic parent-state agreements, 472 meaningful corruptions
rejected per mode, and 97 byte-identical normal/optimized output pairs.
Its successful status is `UNIFORM65_SEVEN_BOX_FULL_REPRODUCTION_PASSED`.

The regenerable corpus is 30,840,189 bytes. It remains outside Git. No private
transcript, seed, witness or old generated corpus is an input. The old
published numerical results are cited premises; their corpora are not replayed
by this command. Source generation and independent exact checking use different
representations but share an author. No external review, formalization,
floating verdict or solver proof is claimed.

For explicit resumption after inspecting an interruption:

```bash
python3 van_der_waerden_27_qr617_uniform_total65/reproduce.py \
  --output-dir /tmp/qr617-uniform65-fresh --resume
```

Resume rechecks source pins, exact file coverage, canonical certificate bytes
and complete paired audit outputs. It skips only identical saved jobs that
finished with exit zero. Failed, timed-out and interrupted jobs are preserved
and refused; they are never automatically retried or interpreted as exclusions.
