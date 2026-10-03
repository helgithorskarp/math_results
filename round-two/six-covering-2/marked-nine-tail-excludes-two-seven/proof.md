# Exactly nine productive tails: the (2,7) allocation is impossible

Actual author **six-covering-2**, role **researcher**, 2026-10-03.
This is an author-checked ordinary conditional proof, with separate same-author
arithmetic audits. Person-independent review is pending; the ordinary bridges
are unformalized. [README.md](README.md) gives source-only reproduction commands
and the exact resource guards. [expected.json](expected.json) gives compact
full-record pins and the complete census.

## Literal theorem domain and dependencies

Consider a finite covering of all integers by congruences with pairwise distinct
**original** moduli, each dividing 10080, minimum **exactly eight**, containing

\[
8:0,\quad 9:0,\quad 10:1,\quad 14:0,\quad 12:10,
\quad 16:2,\quad 28:4,\quad 32:6.
\]

Here `m:a` is residue `a` modulo the original modulus `m`. The placed classes
16:2 and 32:6 are explicitly essential: deleting either destroys the cover.
Every other original label, phase, selection and omission is free. Selected
unproductive tails are allowed. The actual LCM may be a proper divisor of
10080. No additional selected modulus or global normalization is assumed.

BASE consists of selected original moduli dividing 2520; let
\(B\subseteq\mathbb Z/2520\) be its **actual** uncovered set. Other originals
are TAILs of the form \(16d\) or \(32d\), with \(d\mid315\). A selected TAIL
is productive if it meets a physical lift \(x+2520k\), for \(x\in B\) and
\(k=0,1,2,3\). Assume exactly nine productive TAILs, with counts **(2,7)**
in the actual nonempty BASE-hole parents 2 and 6 modulo 8. There are no actual
holes in other parents. We prove this allocation impossible.

The imported [BASE177 lemma, graph 9934](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-2/marked-seven-productive-tails/proof.md)
gives \(|B|\ge177\). The imported
[productive-nine lemma, 10022](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-2/marked-nine-productive-tails/proof.md)
applies to this domain, with its preceding dependencies and explicit hypotheses.
Deleting a redundant productive extra TAIL preserves the prefix, actual BASE
holes, essentiality of the placed 16/32 classes and the covering. It leaves
eight productive TAILs, contradicting 10022. Thus every productive extra is
essential. This argument does not prohibit an unproductive selected class.

Only the final classification consequence uses the
[two-parent classification, 10054](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-2/marked-nine-tail-two-parents/proof.md)
and [six/three exclusion, 10099](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-2/marked-nine-tail-excludes-six-three/proof.md).
The core (2,7) calculation imports no numerical triple-126 or six/three census.
Predecessor [review 10066](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/nine-tail-audit/REVIEW.md)
and [review 10093/5](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/two-parent-audit/REVIEW.md)
apply in their stated relative scopes. They do not review this new proof or
permit transferring weakened hypotheses to it. Their exact source commits and
canonical references, and those of the imported lemmas, are recorded in
`expected.json`.

## The lone parent-2 extra is original 48

Let \(P=(8:0,9:0,10:1,14:0,12:10,28:4)\) be the six placed BASE classes,
and define

\[
R=\{x\in[0,2520):x\text{ is uncovered by }P\},\qquad
R_p=\{x\in R:x\equiv p\pmod8\}.
\]

Fresh literal enumeration gives \(|R|=1396\) and \(|R_2|=|R_6|=150\).
Actual holes have only parents 2/6, so \(B_p\subseteq R_p\), hence
\(|B_2|\ge27\). Essential 16:2 and 32:6 are productive in parents 2 and 6,
respectively, so parent 2 has precisely one productive extra TAIL.

For each \(x\in R_2\), its four lifts occupy quarters 2,10,18,26 modulo 32.
Placed 16:2 fills quarters 2/18. One additional Q32d fills only one quarter
and cannot repair a hole. An H16d in the already filled half is redundant.
Therefore the extra is an H16d in half 10 modulo 16, and \(B_2\) lies in its
one odd column \(x\equiv a\pmod d\).

Write \(D=(3,5,7,9,15,21,35,45,63,105,315)\). The fresh maximum column
populations on \(R_2\) are:

| cofactor d | 3 | 5 | 7 | 9 | 15 | 21 | 35 | 45 | 63 | 105 | 315 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| maximum | 90 | 30 | 25 | 30 | 18 | 15 | 5 | 6 | 5 | 3 | 1 |

Thus \(d\in\{3,5,9\}\). The code records every original H16d phase in the
opposite half, not only the maximum.

For d=5 or 9, dominate the actual hole set by

\[
S=R_6\cup\{x\in R_2:x\equiv a\pmod d\}.
\]

If \(s=|S|<177\), capacity excludes it. Otherwise selected BASE classes cover
at most \(s-177\) points inside S. For every unused original BASE modulus m
and every phase b, record

\[
i_m(b)=|S\cap(b\bmod m)|,\qquad
o_m(b)=|(R\setminus S)\cap(b\bmod m)|.
\]

Every point outside S must be BASE-covered because \(B\subseteq S\). The
sum, over originals, of the largest \(o_m(b)\) with \(i_m(b)\le s-177\)
bounds that outside coverage; omission contributes zero. All 35 unused BASE
originals, all 9251 phases and every omission remain available.

All five d=5 columns have s=180, outside requirement 1216 and coverage bound
1156, a deficit of 60. For d=9, odd phases 0/1/4/7 have s=150. Phases 2/5/8
have s=180 and bound 1155, deficit 61; phases 3/6 have bound 1164, deficit 52.
All d=5/9 columns are excluded. The bitmask producer and literal histogram
audit compare all **92510** shadow phase entries and all **370040** raw bytes.
No transport of a mirrored numerical result is assumed.

Original 48 is therefore spent in parent 2. Its opposite-half phases
48:10, 48:26, 48:42 have repair populations 0,90,60. Phase 10 is unproductive;
only phases 26 and 42 remain.

## All six-extra parent-6 inventories

Parent 6 has placed 32:6 and six productive extras. Extra H cofactors lie in
\(D\setminus\{3\}\), because original 48 is spent. Extra Q cofactors lie
in D; in particular original Q96 is still available. Cross-type equal odd
cofactors are legal: H16d and Q32d are different original labels. Original 16
and 32 cannot be selected again; no original label is reused.

The parent-6 quarters are 6,14,22,30 modulo 32. Extra H classes have orientation
A=14, filling 14/30, or B=6, filling 6/22. A Q in quarter 6 lies inside placed
32:6 and is redundant, so is not a productive extra at the minimum-nine count.
The remaining Q quarters are 14,30,22. Write their odd-row unions as
\(Q_a,Q_b,Q_B\), and the H unions as \(H_A,H_B\). To repair all missing
quarters, the actual support must lie in

\[
S_6=\bigl(H_A\cup(Q_a\cap Q_b)\bigr)\cap(H_B\cup Q_B).
\]

Moreover \(Q_B\ne\varnothing\). Otherwise H_B must fill quarter 22 at every
actual parent-6 hole, and those same H classes fill quarter 6 as well. BASE
already covers points outside actual holes. Placed 32:6 would be redundant,
contrary to its explicit essentiality. This is an original-space argument
about the actual holes, not a conclusion from merely selecting a Q label.

For any odd-row group G, let U(G) be the minimum sum of exact singleton and
pair union maxima over all partitions into blocks of size one or two, capped
at 150. Every raw phase pair for distinct cofactors in D is checked. The audit
computes the same upper bound through maximum matching savings instead of
minimum partition costs. With C(d) the maximum single-column population,

\[
|Q_a\cap Q_b|\le
\min\left(U(Q_a),U(Q_b),\sum_{a\in Q_a,b\in Q_b}
 C(\operatorname{lcm}(a,b))\right).
\]

For every original inventory, enumerate all H splits and nonempty choices of
Q_B, and maximize the support bound. The numerical Q opposite-arm split is
also maximized completely. Swapping those two arms for this maximum loses no
case; no actual original phase is quotient-normalized.

All **54264** inventories and **2958450** cuts are checked:

| extra H | extra Q | inventories | support upper | inventories with upper ≥87 |
|---:|---:|---:|---:|---:|
| 0 | 6 | 462 | 50 | 0 |
| 1 | 5 | 4620 | 70 | 0 |
| 2 | 4 | 14850 | 78 | 0 |
| 3 | 3 | 19800 | 90 | 5 |
| 4 | 2 | 11550 | 94 | 20 |
| 5 | 1 | 2772 | 94 | 21 |
| 6 | 0 | 210 | excluded by essential32 | 0 |

Uniform parent-6 capacity is at most 94. If parent 2 uses 48:42, its capacity
is at most 60, requiring at least 117 holes in parent 6, impossible. Thus the
phase is 48:26, giving capacity at most 90. Parent 6 now needs at least 87;
precisely **46** inventories survive the coarse bounds. All others have
capacity at most 86.

## Coupled modulo-3 branches and coordinate slices

The literal residual R6 is the disjoint union of the complete CRT products

\[
\begin{aligned}
R_6\cap\{x\equiv0\pmod3\}
 &\cong \{3,6\}_{9}\times\{0,1,2,3,4\}_{5}\times\{1,2,3,4,5,6\}_{7},\\
R_6\cap\{x\equiv2\pmod3\}
 &\cong \{2,5,8\}_{9}\times\{0,1,2,3,4\}_{5}\times\{1,2,3,4,5,6\}_{7}.
\end{aligned}
\]

The fixed binary coordinate is 6 modulo 8. The products have 60 and 90 cells;
the mod-3 branch 1 is absent. The producer checks every literal residual point
and coordinate. The separate audit constructs every product point by CRT and
checks its union equals the whole original residual parent.

Each productive cofactor divisible by 3 has one actual mod-3 phase branch,
0 or 2. Both choices remain, independently for each original H/Q label.
On an active branch, the row fixes coordinate 9 if 9 divides d, coordinate 5
if 5 divides d, and coordinate 7 if 7 divides d. Cofactor 3 is the whole
branch. A row fixing several coordinates is contained in a whole slice for
**any one** of those coordinates.

For side lengths \(n=(2,5,6)\) or \((3,5,6)\), assign each row to one
coordinate it fixes. With \(k_j\) rows assigned to coordinate j, their union
is contained in at most \(k_j\) slices there. Consequently

\[
V(G)=\min_{\text{allowed row-to-coordinate assignments}}
\left[\prod_jn_j-\prod_j\max(n_j-k_j,0)\right]
\]

is a valid upper bound. Every assignment is valid for **all phases**, so the
minimum is valid. Repeated cofactors remain repeated rows. Coincident slices,
empty congruences or incompatible original phases only decrease actual union
size. The separate audit computes all reachable slice-count vectors by
dynamic programming, rather than importing the producer's assignment walk.

Within each branch, \(Q_a\cap Q_b\) is a union of pair intersections. Each
intersection is empty or one odd row of cofactor lcm(a,b). Apply V to the
**multiset** of active H_A rows and **all** active Q-arm pair LCM rows, and
separately to active H_B and Q_B rows. Take their minimum in that branch,
add the two branch bounds, and cap by the coarse bound. Allowing independent
coordinate phases in the two branches enlarges support and is safe. Cross-type
equal cofactors and repeated projected LCM rows remain intact.

The 46 inventories have **5976** physical H/Q role assignments. Every role
with coarse bound at least 87 is expanded through every mod-3 branch choice:
**1464** coupled cases. Each expanded case has support at most **80**. Roles
already pruned by their coarse bound have maximum **84**. The 46 inventories
therefore have uniform capacity at most 84. All other inventories have capacity
at most 86, giving

\[
|B|=|B_2|+|B_6|\le90+86=176<177.
\]

This proves the entire (2,7) allocation impossible in the stated domain.
The reduction includes all original inventories and phases through rigorous
upper bounds. A timeout or incomplete search is not used as nonexistence.

As an additional physical check, two kernels compare **3738** H/Q phase rows,
**2242800** physical membership checks and **560700** raw mask bytes. One
tests the four literal lifts per point; the other walks each original AP modulo
10080. They share only the argument driver and record schema. This check
supports the written elementary CRT and essentiality arguments; it does not
replace them.

## Exact evidence and remaining scope

The seven arithmetic source files rebuild all four entire mathematical records
and both raw streams with standard-library exact integers, sets and bitmasks.
There is no solver, CAS, old phase census or external large-corpus input.
`reproduce.py` first runs the producers and separate audits serially, then
`controls.py` validates typed complete reconstruction and damaged evidence,
then checks the reproducibility pins and complete census in `expected.json`.
All generated data remain outside the publication directory.

The 39 negative controls include altered literal hypotheses, omission freedoms,
original-label availability, essentiality, dropped inventories/quarter roles,
changed mod-3 branches, collapsed repeated LCM rows, numeric type confusion,
duplicate/unknown JSON keys and rehashed raw damage. Six positive controls
retain all four whole records, both raw streams, legal cross-type equal
cofactors, Q96 availability, unproductive selected tails, proper-divisor LCMs
and repeated projected rows. Comparison is with fresh independent arithmetic
reconstruction, not only a stored hash. These controls are interface checks,
not a third arithmetic kernel or a person-independent review.

Combining this exclusion with 10054 and 10099 leaves exactly the three
**OPEN** allocations **(3,6), (4,5), (5,4)**. No tenth-tail bound, whole-prefix
exclusion, construction, native-root cut or global improvement of
\(L_{\min}(8)\) is claimed. Applying this conditional lemma in a native search
requires a separate actual-hole, essentiality and exact-count bridge. The
existing native search remains incomplete.

[Zhang and Zhang, 2607.19029](https://arxiv.org/html/2607.19029), reporting the
minimum-seven value 10080, is prior art; its Gurobi exclusions are not
independently recertified here.
[Harrington, Klein, Lowrance and Trifonov, 2605.18644](https://arxiv.org/html/2605.18644)
concerns the restricted 2/3/5 family and does not establish global minimum-eight
optimality. No novelty is claimed for the elementary slice bound or any
already published theorem.
