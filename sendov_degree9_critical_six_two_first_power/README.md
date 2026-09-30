# Degree-nine first power with critical multiplicities 6+2

Actual author **six-sendov-1**, role **researcher**, 2026-09-30.
Complete ordinary author proof with exact finite evidence; unformalized;
independent review pending.

For every complex degree-nine polynomial with all zeros in the closed
unit disk and critical multiset \(\{\zeta_U^6,\zeta_V^2\}\), allowing
coincidence, the reciprocal-distance sum at every marked zero is at
least eight, strictly greater at interior marked zeros. A critical
marked zero contributes infinity. Boundary equality in this class is
precisely \(p(z)=C(z^9-a^9)\), \(|a|=1,C\ne0\).

The new polar mechanism retains the exact even-multiplicity modulus,
saturates weighted radii and real projections, and gives an explicit
mean gap \(\xi-a\ge(1-a)/[288a(1+a)]\) in the stated polar budget.
The asymmetric weighted-mean origin minimum uses both signed imbalance
sectors and a third Newton bound. Read [PROOF.md](PROOF.md) for the
quantified lemmas, polynomial deduction, cell coverage and equality.
[LITERATURE.md](LITERATURE.md) credits primary and campaign antecedents.
The unrestricted degree-nine first-power endpoint remains unresolved here.

## Reproduction

Use CPython 3.10+ and its standard library only; recorded interpreter3.11.2.
From the repository root run these commands sequentially, one process
and every numerical-library thread one:

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I sendov_degree9_critical_six_two_first_power/verify.py
    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -O sendov_degree9_critical_six_two_first_power/verify.py

Both commands must print one JSON record with:

- result **PASS**;
- **3735269** certified sign coefficients, 13 complete origin-envelope
  cells and two corner cells;
- **675** positive polar coefficients, minimum **8/9**, with full inverse,
  two integral expansions, 27 rational controls and a retained boundary
  variance identity;
- **288** signed Gaussian controls, including degenerate faces, and
  eight direct Fraction/shared-denominator evaluation comparisons;
- all origin-cell entries compared between affine substitution and
  de Casteljau, with complete inverse identities on three global origin
  tensors and all 15 origin cell tensors;
- a complete Fraction/integer affine-transform reference comparison;
- an exact nonreal disk-root polynomial control and both communication
  identities checked;
- **8** altered manifests rejected under either optimization mode.

[expected.json](expected.json) is required; ordinary verification
compares its entire compact record and never regenerates it implicitly.
All full coefficient tensors are regenerated in memory and discarded.
No proof corpus, external ledger, solver or floating proof input is used.

The canonical norm record SHA256 is

    409e882c9f7d13d6f1990fbc07aa32408473a49499c2ddd2456f9140219ff58a

The minus/plus margin record SHA256 values are

    7d8aea8fba947da63b73b7f814f5b70e265e48e08dcf263d0d906d11ad8321e9
    5c84c51a59a38a7c90a9f2facf1cf1a0810f117b820dabb3ac37aad420fc914a

The full polar tensor SHA256 is

    558f113c6b54b3f64b67090a6d97dc562e6cbb10c297256fe79dde312071018c

The isolated normal/optimized commands passed in
**293.879/291.405 seconds**,
with peak child RSS **408348/408872 KiB**.
The complete fixture build took 294.319 seconds with peak RSS407128KiB.
These measured runs use one CPU mathematical job and fit the 2GiB local
scope; elapsed costs vary with host load. No extra resources are required.

## Arithmetic and trust

[algebra.py](algebra.py) constructs the origin integral by binomial
heavy/light powers and by two paired quadratics followed by four heavy
linear factors. It reconstructs the full norm by cross-products and by
the complete real/imaginary square. [polar.py](polar.py) uses a full
quadratic product and an independent multinomial integral expansion.
[certificate.py](certificate.py) uses arbitrary-precision shared integers
and Fraction, retaining the slower affine reference. [verify.py](verify.py)
reconstructs all domains, certificates, exact controls and output hashes.
Proof guards use explicit exceptions and remain active under Python -O.
Self-contained author code reuse is attributed in the literature note;
matching algorithms do not provide an independent review.

The actual nonreal control polynomial has marked root3/4, critical points
\(i/20\) sixfold and \((1+i)/40\) twofold. Its exact nonleading coefficient
absolute-value sum is bounded by
\(1851462392517/2867200000000<1\). Rouché proves that all nine zeros lie
strictly in the disk; derivative and origin/polar identities are checked.
The nondegenerate original reciprocal-coordinate bridge is an abstract
functional control, not another asserted disk-root polynomial.

The finite arithmetic layer checks the displayed exact identities and
all sign entries. Written geometry, monotone polar saturation, Lipschitz
estimate, Bernstein interpretation and polynomial deduction remain
ordinary mathematical obligations outside a formal kernel.
