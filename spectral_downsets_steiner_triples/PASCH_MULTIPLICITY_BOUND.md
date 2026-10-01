# Multiplicity-sensitive Pasch defect stability and capped closures

Author: **six-downset-2**, role **researcher**. Ordinary lemma with exact
finite certificates and applications to Spectral Chvátal Conjecture H.
This does not resolve H or I. Pasch switches are classical; the lower
matrix theorem, complement defect identity and joint cap criterion are
credited below. The uniform norm budget **14 is sharp at \(\mu=4\)**;
no optimal cap, closure radius or other-multiplicity norm is claimed.

## Statement

Let \(\mathcal B\) be an existing simple \(2\!-(v,3,\lambda)\) design,
\(v\ge7\), \(2\le\lambda\le v-2\). Its point-by-pair completion matrix is
\(C_{x,p}=1_{p\cup\{x\}\in\mathcal B}\), with zero entries when \(x\in p\).
Put \(r=\lambda(v-1)/2\), \(u=\lambda(\lambda-1)/2\),

\[
 Z=CC^{\mathsf T}-(r-u)I-uJ,\qquad K_v=I-J/v.
\]

In particular \(Z_{xx}=0\) and \(Z\mathbf1=0\). Suppose one legal Pasch
switch replaces four triples by the other four triples on three disjoint
pairs, and let \(\Delta=Z'-Z\). Set \(q=v-2-\lambda\) and
\(\mu=\min(\lambda,q)\). Legality forces \(q\ge1\).

**Lemma.** Both \(\kappa K_v+\Delta\) and
\(\kappa K_v-\Delta\) are positive semidefinite under any of the following
sufficient budgets:

| Smaller complementary multiplicity | Budget |
|---|---|
| \(\mu=1\) | \(\kappa=0\), because \(\Delta=0\) |
| \(\mu=2\) | \(\kappa=22/3\) |
| \(\mu\ge3\) | any real \(\kappa\ge10\) with \(\kappa(\kappa-8)\ge48\mu-108\) |

Thus \(34/3\) works for \(\mu=3\), and **14 works for \(\mu=4\)**.
The last sufficient condition is equivalent, for \(\mu\ge3\), to
\(\kappa\ge4+\sqrt{48\mu-92}\). Increasing a valid budget preserves the
Loewner inequalities. No integrality, symmetry or disjointness between
successive switch supports is assumed beyond the simple-design and
legal-switch hypotheses.
An explicit simple \(2\!-(13,3,4)\) witness below shows that no smaller
real budget can replace 14 uniformly at \(\mu=4\).

The older sufficient condition from
[Pasch defect stability](PASCH_DEFECT_STABILITY.md) was
\(\kappa\ge8\), \(\kappa(\kappa-8)\ge48\lfloor(v-6)/2\rfloor\).
Since \(v\ge2\mu+2\), its right side is at least \(48\mu-96\).
For \(\mu\ge3\), every budget satisfying that older condition also
satisfies the new one. The bounds for \(\mu=1,2\) are likewise smaller
than its minimum budget eight. This compares the sufficient conditions,
not the optimal norm of any particular move.

## Rank-six reduction and exact three-by-three norm test

Write the pairs as \((a_j,b_j)\), \(j=0,1,2\), and orient a move by
removing the even-parity triples and adding the odd-parity triples, or
vice versa. Let \(A_j=e_{a_j}-e_{b_j}\). Let column \(W_k\) be supported
on the four cross pairs between the other two groups, with sign minus
on even parity and plus on odd parity; reverse all its signs for the
reverse move. The entrywise completion update and orthogonality are

\[
 C'=C+AW^{\mathsf T},\quad A^{\mathsf T}A=2I_3,\quad
 W^{\mathsf T}W=4I_3,\quad Y=CW+2A,\quad
 \Delta=YA^{\mathsf T}+AY^{\mathsf T}.
\]

These identities and legality are proved in the parent
[rank-six argument](PASCH_DEFECT_STABILITY.md), and checked entrywise
again here. On the six support points \(Y=AT\), where
\(T_{jj}=0\) and each off-diagonal entry belongs to \(\{-1,0,1\}\).
Write \(O=Y|_{[v]\setminus S}\). Its columns sum to zero.
In the orthonormal inside contrast basis \(A/\sqrt2\), together with
outside coordinate vectors, the only nonzero part of \(\Delta\) is

\[
 \begin{pmatrix}
  2(T+T^{\mathsf T})&\sqrt2\,O^{\mathsf T}\\
  \sqrt2\,O&0
 \end{pmatrix}.                                                   \tag{1}
\]

Inside pair-sum vectors are annihilated. Also \(\Delta\mathbf1=0\), so
a bound by \(\kappa I\) is equivalent to the stated bound by
\(\kappa K_v\). For \(\kappa>0\), Schur complementation of the outside
\(\kappa I\) block in each signed form proves the exact equivalence

\[
 \kappa K_v\pm\Delta\succeq0\ \text{for both signs}
 \quad\Longleftrightarrow\quad
 \kappa^2I_3\pm2\kappa(T+T^{\mathsf T})-2O^{\mathsf T}O\succeq0
 \ \text{for both signs}.                                        \tag{2}
\]

This is an exact norm criterion, not a claim that every admissible
\(T,O\) pattern occurs in a design.

## Pair quotas connect the inside and outside terms

Fix column \(k\), with the other groups \(i,j\). Besides the one legal
removed completion for each cross pair, the only possible other inside
completions are encoded by four bits

\[
 u_b=1_{\{a_i,b_i,g_{j,b}\}\in\mathcal B},\qquad
 z_a=1_{\{g_{i,a},a_j,b_j\}\in\mathcal B},\qquad a,b\in\{0,1\},
\]

where \(g_{h,0}=a_h\) and \(g_{h,1}=b_h\). Put
\(n_k=u_0+u_1+z_0+z_1\). Directly expanding \(CW\) on the support
shows that, up to signs, the two off-diagonal entries of column \(k\)
of \(T\) are \(u_0-u_1\) and \(z_0-z_1\). Thus

\[
 c_k:=\sum_j|T_{jk}|=|u_0-u_1|+|z_0-z_1|,
 \qquad c_k\le n_k\le4-c_k.                                      \tag{3}
\]

For the cross pair \(\{g_{i,a},g_{j,b}\}\), its set \(X_{ab}\) of
outside completing points therefore has cardinality

\[
 h_{ab}=|X_{ab}|=\lambda-1-u_b-z_a\ge0.                            \tag{4}
\]

The outside column of \(O\) is, up to an overall sign,
\(1_{X_{01}}+1_{X_{10}}-1_{X_{00}}-1_{X_{11}}\). Its absolute column
sum is at most \(\sum h_{ab}=4(\lambda-1)-2n_k\).
Expanding its squared norm, discarding the nonpositive opposite-sign
intersection terms, and bounding the two same-sign intersections by
the smaller set size gives

\[
 \|O_k\|^2\le\sum h_{ab}+2\min(h_{01},h_{10})+2\min(h_{00},h_{11}).  \tag{5}
\]

Substitution of (4) makes the right side exactly

\[
 8(\lambda-1)-4n_k-2\,1_{c_k>0}.                                 \tag{6}
\]

For completeness, the elementary maximum identity used in this
substitution is

\[
 \max(u_1+z_0,u_0+z_1)+\max(u_0+z_0,u_1+z_1)
 =n_k+\max(|u_0-u_1|,|z_0-z_1|)
 =n_k+1_{c_k>0}.
\]

It follows by writing each maximum as half its sum plus half the
absolute difference, then using
\((|d_u+d_z|+|d_u-d_z|)/2=\max(|d_u|,|d_z|)\).
The bits are essential for the last equality.

## Complementation and the trace budget

The simple complement design has multiplicity \(q\) and the reverse
legal move. If \(P\) is point-pair incidence, then
\(C_q=J-P-C\), \(W_q=-W\), and \(JW=PW=0\). Therefore
\(C_qW_q=CW\), so its \(Y,T,O,\Delta\) are identical to those above.
Its extra bits are \(1-u_b,1-z_a\); its extra count is \(4-n_k\), and
its \(c_k\) is unchanged. This refines the bookkeeping behind the
already credited identity \(Z_q=Z_\lambda\) from
[dense point defects](DENSE_SCHUR_CAP.md).
We may use (3)--(6) for whichever design has multiplicity \(\mu\).

Set \(e=\sum_kc_k\), the number of nonzero directed entries of \(T\),
and \(p=|\{k:c_k>0\}|\). Then \(0\le e\le6\),
\(p\ge\lceil e/2\rceil\), and (3),(6) imply

\[
 \operatorname{tr}(O^{\mathsf T}O)
 \le M:=24(\mu-1)-4e-2p.                                         \tag{7}
\]

If \(\mu=1\), (4) forces all four extra bits and all outside sets to
be empty for every column. Thus \(T=O=0\), proving \(\Delta=0\).
If \(\mu=2\), nonnegativity of all four values in (4) forces
\(c_k\le1\): two nonzero bit differences would give one
\(u_b=z_a=1\), contradicting \(h_{ab}\ge0\). Consequently
\(e\le3\), \(p=e\), and \(M=24-6e\) is a valid trace bound.

## Small inside certificates and the universal comparison

For \(D=2(T+T^{\mathsf T})\), valid inside norm bounds are

| \(e\) | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| \(\alpha_e\) | 0 | 2 | 4 | 5 | 6 | 7 | 8 |

Here is an ordinary finite proof. The entrywise absolute value of
\(D\) is dominated by a symmetric matrix with off-diagonal entries
\(2a,2b,2c\), where \(a,b,c\in\{0,1,2\}\) count the directed nonzero
entries on each unordered edge and \(a+b+c=e\). Up to permutation the
possibilities are

\[
 (0,0,0);\ (1,0,0);\ (2,0,0),(1,1,0);\
 (2,1,0),(1,1,1);\ (2,2,0),(2,1,1);\ (2,2,1);\ (2,2,2).
\]

For each, \(\alpha_e I-R\succeq0\). All diagonal and two-point
principal minors are nonnegative, and its determinant is
\(\alpha_e^3-4\alpha_e(a^2+b^2+c^2)-16abc\), which is nonnegative
for every listed case. For any real \(x\),
\(|x^{\mathsf T}Dx|\le |x|^{\mathsf T}R|x|\le\alpha_e\|x\|^2\).
This proves the table without assuming a pattern is realizable.
The checker additionally verifies all seven principal minors of both
signed forms for **all \(3^6=729\) directed matrices \(T\)**.

By (7), \(\|O\|^2\le\operatorname{tr}(O^{\mathsf T}O)\le M\).
The norm of (1) is at most the largest eigenvalue of
\(\left(\begin{smallmatrix}\alpha_e&\sqrt{2M}\\\sqrt{2M}&0\end{smallmatrix}\right)\),
by the quadratic estimate in the norms of its inside and outside
components. Thus it suffices that

\[
 \kappa\ge\alpha_e,\qquad \kappa(\kappa-\alpha_e)\ge2M.             \tag{8}
\]

For \(\mu=2\), \(\kappa=22/3\) gives margins
\(52/9,28/9,4/9,46/9\) in (8) for \(e=0,1,2,3\), respectively.
For \(\mu\ge3\) and \(\kappa\ge10\), the needed margin is

\[
 \underbrace{\kappa(\kappa-8)-(48\mu-108)}_{\ge0}
 +(8-\alpha_e)\kappa+8e+4p-60.
\]

The second summand is nondecreasing in \(\kappa\). At ten, its minimum
over admissible \(p\), for \(e=0,1,\ldots,6\), is respectively
\(20,12,0,2,0,2,0\). This proves (8) in all cases and finishes the
unbounded lemma. At \(\mu=4,\kappa=14,e=6\), the sufficient comparison
may be singular. The lemma claims PSD, not strict positivity or a
universal rank for its norm forms.

## Exact sharpness witness for multiplicity four

[sharp_fixture()](pasch_multiplicity.py) gives a compact deterministic
construction of 104 triples, with support pairs \((0,1),(2,3),(4,5)\)
and outside points \(6,\ldots,12\). The independent tuple checker verifies
all 78 pair degrees equal four and all 13 point replications equal 24.
The four even-parity triples are present; all four odd-parity triples are
absent, so the displayed forward switch is legal. For this move,

\[
 T=J_3-I_3,\qquad O=w\mathbf1_3^{\mathsf T},\qquad
 w=(2,2,-2,-1,-1,0,0)^{\mathsf T},\qquad \|w\|^2=14.
\]

In particular \(O^{\mathsf T}O=14J_3\), \(e=6,p=3\), and the trace bound
42 and scalar comparison at \(\kappa=14\) are attained. The integer vector

\[
 x=(7,-7,7,-7,7,-7,6,6,-6,-3,-3,0,0)^{\mathsf T}
\]

has zero sum, squared norm 420, and **\(\Delta x=14x\)**. These equations
are checked against the direct difference of the two literal completion
defects, not only the low-rank formula. Therefore for every real
\(\kappa<14\),

\[
 x^{\mathsf T}(\kappa K_{13}-\Delta)x=420(\kappa-14)<0.
\]

Together with the universal bound, this proves that 14 is the smallest
possible uniform symmetric Pasch norm budget for \(\mu=4\), already at
13 points. The two norm forms at 14 have exact Fraction PSD ranks 11 and
12; their three-by-three Schur forms have ranks two and three. This is an
actual singular equality case, not merely a formally possible local pattern.
Complementing the witness gives the same sharp move at multiplicity seven.
It refutes a smaller proposed local budget, not H or capped feasibility.

For a compact reconstruction, the six graph masks in lexicographic order
of the 21 pairs of \(\{0,\ldots,6\}\) are
\(1482252,1681832,2001546,991329,418224,120368\); the first three have
degrees \((2,2,2,4,4,3,3)\), the last three
\((2,2,2,2,2,3,3)\). Their edge multiplicities are four minus the pair
degrees of the ten outside-only triples listed in the constructor and
compact output. The constructor also lists every remaining block rule;
the checker independently validates the resulting design, legality,
defects, eigenvector and norm forms. A bounded custom graph-factor feasible
search found these masks; no solver verdict, numerical result or completeness
of that search is used in the proof. Replay uses only the fixed six integers
and ordinary exact tuple arithmetic, with no external solver dependency.

## Two capped symmetry-free closure corollaries

Take any 13-point simple design invariant under a 13-cycle, then any
relabeling of it. At multiplicity four there are 762 designs for the
fixed labelled shift \(x\mapsto x+1\pmod{13}\), not 762 isomorphism
classes. The complete base result
[cyclic point budgets](CYCLIC13_SPECTRAL_CAP.md) proves \(Z\preceq20K_{13}\)
for every such base. Complementation gives the same point budget for
all 762 complementary multiplicity-seven bases.

After \(h\) legal moves, accumulating the present lemma gives
\(Z_h\preceq(20+14h)K_{13}\), even for overlapping supports. Apply the
unchanged complete cross-Gram and joint comparison criterion from
[CYCLIC13_SPECTRAL_CAP.md](CYCLIC13_SPECTRAL_CAP.md) and
[DEFECT_GRAM_CAP.md](DEFECT_GRAM_CAP.md). The final comparison matrices
use the following parameters:

| \(\lambda\) | moves allowed | point budget | \(N\) | \(s\) | \(B\) | \(\delta=N-B\) | \((\delta-g)/2\) |
|---|---|---|---|---|---|---|---|
| 4 | at most 3 | 62 | 196 | 37 | 164 | 32 | \(43/13\) |
| 7 | at most 5 | 90 | 274 | 55 | 238 | 36 | \(69/13\) |

In both cases \(g=330/13\). The final complete comparison matrices are

\[
 G_4=\begin{pmatrix}17593/129&16&47\\16&6244/165&34\\47&34&2135/43\end{pmatrix},
 \qquad
 G_7=\begin{pmatrix}11908/57&18&62\\18&9172/165&34\\62&34&1301/19\end{pmatrix}.
\]

The checker verifies all three positive leading minors of \(BI_3-G\)
at these endpoints and at every shorter depth, with **ten comparisons**
in total. This gives \(Q_c|_{\mathbf1^\perp}\prec BI\), hence a centered
upper gap \(\delta\). The inherited sparse repair transfers it to the
maximal matrix with upper gap \(\delta/2\) for every real
\(0<\eta\le1/1352\); the strict margin above is positive throughout.
In the notation of the parent proof, all four forms

\[
 Q_c,\quad Q_m,\quad NI-Q_c-\delta K_N,\quad NI-Q_m-(\delta/2)K_N
\]

are PSD. Their respective ranks, inherited from the lower theorem and
strict upper comparison, are
\(N-14,N-13,N-1,N-1\). The matrices satisfy the original H support and
row-sum conditions after \(M=(Q-sI)/(N-s)\). The centered and maximal
lower theorem and its maximal star kernel are those of
[UNIFORM_LAMBDA_ALL_ORDERS.md](UNIFORM_LAMBDA_ALL_ORDERS.md), not newly
proved here. The same capped factors can be used in the existing tensor
construction only under its stated density and endpoint hypotheses.

Every legal sequence of the stated length is covered by the proof;
the switched design need not retain any cyclic symmetry. We do not
enumerate the closure, count design isomorphism classes, or claim an
upper gap for unrestricted 13-point designs. The previous explicit
multiplicity-four closure allowed at most two moves; it now allows
three. The multiplicity-seven application uses the credited complement
bridge and the improved local bound.

The generic dense theorem [DENSE_SCHUR_CAP.md](DENSE_SCHUR_CAP.md) already
covers **every** simple multiplicity-seven 13-point design, with centered
cap \(3232/13\). Here \(238\) is smaller by \(138/13\) on the specified
five-move closure. This is a stronger numerical cap on that subclass,
not a newly capped multiplicity-seven factor family.

## Reproduction, finite scope and trust boundary

Use CPython **3.11.2**, standard library, assertions enabled. No solver,
floating-point eigensolver or external design corpus is required.
Keep native threads at one; the scripts themselves are single process.

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B verify_pasch_multiplicity.py --check
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B verify_pasch_multiplicity_literal.py --check
```

Run from this directory. The core is
[pasch_multiplicity.py](pasch_multiplicity.py); pinned outputs are
[pasch_multiplicity_expected.json](pasch_multiplicity_expected.json) and
[pasch_multiplicity_literal_expected.json](pasch_multiplicity_literal_expected.json).
The first checker verifies all 729 local directed matrices, all 16
inside Boolean patterns with feasible pair quotas at multiplicities one
through five, 4096
four-set controls on three outside points, the complete 762 base
complement identities, all ten shorter-depth comparisons, and all
572 legal neighbours of the fixed seed at both multiplicities four
and seven. It compares defects directly to tuple-link definitions and
checks reduced full-point norm forms with integer leading minors.
These bounded tests validate the identities; the universal conclusion
comes from the ordinary proof above.
Three additional literal moves test \(\mu=1,2,3\), including a Fano
complement with zero defect change, with six full-point Fraction PSD checks.
The sharpness witness adds all direct pair/replication checks, two singular
or positive norm-form Fraction checks and a negative quadratic control
against every smaller real budget.

The second checker supplies one noncyclic literal three-move matrix
and one noncyclic literal five-move matrix, with all definition-level
entries, incidence/complement identities, six-block and constant
equations, complete point-Gram identities, independent Fraction PSD
checks on small forms, and the full sparse-repair transfer.
Whole-slack positivity and ranks use the cited ordinary decomposition,
not a whole dense elimination. Hashes and exact counts are pinned in
the compact expected outputs. These are author-side checks, not an
independent reviewer verdict or a proof-assistant formalization.

The principal source remains Ellis--Filmus--Friedgut,
[Section 4, Conjectures H and I](https://arxiv.org/html/2609.28404v1#S4),
[version record](https://arxiv.org/abs/2609.28404). Its classical Chvátal
and projection statements do not supply the matrices required by H.
Pasch switches are attributed in the parent proof to the primary
Steiner-triple-system and Grannell--Lovegrove literature. The complement
defect identity and earlier joint Sylvester comparison are credited to
the existing source/graph result, not presented as new ideas.
