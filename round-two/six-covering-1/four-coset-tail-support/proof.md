# A support bound for a four-coset seven-tail

Author: **six-covering-1**, role **researcher**, 2026-10-02.

Let

\[
S=\{x\in\mathbb Z/720\mathbb Z:x\equiv0\pmod4,
                                      x\not\equiv6\pmod9\}.
\]

Thus \(|S|=160\). Let \(K\subseteq S\). Consider the **29 distinct original
moduli** \(7d\), where \(d\mid720\) and \(d\ge2\), with at most one phase
per modulus. Suppose their classes cover every \(x\pmod{5040}\) whose
reduction modulo720 belongs to \(K\). Then

\[
\boxed{|K|\le115.}
\]

This concerns seven copies of an actual subset of one four-coset. It is
neither an exclusion of arbitrary period15120 systems nor a bound on
\(L_{\min}(8)\). No first-stage or full-tail construction is asserted.

## Original resource normalization

CRT identifies the target with \(K\times\mathbb Z/7\mathbb Z\). A phase
of an original \(7d\) class chooses one seven-copy and one phase modulo
\(d\). Since \(K\subseteq0\pmod4\), original moduli14 and28 can each
erase an entire copy. Missing classes may be added; invisible phases may
be replaced by productive ones.

These two whole-copy resources can be put in distinct copies without
losing coverage. To move one, keep all other classes and place it in a
copy without a whole-copy resource. Its old copy remains covered by the
other whole-copy resource if the two coincided. If a whole-copy resource
was initially invisible, replacing it loses no target coverage. Permute
the seven copies so these are0 and1. A copy permutation fixes the720
coordinate and sends every original \(7d\) phase to another phase of that
same original modulus. Each remaining class in an already erased copy
can be moved to one of the other five copies. Consequently any completion
gives a covering of five copies of \(K\) by the **27 separate** resources

\[
\mathcal D=\{d:d\mid720,\ d\ge2,\ d\notin\{2,4\}\}.
\]

The proof below keeps these original resources distinct, including ones
that induce the same effective modulus on the four-coset.

## Capacity and support

Write \(x=4t\), with \(t\in\mathbb Z/180\mathbb Z\). The background is
\(S'=\{t:t\not\equiv6\pmod9\}\). For an original cofactor \(d\), put
\(e=d/\gcd(d,4)\). Its maximum number of hits in \(S'\), on one copy, is

\[
C_d=\begin{cases}160/e,&3\nmid e,\\180/e,&3\mid e.\end{cases}
\]

Indeed an effective phase \(r\pmod e\) has \(180/e\) points. Its intersection
with the removed9-coset has \(180/\operatorname{lcm}(e,9)\) points when
\(r\equiv6\pmod{\gcd(e,9)}\), and is empty otherwise. The formula follows
by maximizing over phases. The exact inventory is:

|d|3|5|6|8|9|10|12|15|16|18|20|24|30|36|40|45|48|60|72|80|90|120|144|180|240|360|720|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|\(C_d\)|60|32|60|80|20|32|60|12|40|20|32|30|12|20|16|4|15|12|10|8|4|6|5|4|3|2|1|

The sum is600, so initially \(5|K|\le600\), or \(|K|\le120\).

Select the seven original cofactors

\[
(8,3,6,12,5,10,20).
\]

On \(S'\) they give one binary class \(B\), three separately owned ternary
classes \(A_1,A_2,A_3\), and three separately owned fifth-classes
\(C_1,C_2,C_3\). Their maximum total mass is
\(80+3\cdot60+3\cdot32=356\). The other twenty resources have total mass244.

For any phases and allocation of these seven classes to five copies,
let \(Q_i\subseteq S'\) be their union on copy \(i\),
\(P\) their summed individual masses,
\(L=|\bigcup_i Q_i|\), and
\(\Delta=P-\sum_i|Q_i|\), the overlap loss within copies.
For any \(K'\subseteq S'\) of size \(h\),

\[
\sum_i|K'\cap Q_i|\le P-\Delta-\max(0,L-h). \tag{1}
\]

At least \(L-h\) points of the total support lie outside \(K'\), and each
is counted in at least one copy. This explains the last subtraction;
it is separate from overlap within copies.

We prove the right side of(1) is at most \(h+216\) for \(115\le h\le120\).
Invisible selected phases can be replaced by a productive phase in the
same copy, increasing coverage, so only productive effective phases need
consideration.

* A ternary phase0 has mass40; phases1 and2 have mass60. If at least two
  \(A_j\) use phase0, \(P\le316\le h+216\). If exactly one does,
  \(P\le336\) and \(L\ge130\): the zero ternary class, a nonzero ternary
  class, and \(B\) already have union130. Equation(1) gives at most
  \(h+206\).
* If both nonzero ternary phases occur and phase0 does not,
  their union with \(B\) has140 points. Thus \(P\le356\) and(1) gives at
  most \(h+216\).
* Otherwise all three \(A_j\) are the same nonzero phase. Let \(r\) be
  the number of distinct selected fifth-phases. Then \(P=356\) and
  \(L=110+10r\). Here \(|A\cup B|=110\), and each new fifth-class adds
  ten points outside that union; distinct fifth-classes are disjoint.

In the last case, if \(r=1\), every pair of the seven selected classes
has intersection at least12. In each occupied copy, every class after
the first loses at least12 hits to the union of earlier classes. Seven
classes in at most five occupied copies therefore give \(\Delta\ge24\).
Equation(1) yields at most \(h+212\).

If \(r=2\), \(\Delta\ge12\). Otherwise all classes sharing a copy would
be disjoint. The binary class intersects every other selected class, so
it would need its own copy; the three identical ternary classes would
need three further copies; and the repeated fifth-class would need two
more, sharing neither a binary nor a ternary copy. That requires at least
six copies. Some pair therefore intersects in one copy. Every nonempty
pair intersection has at least12 points, proving the bound. Equation(1)
yields at most \(h+214\). For \(r=3\), \(\Delta\ge0\) and(1) yields at
most \(h+216\).

These intersection counts follow directly from the literal sets:
\(|A\cap B|=30\), \(|A\cap C|=12\), \(|B\cap C|=16\), and
\(|A\cap B\cap C|=6\). Repeated fifth-classes intersect in32 points;
distinct fifth-classes do not intersect.

If a tail completion had \(116\le h\le120\), the seven selected resources
and the other twenty together would give

\[
5h\le(h+216)+244=h+460,
\]

forcing \(h\le115\), a contradiction. Combined with the initial600
capacity bound, this proves the theorem.

## Application to the owned construction route

Take at most one phase for each original \(m\mid720,m\ge8\), normalized
to \(8:5\) and \(9:6\). Suppose all720-stage holes lie in
\((3\pmod{18})\cup(0\pmod4)\), and let \(K\) be the actual holes outside
the18-coset. They belong to \(S\). The
[published104-hole and18-plus8 obstruction](https://github.com/helgithorskarp/math_results/blob/1aeab40e1251ee6a6be4f839149743d849f70b38/round-two/six-covering-1/stage720-eight-route-exclusion/proof.md)
implies \(|K|\ge74\), because only30 points of the18-coset escape the fixed
classes. Consequently completion by this29-resource seven-tail requires

\[
74\le |K|\le115.
\]

Also \(g(K)=\gcd(720,\{x-x_0:x\in K\})=4\): it is a multiple of4;
values at least12 would permit at most60 points; value8 would put all
stage holes in one18-coset plus one8-coset, contrary to the cited result.
In particular, both8-halves contain an actual hole. These are necessary
constraints, and do not certify a stage or a tail.

The theorem applies whenever the tail is actually asked to cover all
seven copies of \(K\). Using a top completion with partial off-target
coverage requires checking this condition separately. No arbitrary
period15120 reduction is asserted here.

## Reproduction, proof status and context

`check.py` completely checks the selected-seven relaxation. Its productive
effective phase domain has700 multisets: binary phase2 choices, ternary
phase multisets10 choices, and fifth-phase multisets35 choices. Sorting
within the ternary/fifth triples is lossless because their projected
families are identical; their three original resources remain separate.
All855 partitions of seven labeled resources into at most five copies
are checked. Thus598500 cases are completed, without solver calls.

For each case, count how many of the five unions cover each of the160
candidate points. The maximum score on an arbitrary \(h\)-point subset
is the sum of the \(h\) largest multiplicities. The exact maxima are
331,332,333,334,335,336 for \(h=115,116,117,118,119,120\).
The first is a sharpness fixture for the **selected-seven relaxation**,
not a feasible twenty-nine-resource tail or an original first stage.

`audit.py` imports no production bitset or copy-partition routine. It uses
physical sets, all original cofactor phases, original7d physical phase
counts, the written phase cases, and direct set-partition checks of the
overlap minima. The written proof is not formalized. Normal and optimized
Python runs and certificate-damage controls are recorded in the manifest.
Author-checked; no independent reviewer verdict or priority claim.

The original-resource emphasis is shared with
[six-covering-3's eraser/matching proof](https://github.com/helgithorskarp/math_results/blob/b91d0ab7880d4c8065c41a6107f9a63086a7ae86/round-two/six-covering-3/eraser-matching/proof.md).
Exact group-union capacity methods also appear in
[the published residual-weight result](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_residual_weight_duals/proof.md).
Neither numerical certificate is a premise of the upper115 theorem.

Primary literature context: [Zhang–Zhang](https://arxiv.org/html/2607.19029)
addresses minimum exactly7, while
[Harrington–Klein–Lowrance–Trifonov](https://arxiv.org/html/2605.18644)
studies moduli restricted to prime factors2,3,5. These were rechecked live
2026-10-02. No literature solver exclusion is imported and no published
global theorem is claimed as new. The campaign's exact-eight numerical
frontier is unchanged.
