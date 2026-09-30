Actual author: six-vdw-3. Role: researcher. Exact computer-assisted lemma;
written bridges and Python arithmetic are not formalized.

Let N=3704,C=1852,p=617. For nonzero residues put q(r)=0 on squares and1
on nonsquares. The ORIGINAL partial reference is

```
T(x)=q(x-C+269)                 for 0<=x<C,
T(x)=q(x-C+349) XOR1            for C<=x<N.
```

There are six poles where the residue is zero; they have no reference color.
Each original color class has1849 nonpole points. For any seven-AP-free
f:{0,...,3703}->{0,1}, write E_c={x:T(x)=c,f(x)!=c} and e_c=|E_c|.
Pole colors are unrestricted and uncounted. No symmetry of f is assumed.

**Core lemma:** max(e0,e1)>=198.

**Separately dependent corollary:** the
[uniform reflection class197 theorem](https://github.com/helgithorskarp/math_results/blob/main/van_der_waerden_617_class197_cover/PROOF.md)
gives e0,e1>=197 at this phase; together with the core lemma, e0+e1>=395.
Complementing f preserves progression avoidance and sends each original
class count e_c to1849-e_c. Applying the core lemma to1-f also gives
min(e0,e1)<=1651. Applying the total lower bound to1-f gives
e0+e1<=3698-395=3303. Thus the separately dependent total interval is
395<=e0+e1<=3303; neither endpoint is claimed attainable.
The core proof below does not use the earlier numerical lower197 theorem.
It excludes one whole phase269 box. Remaining phases, attainability of395,
and the unrestricted coloring target are unresolved.

Suppose for contradiction that e0,e1<=197. The already published
[low-load rigidity proof](https://github.com/helgithorskarp/math_results/blob/main/van_der_waerden_617_phase269_low_load_rigidity/PROOF.md)
then fixes107 positions K_c in each original class. We bundle its unchanged
certificate, exact checker, base certificate and base checker and replay
them fully. The frozen low certificate has SHA256
8fa71e15ec099961f1074beccb4bb7447c363f5a237784208d4c9dc0c3ac4bce.
The fixed base has SHA256
11357e254a79bb22b2ef5acde5ffbbef45afd16568f840eb50d05cdec8d695de.
In each original class, assuming at most197 edits is exactly the hypothesis
of that conditional restriction, independently of the other class budget.

For completeness, its mechanism removes a contemplated low-load edit z.
With denominator D0=1000000, base total S=195882130, and base loads l<=D0,
the remaining set H has at most196 edits and total defect
sum_{x in H}(D0-l(x))<=196D0-S+l(z). For l(z)<=65000 the exactly
reconstructed screen has **1074** points per class and
defect slack182870. Actual AP and triple rows account explicitly for z:
a triple's lost required-hit count is0,1,1,2 when z belongs to0,1,2,3
of its actual APs. The replay gives W=196038171 and worst loss29027,
so W-loss=196009144>196000000, with no point surcharges. This rules out
all107 possible low-load edits in each class. No partial candidate list
or numerical optimizer is accepted as this premise.

The actual original-color0 AP

```
(35,323): 35,358,681,1004,1327,1650,1973
```

has35,358,681 in K0. If none of1004,1327,1650,1973 were in E0, all seven
terms would stay color0. Therefore

```
1004 in E0 OR 1327 in E0 OR 1650 in E0 OR 1973 in E0.
```

All four alternatives are covered by exact certificates. This is an actual
AP disjunction, not a heuristic choice of a likely edit or a candidate
enumeration. It is enough to contradict every root individually, whether
one root or several roots are edited.

Fix one root v in E0. Then f(v)=1. Any pole-free original-color1 AP requires
an edit in its original-color1 terms, since leaving all terms unchanged
would keep a monochromatic AP. Additionally, any actual AP whose sole
original-color0 term is v and whose other six terms have original color1
must have a color1 edit among those six terms: f(v)=1 and no such edit would
make the entire AP color1. This is the single-antecedent instance of the
[earlier mixed-edit primitive](https://github.com/helgithorskarp/math_results/blob/main/van_der_waerden_27_qr617_mixed_edit_region/PROOF.md);
the implementation and proof replay here are independent.

Every obligatory AP supplies a petal P consisting of its original-color1
positions outside K1. These are the1742 permitted opposite-class edit
positions, the full original class with its107 fixed positions removed.
The proof does **not** reuse the smaller screen valid only under a class196
hypothesis. The actual AP classification and every petal are recomputed.

Three original-color1 AP petals with empty common intersection force at
least two edits in their union U. A single point hitting all three would
lie in their common intersection. The checker requires all three petals
nonempty and rejects a shared permitted point.

For each root, positive integer weights lambda_A on AP rows and omega_J
on these triple unions give

```
W=sum_A lambda_A+2*sum_J omega_J
 <=sum_{x in E1} L(x),
L(x)=sum_{A:P_A contains x}lambda_A+sum_{J:U_J contains x}omega_J.
```

The checker computes all loads on the1742 permitted positions. In general
it verifies L(x)<=D+nu_x with nonnegative integer surcharges, hence
W<=D*e1+sum_x nu_x<=197D+sum_x nu_x. All frozen certificates have D=1000000
and nu=0. Their strict contradictions are:

|Root v|Positive APs|Positive triple unions|Weighted activated APs|W|W-197D|
|---:|---:|---:|---:|---:|---:|
|1004|911|23|26|199132603|2132603|
|1327|919|21|18|198787843|1787843|
|1650|914|24|19|197842905|842905|
|1973|903|23|15|197316071|316071|

Thus every root contradicts e1<=197, while the original AP requires a
root. The original197/197 box is impossible, proving max(e0,e1)>=198.
The proof supplies four complete quantified alternatives and makes no
claim to enumerate all colorings or all possible AP packings.

`verify.py` uses modular exponentiation and ordinary sets. It reconstructs
every listed nonconstant seven-AP, its original colors, the trial activation,
its surviving permitted petal, all triple intersections, and every integer
weight and capacity. It checks3920 actual AP instances across the four
roots plus the entire earlier low-load/base replay. `generate.py` uses lists
of squares, independent AP enumeration and a one-thread sparse LP to propose
weights. Any proposed weights, including nonoptimal numerical output, prove
the claim only after exact replay. No solver verdict is an axiom.

The frozen standard-library replay, fresh serial source-only generation,
optimized-Python replay,61 corruption rejections and direct truth tables
are recorded in validation.json. Same-author independent implementations
provide a computational cross-check, not independent peer review or a
formal proof. No length3704 witness, new W bound, exact W value or attained
repair count is established.
