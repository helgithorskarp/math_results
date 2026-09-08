# Independent review of h3911 Galois-folding obstruction

**Verdict: ACCEPT.**  This review verifies Discovery Net contribution h3911,
`bafkreiaqoxbhkdq4eviltyzhdirkod6krprwk45you7yavhg3htxbeorm4`, at reviewed
source commit `ee45d9f1e6201314cb187c3d6e47369a9b47e8dc`.  The source manifest SHA-256 is
`17d1c67fa46c6b3b29a46a3b7faef7fa134c17320ac908506a95881950f0806f`.

The accepted theorem fixes the 2,131 archived complex coordinates `z_v` in
`K=Q(t,sqrt(5))`, where `t=exp(pi*i/21)`.  If one independently chooses
`sigma_v` in `Gal(K/Q)` for every vertex and the map
`v -> sigma_v(z_v)` preserves all 12,530 archived unit edges, then its image
contains at least 1,251 distinct points.  A common Euclidean isometry after the
map does not change the conclusion.

This is a complete exclusion of one precisely specified folding mechanism
through order 1,250, including 508.  It is not a lower bound for arbitrary
source subgraphs, arbitrary new plane supports, vertex-dependent translations,
or a coordinate-origin change before the pointwise rule.  Attainment at 1,251
is not claimed.

## Algebraic re-derivation

The cyclotomic field `Q(t)` has degree 12.  Since `Q(zeta_42)=Q(zeta_21)` is
ramified only at 3 and 7, it cannot contain `Q(sqrt(5))`, which is ramified at
5.  The compositum therefore has degree 24, with all actions

```
t -> t^a,  sqrt(5) -> e sqrt(5),
gcd(a,42)=1, e in {+1,-1}.
```

This group is abelian, and complex conjugation is the central action
`(a,e)=(41,+1)`.  Consequently every common field automorphism preserves the
identity `(z-y) conjugate(z-y)=1`, although it need not be a geometric isometry
on arbitrary complex points.

This proves the normalization step.  If the anchor image is
`tau(z_1069)`, applying `tau^(-1)` to every image preserves every unit edge,
every coincidence, and the image cardinality.  Each resulting vertex image is
still a conjugate of its own source point, and the anchor is fixed.  The
published computation also checks that the anchor orbit has all 24 actions.

The modular specialization uses the localized integral coordinate ring at

```
p = 1000000009,
t_bar = 41285184,
sqrt(5)_bar = 383008016.
```

The prime, the exact order 42 of `t_bar`, `Phi_42(t_bar)=0`, the square-root
identity, and all required nonzero denominators are checked.  Evaluation is a
ring homomorphism from this localization, not from the characteristic-zero
field itself.

For a point `z`, take the vector of its 24 conjugate evaluations.  Physical
equality implies equality of these vectors.  A true unit edge implies all 24
modular norm identities, because the coordinate indexed by complex conjugation
supplies the conjugate factor.  Neither converse is used: modular collisions
and spurious modular unit pairs enlarge the relaxation and can only weaken the
lower bound.

Thus any physical folding induces a solution of the finite edge CSP, using no
more modular sites than physical points.  After anchor normalization, arc
consistency removes a value only when it has no compatible neighbor value on
some declared edge.  Induction over revisions proves that no value occurring
in a solution is removed.  The identity assignment survives as a positive
control.

At the fixed point, the certificate names 1,251 vertices with nonempty,
pairwise-disjoint domains.  Any CSP solution must choose 1,251 distinct modular
sites on those vertices.  Unequal modular vectors imply unequal physical
points, so every physical folding has at least 1,251 images.

## Reproduction and independent implementation

The reviewed standard-library verifier passed in ordinary and
assertion-disabled CPython 3.11.2.  It independently reconstructs Cartesian
coordinates for all 24 action lifts, checks all 12,530 source edges per action,
builds 6,049 sites and 355 domain orbits, and reaches the fixed point after nine
synchronous changing sweeps.  The final histogram is 1,075 singleton domains
and 1,056 domains of size six; its hash is
`2f4db6e0a7ba543f04ffd1df3ed2695c245703d35e86beff9763ac1da26fad10`.
All 19,208 small-domain propagation controls and seven malformed-certificate
controls passed.

The separate `python-flint==0.8.0` audit also passed in both Python modes.  It
works in the characteristic-zero quotient `Q[t]/Phi_42(t)` and the formal
quadratic extension by `sqrt(5)`, reconstructing point counts 740, 1,066, and
2,131.  It checks all 84 directions and 12,530 declared edges exactly.  Its
24-action reduction agrees entry-by-entry with the Cartesian modular stream,
whose hash is
`a44ff4236832ca6b4eb14a39c27cdc9b4eb2858bb01c8a780c30cb81e839ced8`.

The reviewer-authored `independent_ac3.py` imports no reviewed code.  It uses
the direct complex formulas rather than Cartesian coordinates, deterministic
Miller--Rabin rather than trial division, literal action-by-action modular norm
checks, and an asynchronous AC-3 queue rather than synchronous sweeps.  Both
ordinary and assertion-disabled runs obtain:

- 24 actions and 300,720 source-edge/action checks;
- 2,016 unit-direction/action checks;
- 6,049 sites and 355 distinct initial domains;
- 2,718 queue revisions removing 29,983 values after the anchor pin; and
- the identical final-domain hash and 1,251-domain witness.

The selected witness contains all 1,075 singleton domains and 176 six-element
domains.  They are pairwise disjoint and their union contains 2,131 modular
sites.  This directly checks the certificate rather than trusting the reported
cardinality.

## Reproduction

Install the exact computer-algebra dependency in an environment outside the
repository, then from the repository root run:

```sh
python3 -m pip install -r hadwiger_nelson_haugland_galois_folding_review1/requirements.txt
python3 -B hadwiger_nelson_haugland_galois_folding_review1/reproduce.py
```

The exact expected receipt is [EXPECTED.json](EXPECTED.json).

## Trust boundary and target status

The fixed archived graph input is pinned by SHA-256
`201196679760fc329fff548346b843a821646ce5ffc326a91cc24598effc299d`.
Identification of its 231 paths with [Haugland's Appendix A](https://arxiv.org/html/2608.04542v4)
remains an imported transcription boundary.  The source's chromatic lower bound is neither assumed
nor reproved; the obstruction only needs the declared edges to be exact unit
edges.  Completeness of the archived unit-edge list is also unnecessary,
because preserving a larger edge set implies preserving this checked subset.

The remaining trust boundary includes the elementary cyclotomic ramification
argument, the unformalized normalization and relaxation proof, CPython and
FLINT arithmetic, implementation correctness, the operating system, and
hardware.  Agreement between the Cartesian/synchronous, exact-polynomial, and
direct-complex/asynchronous implementations is cross-validation, not a formal
proof or independent historical-priority claim.

No new graph, five-chromatic certificate, source subgraph, or record
improvement is established.  The Parts 509-vertex benchmark remains unchanged;
this review accepts only the target-scale exclusion of the specified Galois
folding family.
