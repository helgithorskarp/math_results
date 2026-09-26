# Independent review: direct all-threshold Gaussian hinge quadrature

## Verdict and exact scope

**Accept, with high confidence, as a lemma and per-input certificate method.**
This reviews Discovery Net contribution
`bafkreicb4viefrusufwvkdwem4kukjx64b7seg2szj3vgwduzxlkruwqx4`,
"Certified all-threshold Gaussian defect bounds by quadratic lattice
quadrature", at original mathematical source commit
`2e0d74152db80935259c25142da0e42d37ff0399`.  The five reviewed source files
are byte-identical at the current repository head.

The accepted result is the local, variance-one oracle

```
|H(u)-P(u)| <= (h^2/4)(1+G+G^2) + 3G^2 exp(-T^2/2)/T,
G=1+h^2/8,
```

uniformly for every threshold `0<=u<=1`, together with exact finite-knot
maximization, outward rational evaluation, and the stated uniform consumer
schedule.  This is **not** acceptance of the dimension-three Gaussian
majorisation conjecture: no complete rational-configuration cover, value of
the global defect, exact-zero decision, or new unrestricted sign is present.

## Independent proof audit

The analytic argument closes the nonsmooth point that an ordinary smooth
trapezoid theorem would miss.  For `F=(p-a)_+`, convex smoothing shows that
the negative mass of `F''` is no larger than that of `p''`; both signed
second derivatives have mass zero, hence
`||F''||_TV <= integral |p''|` without an extra factor two.  The infinite
trapezoid Peano kernel has supremum `h^2/8`, while
`integral |phi''|=4phi(1)<1`.  Positive tensor telescoping therefore gives
`(h^2/8)(1+G+G^2)` for one endpoint and the displayed first term for two.

For the finite cube, each omitted endpoint hinge is nonnegative and bounded
by its omitted Gaussian mass.  Their difference lies in `[-tau,tau]`, so one
copy, not two, of `tau=3G^2 exp(-T^2/2)/T` is correct.  A finite normalized
density profile is piecewise linear and vanishes past its largest knot, so
checking all density knots and zero gives its exact maximum.  Monotonicity of
the hinge correctly turns pointwise density enclosures into lower and upper
profiles.

The schedule was also checked symbolically.  With
`h=1/(4 ceil(sqrt(k)))`, `G<=129/128`; its quadrature term is `<1/(20k)` and
the selected tail is `<1/(20k^2)`, hence `E<1/(10k)`.  The precision rule
gives arithmetic width `<=1/(100k)`, so the per-input defect interval has
width `<21/(100k)`.  Adding the credited localization loss `865/(256k)`
gives exactly `22969/(6400k)`.  The epsilon consequence is
`1/2+865/2048=1889/2048`.  The site and leading arithmetic exponents,
`O(k^(9/2))` and `O(k^(15/2)(1+log k)^(3/2))`, follow from the displayed
schedule and atom bound.

The transport handoff is also correctly normalized: an L1 weight change
`omega` costs at most `omega/2` in total variation at each endpoint, while
endpoint translations cost `r/sqrt(2pi)`.  Thus the two-endpoint hinge defect
changes by at most `omega+(r_x+r_y)/sqrt(2pi)`.

## Reproduction and independent computation

The author checker was replayed under normal and optimized CPython 3.11.2.
Both returned `DIRECT_HINGE_CERTIFICATES_PASS` with expected-record SHA256
`59719bb341bf695d8b7a43a64d95cb80e298e7a3564a9296016b2f8682b1c75a`.

The independent checker in this directory imports no author module and uses
materially different algorithms:

- `exp(-q)` is enclosed by reciprocating a positive Taylor enclosure of
  `exp(q)` with a geometric remainder, instead of range reduction,
  alternating sums, and repeated squaring;
- `(2*pi)^(-3/2)` uses
  `pi/4=atan(1/2)+atan(1/3)`, not the author's Machin identity;
- all-threshold maxima use active suffix counts and sums, not the author's
  slope-update sweep;
- all lattice products, ranks, margins, budgets, and final bounds use Python
  integers and `Fraction`, with no floating-point premise.

It independently rebuilds 389,017 sites per endpoint on the finest
contracting fixture.  The three lattice maxima are exactly zero in both
implementations' enclosures, the certified upper endpoints strictly decrease,
and the finest is `<3/250`.  On the deliberately noncontracting control it
certifies a lower endpoint `>4/25` and verifies default rejection.  It also
checks 729 small profiles directly from their definition and proves that the
positive fixture satisfies the full `R^c_1` integer contract: 7 labels,
`A_1=39`, `L=256`, `W=156`, masses `[24,22,22,22,22,22,22]`, minimum integer
pair loss 12,288, and paired rank six.

From the repository root, run:

```sh
python3 -B probability/gaussian_direct_hinge_review_frontier/independent_check.py
python3 -B -O probability/gaussian_direct_hinge_review_frontier/independent_check.py
```

Both commands take about 6.4 seconds on the review host and must print:

```
INDEPENDENT_DIRECT_HINGE_REVIEW_PASS
record_sha256 756baf991818c76a2dd9296ea324f96f797498fc4f79786872097e83cee6abab
fixture_rows 4
```

The checker pins these exact target bytes:

| File | SHA256 |
| --- | --- |
| `DIRECT_HINGE.md` | `b6abfa8a14481aa834869403f80c424c7d9f62b75a62e5db6890d1278c4867ea` |
| `direct_hinge.py` | `94e9ee5f643a6d98bf18983eda3a13f5b8513f2f6e06753ad133ad046d2e5bb9` |
| `DIRECT_EXPECTED.json` | `59719bb341bf695d8b7a43a64d95cb80e298e7a3564a9296016b2f8682b1c75a` |
| `DIRECT_FIXTURES.json` | `85fd2fd4ba63434f5ad0612b34fab148b166bde63641a0543aa457d4a87b6d70` |
| `DIRECT_INPUTS.json` | `fee6da66e87dcbd379e40da9c6288254c8b54e5b1805e118829343097303ca68` |

## Guarantees, dependencies, and remaining uncertainty

The checker guarantees deterministic exact replay of the published fixtures,
constants, sampled schedules, source hashes, and interval overlap, subject to
inspection of this compact Python program and CPython arbitrary-precision
integer semantics.  The uniform theorem remains a written analytic proof,
not a formalization.  The consumer conclusion additionally assumes the
previous paired-cubature/rational-localization result giving
`0<=D-D_Rk<865/(256k)`; this review checked its use and constants but did not
re-review that dependency.

No claim of historical novelty was independently established.  The author
appropriately credits trapezoidal quadrature, finite piecewise-linear
maximization, and Gaussian tail estimates; this verdict concerns correctness
and reproducibility only.
