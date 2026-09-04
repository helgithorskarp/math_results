# A response-fiber descent criterion

This note gives a sufficient condition for two cops to win the full-feedback
directional localization game and records its exhaustive verification for all
connected graphs through order 10.

## Definitions

For \(X\subseteq V(G)\), write

\[
\Gamma(X)=\bigcup_{x\in X}N[x].
\]

Every robber territory immediately after a recontamination phase has this
form: if \(X\) was the response cell just before the robber moved, the next
territory is \(\Gamma(X)\).  The initial territory also has this form because
\(V(G)=\Gamma(V(G))\).

An action \(A\) consists of at most two simultaneous probes.  The deterministic
full-feedback response signature partitions \(V(G)\); let \(\mathcal P_A\)
denote that partition.  A territory \(B\) is *statically two-resolvable* if
some action has only singleton intersections with \(B\).

We say that \(G\) has the **response-fiber descent property** when, for every
nonempty \(X\subseteq V(G)\) with \(B=\Gamma(X)\) and \(|B|>1\), there is an
action \(A\) such that every \(P\in\mathcal P_A\), on writing \(C=B\cap P\),
satisfies at least one of

1. \(|C|\leq1\);
2. \(|\Gamma(C)|<|B|\); or
3. \(\Gamma(C)\) is statically two-resolvable.

## Sufficient-condition theorem

> **Theorem.** If a finite graph has the response-fiber descent property,
> then its full-feedback directional localization number is at most two.

**Proof.**  Strongly induct on the cardinality of a neighborhood-generated
territory \(B\).  A singleton territory is already located.  For larger
\(B\), use the action supplied by the property.  If the observed cell \(C\)
is a singleton, the cops win immediately.  Otherwise the territory after the
robber moves is \(B'=\Gamma(C)\).  In case 2, \(|B'|<|B|\), so the induction
hypothesis supplies a bounded winning strategy from \(B'\).  In case 3, one
more probing phase resolves \(B'\).  The strategy may depend on the observed
cell, as permitted in the game.  There are finitely many cells at every
stage, so the maximum of their bounded continuation times is bounded.
Finally, the initial territory is \(V(G)=\Gamma(V(G))\).  \(\square\)

This theorem is a genuine reduction, not a proof that every graph has the
property.  Establishing the property universally would answer the motivating
open question negatively.

## Exact finite verification

[`dirloc_solver.cpp`](dirloc_solver.cpp), with `--check-descent`, enumerates
every nonempty generator mask \(X\), canonicalizes duplicate territories by
the mask \(\Gamma(X)\), and checks all response cells and one-phase resolver
conditions exactly.  It reports the first failing territory rather than
silently treating a failure as success.

The complete result is in [`descent_results.json`](descent_results.json):

| order | connected graphs | distinct territories \(\Gamma(X)\) | failures |
|---:|---:|---:|---:|
| 1 | 1 | 0 | 0 |
| 2 | 1 | 1 | 0 |
| 3 | 2 | 4 | 0 |
| 4 | 6 | 24 | 0 |
| 5 | 21 | 135 | 0 |
| 6 | 112 | 1,092 | 0 |
| 7 | 853 | 12,081 | 0 |
| 8 | 11,117 | 224,819 | 0 |
| 9 | 261,080 | 7,382,440 | 0 |
| 10 | 11,716,571 | 455,183,665 | 0 |

Thus all 11,989,764 connected graphs through order 10 satisfy the sufficient
condition, across 462,804,261 checked non-singleton territories.  This is
strictly more state-level information than checking only the initial
territory, although its consequence \(\zeta_d^*(G)\leq2\) is the same finite
theorem already recorded in the main README.

[`run_descent_census.py`](run_descent_census.py) performs the deterministic
nauty residue-class partitioning, validates every worker summary, checks the
predeclared number of connected graphs at each order, and rejects any emitted
counterexample.  The order-10 run used 16 residue classes and 16 processes.
The slowest partition took 337.719 seconds and the sum of per-partition solver
times was 3,927.100 seconds on the reference machine.

[`verify_descent.py`](verify_descent.py) is a definition-level Python replay
using arbitrary-precision masks and a separately written recurrence.  It
agrees entry by entry with the optimized C++ result through order 8, including
all 224,819 order-8 territories.  The Python checker uses distinct probe pairs;
allowing a single probe does not enlarge the accepted class because adding a
second probe refines response cells, neighborhood union is monotone, and
static resolvability is downward closed.

For the verified range, 64-bit masks are exact: at most ten low bits encode
vertices, population counts are integral, and no arithmetic operation can
overflow.  The external trust boundary is nauty/Traces 2.9.3 for complete
unlabeled generation, plus the compiler and hardware.  The mathematical
trust boundary is the belief-state reduction and induction above.

## Reproduction

After building `dirloc_solver` as in the main README and setting `GENG`:

```bash
python3 verify_descent.py \
  --compare ./dirloc_solver --geng "$GENG" --max-order 8

python3 run_descent_census.py \
  --geng "$GENG" --solver ./dirloc_solver \
  --max-order 10 --partitions 16 --jobs 16 > observed_descent.json

diff -u descent_results.json observed_descent.json
```

The production scripts use only the Python 3.11 standard library.  The
reference build used GCC 12.2.0 and nauty/Traces 2.9.3.
