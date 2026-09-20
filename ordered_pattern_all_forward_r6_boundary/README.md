# The all-forward ordered 6-pattern at the `6m+2` boundary

## Result

Let `m>=2`, and let `P^(m)` be the all-forward 6-partite ordered
6-matching on `[6m]`, with edges

```text
{j,m+j,2m+j,3m+j,4m+j,5m+j},          1 <= j <= m.
```

Then

```text
ex_<(6m+2,P^(m)) = C(6m+2,6)-28.                     (1)
```

The case `m=2` is already covered by the theorem of
Anastos--Jin--Kwan--Sudakov for two-edge matchings.  The new range in (1) is
every `m>=3`.  The proof below is parameter-uniform; it is not a rank-six or
matching-size census.

## Blockers and the 28-edge construction

Put `N=6m+2`.  Every canonical copy of `P^(m)` on `[N]` is determined by its
omitted pair.  A set `D` of 6-edges is a *blocker* if it meets every canonical
copy.  Taking complements makes (1) equivalent to

```text
minimum blocker size = 28.                            (2)
```

There is a blocker of size 28.  In one-based indexing, take all
`e={e_0<...<e_5}` satisfying

```text
e_(i+1)-e_i >= m for 0<=i<5,       e_5 <= N-(m-1).    (3)
```

The first edge of every canonical copy satisfies (3).  Subtracting
`(0,m-1,...,5(m-1))` bijects (3) with the 6-subsets of `[8]`, so there are
`C(8,6)=28` such edges.  It remains to prove that 27 edges never suffice.

## Four occurrence-graph types

Identify the omitted vertices cyclically with `Z_N`, and put `M=3m+1`, so
`N=2M`.  For an active 6-edge `e`, let `Omega(e)` be the graph whose vertices
are `Z_N` and whose edges are the omitted pairs whose canonical copy contains
`e`.

Every cyclic gap of `e` contains at least `m-1` vertices.  The two surplus
vertices therefore determine one of the following four graphs:

```text
Q_s = K_[s,s+m],                                      s in Z_N,
R_s = K_([s,s+m-1],[s+m+1,s+2m]),                    s in Z_N,
T_s = K_([s,s+m-1],[s+2m+1,s+3m]),                  s in Z_N,
S_s = K_([s,s+m-1],[s+M,s+M+m-1]),                  s in Z_M.  (4)
```

Conversely, deleting any pair in a graph in (4) leaves exactly `m-1`
retained vertices in each cyclic gap, so the list is complete.  A blocker is
exactly a selection of these occurrence graphs covering `K_N`.

Cyclic distances `1`, `m+1`, `2m+1`, and `M` are private to `Q`, `R`, `T`,
and `S`, respectively.  A graph of the corresponding type covers `m` pairs
in its private layer.  A non-diameter layer has `N` pairs, while the diameter
layer has `M`.  If `q,r,t,s` are the four selected type counts, then

```text
q>=7,                    r>=7,                    t>=7,       s>=4.  (5)
```

The remaining three units in (2) are forced by a four-band repair cascade.

## Paired repair intervals

List the selected `T`-starts cyclically as `a_0,...,a_(t-1)`.  Covering the
private distance `2m+1` says that their gaps satisfy

```text
h_i=a_(i+1)-a_i <= m,        d_i=m-h_i >=0,
sum_i d_i = (t-6)m-2.                                  (6)
```

For each start gap, direct membership in (4) gives two boundary pairs.  The
permissible `T`-starts for each pair form the empty open gap
`(a_i,a_(i+1))`.  The low boundary therefore forces an `R`-start into

```text
J_i=[a_(i+1),a_i+m] in Z_N,             |J_i|=d_i+1,   (7)
```

and the high boundary forces an `S`-start into

```text
K_i=[a_(i+1)-m,a_i] in Z_M,             |K_i|=d_i+1.   (8)
```

Here and below endpoints are included.  We use the following finite
boundary-signature lemma.

### Paired-repair lemma

For the interval systems (7)--(8):

1. If `t=7`, the seven `K_i` are pairwise disjoint.
2. If `t=8` and two `J_i` intersect, at least six points are required to hit
   all eight `K_i`.
3. If `t=8`, all `J_i` are disjoint, and four points hit all eight `K_i`, then
   every cyclic triple satisfies

   ```text
   d_i+d_(i+1)+d_(i+2) <= m-1.                         (9)
   ```

4. If `t=9` and seven points hit all nine `J_i`, at least five points are
   required to hit all nine `K_i`.

The lemma holds over the reals for every `m>=2`, so in particular it applies
to the integer start deficits above.

### Proof of the paired-repair lemma

The proof is a short endpoint calculation.  We include the complete
signature audit because it is the reusable part of the argument.

For `i<j`, put

```text
A_(i,j)=d_i+...+d_(j-1),       L_(i,j)=(j-i)m-A_(i,j).
```

Since `K_i=[a_i-d_i,a_i]` modulo `M`, the exact intersection criterion is

```text
K_i intersects K_j
iff there is q in {0,1,2} such that
    qM <= L_(i,j) < (q+1)M
and either
    L_(i,j)-qM <= d_j
or  (q+1)M-L_(i,j) <= d_i.                         (10)
```

No approximation enters (10): it merely chooses the lift of the second
backward interval to the line.  The analogous line calculation for (7)
shows the following.

- When `t=8`, two `J` intervals can intersect only at adjacent indices, and
  `J_i intersects J_(i+1)` exactly when `d_i+d_(i+1)>=m`.
- When `t=9`, saving two points in a transversal of the `J_i` has, up to
  dihedral symmetry, exactly four signatures: one point hits
  `J_0,J_1,J_2`, forcing `d_0+d_1+d_2>=2m`; or two points hit the disjoint
  adjacent pairs `{J_0,J_1}` and `{J_p,J_(p+1)}`, where `p=2,3,4`, forcing
  the two corresponding pair sums to be at least `m`.

Indeed, an intersection at index distance `u` requires a sum of `u+1`
consecutive deficits to be at least `um`.  The total deficit in (6) rules
out every omitted signature.  If an index-distance-two pair occurs in the
`t=9` case, the intervening interval contains the same intersection point,
so this is the three-interval signature.

It remains only to substitute these four `J` signatures into (10).  A hit
set partitions the `K` intervals into subfamilies with a common point.  The
only relevant block-size profiles and the deficit lower bound produced by
(10) are:

| case | assumed `K` hits | possible block sizes | consequence |
|---|---:|---|---|
| `t=7` | 6 | `2,1,1,1,1,1` | `sum d_i >= m-1` |
| `t=8`, some `J_i intersect J_(i+1)` | 5 | `2,2,2,1,1`; `3,2,1,1,1`; `4,1,1,1,1` | `sum d_i >= 2m-1` |
| `t=8`, disjoint `J`, a triple sum at least `m` | 4 | all partitions of 8 into 4 nonempty blocks | `sum d_i >= 2m-1` |
| `t=9`, each of the four `J` signatures above | 4 | `6,1,1,1`; `5,2,1,1`; `4,3,1,1`; `4,2,2,1`; `3,3,2,1`; `3,2,2,2` | `sum d_i >= 3m-1` |

For completeness, the substitution is performed as follows.  Within each
block require (10) for every pair, choose the lift `q` and one of its two
endpoint inequalities, and add the displayed `J` inequalities.  The two
orientations of a block and cyclic rotation are equivalent.  Summing the
remaining endpoint inequalities gives the last column.  This exhausts the
three integer partitions of `8-5`, all partitions of eight into four
blocks, and the six integer partitions of nine into four blocks; there is no
unstated geometric case because a common hit supplies all pairwise
conditions (10).

The totals in (6) are respectively `m-2`, `2m-2`, and `3m-2`, one below the
last column.  This proves assertions 1, 2, and 4.  In assertion 3, the same
substitution with the negation of (9) gives the third-row contradiction.
Equivalently, when four hits are possible the only tight intersection
signature pairs `K_i` with `K_(i+4)`; if some triple beginning at `i` had
sum at least `m`, applying (10) to the opposite pair beginning at `i-1`
would force that same triple to have sum at most `m-1`.  This proves (9) and
the lemma.

The accompanying `symbolic_audit.py` encodes exactly (6), (8), and the six
displayed `J` cases in quantifier-free linear real arithmetic.  It returns
six `unsat` results already for real `m>=2`.  This is a definition-level
corroboration of the endpoint audit; the written calculation above carries
the lemma.

## The tight eight-start propagation

Suppose `t=8`, `r=8`, and `s=4`.  Assertion 2 of the paired-repair lemma
shows that the `J_i` are pairwise disjoint.  Thus the eight selected
`R`-starts occur one per repair interval; write

```text
b_i=a_(i+1)+u_i,                 0<=u_i<=d_i.          (11)
```

Their cyclic gap deficits are

```text
e_i=d_(i+1)-u_(i+1)+u_i.                               (12)
```

They are nonnegative because the selected `R` family covers its private
layer.  Each `R`-gap now gives the analogous low boundary pair and forces a
`Q`-start into an interval of length `e_i+1`.  Assertion 3 and (11)--(12)
give

```text
e_i+e_(i+1)
 <= d_i+d_(i+1)+d_(i+2)
 <= m-1.                                                (13)
```

Hence adjacent `Q`-repair intervals are disjoint.  Nonadjacent ones could
intersect only if at least `2m` total `e`-deficit were available, whereas
`sum e_i=sum d_i=2m-2`.  All eight are therefore disjoint, and

```text
t=8, r=8, s=4  implies  q>=8.                          (14)
```

## Completion

If `t>=10`, (5) immediately gives `q+r+t+s>=28`.  The remaining cases are:

- `t=7`: assertion 1 gives `s>=7`, so the total is at least
  `7+7+7+7=28`.
- `t=8`: if `r=7`, some two `J_i` must share an `R`-start, so assertion 2
  gives `s>=6`, and the total is at least 28.  If `r>=9`, (5) again gives
  28.  The only remaining counts are `r=8,s=4`; (14) gives `q>=8`.  If
  instead `s>=5`, the total is already 28.
- `t=9`: if `r=7`, assertion 4 gives `s>=5`; if `r>=8`, the private bound
  `s>=4` suffices.  Both alternatives total at least 28.

Thus every blocker has at least 28 edges.  Construction (3) proves equality,
and therefore (1).

## Reproduction and trust boundary

Python 3.11 or later is required.  The definition-level checker uses only
the standard library:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_verify.py
sha256sum -c SHA256SUMS
```

It reconstructs occurrence graphs directly from all omitted pairs, compares
them with (4), checks the 28-edge blocker, and exhausts 121,698 paired-repair
deficit vectors for `2<=m<=5`.  These finite checks corroborate definitions
and boundary cases; they do not replace the parameter-uniform proof.

For the exact symbolic audit, install the pinned optional dependency and run

```bash
python3 -m pip install -r requirements-symbolic.txt
PYTHONDONTWRITEBYTECODE=1 python3 symbolic_audit.py
```

Z3 4.15.3 uses exact rational arithmetic and confirms that all six complete
linear-real signature formulas are unsatisfiable.  The audit does not export
an independently checkable Z3 proof trace, so its solver trust is explicitly
corroborative rather than the logical basis of (1).

## Scope and literature status

The primary source is Michael Anastos, Zhihan Jin, Matthew Kwan, and Benny
Sudakov, *Extremal, enumerative and probabilistic results on ordered
hypergraph matchings*, Forum of Mathematics, Sigma 13 (2025), e55
([DOI](https://doi.org/10.1017/fms.2024.144),
[open manuscript](https://arxiv.org/abs/2308.12268)).  Its Theorem 1.18(1)
gives construction (3), Conjecture 1.20 proposes the full formula, and
Theorem 1.17 covers matching size two.

A targeted primary-literature and web search through 2026-09-20 found no
later resolution of this exact all-forward `r=6`, `N=6m+2`, `m>=3` case.
That is a search-relative status statement, not a claim of historical
priority.  The theorem does not settle rank `r>=7`, larger excess, or other
orientations.
