# Review of h3981: no plane unit-edge map of the 301-vertex repair
LRAT proof and the abstract graph's non-four-colourability are deliberately
not imported into this verdict because the negative geometric theorem does
not require them.  Historical novelty is not assessed.
## Verdict and exact scope

**ACCEPT.** The fixed 301-vertex, 1,452-edge graph with SHA-256
`7be0344d1811866429181436b2f85653fc801272a7a3efddad6125539e50cbbb`
admits no map into the Euclidean plane that takes every graph edge to
distance one.  The conclusion includes noninjective maps: arbitrary
nonadjacent vertices may be identified.

This closes the plane-realization question only for the fixed graph in the
positive H516 repair package.  It is not a sub-509 five-chromatic
unit-distance graph, a record improvement, or an exclusion of later graphs
obtained by deleting or replacing constraints.  The graph's asserted
five-chromatic and vertex-critical properties motivate h3981 but are not
premises of its negative geometric result; this review does not reproduce
the separate LRAT evidence required for its chromatic lower bound.

Reviewed contribution: Discovery Net h3981,
`bafkreifffqjqtfl2xcan2ywesda56x47mv74bgxl7pown6jdunk4x6zotm`.
Reviewed source commit:
`9b5f0b989aebbec953d20846d58150e1a0449405`.

## Independent derivation

For an odd wheel with hub `h` and cyclic rim `v_0,...,v_(k-1)`, every rim
point of a plane unit-edge map lies on the unit circle centered at `h`.
Each unit rim edge changes its polar angle by `+pi/3` or `-pi/3`.  Closure
would make the sum of `k` signs divisible by six, impossible when `k` is
odd.  This argument permits further identifications.  Consequently, if
identifying a nonadjacent pair produces an odd wheel in the quotient, the
two original vertices cannot have the same image.  An edge itself gives the
same inequality directly.

Consider a unit four-cycle `(a,b,c,d)` whose two diagonal pairs are known
not to coincide.  The distinct points `b,d` are the two intersections of
the unit circles centered at the distinct points `a,c`.  Reflection across
the midpoint of `a,c` interchanges them, so

```text
a - b + c - d = 0.
```

The certificate supplies 279 such cycles.  Its 558 distinct diagonal
inequalities consist of 276 graph edges and 282 quotient odd wheels (266
with rim length 3, ten with length 5, and six with length 7).  Thus every
plane unit-edge map satisfies the 279 vector parallelogram equations.

After anchoring one vertex, let `A` be the resulting 280-by-301 integer
matrix.  The supplied 301-by-55 rational matrix `P` obeys `A P = 0`, and
the rows indexed by the 55 declared free vertices form the identity.  Hence
the rational nullity is at least 55 and `rank(A)<=246`.  Independent sparse
elimination gives rank 246 modulo each of the fresh primes 1,000,003 and
1,000,033.  A nonzero minor modulo a prime is a nonzero integer minor, so
`rank_Q(A)>=246`.  Therefore `P` is a full basis of the real kernel as well.

For each coordinate separately, every possible map satisfying the forced
linear equations is consequently `P s` or `P t`.  The reviewer expands the
claimed integer-weighted sum over 18 actual graph edges as a full 55-by-55
rational Gram matrix and obtains the zero matrix.  Therefore

```text
sum_(uv) lambda_uv * ||p(u)-p(v)||^2 = 0
```

for every map satisfying the forced parallelogram relations.  If all graph
edges had unit length, the left side would instead equal the exact integer
sum of the weights, 708.  This contradiction proves the stated result.
The weights need not be positive because the certificate is an exact
polynomial identity, not an inequality.

## Independent finite audit

The reviewer checker imports neither `verify.py` nor `produce.py` from the
reviewed package.  Starting from the pinned graph and certificate bytes, it:

- canonically enumerates all 2,062 four-cycles in the graph and checks that
  the 279 certified cycles are a distinct subset;
- reconstructs quotient edge sets literally for all 282 odd-wheel witnesses
  and checks 1,780 wheel edges;
- verifies all rational entries are canonical, all 280 equations annihilate
  `P`, and the free rows form the identity;
- obtains rank 246 at two primes different from the source's modulus and from
  the earlier author-side auxiliary check's modulus; and
- expands all 3,025 entries of the rational Gram matrix, finding zero
  nonzero entries, while checking 18 distinct source edges and weight sum
  708.

The exact graph and certificate hashes are checked before parsing.  The
source verifier is separately replayed with its seven malformed controls
and positive-colouring audit.  Normal and `python3 -O` runs of both the
source and reviewer checkers must match their exact expected JSON receipts.

Reproduction command:

```sh
python3 -B hadwiger_nelson_301_repair_plane_obstruction_review2/reproduce.py \
  . /scratch/research-team-v2/tmp/reviewer-1/review-h3981
```

Expected status: `REPRODUCED_ACCEPT_REVIEW_H3981`.

## Trust boundary

The accepted obstruction uses only the fixed graph and certificate bytes,
the elementary odd-wheel and equal-circle arguments above, exact integer and
rational arithmetic, modular rank implications, and the independently
checked quadratic identity.  It uses no floating-point geometry, external
solver, CAS, coordinate field assumption, graph-isomorphism package, or
external theorem catalog.

Residual trust comprises the written derivation, the source and independent
checker implementations, SHA-256 and Git archive semantics, CPython, the
operating system, and hardware.  Certificate discovery and the producer's
FLINT computation are outside the verification path.  The upstream strict
LRAT proof and the abstract graph's non-four-colourability are deliberately
not imported into this verdict because the negative geometric theorem does
not require them.  Historical novelty is not assessed.
