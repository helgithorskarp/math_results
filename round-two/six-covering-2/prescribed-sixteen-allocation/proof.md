# Two-layer allocation after prescribing sixteen

Actual author: **six-covering-2**, role **researcher**. Status: written,
unformalized combinatorial proof with exact author controls.
No outside review verdict is asserted.

The equal-resource two-layer argument is credited to **six-covering-3,
researcher**, published [Lemma 2 at graph 9160](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-3/eraser-matching/proof.md),
source b91d0ab7880d4c8065c41a6107f9a63086a7ae86, first communicated in
campaign message1319 on 2026-10-01. The contribution here is its
unequal-resource version and the explicit conditioning on an ORIGINAL16 class
at our two open children. Its full committed body and source proof were read before this publication.
The unequal-resource counting argument is written out below; no numerical
certificate from that source is imported.

## Two remaining binary levels

Let M be odd. There are T initially nonempty, labelled cofactor sets V_i
in Z/MZ. At the first remaining level, there is at most one congruence
for each label d in a divisor set D_1. Each resource acts on ONE initial
fibre, removing ONE residue class modulo d. Each remaining nonempty set is
then duplicated into two final children. At the final level there is at
most one resource for each d in a possibly different divisor set D_2; each
resource acts on ONE final child. Resources may be omitted. Put k_i=|D_i|.

The single-eraser graph has fibre vertices i and label vertices in
D_1 union D_2. Edge (i,d) exists exactly when the ORIGINAL V_i is contained
in one residue class modulo d. Let (C,B) be any vertex cover, meaning that
every edge meets the fibre set C or label set B. Put B_i=B intersect D_i.

**Lemma.** Every complete two-level allocation satisfies

\[
 4|C|+2|B_1|+|B_2|\ \geq\ 4T-2k_1-k_2.                 \tag{1}
\]

Equality is permitted. A strict deficit excludes completion.

**Proof.** Let e initial fibres be erased at the first level. Every erased
fibre receiving only one resource is either in C or uses a label in B_1.
At most |C|+|B_1| erased fibres received only one resource: each label can
be used at most once. Every other erased fibre received at least two.
At least 2e-|C|-|B_1| first-level resources were spent on erased fibres.

Let s be the number of nonempty survivors CHANGED by the first-level
choices. Each received at least one additional resource. Thus

\[
 s\leq k_1-2e+|C|+|B_1|.                               \tag{2}
\]

There are 2(T-e) nonempty final children. A final child covered by a
single resource is either descended from a fibre in C, descended from
one of the s changed survivors, or uses a label in B_2. An unchanged
survivor outside C still obeys the ORIGINAL eraser graph. At most
2|C|+2s+|B_2| final children receive only one resource. Every other final
child needs at least two, giving

\[
 k_2\geq 4(T-e)-2|C|-2s-|B_2|.
\]

Substitute (2) and simplify to obtain (1). Double counting a changed
fibre in C only weakens the bound. Redundant chosen classes consume
resources without contributing changes or erasures. Overlaps, omissions
and arbitrary cofactor phases are allowed. QED.

For D_1=D_2=D and k_1=k_2=k, (1) becomes the credited equal-resource cut
4|C|+3|B| >=4T-3k. That special case is not our own discovery.

## Application after all core phases at period 10080

Let F consist of 8:0,9:0,10:1,14:0,12:4. Our published first-root
reduction establishes that every divisor 10080 completion of F has
ORIGINAL16 present, and reduces its phase to a=2 or a=4. Neither child
is excluded here.

FIX that phase and choose all 36 still free ORIGINAL core phases, where
a core modulus divides 2520 and is at least 8. Together with the five
fixed classes, this uses 41 core resources, one phase per original label.
Omitted core moduli may be adjoined with arbitrary phases.

Under CRT write a point as

\[
 (b+8j\pmod{32},z\pmod{315}),\qquad 0\leq b<8,\ 0\leq j<4.
\]

The core choices leave a set H_b of cofactor holes, identical in all four
high binary copies. H_0 is empty because8:0 is fixed. Let m be the number
of nonempty parents and b_*=a mod8. The prescribed16:a erases one of the
two initial copies of H_{b_*}, if that parent is nonempty. Otherwise it
is wasted. Put e_0=1 or0 accordingly. The remaining tail resources are

\[
 D_1=\operatorname{Div}(315)\setminus\{1\},\quad k_1=11,
 \qquad D_2=\operatorname{Div}(315),\quad k_2=12.
\]

These are ORIGINAL moduli16d and32d, rather than virtual copies of a
single modulus. The initial child count is T=2m-e_0.

For each nonempty H_b, define g_b to be the gcd of315 and all differences
of its elements. For a singleton use g_b=315. A label d|315 is a single
eraser exactly when d|g_b. For any NONEMPTY set I of nonempty parents put

\[
 B_I=\bigcup_{b\in I}\operatorname{Div}(g_b).
\]

Take C to contain all remaining initial children of parents outside I,
and B=B_I. This is a vertex cover. Since1 belongs to B_I,

\[
 |C|=2(m-|I|)-e_0\mathbf1_{b_*\notin I},\quad
 |B_1|=|B_I|-1,\quad |B_2|=|B_I|.
\]

Substitution in (1) gives

\[
 \boxed{\quad 8|I|-3|B_I|\leq32+4\mathbf1_{b_*\in I}.\quad} \tag{3}
\]

If b_* belongs to I it is nonempty, so e_0=1. Outside I, the prescribed
class either erased an outside initial child or was wasted; both cases
give32. The empty I case is not used in this formula.

Six nonempty UNMARKED parents therefore need at least six collective
eraser labels. With16 free the bound is instead8|I|-3|B_I|<=36, requiring
only four collective labels. This refinement retains information about
the already chosen16 phase.

The condition applies AFTER all core phases are selected. It is a
necessary restriction, not a terminal exclusion at the five-class root
or either six-class child before those choices.

## A genuine positive fixture and a strict conditioned obstruction

Take the artificial demand R of 48 points modulo10080 defined by

\[
 b\in\{1,3,4,5,6,7\},\quad z\in\{2,17\},\quad j\in\{0,1,2,3\}.
\]

The marked parent2 is empty. Every point of R is literally uncovered by F.
No realization of R by the 36 free core
phases is asserted. This fixture is neither a covering of all integers
nor a construction bound for L_min(8).

Every nonempty parent has g_b=15 and eraser labels B={1,3,5,15}.
With16 free, there are12 resources at both levels, T=12, and the
C=empty cut is equality12>=12. The 24 ORIGINAL classes printed by
controls.py explicitly cover every point of R; the16 phase is1.
The checker constructs their phases by CRT and then independently scans
the literal predicates x mod n=a at all 48 demand points. The moduli are
distinct, at least 8, and divisors of10080.

Prescribed16:2 meets no point of R, leaving11 first-level and12 final
resources. For the same vertex cover,

\[
 2|B\cap D_1|+|B\cap D_2|=2\cdot3+4=10
  <4\cdot12-2\cdot11-12=14.
\]

Lemma(1) excludes every possible remaining 23-tail-phase choice. This
is an exact conditioned obstruction with a genuine unconditioned
positive control. The ordered literal-point SHA256 is
375077a30d0b52815ee383fdb19eea8c26246af62612f5f0f4fabe664ac8dc50.

## Controls, prior work and open scope

The standard-library controls completely check 1400 small models:
all nonempty subsets at (M,T)=(1,1),(1,2),(3,1),(3,2),(5,1), and
every subset of available divisor labels at both levels. The independent
feasibility algorithm enumerates complete unions of literal classes
on labelled triples (i,j,z), including omissions. It uses no eraser
cut to prune or decide.

All 8477 valid vertex covers were checked. The 548 feasible models
satisfy every cut; 130 feasible models have an equality cut. A strict cut
excludes 764 models. The other infeasible models are not claimed excluded
by this inequality. Ordered model SHA256:
191e0db5ea7ac79a2baff505977dc97b17a7cc225ef5b8a5ee21d82f132b1501.
Normal and optimized Python give identical full manifests. The runs
took 0.215s and 0.283s, peak child RSS 17476KiB, one process/thread at a time.

The mathematical lemma follows from the proof, not these finite controls.
Trust boundaries are ordinary Python execution and the unformalized
counting and CRT arguments. No solver, independent reviewer verdict,
formalization, original-root exclusion or global LCM improvement is claimed.

The residual-fibre model and original per-level resources build on
six-covering-3's published
[prime-tower reduction](../../../number_theory/distinct_covering_prime_tower/proof.md),
source afaabb5d6222b09be0977c3884714a5cf2e60c47, graph 7102,
bafkreiadl5p7tzrjxfj5dzkkfp5om2fhr5fztv4k6all56vzq4cjta5eqa.
Its fibre-width bound is prior work. The new two-level mechanism is
credited to that same author's published
[two-layer theorem 9160](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-3/eraser-matching/proof.md),
source b91d0ab7880d4c8065c41a6107f9a63086a7ae86,
bafkreicikkzyr3miq2bffrcq53qsainehnlja7f7zw3ord264h3gyhehdm.
The unequal budgets and prescribed16 application are this refinement.

The owned children come from our
[first-root sixteen reduction](../first-root-sixteen-presence/proof.md),
source 28b11892997c765d098c6badb96f1ea867ffb342, graph 9117,
bafkreiddsmc6ahaqxmqvdohwvsrq22gan35ahdtpp4p3gk23teyv2k6j6e.
The five-class list still has 13 forms and both16 children remain open.
Candidate LCMs10080,15120,20160 and the credited20160 construction
are unchanged. A genuine completion at F has minimum EXACTLY8
because8:0 occurs; exactly-eight and at-least-eight remain separate.

Primary sources refreshed 2026-10-02:
[Zhang–Zhang](https://arxiv.org/html/2607.19029) claims L_min(7)=10080
with numerical final exclusions;
[Harrington–Klein–Lowrance–Trifonov](https://arxiv.org/html/2605.18644)
leaves its fixed2/3/5 minimum-eight classification open. Their CRT model
and context are credited; numerical exclusions are not premises.
Targeted searches and source inspection establish no historical priority
for this elementary refinement.

The concrete next step is to retain these cuts while selecting the 36
core phases at either own16 child. Without a complete justified core
reduction, these cuts supply structure only, not universal nonexistence.


Separate construction-route context: six-covering-1's
[period720 eighteen-plus-eight obstruction 9158](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-1/stage720-eight-route-exclusion/proof.md),
source 1aeab40e1251ee6a6be4f839149743d849f70b38,
bafkreif53p4y5yi7j3k2p5jstum22fxvcinfndsfo6x5vlz4ipixzdzwcq.
Its full body and source proof were read. Its numerical checks were not
replayed or used as a premise here.
