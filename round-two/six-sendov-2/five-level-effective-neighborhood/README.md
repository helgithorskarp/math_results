# Effective five-level angular neighborhood

Actual author **six-sendov-2**, role **researcher**, 2026-10-02.
Complete author proof and finite exact certificates; unformalized and
independently unreviewed.

[PROOF.md](PROOF.md) proves two complementary five-level collars:

- \(u=((A-s)^3,(1-t)^2,A+3s,1+2t,-4A-3)\), \(W=12s^2+6t^2\);
- \(u=((A-s)^2,(A+s)^2,(1-t)^2,1+2t,-4A-3)\), \(W=4s^2+6t^2\).

For \(A\in[-43/50,-17/20]\), \(|s|,|t|\le1/200\), every collision included,
\[
C(u/\|u\|)\le F(A)-50W
\le c_3-800(A-\alpha)^2-50W
\le c_3-300\,\operatorname{dist}(u/\|u\|,\mathcal O_3)^2.
\]
The constant, maximizing root and orbit are inherited from 8753.

Together with the prior 9121 collar, these charts cover **every** balanced
unit profile with at most five levels, largest multiplicity at most three,
and orbit distance at most \(1/10000\). All these profiles satisfy the
displayed coefficient-300 distance bound. With the full fourfold theorem
9019/9055, **all** profiles with at most five levels in that explicit ball
satisfy \(C\le c_3\), equality only on the known orbit.
The coefficient-300 conclusion is not asserted by this last corollary
for every fourfold profile.

An earlier independent review 8806 already proves local full-sphere
stability with every coefficient below \(340.462200\ldots\), with an
existential radius. The new information is explicit domain coverage.
Global five-level bounds, six-to-eight levels, unrestricted \(C_*\),
effective full-sphere stability and actual degree-nine complex first power
remain open.

## Reproduce

CPython 3.11.2, standard library only; no CAS or campaign imports:

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
      NUMEXPR_NUM_THREADS=1 python3 -I -B \
      round-two/six-sendov-2/five-level-effective-neighborhood/verify.py

The complete 44-record fixture has canonical SHA256
**e1484d98311b742eda2154b1145d7b4faf16d4f5df0cd563d7581db8baffc58f**.
Expected summary: PASS; 13 full8 commutant controls; six whole collar
Bernstein reconstructions; 30,702 entries, 30,282 positive and 420
structural zeros. Every fixture field is compared, including complete
coefficient hashes. The fixture may be independently regenerated:

    python3 -I -B round-two/six-sendov-2/five-level-effective-neighborhood/verify.py \
      --emit /tmp/independent-five-level-fixture.json

The integer kernels clear moment denominators using roots scaled by eight.
Whole adjugate/determinant checks and separate literal full-matrix controls
protect this normalization. Changing to the initially proposed \(1/100\)
split width actually fails the raw-50 claim at a certified rational profile.
That example is not a counterexample to \(C\le c_3\).
Runtime is about 17 seconds in the author's fixed one-thread scope.
The written spectral-support and coordinate-coverage arguments remain
ordinary proof bridges; exact replay is not an independent review.
