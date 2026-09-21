# Theorem and proof

Let `k>=3`, `N=2k+1`, and `P=2^k`.  Label `C_N` cyclically by
`0,1,...,2k`.

## Theorem

For every three-element set `S` contained in `{1,...,2k}`, the configuration

```text
c_S = (5P/2-7)e_0 + sum_(s in S) e_s
```

is stackable.

In particular, at mass `5P/2-4`, the stable two-singleton obstruction cannot
be replaced by an obstruction having three singleton light piles.

## Transfer formulas

For a nonempty path branch, listed from its leaf toward its target, the exact
signed transfer uses

```text
g(z) = 2z-3       if z<=1,
       z/2        if z>=2 is even,
       (z-3)/2    if z>=3 is odd.
```

The split-path theorem says that a cycle configuration is stackable exactly
when some cut and endpoint split gives a path target with positive root
score.

A branch containing one unit at target-distance `x` sends

```text
3-2^(x+1).
```

A branch containing two units at distances `y<z` sends

```text
3-2^(z+1)+2^y,
```

and a branch containing three units at distances `x<y<z` sends

```text
3-2^(z+1)+2^y+2^x.
```

Each identity follows by induction across the intervening zero runs.  They
can also be read directly from `g(1)=-1` and
`g^r(-1)=3-2^(r+2)`.

## The antipodal split

Cut vertex `k`, put its pile on the endpoint reached clockwise from zero, and
target the heavy vertex.  The two branches correspond to clockwise and
counterclockwise distances `1,...,k`.

If all three singleton piles lie on one branch, the three-unit formula makes
the root score positive.  Otherwise reflect if needed and write the two
distances on one branch as `y<z` and the distance on the other as `x`.
The heavy root score is

```text
Q(x,y,z) = 5P/2-1 - 2^(x+1) - 2^(z+1) + 2^y.       (1)
```

If `x,z<=k-1`, then `Q>=P/2+1`.  If `z=k` and `x<=k-2`,
or if `x=k` and `z<=k-2`, then `Q>=1`.  Hence (1) can fail only for

```text
(x,z)=(k,k), (k,k-1), (k-1,k).
```

In cyclic coordinates, and up to reflection `i -> N-i`, these are exactly

```text
F1(a)={a,k-1,k+1},  1<=a<=k-2,
F2(a)={a,k,k+1},    1<=a<=k-1,
F3(a)={a,k,k+2},    1<=a<=k-1.                    (2)
```

This proves both the completeness and the linear size of the exceptional
list; no finite search enters the reduction.

## Uniform witnesses for the exceptional families

Split a cut pile into `L` pebbles at the left endpoint followed clockwise by
the remaining cycle vertices.  Targets in the table are path coordinates,
so a cut at zero produces coordinates `0,1,...,2k,2k+1`.  Every unlisted cut
is zero.  Direct iteration of `g` gives the displayed positive score.

| family and condition | cut | `L` | target | score |
|---|---:|---:|---:|---:|
| `F1`, `a=2` | `k-1` | `0` | `2` | `1` |
| `F1`, `a` odd, `k` even | `0` | `P-2^a` | `k-2` | `1` |
| `F1`, `a` odd, `k` odd | `0` | `P/2-2^a` | `k-1` | `1` |
| `F1`, even `a>=4` | `0` | `P/2-2^a` | `k` | `1` |
| `F2`, `a` odd, `k` even | `0` | `P-2^a` | `0` | `3` |
| `F2`, `a` odd, `k` odd | `0` | `P/2-2^a` | `k-2` | `1` |
| `F2`, `a` even | `0` | `3P/4-2^a` | `k-3` | `1` |
| `F3`, `(k,a)=(3,1)` | `0` | `6` | `3` | `1` |
| `F3`, `a=2` | `k` | `0` | `1` | `1` |
| `F3`, `a` odd, even `k` | `0` | `P/2-2^a` | `k-2` | `1` |
| `F3`, `a` odd, odd `k>=5` | `0` | `3P/4-2^a` | `k-3` | `1` |
| `F3`, even `a>=4` | `0` | `P-2^a` | `0` | `3` |

All endpoint allocations are nonnegative and at most `5P/2-7`; the stated
ranges make this immediate.  For example, every row reduces to repeated
applications of

```text
g(2q)=q,   g(2q+1)=q-1,   g(1)=-1,   g(0)=-3
```

once the branch has become occupied.  Induction on the zero-run lengths
gives the score column.  The two nonzero-cut rows are the boundary cases in
which that cancellation begins at a singleton endpoint.  Reflection swaps
the two split endpoints, sends a target coordinate `t` to `N-t`, and
preserves the score, so the same table covers the three reflected families.

Together with the antipodal reduction, the table proves the theorem.

## Scope and trust boundary

The universal argument is the displayed branch algebra and case split.  The
checker independently reconstructs all path scores from the definition and
audits a large finite range, but finite testing is not used to infer the
all-`k` statement.  The result depends on the previously proved split-path
characterization and signed tree-transfer criterion.
