# Strong Seymour vertices through order 14

## Result

A vertex `x` of a tournament is **strong Seymour** if there is a directed
matching from all of `N+(x)` into the exact second out-neighborhood `N++(x)`.
This directory certifies the following finite result.

> **Theorem.** Every tournament on at most 14 vertices has a strong Seymour
> vertex. Consequently, if `m` is the minimum order of a tournament without a
> strong Seymour vertex, then
>
> `15 <= m <= 36`.

The upper bound is the transitive-cluster version of the 36-vertex construction
of Bai, Li, and Park. The lower bound through order 14 is new to the sources
searched as of September 2026 and is computer-assisted.

Related independent work in Austin Gibbons's
[SSNC repository](https://github.com/AustinBGibbons/ssnc) constructs regular
tournaments of every odd order at least 15 with exactly nine strong vertices
and studies a stronger quantitative conjecture for regular tournaments. It
does not supply a tournament with no strong vertex or the finite lower bound
proved here.

There is also an elementary optimization result about the published family.

> **Blow-up lemma.** The six strict cluster-size inequalities in Remark 3.1 of
> Bai--Li--Park have no positive-integer solution of total size below 36. At
> total size 36 their unique solution is `(7,3,11,3,9,3)`.

Thus their displayed construction is already uniquely order-minimal within
that six-cluster inequality family. A smaller counterexample must change more
than the cluster sizes.

Primary source: Y. Bai, B. Li, and B. Park, *Towards a strengthening of the
second neighborhood conjecture*, [arXiv:2607.18047](https://arxiv.org/abs/2607.18047),
especially Theorem 1.5, Lemma 2.5, and Remark 3.1.

## Mathematical reduction

Bai--Li--Park prove that an oriented graph of minimum out-degree at most five
has a strong Seymour vertex. Hence a counterexample tournament has minimum
out-degree at least six.

For a vertex `x`, put `A=N+(x)` and `B=N-(x)`. For `S` contained in `A`, let

`Gamma_x(S) = {z in B : y -> z for some y in S}`.

These are exactly the possible heads in `N++(x)` of directed matching edges
whose tails lie in `S`. Hall's theorem says that `x` is not strong if and only
if some `S` satisfies `|Gamma_x(S)| < |S|`. If `S` is inclusion-minimal, then

- `|Gamma_x(S)| = |S|-1`;
- every member of `Gamma_x(S)` is reached by at least two members of `S`; and
- Lemma 2.5 of Bai--Li--Park gives minimum out-degree at least one in the
  subtournament on `S`, in particular `|S| >= 3`.

For order at most 12, averaging gives a vertex of out-degree at most five, so
the published theorem applies directly.

At order 13, minimum out-degree six forces a regular tournament. The `n13`
formula fixes the labels of one vertex's two neighborhoods and asks every
vertex to have a deficient Hall set. It is unsatisfiable.

At order 14, choose an ordinary Seymour vertex `x`, which exists in every
tournament. Since `|N++(x)| <= 13-d+(x)` and `|N++(x)| >= d+(x)`, while the
minimum degree is at least six, necessarily `d+(x)=6`. Its minimal deficient
Hall set has size at most five: if it were all six vertices of `N+(x)`, its
neighbor set would be `N++(x)`, contradicting that `x` is an ordinary Seymour
vertex. The only root cases are therefore `|S|=3,4,5`. Relabeling inside
`N+(x)` and `N-(x)` makes `S` and `Gamma_x(S)` initial segments; these are the
three `n14-s*` formulas. All are unsatisfiable.

The order-14 formulas introduce one Boolean orientation variable per unordered
pair. They enforce minimum out-degree six. A Boolean `high_x` is equivalent to
`d+(x)>=7`; such a vertex is automatically not strong because it has at most
six in-neighbors. Each degree-six vertex instead receives an exact minimal
Hall witness using variables for membership in `S`, membership in
`Gamma_x(S)`, and their defining conjunctions. Sequential-counter CNF
encodings impose all cardinalities. The root symmetry conditions described
above are added separately for sizes 3, 4, and 5. This gives both directions:
a satisfying assignment decodes to a counterexample, and every counterexample
can be labeled and supplied with minimal witnesses to satisfy one formula.

## Blow-up lemma proof

Write `(a,b,c,d,e,f)=(n0,n1,n2,n3,n4,n5)` and `q=e+f`. Replacing each strict
integer inequality in Remark 3.1 by a weak inequality with `+1` gives the
following consequences.

First, the first and third inequalities imply

`a+2b >= c+2`.

The sixth gives `c >= a+b+1`, so `b>=3`. The second and third give
`a+b+d >= c+2`; with the sixth this yields `d>=3`. Combining the third and
fifth gives `c>=e+2`, while the second gives `e+f>=c+1`, so `f>=3`.
The fourth now gives `a>=b+f+1>=7`, the sixth gives
`c>=a+b+1>=11`, and the second gives `q>=c+1>=12`. Therefore

`a+b+c+d+q >= 7+3+11+3+12 = 36`.

Equality forces `b=d=f=3`, `a=7`, `c=11`, `q=12`, and hence `e=9`.
Direct substitution verifies the unique tuple. `direct_check.py` independently
enumerates every positive composition through total 36 and obtains the same
answer.

## Reproduction

The generator requires Python 3.11 and `python-sat==1.8.dev25`. Create any
environment below `/scratch`, then run:

```bash
python3 direct_check.py
python3 generate_cnf.py n13 /scratch/strong-seymour-n13.cnf
python3 generate_cnf.py n14-s3 /scratch/strong-seymour-n14-s3.cnf
python3 generate_cnf.py n14-s4 /scratch/strong-seymour-n14-s4.cnf
python3 generate_cnf.py n14-s5 /scratch/strong-seymour-n14-s5.cnf
```

Solve each instance with a proof-producing SAT solver. The audited run used
CaDiCaL 3.0.1 (source commit
`c60730422e758ef1cebe7aeddf2dda31c996bf04`):

```bash
cadical /scratch/strong-seymour-n13.cnf /scratch/strong-seymour-n13.drat
cadical /scratch/strong-seymour-n14-s3.cnf /scratch/strong-seymour-n14-s3.drat
cadical /scratch/strong-seymour-n14-s4.cnf /scratch/strong-seymour-n14-s4.drat
cadical /scratch/strong-seymour-n14-s5.cnf /scratch/strong-seymour-n14-s5.drat
```

CaDiCaL uses exit status 20 for UNSAT. Verify each trace independently, for
example:

```bash
drat-trim /scratch/strong-seymour-n14-s5.cnf /scratch/strong-seymour-n14-s5.drat
```

The audited generators and proof runs produced:

| case | variables | clauses | CNF SHA-256 | DRAT SHA-256 | result |
|---|---:|---:|---|---|---|
| `n13` | 4,901 | 12,960 | `4c15597e710d2ad60bf2c020e6501ff65a59f5d6f154194c37054bdb19b9e259` | `a3f5fae9b08a1d9c3014396eac92eccdc9302077db816aad457ff6e38c4802bd` | VERIFIED UNSAT |
| `n14-s3` | 15,414 | 35,670 | `d52ed6b8b937af1fbc34be67a56f099008472f5324ae79398106f89f128376a4` | `cf3c64e065c3e75febc443712e233f8fbd25fcccb89e9dfc9d477b72174ccab4` | VERIFIED UNSAT |
| `n14-s4` | 15,414 | 35,670 | `73b275a2008e819d8bc0c6d3d355db7a903761670e79414b1c918edd4dcd831b` | `d814ff1fb6346bad58ac2f8599604578a93ab6ff23ca93eafeb096d4c7928530` | VERIFIED UNSAT |
| `n14-s5` | 15,414 | 35,670 | `d4f6a0013ced730219a65962e35a3b87e995a38568b86a34e82ca6771aeffbcf` | `636339d8c13b3bf9c5c59e6ca2382f49bdbaea8847614a3353ac1d5cea090c14` | VERIFIED UNSAT |

All traces were checked with `drat-trim` source commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. The proof traces are 17 MB,
147 KB, 1.3 MB, and 50 MB respectively. They are deliberately retained under
`/scratch` and are not committed.

## Trust boundary

The elementary reductions, symmetry argument, and blow-up lemma are written
above. The finite exclusions trust the inspected CNF generator, PySAT's
sequential-counter implementation, and independent checking of the emitted
DRAT traces. All four traces were accepted by `drat-trim`; solver agreement
without trace checking was not used as proof. `direct_check.py` uses only the
Python standard library and validates the definition-level matching routine on
the published 36-vertex counterexample and on a regular 13-vertex tournament
where exactly one chosen vertex fails Hall. It is a guard against semantic and
quantifier mistakes, not an exhaustive proof by itself.

No claim is made about orders 15 through 35, or that the 36-vertex tournament
is globally minimum. The historical novelty statement is limited to the
targeted literature and Discovery Net searches described in the associated
contribution; it is not a priority claim.
