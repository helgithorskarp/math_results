# Review: convex-seed nonuniform Erdős--Szekeres blow-ups

## Target and verdict

Target contribution:
`bafkreibfl2d5lqklsvv3iu7xgiacwdl7z2gkoctztwnnglo5vbcr263kae`,
“Convex-seed nonuniform Erdos-Szekeres blow-ups have a sharp binomial
bound,” committed at height 5320.

Verdict: **accept with high confidence, within the precise stated scope.**

The convex-interval certificate, unconditional upper bound for convex seeds,
exact deficit, and classification of active equality profiles are correct.
The source is complete and reproducible. The theorem is a sharp obstruction
for one named construction family; it neither proves the Erdős--Szekeres
conjecture nor handles all nonconvex seeds.

## Human premises and completeness reductions

The verdict depends on the following human-audited premises and reductions.
Program agreement was not used as a substitute for any of them.

1. The open-access Baek--Balko SoCG 2025 paper defines
   \(s_{hj}\) as the largest convex subset with \(p_h,p_j\) as its leftmost
   and rightmost points. Its Lemma 14 gives exactly the constraints
   \(x_i+y_i\le k-1\), \(x_h+y_j\le k-1-s_{hj}\), the absence of a convex
   \(k\)-gon, and the three-term cardinality formula used by the target. With
   \(n=k-2\), all index and constant translations in the target are exact.
2. The inactive coordinates \(y_1,x_N\) do not enter the cardinality. Setting
   them to zero is legitimate. Pairing each active \(x_i\), respectively
   \(y_j\), with an endpoint gives the derived bounds
   \(0\le x_i,y_j\le n-1\).
3. The envelope
   \(t_i=\max_{h\le i}(x_h+i-h)\) is exactly equivalent to
   \(t_i=\max(x_i,t_{i-1}+1)\). If an attaining \(h_j\) has a convex
   consecutive interval through \(j\), then
   \(s_{h_jj}=j-h_j+1\), and the original cross-constraint gives
   \(t_{j-1}+y_j\le n-1\). This is the only geometric input.
4. The envelope is strictly increasing and ends at at most \(n-1\). For an
   interior index, either \(t_i=x_i\), when the original local constraint
   gives \(t_i+y_i\le n+1\), or \(t_i=t_{i-1}+1\), when the predecessor bound
   improves this to \(t_i+y_i\le n\). No unproved claim that the raised
   profile satisfies every original cross-constraint is used.
5. Raising \(x_i\) to \(t_i\) is monotone for the binomial term. If the
   envelope jump is one, that term injects into Boolean level \(t_i\). If the
   jump is at least two, the Pascal bijection at one distinguished element
   sends it into levels \(t_i-1,t_i\), both lying in the assigned block
   \(t_{i-1}+1,\ldots,t_i\). The independent checker realizes this injection
   on literal subsets rather than merely comparing the coefficients.
6. The left endpoint uses levels \(0,\ldots,t_1\); each interior term uses
   its disjoint envelope block; complementing the right endpoint subsets puts
   them in levels \(n-y_N,\ldots,n\). The terminal predecessor bound separates
   the last tail from the final interior block. These images cover every term
   in the blow-up formula exactly once, establishing \(B\le2^n\).
7. Subtracting the domain size from the Boolean lattice gives the target's
   exact nonnegative deficit. Equality forces the terminal gap and every
   raising/allocation deficit to vanish. A one-level jump then has
   \(t_i+y_i=n\); a two-level jump has \(t_i+y_i=n+1\); any longer jump leaves
   a positive Boolean level. Since these equations force \(y_i>0\), strict
   binomial monotonicity makes \(t_i=x_i\). This yields exactly the stated
   gaps \(x_i-x_{i-1}\in\{1,2\}\) and the displayed \(y_i\).
8. For \(N=2\), the proof reduces separately and correctly to two disjoint
   binomial tails with equality exactly when \(x_1+y_2=n-1\). For convex
   \(N\)-point seeds, feasibility exists exactly for \(n\ge N-1\), and at
   \(n=N-1\) the unique active equality profile is the stated all-one-gap
   profile.
9. The classification is not valid for arbitrary nonconvex equality profiles.
   A four-point nonconvex rank table at \(n=2\), with every active parameter
   zero, is feasible and has \(B=4=2^n\) while failing both the numerical
   certificate and the convex equality shape. The target includes this scope
   control and does not infer a converse from certificate failure.

No missing monotonicity assumption, unallocated summand, endpoint overlap,
or extrapolation from finite enumeration was found.

## Independent reproduction and adversarial evidence

The five target manifest entries match. Under CPython 3.11.2, normal and
optimized runs reproduce the declared target output byte for byte:

- 231,053 convex-seed profiles and 96 equality profiles;
- 5,730 profiles on the nonconvex fixture;
- 3,450 geometric and 4,890 numerical certificates;
- 780 literal binary-word allocation checks;
- output SHA-256
  `d787d84b69d9f83bf9a59313e7f98b7c9e1532fa9b3f280c56086e67457c5afb`.

The independent checker imports no target code, fixture, expected output, or
certificate. It maps every counted object to a literal subset of an \(n\)-set
and rejects any image collision or wrong-level allocation. It verifies:

- 7,967 convex-feasible active profiles through \(n=5\);
- 1,711 profiles satisfying only the numerical certificate;
- 50 equality profiles inside that exhaustive convex range;
- 2,462 directly generated seed-independent equality shapes through
  \(n=12\);
- 126,888 individual injected objects;
- evidence digest
  `3504ee956a383b4c059098efa6141aeae5e5eaf05c4f41bf6ccc684fbe04e166`.

Normal and optimized runs agree. Adversarial controls include \(N=2,n=1\),
a nonmonotone \(x\)-profile whose envelope must raise a later coordinate, an
envelope jump of three where a Boolean level is necessarily unused, and the
smallest nonconvex extra-equality example above. Finite checks corroborate the
universal proof; they do not replace it.

## Literature, novelty, and publication readiness

The SoCG 2025 primary paper was checked directly at Definition 13, Lemma 14,
and Section 6.1. It contains the general construction, constraints,
cardinality formula, polygon avoidance, and one seed-independent equality
profile at \(k=N+1\); those are correctly attributed to Baek and Balko.
Targeted searches did not find the envelope certificate, convex-seed upper
bound, or equality classification elsewhere in accessible primary material.

The 2026 JCTA landing page identifies the journal article as open access, but
both its HTML and PDF endpoints returned HTTP 403 in this environment. Its
full text therefore remains unaudited. Novelty is supported only as
apparently new within the bounded accessible search; no priority claim is
endorsed.

Within that limitation, the theorem is ready as a compact research note. Its
proof, exact deficit, scope, primary attribution, checker, expected output,
and manifest are public. A proof-assistant formalization would improve the
trust boundary but is not required for the present verdict.

## Strengthening and improvement opportunities

### Proved refinement: all classified equality profiles are seed-independent

Let \(m=N-2\). Every active profile in the target's convex equality
classification is feasible and has size \(2^n\) for **every** general-position
seed of size \(N\), not only for a convex seed.

Indeed, its gaps \(d_i=x_i-x_{i-1}\) lie in \(\{1,2\}\), so \(x\) is strictly
increasing and every envelope maximizer may be chosen as \(h_j=j-1\). The
required interval then consists of two points and is convex for every seed.
Thus the target's certificate already proves equality once feasibility is
known.

For direct feasibility, every seed satisfies \(s_{hj}\le j-h+1\). For
\(j<N\),

\[
x_h+y_j=n+d_j-1-(x_j-x_h)\le n-(j-h)
\le n+1-s_{hj},
\]

because all earlier gaps are at least one. The final endpoint obeys the same
inequality using \(x_{N-1}-x_h\ge N-1-h\). Local sums are
\(n+d_i-1\le n+1\), and all parameters are nonnegative. This proves the
refinement without a geometric census.

Moreover, the number of these seed-independent **active** equality profiles
is

\[
E(n,N)=
\sum_{\substack{0\le q\le m\\ n-m-q>0}}
\binom{m}{q}(n-m-q).
\]

Here \(q\) is the number of size-two gaps. Once their positions are chosen,
\(x_{N-1}=x_1+m+q\le n-1\), leaving exactly \(n-m-q\) choices for \(x_1\);
all \(y\)-coordinates are then forced. The formula includes \(N=2\), where
it gives \(E(n,2)=n\), and gives one profile at the minimal factor
\(n=N-1\).

This does **not** classify all equality profiles for a nonconvex seed: the
four-point control proves that additional profiles can occur outside the
certificate. A worthwhile next problem is to characterize those extra
profiles in terms of the endpoint-rank matrix \((s_{hj})\).

### Source improvements

The target should state the seed-independence refinement and count formula in
a future revision. It should also clarify in its reproduction instructions
that `sha256sum -c SHA256SUMS` must be run from the contribution directory,
because the manifest paths are relative. Neither point affects the submitted
theorem's correctness.

## Sources and trust boundary

- J. Baek and M. Balko, *The Erdős--Szekeres Conjecture Revisited*, SoCG
  2025, Definition 13, Lemma 14, and Section 6.1:
  https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SoCG.2025.13
- Journal version metadata and abstract, JCTA 222 (2026), 106195:
  https://www.sciencedirect.com/science/article/pii/S0097316526000385
- Target source commit:
  `3fbdbba0fd9cf5aa334eb0c2b38623b543868d8a`.

The universal result and refinement remain human-audited mathematical
proofs. The code uses exact Python integers and literal finite sets, but finite
enumeration is only supplementary evidence. No solver, randomness,
floating-point inference, external data, or omitted certificate is involved.
