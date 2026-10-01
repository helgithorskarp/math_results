# Two necessary constraints for order7 templates over F617

Author: **six-vdw-2**, researcher, 2026-10-01. This is a computer-assisted lemma
about two colors and seven-term arithmetic progressions, using the notation
W(2,7). It produces no coloring of [1,3704] and no global upper or lower bound.

Let H=<3^88> have order7 in F617*, and let c:F617*->{0,1} be H-invariant.
Assume every seven-term field arithmetic progression with nonzero difference
and all seven terms nonzero is nonmonochromatic. Two constraints are proved:

1. Every eight-term **geometric** color progression of ratio in
   57H union 57^-1 H is nonmonochromatic.
2. Set f(x)=c(x) XOR c(-x), and write f_i=f(3^i), i modulo44. If its weight
   K is8 or36, its eight minority positions have minimum cyclic distance<=2.
   Equivalently, a minority pair occurs at exponents i and i+1 or i+2.
   Their eight intervening majority gaps g_j sum36, and sum g_j^2>=176.

The first constraint adds14 ratios distinct from the previously established
color-seven ratios 3H union 3^-1 H. The second restricts the geometry at the
endpoints of the previously established nonconstant phase band8..36; **it
does not remove either endpoint**. Both phase backgrounds and all44 color
orientation variables are retained, including phases with period11 or22.

[PROOF.md](PROOF.md) gives the reductions and scope. [EXPECTED.csv](EXPECTED.csv)
lists the95 canonical CNF and positive-RUP proof hashes. The seven root57
cases use the published color-seven constraint; the84 packing and four
closest-pair cases additionally use the published phase-eight constraint.
Those dependencies and their exact source hashes are in
[SOURCE_PINS.json](SOURCE_PINS.json). Large CNF/DRAT/LRAT files are regenerated
locally and are deliberately omitted.

## Reproduction

Run from the repository root, with an external scratch directory. Tested:
Python3.11.2, python-sat1.8.dev24, CaDiCaL195. All computation is serial.

```sh
python3 -m venv /tmp/h7-constraints-env
/tmp/h7-constraints-env/bin/python -m pip install python-sat==1.8.dev24 six==1.17.0
mkdir -p /tmp/h7-constraints-tools
curl -fL https://raw.githubusercontent.com/marijnheule/drat-trim/2e3b2dc0ecf938addbd779d42877b6ed69d9a985/drat-trim.c -o /tmp/h7-constraints-tools/drat-trim.c
cc -O2 /tmp/h7-constraints-tools/drat-trim.c -o /tmp/h7-constraints-tools/drat-trim
/tmp/h7-constraints-env/bin/python round-two/six-vdw-2/order7-cluster-and-root57/reproduce.py --work /tmp/h7-constraints-run --converter /tmp/h7-constraints-tools/drat-trim
/tmp/h7-constraints-env/bin/python round-two/six-vdw-2/order7-cluster-and-root57/guards.py --work /tmp/h7-constraints-run --output /tmp/h7-constraints-corruptions
```

Expected final status: `EXACT_H7_TWO_NECESSARY_CONSTRAINTS`,95 refutations,
293281 RUP additions and3627680 propagation hints. Every definition and
certificate is checked in normal Python and under `-O`; no correctness guard
depends on `assert`. Each native proposal requests50000 conflicts and has a
30-second external deadline; conversion has25 seconds internally and30
externally, and each strict proof replay30. Separate definition stages have55
seconds. No timeout, UNKNOWN, SAT candidate, incomplete conversion or partial
case cover proves an exclusion. Stop at the first incomplete stage; do not
raise caps. `--resume` exact-replays completed positive cases and refuses an
identical recorded UNKNOWN/timeout retry. An interrupted unchecked native
stage requires diagnosis before resumption.

For an already-held candidate proof corpus, `--certificate-cache DIR` reads
`DIR/{root57,packed,close}/STEM.{cnf,lrat}`. It checks canonical input hashes,
regenerates every model, audits the mathematical definitions, and strict-replays
every proof again; cached status flags are never used as proofs.

Trust boundaries: ordinary exact integer arithmetic and the published source
of the positive-only RUP checker; no SAT/DRAT-trim verdict is itself trusted.
This is same-author algorithmic separation, not independent peer review or
proof-assistant formalization. [VALIDATION.md](VALIDATION.md) records checks
and bounded failures.
