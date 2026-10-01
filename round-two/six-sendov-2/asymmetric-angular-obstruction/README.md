# Asymmetric angular obstruction

Actual author **six-sendov-2**, role **researcher**, 2026-10-01.

[PROOF.md](PROOF.md) disproves the candidate universal extension of the
sharp symmetric triple-family bound
\(\eta\ge1-(208/9)(X-1/8)\). The restricted theorem in graph8672
did not assert that extension and remains intact.

Take three copies each of \(1+10\sqrt3,1-10\sqrt3\), plus \(7,-13\),
and divide by \(\sqrt{2024}\). The exact values are

\[
X=601/4232,\quad\eta=46573202983/78109350583,
\]
\[
\eta-1+(208/9)(X-1/8)=-823964384/78109350583<0.
\]

Thus any universal constant must be at least
\(3504016400/147654727\), about23.73115. This is a necessary lower
bound, not a sharp universal theorem. At \(R=-208/9\) the profile
strictly beats uniform4+4. The corresponding uniform-optimality radius
obstruction is the positive root of
\(5295721648a^2+8514352856a-584718545=0\), isolated by exact rational
signs to \(0.0659677<a<0.0659678\). The true transition is not located.

A second explicit witness has all eight slopes distinct and norm one
already after division by45. Both witnesses use only a quadratic real
field; their compression weights are certified without numerical roots.
These are angular counterexamples and do not refute first-power
Tang--Zhang or classify finite-energy disk minimizers.

Run with CPython3.11 or later and no packages, from this directory:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B verify.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O verify.py
```

Both should print

```json
{"checks":31,"damage_controls":4,"record_sha256":"58a036ae8abcdb2e16aea217e9dfb66a8e9713cf8f6302dd62143789c1adefb7","status":"exact asymmetric counterexample verified"}
```

The compact witness is checked in three ways: Newton sums of the
compression residue polynomial, the companion-matrix squared trace,
and an independent three-moment Gram inverse. The eight-distinct witness
is derived from its rational polynomial and checked by both trace routes.
Root moments, factorization, congruences, signs and the radius equation
are regenerated. Explicit fixture comparisons and all damage controls
remain active under `-O`. `--expected PATH` supports an independently
copied fixture; `--write-expected` is a maintainer generation option.

The finite spectral identification and radius interpretation are ordinary
written mathematics outside a formal kernel. Independent review is
pending. [LITERATURE.md](LITERATURE.md) records prior art and precise scope.
