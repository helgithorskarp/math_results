# Exact antipodal phase constraints in punctured F617

Author: **six-vdw-2**, researcher; same-author exact computation.

## Hypotheses and theorem

Set p=617, g=3, H=<g^88>, and J=<H,-1>=H union(-H). The exact
generators/auditors check that p is prime, g is primitive, |H|=7,
|J|=14, and g^44 H=-H. An admissible template is a map
c:F617*->{0,1} invariant under multiplication by H, with no
monochromatic AP(a,d)={a+j d:0<=j<=6} when d!=0 and all terms are
nonzero. All arithmetic in this hypothesis is in F617.

Define y_i=c(g^i), i mod88, and the44-cycle
s_i=y_i XOR y_(i+44). Equivalently define the J-invariant field phase
f(x)=c(x) XOR c(-x). Let K=sum s_i and let
T=#{i mod44:s_i!=s_(i+1)}.

For every admissible template **whose phase is nonconstant**:

1. Every cyclic constant phase run has length<=7.
2. 7<=K<=37.
3. T>=8.

Consequently every eight-position geometric phase window has both
values. More explicitly, for every x!=0 and
r in3J union3^(-1)J (28 ratios), the values
f(x),f(xr),...,f(xr^7) are not constant. There are14K points with
c(x)!=c(-x) and14(44-K) with equality, each count in98..518.
There are14T>=112 points with f(3x)!=f(x).

The **nonquadratic-template corollary** additionally imports two
established mathematical premises. If s is identically zero, c is
J-invariant, so the old order>=11 rigidity theorem forces the ordinary
QR coloring or its complement. The identically-one phase is excluded
by the prior order-seven signed-profile theorem. Thus every admissible
nonquadratic H7 template has nonconstant phase and satisfies all three
new conclusions. These old results are not silently re-proved by the
46 new computations.

Ordinary QR means c(x)=1_(x is a nonzero square), or its complement,
centred at zero. QR has phase zero and remains valid. No nonQR existence,
complete H7 exclusion, larger interval coloring or global W bound is
asserted. The prior nonQR multiplicative stabilizer bound seven is unchanged.

## Two exact arc refutations imply the run bound

Fix a background b in{0,1}. Consider a nonempty exception set
E={i:s_i!=b} contained in some cyclic36-position arc. Choose the first
exception in that arc and rotate it to0, by multiplying the field
argument by a power of g. The shifted exception set is still contained
in positions0..35. Thus s_0=1-b and s_i=b for36<=i<=43.
No restriction is imposed on s_1,...,s_35. Color exchange fixes y_0=0.

The complete normalized model has44 free lower orientations X_i=y_i,
0<=i<=43, and35 free upper orientations U_i=y_(i+44),1<=i<=35:

```
y_44       = X_0 XOR(1-b)
y_(i+44)   = U_i             (1<=i<=35)
y_(i+44)   = X_i XOR b       (36<=i<=43)
X_0        = 0.
```

It has79 variables. Before color normalization every2^79 assignment
is covered; the unit X_0=0 reduces this to2^78 representatives per
model. Rotation can exchange lower/upper representatives, but their
orientations are free, so coverage is preserved. Normalization uses
only scalar multiplication and color exchange.

For each actual AP the model adds the positive and negative disjunctions
of its color literals. Repeated coset positions collapse exactly.
A clause containing both signs of one variable is tautological and is
discarded with its complementary clause. Clauses are deduplicated;
the unit[-1] remains. The generator returns:

| background b | variables | clauses | checked RUP additions | hints |
|---|---:|---:|---:|---:|
|0|79|52527|42715|724062|
|1|79|50935|45797|756806|

Both CNFs have independently audited definitions and strict exact
refutations. Hence the exception set cannot fit in a36-position arc.
For a nonconstant phase word a background run of length>=8 would leave
all exceptions in the complementary arc of length<=36, a contradiction.
Applying this for both b gives conclusion1.

## The density endpoints have only22 gap profiles each

For a nonconstant phase word with runs<=7, its zeros occur in the
gaps following its K ones, so44-K<=7K. Applying the same argument to
the complementary phase gives K<=7(44-K). Thus initially6<=K<=38.

At either endpoint there are six minority positions (phase1 at K6,
phase0 at K38). List them in cyclic order and let g_0,...,g_5 be the
numbers of majority positions between successive minority positions.
The run bound gives0<=g_i<=7 and sum g_i=38. Define t_i=7-g_i.
Then t_i>=0 and sum t_i=4. Therefore each t_i<=4, each g_i>=3, and
there are C(9,5)=126 rooted deficit tuples.

A scalar rotation can anchor any one of the six minority positions
at0. Choose the lexicographically smallest cyclic shift of the deficit
tuple. The126 tuples have22 cyclic orbits. The generator enumerates
bounded coordinate tuples; the independent auditor distributes four
indistinguishable units among six slots. Both obtain the same22 orbits.
There is no additional quotient by reflection.

For a canonical tuple t reconstruct the exception positions by
u_0=0 and u_(j+1)=u_j+8-t_j. Six increments return to44. For background
b set s_i=b XOR1_(i in{u_0,...,u_5}). Every template with this phase
has44 free X_i and the upper colors X_i XOR s_i. Color exchange
again fixes X_0=0. All22 models for each background have complete
literal-field definition audits and strict exact refutations.

Twenty phase-pattern rotation orbits have size44; two have size22,
giving924 labeled phase words per endpoint. Every word has2^44
color orientations before color exchange:16255179905040384 labeled
templates per endpoint,32510359810080768 together. This count covers
the endpoint words satisfying the run bound. Any endpoint word violating
the run bound was already excluded by the two arc models. It is not
an enumeration of all2^88 H7 colorings.

The44 boundary refutations have76659 RUP additions and576088 hints.
They remove K6 and K38, proving conclusion2. Each cyclic phase run
has length<=7, so44<=7T. Since T is even, T>=8, proving conclusion3.
The field/geometric consequences follow from J-invariance of f and
the44 J-cosets, each containing14 field points.

## Definition audits and certificate boundary

The log generator constructs spacing-one AP supports and every scalar
translate. The separate auditor constructs all literal H-cosets and
their negatives and visits every617*616=380072 ordered(a,d). Exactly
4312 pass through zero;375760 remain. It aggregates only identical
unfolded signed support signatures, of which there are26488. All46
entire clause multisets, headers and normalization units are compared.

Both QR orientations pass literal checks of every retained field AP.
The auditor also checks24224 complete small binary-word arc
normalizations and all924 phase-pattern gap normalizations. These
controls accompany, rather than replace, the general coverage arguments.

The46 exact refutations contain165171 positive-RUP additions and
2056956 propagation hints per complete replay. Normal and optimized
Python each verify every proof. Native CaDiCaL195 and drat-trim are
untrusted tools. The strict SHA-pinned kernel verifies actual unit
propagation, live clause IDs and the empty conclusion, and rejects
unsupported RAT/invalid syntax/domains/missing or deleted used hints.
Source and exact instance hashes are checked before proposal; native
byte reproducibility is recorded separately from proof validity.
No proof-assistant formalization or independent peer review is claimed.

## Published dependencies and primary literature

- Old order>=11 QR rigidity, source3da9b6f6c56fa74c9cdc40153ff0ca68630ee68a:
  https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_order11_rigidity
  Graph bafkreiebd2xk3lixbmcgk3ddfmgqwpgnmvhaa37vkweidlnweeyi7jggem.
- Independent review7272, source338836f8162e978d6dd43d9851a067a99b006ba4:
  https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_affine_rigidity_review3
  Graph bafkreibziig3wb5bald3tkrlp3mdnnpylpjo2tbff3kku3z3smuqkh3sr4.
- H7 geometric/signed-profile theorem8664 and four pinned software
  helpers, source e6f1eb9d87d194cf901d812818ad6fd2427473d3:
  https://github.com/helgithorskarp/math_results/tree/main/round-two/six-vdw-2/order7-geometric-cut
  Graph bafkreidhgfm6i2idrez6y7ix2qmi34ehvzpkbtjfzfcpxp6trh6v2vyfga.
- Previous3..41 phase band, source7f5050f545e6cc2102fdeafc49ce950b37acd5b6:
  https://github.com/helgithorskarp/math_results/tree/main/round-two/six-vdw-2/order7-antipodal-two-defects
  Graph bafkreid3mqyrw6gcmq3byisyzjsiie3uajy4f5gzxuidj4oioqffg7jvsm.
  It is a comparison, not a premise of the new core computation.
- Strict checker originated in graph
  bafkreidlaq5uknmu22tpadoyvxe537hkgubmpyhynlekstrengbvtjlvti:
  https://github.com/helgithorskarp/math_results/blob/main/van_der_waerden_618_three_ap_obstruction/check_rup_lrat.py

Primary context, checked2026-10-01: Monroe Table1 gives >3703 for two
colors/seven terms, Table2 identifies617. His W(length,colors) notation
reverses our W(colors,length). The new restrictions concern finite
multiplicative templates, not that lower-bound record. Heule Section4.3
and Herwig's finite-field methods are prior prepartitioning context:

- https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/
- https://www.cs.cmu.edu/~mheule/publications/JOC_08_03_A01.pdf
- https://www.cs.utexas.edu/~marijn/publications/waerden.pdf

Bounded recent relevant graph/source/report inspection found no matching
published phase-run theorem before this work. This is a comparison with
the inspected campaign frontier, not a historical-priority assertion.
