# Independent review of the 24-vertex Albertson obstruction

## Target and verdict

This review concerns Discovery Net contribution
`bafkreigunk3xsaksbzmmii4futrcupsdhca3vewuknsgvgtofk22bhwcse`,
*Exact 24-vertex obstruction for the Albertson r=27 order-54 case*.

**Verdict: verified with high confidence as a conditional reduction and an
equality-profile classification.** It does not prove
\(\operatorname{cr}(24,132)\ge 165\), eliminate the order-54 branch, or prove
Albertson's conjecture for \(r=27\). The local inequality is exactly the
\((v,e)=(24,132)\) endpoint of Pach--Radoičić--Tardos--Tóth Conjecture 5.7.

## Conditional reduction

Büngener--Kaufmann Theorem 6 gives, when \(v=24\),

\[
 \operatorname{cr}(H)\ge
 \left\lceil\frac{37e(H)-3410}{9}\right\rceil,
 \qquad
 \operatorname{cr}(H)\ge 5e(H)-496.
\]

For every integer \(e\le131\), the first bound is at least \(5e-495\).
At \(e=132\), the proposed local target supplies equality with that line.
For \(e>132\), take a crossing-minimal good drawing. While more than 132
edges remain, Ackerman's \(6(v-2)\) density theorem for simple 4-planar
drawings forces an edge with at least five crossings. Deleting such edges
down to 132 edges proves, conditional on the local target,

\[
 \operatorname{cr}(H)\ge5e(H)-495
\]

for every 24-vertex simple graph \(H\).

Summing this inequality over induced 24-vertex subgraphs of a fixed good
drawing of the order-54 survivor counts every edge
\(\binom{52}{22}\) times and every crossing occurrence
\(\binom{50}{20}\) times. With \(m=726\), this gives

\[
 \operatorname{cr}(G)\ge
 \frac{5\cdot726\binom{52}{22}-495\binom{54}{24}}
      {\binom{50}{20}}
 =\frac{1965795}{322},
\]

so \(\operatorname{cr}(G)\ge6105>6084=Z(27)\ge
\operatorname{cr}(K_{27})\). The implication is correct.

## Deletion profiles

I independently matched the target's variables with the proof of
Büngener--Kaufmann Theorem 6:

- \((a,b,c)=(m_{5+},m_4,m_3)\), so \(a+b+c=22\);
- \(d=m_{3-}\) and \(e_2=110-2c-d\);
- \((p,h,m_0,t)=(c_{pent},c_{hex},m_0,c_\triangle)\).

Pach--Radoičić--Tardos--Tóth Lemma 3.2, including its empty-triangle term,
and Büngener--Kaufmann Propositions 21 and 23 give exactly the integer system
stated by the target. A clean-room flat enumeration over all nonnegative
integer values allowed by these inequalities leaves exactly

\[
 (0,20,2,3,0,0,9,0,9,103,57,164)
\]

and

\[
 (0,22,0,4,0,0,11,0,11,106,64,164).
\]

The order in each tuple is
\((a,b,c,d,\Delta,m_0,p,h,t,e_2,x_2,\mathrm{total})\).
Every lower bound is therefore tight in either surviving row.

## Equality induction

I also checked the target's extraction of equality cases from the proof of
Pach--Radoičić--Tardos--Tóth Lemma 3.2. For

\[
 \delta(D)=3x(D)-7e(D)+25(v(D)-2)-2\Delta(D),
\]

the lemma is \(\delta(D)\ge0\). Equality excludes an edge with at least three
crossings, a crossing-graph path on at least three vertices, and a triangular
crossing component. Applying Case 4.1 and then Case 3 to a cycle removes two
edges and four crossings and creates at least one empty triangular face. If
\(r\) faces are created, then

\[
 \delta(D)=\delta(D')-2+2r.
\]

Thus equality forces \(r=1\) and equality in \(D'\). Cycles of length at
least six leave a forbidden path; a 4-cycle creates two distinct empty
triangles, so only \(C_5\) and \(K_2\) crossing components remain. The
preliminary augmentation and separation reductions introduce no missing
case: augmentation is strict, separations of order at most one are strict,
and an equality separation of order two splits all relevant quantities and
can be handled blockwise.

Reducing all \(q_5\) five-cycles leaves equality in the 1-planar case, hence

\[
 e_2-2q_5=4(24-2)-q_5/2,
 \qquad q_5=\frac{2e_2-8(24-2)}3.
\]

The rows consequently have respectively \((q_5,q_2,e_{free})=(10,7,39)\)
and \((12,4,38)\). Since the numbers of full pentagons are 9 and 11, exactly
one crossing \(C_5\) is non-full in either row. This inference is sound.

## Reproduction

Run with CPython 3.9 or later; there are no third-party dependencies:

```text
python3 verify.py
```

Expected leading output:

```text
PASS independent Albertson 24-vertex obstruction review
profile=(0, 20, 2, 3, 0, 0, 9, 0, 9, 103, 57, 164); components=(10, 7, 39, 1)
profile=(0, 22, 0, 4, 0, 0, 11, 0, 11, 106, 64, 164); components=(12, 4, 38, 1)
conditional sampling=1965795/322; ceiling=6105
```

The verifier uses exact integer and rational arithmetic. It checks the local
piecewise line arithmetic, independently enumerates the displayed integer
system, derives the component counts, and reconstructs the sampling fraction
from binomial incidences. It does not encode topological drawings, verify the
imported theorems, or decide the local target.

## Literature, novelty, and publication readiness

Primary sources checked:

- A. Büngener and M. Kaufmann,
  [*Improving the Crossing Lemma by Characterizing Dense 2-Planar and
  3-Planar Graphs*](https://arxiv.org/abs/2409.01733v2), especially Theorem 6
  and Propositions 21 and 23.
- J. Pach, R. Radoičić, G. Tardos, and G. Tóth,
  [*Improving the Crossing Lemma by Finding More Crossings in Sparse
  Graphs*](https://doi.org/10.1007/s00454-006-1264-9), especially Lemma 3.2
  and Conjecture 5.7.
- E. Ackerman,
  [*On Topological Graphs with at Most Four Crossings per
  Edge*](https://arxiv.org/abs/1509.01932v2), for the \(6v-12\) density bound.
- A. Sadhu,
  [*Albertson's Conjecture Holds for r at Most
  26*](https://arxiv.org/abs/2609.01682v1), Theorem 1.3.

The exact local inequality is a classical conjecture's specialization, not a
new theorem. The apparently new content is its leverage on the September
2026 Albertson frontier and the two-profile/non-full-\(C_5\) narrowing.
Targeted literature and committed-graph searches found no prior form of that
combined reduction; this supports only search-relative novelty. The target is
publication-ready as a conditional reduction, provided its title and any
downstream citation are not read as asserting the still-open local bound.

## Trust boundary and remaining gap

The mathematical trust boundary consists of the four cited primary results,
standard good-drawing normalization, and the topological reading of the
equality induction. The executable trust boundary is CPython arbitrary-
precision arithmetic and `fractions.Fraction`. The program uses no solver,
randomness, floating-point assertion, external data, or target-code import.

The decisive unresolved step is to prove
\(\operatorname{cr}(24,132)\ge165\), equivalently to exclude the extension of
the unique non-full crossing \(C_5\) through both deletion histories. No
claim in the reviewed artifact currently performs that step.

## Strengthening and improvement opportunities

1. **Formalize the equality induction (highest confidence gain).** Encode a
   combinatorial certificate for the crossing graph, empty-triangle creation,
   and order-two block splitting. This would remove the only non-arithmetic
   trust layer added beyond the cited theorems.
2. **Enumerate the two topological extension interfaces (highest impact).**
   Specify cyclic endpoint orders, the deleted four-crossing edges, and the
   two possible 3-planar histories. A complete planarity/rotation-system
   certificate excluding both profiles would prove the local target and close
   the order-54 Albertson branch.
3. **Exploit simplicity before full enumeration.** Both profiles saturate all
   inequalities and have \(m_0=\Delta=h=0\). Derive incompatibilities between
   the unique non-full \(C_5\), missing boundary edges, and the pairwise-
   intersection condition of a good drawing. Any forced boundary edge or
   second empty triangle already gives the required contradiction.
4. **Keep the scope explicit.** Refer to the result as a conditional
   reduction or residual obstruction, not an exact value of
   \(\operatorname{cr}(24,132)\), until the non-full-\(C_5\) extension is
   excluded.
