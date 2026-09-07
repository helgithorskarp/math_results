# Review: all 812 Snail dihedral-nine closures

## Verdict

**Accepted with high confidence at the exact stated scope.**  The target's
field reduction, complete case coverage, positive colour certificates, lower
obstructions, and numerical census all check.  No correction is required.

The accepted theorem is:

> For each ordered pair of distinct vertices of the frozen 29-point Snail
> seed, form the full order-nine rotational closure together with reflection
> in their axis.  Of the 812 labelled graphs, 157 have chromatic number three
> and 655 have chromatic number four.  They have 271--496 vertices and
> 738--1,494 unit edges.

This is an intermediate family exclusion, not a sub-509 five-chromatic graph.

Target Discovery reference:
`bafkreicb5nyjzrmpvafoxr3r3d45tydgbc4kkbwza6qhen626ve5xteboa`.

Target source commit:
`dd252d8f830c0a116a053edcfbda694609152d19`.

## Independent mathematical audit

Let

\[
 K=\mathbb Q(a,b,c,e),\qquad
 a^2=-3,\ b^2=-11,\ c^2=5,\ e^2=-3320+632ab,
\]

with physical conjugation negating \(a,b,e\) and fixing \(c\).

1. The square classes \(-3,-11,5\) are independent: every nonempty product
   has an odd valuation at one of 3, 11, or 5.  Hence
   \(K_0=\mathbb Q(a,b,c)\) is multiquadratic of degree eight.
2. If \(e\in K_0\), commutativity of physical conjugation with every
   automorphism of the abelian extension would make every conjugate of \(e\)
   purely imaginary.  But changing the sign of \(ab=-\sqrt{33}\) sends
   \(e^2\) to \(-3320+632\sqrt{33}>0\), since
   \(632^2\cdot33>3320^2\).  Thus \([K:\mathbb Q]=16\).
3. With \(r=e^{2\pi i/9}\) and \(\rho=r^3\in K\), every root of
   \(X^3-\rho\) is a primitive ninth root and has rational degree six.  No
   such root lies in a degree-16 field, so this cubic has no root in \(K\),
   and therefore is irreducible.
4. For nonzero \(x,y\in K\), the expansion of
   \(|x-r^t y|^2-1\), \(t=1,2\), has nonzero \(r\)- and \(r^2\)-coefficients.
   Linear independence of \(1,r,r^2\) excludes cross-copy unit edges.
   Likewise the three copies intersect only at zero.  Three copies of the
   smaller \(D_3\) graph can therefore be coloured independently after
   permuting colours to agree at the common centre, and their chromatic
   number equals that of one copy.
5. The centre contributes one point, the second axis point at most three,
   and the remaining 27 seed points at most six each.  Thus the smaller graph
   has at most 166 vertices and the full graph at most \(3(166)-2=496\).

These steps correctly distinguish the algebraic reduction from the finite
classification.

## Target replay

At the exact detached target commit, all manifest entries passed.  The
following solver-free commands succeeded:

```sh
python3 verify.py
python3 -O verify.py
python3 controls.py
python3 audit_geometry.py
```

Normal and optimized verification agreed on all 812 cases, 157/655
classification counts, 3,548,735 family same-colour tests, and certificate
SHA-256
`c217efc0649faf986475dac157e7f2ac4bb992e4f4ac88a108e3217808d20dc3`.
The controls rejected all 20 corruptions.  The geometry audit covered 141,288
formal positions and 8,738,622 distinct-point pairs.

## Reviewer-owned computation

`audit_review.py` imports no target implementation.  Its independent layers
are:

- **Different modular image.**  It proves 1,000,010,251 prime by trial
  division and checks the defining relations at
  \((a,b,c,e)=(863024046,726668820,504977047,548931751)\).  This modulus is
  different from both target moduli.  Every direct modular address agrees
  with the independently reduced exact address after scaling.  All 132 seed
  and 3,548,735 family same-colour pairs are nonunit in this image.
- **Fresh exact arithmetic.**  Products are reduced directly at the monomial
  level, including the two terms of \(e^2\); no target multiplication table or
  module is imported.  The checker tests all 256 basis products as a residue
  homomorphism and all 4,096 basis associativity triples.
- **Complete geometry census.**  Exact coincidence classes and unit edges are
  reconstructed for every case.  The 8,738,622 pair scan performs 295,485
  full exact norms after sound modular rejection.  The resulting complete
  census digest is
  `cafc136a70b10e3b4b97537cdd319eb573e16307a2396a6730ee032da98728b5`,
  identical to the target.
- **Different lower traversal.**  A bitset DSATUR checker traverses ties and
  colours in the opposite order from the target.  It independently rejects
  all 655 lower cores in 49,311 nodes (maximum 8,720), rather than the target
  traversal's 47,634 nodes (maximum 6,648).  Its correctness is compared with
  chromatic-polynomial inclusion--exclusion for every labelled simple graph
  through five vertices.

Both normal and optimized reviewer runs match `EXPECTED.json`.

## Primary-source provenance

On 2026-09-07 the primary
[Dúcz--Varga paper](https://arxiv.org/html/2606.28157v1) independently confirmed
that its graph \(G_{29}=G_{27}\cup\{p,q\}\) is nicknamed the Snail graph and
that the paper's geometric fractional chromatic number is the relevant source
invariant, not an ordinary chromatic-number premise here.

The live supplementary archive was 45,637,428 bytes with SHA-256
`ff6c9fc9df606ee15be9b4e3d14e7144e3d829fbd7fbeca3bc21bdd50e43667c`.
Its `snail_reproduction/verts_sym.npy` member was 2,146 bytes with SHA-256
`19766f3a5c31d544c5b15aa2f64cb2996684dc17b1818d9a5e5b20a90d8614a3`.
Running the target's closed-allowlist importer under pinned SymPy 1.14.0
reconstructed all 29 symbolic points and matched the frozen seed exactly.
The large archive and scratch environment are intentionally not published.

## Scope and trust boundaries

The audit accepts the 812 **labelled** seed-centre/seed-axis cases; it makes no
nonisomorphism claim.  It accepts neither arbitrary axes or centres nor other
rotation orders, combined closures, the source paper's blow-ups, or a global
four-colouring of \(K\).  Every subgraph of a reviewed closure is of course
four-colourable, but no five-chromatic unit-distance graph is produced.

Remaining trust boundaries are the unformalized elementary field/gluing
argument, the upstream coordinate table, CPython arbitrary-precision integer
arithmetic and exhaustive search, JSON/base64 parsing, and SHA-256.  Source
attribution was checked live, but the paper's unrelated geometric-fractional
theorem was not reviewed.  No SAT verdict, floating-point decision, omitted
expanded geometry, or researcher-supplied verdict is used for acceptance.
