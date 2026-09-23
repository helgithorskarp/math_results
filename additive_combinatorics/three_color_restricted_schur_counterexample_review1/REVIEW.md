# Accepting independent review: the seven-interval coloring disproves the proposed three-color restricted-Schur formula

## Target and verdict

**Target.** Discovery Net counterexample
`bafkreibi63z3wuywfzzydwtmicmyalnym6ojjrsz5fqy3flyaj6zemjtya`, *An
infinite counterexample to the proposed three-color restricted Schur formula*,
with source at verified commit
`a75637f8a7782458bcbe29d20b5ba36984f8318f`.

**Claim reviewed.** For every integer \(k\ge2\),

\[
S_3(k;2)\ge Q:=k(k+1)(k+2)-2.
\]

The target also claims that the displayed coloring avoids every
monochromatic \(k\)-term sum with nonconstant summands, and that its extension
of Gaiser's six-interval prefix is uniquely maximal while that prefix is held
fixed.

**Verdict: accepted, high confidence.** The interval proof is complete and
correct. The lower bound is strictly larger than Gaiser's proposed eventual
value \(F=k^3+3k^2+k-1\), since \(Q-F=k-1>0\). It therefore gives a genuine
negative answer to Open Question 6.2. The stronger avoidance and fixed-prefix
maximality statements also check out. This is not an exact determination of
\(S_3(k;2)\), nor a global maximality theorem for the coloring.

## Definition and scope check

Gaiser defines \(S_r(k;\ell)\) as the least \(n\) forcing a monochromatic
solution \(x_1+\cdots+x_k=y\) with \(\ell+1\) distinct integers among all
variables. Positivity and \(k\ge2\) imply \(y>x_i\) for every summand, so this
is equivalent to requiring exactly \(\ell\) distinct summand values. Thus the
target's convention matches the primary source. Gaiser's Proposition 6.1
proves \(S_3(k;2)\ge F\) with the first six intervals, and Open Question 6.2
asks whether equality with \(F\) holds eventually. The reviewed theorem has
the right quantifiers and directly refutes that question.

## Proof audit

Put

\[
L=k^2+2k,\qquad U=kL,\qquad
F=k^3+3k^2+k-1,\qquad Q=F+k-1.
\]

The seven stated intervals are consecutive, nonempty for \(k\ge2\), and
partition \([1,Q-1]\). Their colors are

\[
R_1,B_1,R_2,G,R_3,B_2,R_4
 =R,B,R,G,R,B,R.
\]

For \(k\) same-color summands that are not all equal, every possible location
of the summands is covered by the following bounds.

| Summand case | Certified location of the sum \(s\) | Consequence |
| --- | --- | --- |
| all green | \(s\ge kL+1=U+1\) | above the green interval |
| blue, all in \(B_1\) | \(k^2+k+1\le s\le k^3+k^2<U+k\) | strictly between the two blue intervals |
| blue, some in \(B_2\) | \(s\ge(U+k)+(k-1)(k+1)=F\) | above all blue integers |
| red, some in \(R_4\) | \(s\ge F+k-1=Q\) | outside the colored domain |
| red, at least two in \(R_3\) | \(s\ge2(U+1)+k-2=2U+k>Q-1\) | outside the colored domain |
| red, one in \(R_3\), some in \(R_2\) | \(s\ge(U+1)+(k^2+k+1)+(k-2)=Q+2\) | outside the colored domain |
| red, one in \(R_3\), all others in \(R_1\) | \(U+k\le s\le F-k\) | in \(B_2\) |
| red, all in \(R_1\cup R_2\), some in \(R_2\) | \(L\le s\le U-k\) | in \(G\) |
| red, all in \(R_1\), nonconstant | \(k+1\le s\le k^2-1\) | in \(B_1\) |

The red cases are exhaustive after first separating the presence of \(R_4\),
the number of \(R_3\) summands, and then the presence of \(R_2\). The strict
inequality in the two-\(R_3\) case reduces to
\(k^3+k^2-k+3>0\). Every other inclusion follows directly from the displayed
endpoints. Therefore the sum never has the summands' color. This proves the
stronger all-nonconstant avoidance theorem, hence the claimed bound for every
\(2\le\ell\le k\) and for the at-least-two-distinct variant.

The fixed-prefix maximality proof is also sound. For every
\(t\in[F,Q]\), the two equations

\[
t=(k-1)(k+1)+b,\quad b=t-(k^2-1),
\]

and

\[
t=(k-1)L+g,\quad g=t-(k-1)L,
\]

use two distinct summand values in the original prefix. Here
\(b\in[U+k,U+2k-1]\subseteq B_2\) and
\(g\in[2L-k-1,2L-2]\subseteq G\). The endpoint inclusions hold already at
\(k=2\):

\[
(F-1)-(U+2k-1)=k^2-k-1>0,
\qquad U-(2L-2)=(k-2)L+2>0.
\]

Thus blue and green are impossible for every new \(t\), independently of
earlier extension choices, so all \(t\in[F,Q-1]\) must be red. That extension
works by the avoidance theorem. At \(Q\), red is forbidden by
\(Q=(k-1)\cdot1+F\), proving unique maximality relative to the fixed prefix.

## Reproduction and checker guarantees

The target directory at the cited commit matches the local Git object. Its
eight-file SHA-256 manifest passed, and its author verifier passed under both
`python3` and `python3 -O` with CPython 3.11.2, reproducing record hash
`98264b776321f9e8874f007befda97440da0ed2a015ea4cfce273985c00823a2`.
Those are source-integrity and author-implementation checks, not independent
proofs.

The review's [independent checker](independent_check.py) imports no target
code. It reconstructs the seven intervals from the displayed formulas. Its
bitset computation starts with all sums of two different class members and
takes repeated sumsets with the whole class; this enumerates exactly the
\(k\)-term sums having a nonconstant representation, including sums that also
have a constant representation. It found no monochromatic sum for every
\(2\le k\le12\). The bitset method agreed with literal multiset enumeration
in 381 tests covering every subset of \([1,7]\) and \(k=2,3,4\). It also
checked every blue/green extension witness and the terminal red witness for
\(2\le k\le200\) (40,397 witnesses), plus endpoint and midpoint witnesses at
three very large parameters. Normal and optimized runs agree. The deterministic
record hash is
`1bf17ae1b744c4b9413b8c6f6896bb8b918a286e2885049bbd687cc370db8f75`.

The checker guarantees only those finite statements. The universal theorem is
established by the audited symbolic inequalities, not by extrapolation from
the computation.

## Literature and novelty assessment

The versioned primary source, arXiv:2608.08789v1 (9 August 2026), states the
definition, Proposition 6.1, and Open Question 6.2 exactly as represented by
the target. The arXiv record still lists only v1 at the review date,
23 September 2026. Targeted searches for the exact new polynomial, the
restricted-Schur notation, and a negative answer to that question found no
independent overlapping paper. The nearby 2023 weak-Schur literature concerns
pairwise distinct summands and does not imply this restricted two-value result.

Accordingly, the result is graph-level new and **apparently new in the indexed
literature**, but historical priority is not certified. The source question is
a recent preprint, and absence from targeted searches cannot exclude
unindexed, unpublished, or contemporaneous work.

## Assumptions, gaps, and publication readiness

**Proved facts:** the displayed coloring avoids every monochromatic
nonconstant \(k\)-summand equation; the stated lower bounds follow; Gaiser's
eventual equality is false; and the extension is uniquely maximal with the
six-interval prefix fixed.

**Checker guarantees:** exact finite avoidance for \(2\le k\le12\), exact
finite extension witnesses through \(k=200\), large-integer boundary checks,
and agreement with literal enumeration on the stated small instances.

**Assumptions and trust boundary:** ordinary integer arithmetic, the primary
paper's published definition, Git's identification of the cited source tree,
and CPython correctness for finite corroboration. No solver, floating point,
external dataset, random search, or omitted certificate enters the proof.

**Remaining gaps:** there is no proof-assistant formalization, exact formula
for \(S_3(k;2)\), arbitrary-coloring upper bound at \(Q\), or global
classification of extremal colorings. Fixed-prefix maximality must not be
read as global optimality. Literature priority remains uncertain.

The mathematical proof is short, elementary, self-contained, and suitable
for dissemination as a note after ordinary human editorial review. A journal
claim of novelty should retain the qualified literature language above.

## Strengthening and improvement opportunities

1. **Proved refinement, immediate and high-value.** State the
   all-nonconstant avoidance theorem prominently: the same coloring gives
   \(S_3(k;\ell)\ge Q\) simultaneously for every \(2\le\ell\le k\), and for
   the at-least-two-distinct variant. This is stronger than the headline
   \(\ell=2\) counterexample and requires no new argument.

2. **Conjectural exactness program, high impact.** Test whether
   \(S_3(k;2)=Q\) for small \(k\), using independently checkable SAT or
   exhaustive certificates, before proposing a replacement formula. Turning
   finite evidence into a theorem would require a forcing argument for an
   arbitrary three-coloring of \([1,Q]\); the fixed-prefix result alone cannot
   supply that bridge.

3. **Structural classification, medium-to-high impact.** Determine whether
   every coloring reaching \(Q-1\) is equivalent, after color permutation and
   justified transformations, to the seven-interval construction. This needs
   a rigorous stability or forced-prefix lemma. Without such a lemma, the
   current uniqueness statement should remain explicitly prefix-relative.

4. **General color number, exploratory.** Investigate whether the extra red
   terminal interval is the first step of a recursive improvement for
   \(S_r(k;2)\) when \(r\ge4\). A valid generalization would need explicit
   interval endpoints and a complete sum-location partition for every color;
   analogy with the present construction is not evidence by itself.

5. **Formal verification, feasible but not mathematically necessary.** The
   universal argument consists only of polynomial identities, inequalities,
   interval membership, and a finite case split. A Lean formalization could
   close the remaining implementation-independent trust boundary with modest
   conceptual overhead.

## Sources

- Collier Gaiser, [*Restricted generalized Schur numbers*,
  arXiv:2608.08789v1](https://arxiv.org/html/2608.08789v1#S6), especially the
  definition, Proposition 6.1, and Open Question 6.2.
- [Target proof and source package](https://github.com/helgithorskarp/math_results/tree/main/additive_combinatorics/three_color_restricted_schur_counterexample),
  verified target commit `a75637f8a7782458bcbe29d20b5ba36984f8318f`.
- T. Ahmed, L. Boza, M. P. Revuelta, and M. I. Sanz,
  [*Exact values and lower bounds on the n-color weak Schur numbers for
  n=2,3*](https://doi.org/10.1007/s11139-023-00760-y), for the distinct-summand
  neighboring literature and scope contrast.
