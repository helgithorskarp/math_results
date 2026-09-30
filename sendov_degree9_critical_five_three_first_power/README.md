# Degree-nine first power with critical multiplicities 5+3

Actual author **six-sendov-1**, role **researcher**, 2026-09-30.
Complete ordinary author proof with exact finite evidence; unformalized;
independent review pending.

For every complex degree-nine polynomial with all zeros in the closed
unit disk and critical multiset \(\{\zeta_U^5,\zeta_V^3\}\), allowing
coincidence, the first reciprocal-distance sum at every marked zero is at
least eight. It is strictly greater than eight at every interior marked
zero. Boundary equality is precisely \(p(z)=C(z^9-a^9)\), \(|a|=1\).
A critical marked zero contributes infinity.

The new mechanism centers the reciprocal phase at its weighted complex
mean. A rational estimate for the signed term, with both imbalance signs,
proves the full asymmetric origin minimum. A 5+3 polar-mean certificate
then supplies the polynomial contradiction. The theorem covers this whole
critical multiplicity class; the unrestricted degree-nine first-power
conjecture remains open here.

Read [PROOF.md](PROOF.md) for all quantified statements, coordinate and
polynomial deductions, equality cases and trust boundaries. Read
[LITERATURE.md](LITERATURE.md) for primary sources, source attribution and
the comparison with the earlier critical4+4 theorem and complementary
original-root energy and displacement work.

## Reproduction

Use CPython 3.10 or later and only its standard library. The recorded
interpreter is CPython 3.11.2. From the repository root, run these commands
**sequentially**, with one process and all numerical-library threads one:

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I sendov_degree9_critical_five_three_first_power/verify.py
    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -O sendov_degree9_critical_five_three_first_power/verify.py

Both commands must print a single JSON record with:

- result **PASS**;
- **898201** certified sign coefficients, eight envelope cells and two
  corner cells;
- **288** signed Gaussian rational controls, including degenerate faces,
  and eight Fraction/reference evaluation comparisons;
- every origin cell entry compared between affine substitution and
  de Casteljau subdivision;
- all three global origin tensors, every origin cell tensor and the polar
  scalar tensor inverted to their complete power polynomials;
- the exact nonreal polynomial control and both communication identities
  checked;
- **8** deliberately corrupted manifests rejected.

The deterministic norm record SHA256 is

    77ba8f83c6fad9b04ea659d8efc2df964b0c4697de2e536582df5482c215e950

The two deterministic margin record SHA256 values, in minus/plus order, are

    a920bf8e329d82b92cbc0d5542ca0cb4bf7cc9285971e07fdec500d5b1db2493
    9cad3434c474e1a34d3e8173a45cac7ec8d17e99720ebe1f18eab829ea964632

[expected.json](expected.json) contains all compact summaries, exact
minima, equality supports, hashes and the complete 23-entry scalar
certificate. The full origin coefficient tensors are regenerated in
memory and are not stored or imported. The source build took about
135 seconds and 128 MiB peak resident memory in the constrained single
CPU environment. Isolated normal/optimized runs took 136.953/138.453
seconds, with peak child RSS 131484/133212 KiB. Costs vary by host.

## What the computation checks

[algebra.py](algebra.py) derives the integral coefficients by binomial
powers and by three paired quadratics followed by two heavy linear
factors. It derives the norm both by coefficient cross-products and by
squaring its full real and imaginary parts. [certificate.py](certificate.py)
uses arbitrary-precision rational and shared-denominator integer
arithmetic. [verify.py](verify.py) reconstructs all coefficients,
partitions, basis identities, exact controls and the compact manifest.
Proof guards remain active under Python optimization.

The actual nonreal control polynomial has marked root \(3/4\), critical
points \(i/20\) fivefold and \((1+i)/40\) threefold. Its nonleading
coefficient absolute-value sum is at most
\(3650539170933/5734400000000<1\), proving by Rouché that all nine roots
are strictly inside the unit disk. The original reciprocal-coordinate
control is an abstract functional control and is not asserted to be a
second disk-root polynomial.

Author algorithm cross-checks do not provide an independent review or a
formal kernel. The written geometry, rational bound, Bernstein positivity
and strictness, convex moment reduction and polynomial interpretation
remain explicit mathematical obligations in the proof. No solver,
floating-point proof input, imported large certificate or external data
is needed.
