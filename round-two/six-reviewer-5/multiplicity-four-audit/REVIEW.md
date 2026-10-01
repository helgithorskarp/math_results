# Independent multiplicity-four audit with a repaired structure bridge

Actual reviewer: **six-reviewer-5, independent mathematical reviewer**, 2026-10-01.
The campaign uses a shared signing identity; independence here means this named
reviewer's own reductions and checkers, with no researcher proof module executed.

**Verdict.** The multiplicity-four exclusion in lemma 8783 is confirmed under
explicit reviewed finite-classification premises. I independently close its
structure premise 8716, including all six integer dual certificates, and its
shared-isolated-hub premises 8356, 8397 and 8438. One sentence in 8716's final
heavy-edge case is incorrect. The direct row-sum contradiction below repairs
that case and removes its paired-2111 completion premise entirely. The exclusion
also has a shorter equality proof that removes its 29-case scalar inventory.
These are complete ordinary/computer-assisted proofs within the stated premises,
with high confidence; the mathematical bridges have no proof-assistant formalization.

The theorem reviewed is this: a family of 71 five-subsets of 18 points, distinct
members meeting in at most two points, with replication multiset
\((16,19,20^{16})\), cannot have multiplicity four between its replication-16
and replication-19 points. **The multiplicity-five corollary additionally imports
the older exclusion of multiplicities zero through three in 8637. I do not
independently review that older chain here.** This verdict excludes the multiplicity-four case; a full profile exclusion needs
separate premises for the other hub multiplicities. No free-involution hypothesis
is used, and no new global upper bound is claimed.

Reader source: [this audit directory](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-reviewer-5/multiplicity-four-audit).
Run `python3 -B round-two/six-reviewer-5/multiplicity-four-audit/audit.py` and
`python3 -B round-two/six-reviewer-5/multiplicity-four-audit/local_pair.py` from
the repository root, with all numerical threads one. Repeat with `-O`.
The [README](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/multiplicity-four-audit/README.md)
and [validation record](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/multiplicity-four-audit/VALIDATION.json)
state exact results and provenance. The verified publication commit is recorded
separately in the graph contribution.

## Targets, scope and imported evidence

The complete committed bodies and relation neighborhoods were inspected at index
8942 and refreshed at 8964. No sufficient review of this full mechanism was present.
Earlier review 8885 independently proved the local charge obstruction but **imported
8783's global conclusion**; review 8933 independently covered the generic twenty-star
classification. Neither supplied the present structure/transfer verdict.

The main sources, all by **six-code-1, researcher**, are:

* Lemma 8783, `bafkreid2i2qb3r73s2vj2ymu3fhsmmqwdif5se2ku3ybvk6rvktenf4qnu`,
  [multiplicity-four exclusion](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-1/multiplicity_four_exclusion/PROOF.md),
  source `4161c69604a7fe30d3598cae9e9ca1bf33554748`.
* Lemma 8716, `bafkreiadksw3u4yf52baubny2st53gwlbbqfuifccyrdaqms3ryfcmusku`,
  [multiplicity-four structure](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-1/multiplicity_four_structure/PROOF.md),
  source `4983b8eca2f526f445be39cce7de0a41ef66836e`.
* Lemmas 8356, 8397 and 8438, respectively
  `bafkreiftuehz5sjq2xfcnptcxe3kgnlebt2uxwtnuocnif7cvej6d7744e`,
  `bafkreig3ciisnimaakp3xtfhbdjw74mhnyofioqpb7fuvupex4kx3feyky`,
  `bafkreidxvrcfr7vmvsldakldkluxqblqtzwnqrxdvu56m5sufdm62fjgly`:
  [mixed/mixed](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_18_6_5_equality_structure/COMMON_MIXED.md),
  [unit/unit](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_18_6_5_equality_structure/COMMON_UNIT.md),
  [mixed/unit](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_18_6_5_equality_structure/COMMON_MIXED_UNIT.md).
  Their original commits are, respectively,
  `efc8f0792caf5d05d745165c55d42d45c9945058`,
  `053622a2c8a24c2e83a6702e0d0648ede8031270`,
  `3ab925702e52e327e647d57254bfd72f6608b0e3`.

The mathematical imports retained are:

1. Reviewed universal twenty-star no-low-low-leave theorem 8323,
   `bafkreibz6cr3e3mjpadu4jjr5n3kzwlji4ijgzbto7mw66xoqtyaa37ohe`.
2. Generic twenty-star fixture coverage, independently established by review 8933,
   `bafkreic2wb2z6reycvrsrywbgjxdtjl5f7eqkbe2yk2xtco2su6tgn43aq`.
   Only coverage of 23 point-isomorphism classes is used, not its full groups,
   nor any involution completion conclusion of original 8720.
3. The positive-low-low nineteen-star classification, independently reviewed in
   8623, `bafkreigwxizlsmaqrzaha25uvkdymf2ae6g5iiblyflmx5rpyi4zz5vpoi`.
   Its 46 representatives with a low-low pair marked cover 44 unmarked classes;
   the leave has one or two disjoint low-low pairs. I inspect all replication-four
   hub markings without a symmetry quotient, rather than repeat a sufficient
   classification audit.

The unchanged nineteen-star manifest and the six integer duals are credited
inputs. The generic twenty-star fixtures are credited to six-code-2, from source
`69f2312bb468eb59b8ab3d8978fe19b3d86cf58a`. Every imported group is ignored.
The local checker extends **this reviewer's own** source
`e5f6f9cc00a7bd3b590d0469b392219fae05cfc0`. Its standalone local component,
not the whole verdict of review 8885, is reused and cold-replayed here. This
avoids the cycle that would result from importing 8885's global conclusion.

## Incidence identities derived independently

Write \(\lambda_{xy}\) for pair multiplicity and
\(\delta_{xy}=5-\lambda_{xy}\). Tails through a pair are disjoint triples,
so \(\lambda_{xy}\le5\). Assume \(\lambda_{uv}=4\), where
\(r_u=16,r_v=19\), and let \(S\) be the sixteen replication-20 points.
The deficit sums from \(u\) and \(v\) to \(S\) are 20 and 8, and the
sum over unordered \(SS\) pairs is 26. Let \(G\) be their positive-deficit
support and \(X=\sum_{SS}\max(\delta-1,0)\); then \(|E(G)|=26-X\).
Partition \(S\) into \(A,B,T,Z\), deficient only to \(u\), only to \(v\),
to both, or to neither. Let \(C\) be the 12 positions in the four common
\(uv\) tails, \(W=B\cup T\), \(p=|W|\le8\), \(k=|W\cap C|\),
\(c=|T\cap C|\), and \(z=|Z|\).

There are 106 uncovered triples. If \(N_0,N_1,N_2\) count them with zero,
one or two hubs, then \(N_2=4\). Summing their incidences at saturated points
and summing all triples gives \(3N_0+2N_1+N_2=256\) and
\(N_0+N_1+N_2=106\), hence **\(N_0=48\)**.
The no-low-low theorem forces at least two \(G\) edges in each such wholly
saturated triple. Let \(\tau\) count those with all three edges. They supply
\(48+2\tau\) high-high leave incidences.

At a saturated center with \(h\) deficient neighbors, its high-high leave
has \(h-1\) edges: each of its \(17-h\) replication-five neighbors has exactly
one leave edge, necessarily to a high neighbor. Summing \(h-1\) gives
\(2|E(G)|+|T|-z\). The other high-high contributions are the one-hub homogeneous
incidences \(H\), and \(|T\setminus C|\) uncovered hub pairs. Therefore

\[
R:=H+2\tau=4-z+c-2X.
\]

Also \(Z\subset C\): otherwise both hubs would be low and uncovered in a
\(Z\) center's twenty-star. Inspecting **all 76** covered pairs of high marks
in the 23 generic fixtures shows their hub-to-saturated high-leave cost is at
least two; the cost histogram is \(2:64,3:8,4:4\). Thus each covered \(T\)
center costs at least two units, and \(2X+z+c\le4\).
This independently establishes exactly the part of incidence lemma 8497 needed
here; no verdict on its other conclusions is transferred.

At \(X=0\), a single-hub center with zero homogeneous charge is good. Its
hub is isolated in the high leave, and its internal degree \(g\) obeys
\(g\le\binom g2\), with \(g\le4\). Consequently \(g\in\{0,3,4\}\).
Its nonzero row is unit with isolated unit hub, or mixed \((2,1,1,1)\) with
isolated deficit-two hub.

## Independent shared-hub and local-charge proofs

[iso_pairs.py](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/multiplicity-four-audit/iso_pairs.py)
inspects every literal generic fixture. There are seven raw \((\text{fixture},u,y)\)
isolated-hub markings: three from mixed fixture 9 and four from unit fixture 17.
All **49 ordered pairs** are retained: 9 mixed/mixed, 16 unit/unit and 24 mixed/unit,
including both orders. The common-center multiplicity is four. Fix the common
hub, match its common tail in two ways, then the remaining three tails in
\(3!\,6^3\) ways and the four residual points in \(4!\) ways. This gives
**62,208 full relative maps per case**, or **3,048,192** in total.

Only an actual triple in a private second-star block mapping into a private
first-star word prunes a branch. Each pruned prefix is weighted by the exact
number of its remaining bijections. The complete disjoint prefix domains sum
to the full carrier, with no accepted map. This proves precisely the quantified
local conclusions of 8356, 8397 and 8438; no total code size, hub replication,
ambient automorphism, supplied group or author pair certificate is assumed.
The new calculation has **129,759 visited prefixes**, maximum 3,135 per case.

[local_pair.py](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/multiplicity-four-audit/local_pair.py)
cold-replays the standalone earlier charge lemma over **448 raw cases** and
**6,967,296 full maps**. If a good single-hub center \(x\) is joined at
multiplicity four to a covered \(T\) center \(y\) with unit \(v\) deficit,
\(\lambda_{xv}=5\), \(uxy,uvy\) covered and \(vxy\) uncovered, and all
other positive deficits at \(y\) are one, then the number \(e_u\) of
\(uS\) high-leave edges at \(y\) is at least **two**. The checker covers
both \(e_u=0\) and \(e_u=1\); it uses 14 first and 32 second raw markings,
with no orbit or transitivity reduction. There are 413,196 visited prefixes,
maximum 1,611 per case. The earlier complete stream digest is unchanged:
`c2fa107a505b44e21f83e99415a4dde3af4d3061b1e735554eb4e4250b619dbb`.

Every actual positive map is recovered for the known 35-word joint packing
(two degree-20 centers, multiplicity five), with 144 compatible maps. Removing
one common word gives a 34-word control with degree-19 centers and multiplicity
four; the isolated-pair carrier recovers its known map among 48 compatible maps.
Neither control satisfies the forbidden local hypotheses. Zero-state and
out-of-contract guards are rejected. Incomplete runs supply no exclusion.

## Closing 8716: low-low branch and exact duals

If the nineteen-word \(v\) link has a low-low leave, the reviewed census applies.
The direct cell/subset decoder and an independent injection decoder agree on all
representatives. I retain **all 388** replication-four marks for \(u\), including
duplicates: \(33\cdot9+13\cdot7\). All endpoints of its low-low matching lie
in \(C\). For \(y\in W\), let \(q_y\) count its low friends in \(C\).
Each forces an internal positive deficit and a homogeneous \(v\) incidence at
\(y\). Their compulsory cost, combined without double counting with the covered
\(T\) cost, is

\[
Q(T_C)=\sum_{y\in W}\max(q_y,2\mathbf1_{y\in T_C}).
\]

All subsets \(T_C\subset W\cap C\), \(X\in\{0,1,2\}\), and
\(z\in\{0,\ldots,4\}\) satisfying \(2X+z+|T_C|\le4\) are checked:
**32,578 inventories**. \(Q\le R\) eliminates every \(X>0\) case.
If the leave matching has \(\mu\) edges, at most \(z\) meet \(Z\);
all others would join two good \(A\) points unless an endpoint is charged.
The independent shared-hub proof forbids that pair. Hence
\(H_A\ge\max(0,\mu-z)\).

Exactly **62** inventories satisfy \(Q+\max(0,\mu-z)\le R\), all with
\(\mu=1,X=0,z\in\{0,1\}\) and \(R-Q=1-z\). Thus there is a single
exceptional low point \(e\), an endpoint of that matching: it is the charged
\(A\) point when \(z=0\), or the \(Z\) point when \(z=1\). Every other
low point is good \(A\). Every forced friend avoids both matching endpoints,
because a low point has only one leave edge.

Applying \(e_u\ge2\) to each unit-\(v\) covered \(T\) center having a forced
friend strengthens its cost to \(q_y+2\). For heavy-\(v\) centers retain the
old bound. **Exactly six inventories survive**, all with \(T_C=\varnothing\),
\(p=8,k=7\), unit \(v\) deficits, matching \(\{15,16\}\) and three
\(q_y=1\) values. Their raw carrier identifiers are
\((0,17,14),(0,19,1),(1,11,7)\), each with \(z=0,1\).
For comparison, the author's weaker shared-hub screen leaves 40 cases. Both
original 62/40 streams and all eleven readout buckets match entrywise.

Retain both choices \(e\in\{15,16\}\). Put \(L=\mathrm{low}\setminus\{e\}\)
and \(K=(W\cap C)\setminus\operatorname{supp}q\). These are good \(A\) and
\(B\) cohorts, respectively, so internal pairs in either cohort have multiplicity
five; \(\lambda_{ux}=5\) on \(K\). A degree-zero good \(A\) point would
force \(u\) deficient to all \(S\), by the no-low-low theorem at other
centers, giving \(T=W,c=k=7\), impossible. Hence
\(3\le\lambda_{ux}\le4\) for \(x\in L\).
If \(e\) is charged \(A\), its matching mate is good and their \(u\)
triple is covered; its charge therefore requires another internal neighbor.
Thus \(\lambda_{ue}\ge2\); if \(e\in Z\), it is five.

There is one \(W\) point outside \(C\). If it is \(T\) and has \(q=1\),
its internal degree is positive, giving \(\lambda_{uy}\ge2\). If \(q=0\),
it has no homogeneous charge; its high leave consists of the uncovered hub pair
and internal edges, giving internal degree zero or three. Degree zero would give
\(\lambda_{uy}=1\); the seven \(B\) points in \(W\cap C\) would all
have to occur in that single word's three-point tail, a contradiction. Therefore
\(\lambda_{uy}\ge4\) in this case. \(B\) instead gives five.
Every pair \(xy\) touching \(L\) satisfies
\(\lambda_{xy}+\mathbf1_{uxy\text{ covered}}\ge5\). Every uncovered
\(v\)-link pair touching a low point has multiplicity four.
These prove the exact row meanings used by the integer certificates. All covered
\(W\) points are now \(B\); the certificates' weaker lower-three rows there
remain sound, and none of those rows has positive weight in the six duals.

I inspect all \(\binom{18}{5}=8,568\) five-subsets, retaining exactly the
**1,219** words avoiding \(v\) and meeting every fixed quadruple in at most two
points. This is the entire additional-word universe, without a symmetry quotient
or necessary-row filter. Each positive integer multiplier is validated against
its literal row descriptor and fixed-star incidences. Negative coefficients and
negative right sides are kept with their correct signs.

The independent column evaluation aggregates multipliers by one-, two- and
three-point subsets, then sums the 25 contained subsets of each candidate;
it does not import the author's row factory or evaluate its matrix.
With scale \(D=100,000\), every column dominates \(D\), while:

| Carrier; exception | Weighted rows | Minimum column | Weighted right side |
|---|---:|---:|---:|
|0/17/14; 15|437|100002|5193506|
|0/17/14; 16|435|100002|5194350|
|0/19/1; 15|186|100000|5160000|
|0/19/1; 16|186|100000|5160000|
|1/11/7; 15|424|100003|5185551|
|1/11/7; 16|428|100000|5189281|

For nonnegative completion variables, weak duality gives
\(D\sum_w x_w\le\sum_i a_i b_i<52D\). An actual size-71 code requires
52 additional words and is therefore impossible in every case. This proves
**\(\mu=0\)**. The duals are existing author-discovered weights, not new
optimizations; integer arithmetic and full column domination provide the proof.

## Closing 8716: internal excess and the repaired last placement

This branch concerns an arbitrary nineteen-star without a low-low leave and
does not extrapolate the positive-\(\mu\) census. The \(v\)-link degree counts
give \(6+k\) leave edges within \(W\). Counting blocks by their number of
\(W\) points gives
\(6+k\le\binom p2\) and \(5p+k\le21+\binom p2\).
Every one of the \(12-k\) low points in \(C\) has a distinct forced incidence
at a \(W\) center. Combining this with \(R\) and the two-charge bound leaves
exactly
\((X,z,c,p,k,R)=(1,0,2,8,8,4)\) when \(X>0\).

All eight \(W\) deficits at \(v\) are one. The two covered \(T\) centers
already cost all four units, so each has exactly two forced \(v\) incidences
and no \(u\) incidence, every \(A\) center has zero charge, and the four low
friends are distinct. All friends are in \(A\); both \(T\) centers are in \(W\).
There is a single internal deficit-two edge.

Unless that heavy edge joins both \(T\) centers, a \(T\) center and one of
its friends both avoid its endpoints. This follows from the two disjoint friend
pairs; all **119** other heavy-edge positions are also checked literally. Their
unit internal edge joins two allowed isolated-\(u\) rows, contradicting the
49-case local proof.

**Correction:** 8716's remaining-placement paragraph says that a forced low friend
can be the deficit-two \(T\) partner. That is impossible: the partner is in
\(W\), not the low set. In that placement a \(T\) center has distinct deficient
neighbors \(u,v\), the other \(T\) center, and its two low friends. Their
minimum deficits are

\[
1+1+2+1+1=6>5,
\]

contradicting the saturated row sum directly. Thus **\(X=0\)**. The published
paired-2111 upper-66 input 8232, and its review 8295, are unnecessary for this
independent proof; no result about them is inferred. The original theorem's
conclusion is confirmed with this corrected bridge, rather than accepting that
sentence as written.

## Closing 8783 without the scalar census

Now \(\mu=X=0\), \(|E(G)|=26\), and \(R=4-z+c\). Let \(q_y\) count
low friends in \(C\) at \(y\in W\). There are \(q=12-k\) distinct friends,
all in \(A\cup Z\). At most \(z+H_A\) are nongood; let \(n_y\) count
them at \(y\).

A covered \(T\) center with unit \(v\) deficit and a good friend costs at
least \(q_y+2\), by the standalone local charge theorem. With no good friend,
the older two-charge and forced-charge bounds give at least
\(q_y+2-n_y=2\). For a heavy-\(v\) center, drop the two extra units; there
are at most \(8-p\) such centers. Adding \(H_A\) and using
\(\sum n_y\le z+H_A\) proves the author's strengthened inequality

\[
R\ge12-k+2c-z-2(8-p),\qquad k\ge2p+c-8.
\]

Separately \(R\ge q\) gives \(k+c\ge8+z\). Now use only \(k\le p\):

\[
p+c\le8,\qquad 8+z\le k+c\le p+c\le8.
\]

Therefore **\(z=0,k=p,p+c=8\)**. This proves the equality reduction without
any high-core block inequalities, degree-capacity screen, nineteen-star census
or 29-case scalar enumeration at this final stage. It follows that
\(R=q\), \(H_A=0\), and all \(A\) points are good and independent by the
shared-hub proof.

A degree-zero \(A\) point has \(\lambda_{ux}=0\), and multiplicity five to
all other saturated points. Every \(uxy\) is uncovered; applying no-low-low
at \(y\) forces all sixteen \(uS\) deficits positive. Their sum is 20 and
one is five, so all the others are one. The other \(A\) degrees are four.
Since \(|A|=16-p\ge8\), its total degree would be
\(4(|A|-1)\ge28>26\), contrary to independence. Hence every \(A\)
degree is at least three. Independence gives
\(3(16-p)\le D_A\le26\), forcing \(p=8\). Then \(c=0\),
\(W\subset C\), and \(T=\varnothing\). The eight \(A\) points carry
all 20 \(uS\) deficit units, so
\(D_A=5\cdot8-20=20\), contradicting \(D_A\ge24\).
This independently proves the complete multiplicity-four exclusion.

## Strengthening and improvement opportunities

**Proved here:** the shared-hub premises have a single raw 49-case, group-free
proof; the positive-low-low structure screen shrinks 40 inventories to six
with \(T_C=\varnothing\); the heavy-\(T/T\) row-sum repair eliminates the
paired-2111 completion dependency; and the final charge proof replaces the
29-case scalar screen by equality and two degree contradictions. The latter
removes a finite verification layer, rather than changing the numerical bound.
The local obstruction also excludes both zero and one \(u\) incidence, beyond
the isolated statement of 8783's new one-incidence lemma; that stronger local
component already appeared in this reviewer's earlier work and is credited.

Within this reviewed chain, the next case is multiplicity five in this profile.
During the final source refresh, six-code-1 published an author-checked
[uniform two-unsaturated tail theorem](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-1/two_unsaturated_tail_structure/PROOF.md),
source `7b27b9c58b3e218172eaf9b1c0986d48e706e29b`, asserting an upper-four hub
multiplicity. Its new M/S local exclusions and equality transfer receive **no
verdict here**. Auditing that theorem would be a consequential next step: if its
upper-four result and the older lower-four chain both hold, the present
multiplicity-four exclusion eliminates the entire 16/19 profile. This is a
conditional composition opportunity, not a verified whole-profile result.
The present equality mechanism depends on the specific deficit sums 20 and 8,
26 internal edges, and budget 4. A broader profile theorem would require new
budget constants and local marked-star hypotheses; this review proves none.
For publication, replace the erroneous heavy-placement sentence, expose the
shorter equality proof, and keep the older zero-through-three premise visibly
separate. Formalization of the finite carrier accounting, row semantics and
charge identities would reduce the remaining ordinary-proof trust boundary.

## Reproducibility, literature and limitations

CPython 3.11.2, standard library, exact sets and integers. No LP solver executes;
no researcher proof code, author symmetry group or same-author execution seal
is a trusted computational input. The compact bundle includes literal manifests,
credited 53,682-byte integer duals, source and summaries; it omits full map lists,
matrices and generated packing corpora. [INPUTS.json](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/multiplicity-four-audit/INPUTS.json)
binds every mathematical data file to its original source and bytes.

The main independent record has SHA256
`b841641fe298f00ae24f9759de6b3972416063dabab058af67e0edf3b4b65e0e`.
Normal and optimized runs agree, as do the earlier local runs. Thirteen damaged
dual controls reject negative/noninteger weights, invalid domains/descriptors,
missing/duplicated cases or rows, insufficient column coverage and a correctly
column-covering bound equal to 52. Two literal positive carrier controls and
three guard controls pass. No timeout, UNKNOWN, resource kill or unfinished
enumeration is treated as a proof. Per local case the fixed limits remain
200,000 states and ten seconds; the main audit has a fixed 60-second guard.
One computational job runs at a time and all solver/BLAS/OpenMP threads are one.

Candidate-specific literature searches on 2026-10-01 used the exact code
parameters with “multiplicity”, “71 replication 16 19”, and “isolated hub”.
They did not settle historical priority of these restricted transfer results.
The established 69 construction remains credited to
[Aw--Chee--Ling 2003](https://ymchee66.github.io/home/PDF/6cwc.pdf),
and the point cap comes from [Brouwer's 1975 report](https://ir.cwi.nl/pub/6883/6883D.pdf).
The live [primary bounds table](https://aeb.win.tue.nl/codes/Andw.html) reports
69--72; the campaign's reviewed upper 71 is separate prior work. This audit
changes neither bound. Standard weak duality and the old templates are method
and prior art, not novel constructions. Historical priority remains unassessed.

A bibliographic correction to this reviewer's previous generic-census graph
body: `bafkreigsaibox67ch5nagmc6cm225eg7sxfqfvmlcuot75cbi55vvtvwhi` is the
marked-unit contribution **8350**, not 8438. The previous carrier credit,
directed relation and mathematics were unaffected. The actual mixed/unit
8438 reference is stated correctly above.
