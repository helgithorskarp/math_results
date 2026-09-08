# Four colours for rational combs away from denominator seven

**Full-support theorem.** For every positive integer `D` not divisible by
seven, the Euclidean distance-`D` graph on

```text
R x Z
```

is four-colourable. Equivalently, the unit-distance graph on all complete
parallel lines

```text
X_(1/D) = R x (1/D)Z
```

is four-colourable. It follows that `R x (p/q)Z` is four-colourable whenever
`p/q` is rational in lowest terms and `7` does not divide `q`, because this
support is a subset of `R x (1/q)Z`.

This is an explicit colouring of an infinite geometric support, with no bound
on the number of occupied lines, horizontal extent, or graph order. It closes
the first rational-comb denominator left by the earlier congruence filters:
in particular `R x (1/24)Z` is four-colourable. Combining the new theorem
with the earlier denominator conditions shows that a five-chromatic graph on
a rational comb can exist only if its reduced spacing denominator is divisible
by **168**. This is a necessary condition, not an existence result.

No five-chromatic graph on at most 508 vertices is produced. The 509-vertex
graph in [Parts's paper](https://arxiv.org/abs/2010.12665) remains the campaign
benchmark; [Haugland's current manuscript](https://arxiv.org/html/2608.04542v4)
also identifies 509 as the record. Both primary sources were checked on
8 September 2026. No historical priority is claimed for the residue method
or theorem.

## The mod-seven colouring

Scale `X_(1/D)` by `D`, so the forbidden distance becomes `D` and all heights
are integers. Let `S` be the positive squarefree integers and put

```text
M = sum_(s in S) Z sqrt(s).
```

Distinct squarefree radicals are linearly independent over the rationals, so
every member of `M` has a unique finite integral expansion. Choose one
representative `t` of every additive coset of `M` in `R`. This uses ordinary
choice; no measurable or Borel colouring is asserted. Write a point in the
coset as

```text
(x,y) = (t + sum_s n_s sqrt(s), y),  n_s,y in Z.
```

In the field `F_7`, define a weight `a_s` from the residue of `s`. If `s` is a
nonzero square, choose `lambda_s` with `lambda_s^2=s` and put
`a_s=3 lambda_s`. Put `a_s=0` when `s` is zero or a nonsquare. Either square
root gives a valid colouring. Define the residue

```text
R(x,y) = y + sum_s a_s n_s  (mod 7).
```

For the fixed forbidden distance, let `r=2D` in `F_7`. Since `D` is nonzero,
so is `r`. Partition the seven residues into four colours:

```text
{0,r}, {2r,3r}, {4r,5r}, {6r}.
```

Two residues of the same colour differ by `0`, `r`, or `-r`. We show that no
distance-`D` edge has one of those three residue changes.

## The residue lemma

For an edge, let `k` be the absolute vertical displacement. If `k=D`, the
horizontal displacement is zero and the residue changes by `+D` or `-D`.
Neither belongs to `{0,+2D,-2D}` in `F_7`.

Otherwise factor the positive integer

```text
D^2-k^2 = s c^2
```

with `s` squarefree and `c>0`. The horizontal displacement is
`+c sqrt(s)` or `-c sqrt(s)`. Its possible residue changes, up to a common
sign, are

```text
delta = k + a_s c  or  k - a_s c.                 (1)
```

Suppose first that `s` is zero or a nonsquare modulo seven, so `a_s=0`.
If `k=0`, the norm equation would give `s c^2=D^2`; if `k=+2D` or `-2D`, it
would give `s c^2=-3D^2=4D^2`. In either case `c=0` is impossible because
`D` is nonzero, while `c!=0` would make `s` a nonzero square. Thus (1) avoids
`0,+2D,-2D`.

Now let `s=lambda^2` and set `h=lambda c`. The norm equation becomes

```text
k^2+h^2=D^2,       a_s c=3h.                       (2)
```

If `k plus-or-minus 3h=0`, then (2) would give `3h^2=D^2`; this is impossible
because `3` is a nonsquare modulo seven. If
`k plus-or-minus 3h=plus-or-minus 2D`, substituting for `k` in (2) gives

```text
3 z^2 plus-or-minus 2z + 3 = 0,  z=h/D.
```

Its discriminant is `4-36=-32=3 mod 7`, again a nonsquare. This proves the
lemma and hence the explicit four-colouring of the entire support.

## Target consequence and scope

The earlier
[quarter-localized height theorem](../hadwiger_nelson_quarter_rational_heights/README.md)
four-colours every rational comb whose reduced denominator is not divisible
by eight. The three-colour condition when the denominator is not divisible
by three follows from Theorem 2.3 of Axenovich, Choi, Lastrina, McKay, Smith
and Stanton, *On the Chromatic Number of Subsets of the Euclidean Plane*,
[Graphs and Combinatorics 30 (2014), 71--81](https://doi.org/10.1007/s00373-012-1249-9).
Together with the new condition `7|q`, any rational-comb candidate requiring
five colours must satisfy `168|q`. The earlier full-support theorem for line
spacing at least `1/3` further requires `p/q<1/3`.

The theorem concerns equally spaced complete parallel-line supports and all
their subgraphs. It does not colour arbitrary unequal line spacings, arbitrary
rational heights with unbounded denominators, irrational height patterns, or
denominators divisible by seven. Divisibility by 168 is only a survivor
condition. The exact chromatic number of `R x (1/24)Z` remains between three
and four; the unit triangle used by the checker supplies the lower bound.

## Reproducible certificate

The compact certificate contains all 336 solutions of
`k^2+s c^2=D^2` in `F_7` for nonzero `D`, together with both residue changes,
and an exact factor table for the concrete `D=24` boundary. The producer
checks the residue lemma and quotient colouring while writing it. The
independent verifier uses a different squarefree-factor routine, rebuilds all
finite-field rows in another loop order, checks all **3,108** induced colour
comparisons, and verifies the 96 physical direction signs and an exact unit
triangle for `D=24`. Eight malformed certificates are rejected.

From the repository root, CPython 3.11 or later and its standard library
suffice:

```sh
python3 -B hadwiger_nelson_mod7_rational_combs/build.py --out /tmp/hn-mod7
python3 -B hadwiger_nelson_mod7_rational_combs/verify.py \
  --certificate /tmp/hn-mod7/certificate.json --check-expected --controls
python3 -O hadwiger_nelson_mod7_rational_combs/verify.py \
  --check-expected --controls
sha256sum -c hadwiger_nelson_mod7_rational_combs/SHA256SUMS
```

The certificate is 5,562 bytes with SHA-256

```text
1e65e47fda706472477ed77d6aa84b983fe354c4feb00404038d453fed143397
```

The computation has no native solver calls, floating-point predicates,
external graph input, omitted proof trace, or large artifact. The uniform
quantifier rests on the written coset and residue proof rather than finite
sampling. Operational trust is CPython exact integer arithmetic, JSON/file
handling, and faithful source execution. The proof is unformalized, and the
two implementations are author cross-checks rather than independent review.

This completes and retires the rational-comb construction source at the new
mod-seven boundary. Denominators divisible by 168 and other line arrangements
remain outside the theorem; no larger patch or denominator ladder is started.
