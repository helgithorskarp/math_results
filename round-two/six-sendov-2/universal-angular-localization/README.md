# Universal degree-nine real angular localization

Actual six-sendov-2 / researcher, 2026-10-05. Complete ordinary author
proof, unformalized and independently unreviewed. This is complementary
real angular stability in the degree-nine first-power Tang--Zhang family.

For EVERY balanced norm-one real8 profile, all original/compression
multiplicities and without odd-moment assumptions, D=mu4-1/8>0 gives:

- D<=1/676: C<=5560/243<23, via a separated central compression eigenvalue
  and the six remaining FULL grouped masses.
- D>=3/112: C<=23, via the complete compression traces and Cauchy--Schwarz.
- Outside strict4+4/no-zero: C<=412/19<23, combining the trace estimate
  with the credited sharp8851 moment theorem.

Thus any strict C>T counterexample with T>=23 must be strict4+4/no-zero,
1/676<D<3/112. The existing licensed four-/six-coefficient angular test
may add39/896<E<505/10816 andc>0 as necessary guards. Original-root
feasibility and all denominator guards remain required. There is NO
remaining-band infeasibility certificate, numerical whole-locus gap/collar,
sharp optimizer or complex first-power theorem here.

The former published small-D collar assumed mu3=mu5=0 and D<=1/729.
The new spectral proof removes those assumptions and its Taylor-loss
term, and enlarges the sufficient domain. The uniform limiting value16,
angular framework, classical min--max/Cauchy methods and sharp sign moment
lemma are credited. See [PROOF.md](PROOF.md), [LITERATURE.md](LITERATURE.md)
and [DEPENDENCIES.json](DEPENDENCIES.json).

Reproduce with Python3.11+ (validated on Python3.12.14):

```sh
python3 -B check.py > /tmp/records-normal.json
python3 -B -O check.py > /tmp/records-optimized.json
cmp /tmp/records-normal.json /tmp/records-optimized.json
```

The 52 finite exact checks reconstruct the full8x8 rational reference
compression and its whole projector resolution/ranks, complete scalar
cutoff/derivative identities, trace Gram slack, endpoint margins and E-band.
No parent executable or generated mathematical input is loaded. Generated
records stay in scratch or/tmp, not this source directory. Whole normal/O
records must agree; provenance is in [VALIDATION.json](VALIDATION.json).
There is no floating eigensolver, solver, exhaustive enumeration or formal
kernel. Min--max, full masses, inequality substitutions, classical trace
expansion and the imported8851 moment theorem remain ordinary proof.

The independent prior8753/8806 uniform-continuity result includesD=0 with
C_tilde=16 if desired; its review does not transfer to this contribution.
No new graph transaction is implied by source publication.
