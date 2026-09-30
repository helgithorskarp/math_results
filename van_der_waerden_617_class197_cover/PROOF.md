Author: six-vdw-3, researcher. Status: exact finite certificates with written
mathematical bridges; same-author independent checking, unformalized and
without external review.

Let N=3704, C=1852, p=617. Write q(r)=0 for a nonzero quadratic residue modulo
p and q(r)=1 for a nonsquare. It is undefined at r=0. For 0<=s<p set
t=1-s modp and define the partial reference

```
T_s(x) = q(x-C+s)          for 0<=x<C,
T_s(x) = q(x-C+t) XOR 1    for C<=x<N.
```

Arguments to q are reduced modp. Points at which the argument is zero are
free poles. Let f:{0,...,3703}->{0,1} contain no monochromatic nonconstant
seven-term integer AP. Define E_c={x:T_s(x)=c and f(x)!=c} and e_c=|E_c|.
No values of f at poles, symmetry of f, or other-class edit budget are imposed.

For any nonpole AP A monochromatic of reference color c, E_c must hit A:
otherwise A remains monochromatic in f. Any selected subfamily of such APs
therefore provides valid necessary constraints on E_c.

The four new exact conclusions are e_c>=197 for s=184,201,205,269, c=0,1.
The cited old complete profile gives e_c>=197 at all remaining 613 phases,
so their combination gives e_0+e_1>=394 for all 617 specified references.
This does not assert that any such repair exists or exclude an arbitrary
coloring on 3704 points. The local verifier checks the four new phases only;
the all617 corollary retains the old profile as a numerical dependency.

**Screening.** Each included base certificate gives positive integer weights
w_A on actual reference-color-zero APs, common denominator D0=1,000,000,
and point loads l(x)<=D0. Their sum is S. For a hypothetical e_0<=B=196,
AP hitting and double counting imply

```
S <= sum_{x in E_0} l(x)
  = D0*e_0 - sum_{x in E_0}(D0-l(x)).
```

All defects d(x)=D0-l(x) are nonnegative. Thus every edited point belongs to
V_0={x:T_s(x)=0 and d(x)<=delta}, delta=196*D0-S. The checker reconstructs
these loads and the eligible set; neither is supplied by a new certificate.

| s | S | delta | eligible points |
|---|---:|---:|---:|
|184|195333906|666094|1555|
|201|195802847|197153|1086|
|205|195658651|341349|1221|
|269|195882130|117870|1012|

Each actual original monochromatic AP has a petal P=A intersect V_0. A
hypothetical E_0 must hit every listed petal. For three nonempty petals
P1,P2,P3 with empty common intersection, no single point hits all three.
Consequently |E_0 intersect U|>=2 for U=P1 union P2 union P3. The checker
validates the three actual APs, nonempty petals and empty common intersection
for every positive cover-two weight. This elementary cut is not claimed as
a new general combinatorial principle.

**Complete branches.** A split at a new point x in V_0 has both children:
x unchanged (x notin E_0) and x edited (x in E_0). At a node let T be the
forced edited set and X the forced unchanged set inherited from the path.
Then E_0=T union H, H subset V_0\(T union X), |H|<=196-|T|. An AP petal P
requires |H intersect P|>=max(0,1-|T intersect P|), and a cover-two union U
requires |H intersect U|>=max(0,2-|T intersect U|).
The tree checker accepts no extra inherited assumptions, requires both
children, forbids reused/ineligible split points, and starts from T=X=empty.
Hence verified leaves cover every possible E_0 of cardinality at most196.

**Exact leaf inequality.** A leaf has positive integer weights lambda_P on
AP rows and omega_U on cover-two rows, denominator D>0, and optional
nonnegative free-point surcharges nu_x. Let W be their weighted sum of the
residual right-hand sides above. The checker verifies at each free point

```
sum_{P containing x} lambda_P + sum_{U containing x} omega_U <= D+nu_x.
```

Summing the necessary constraints over H, and using that H is a set, yields

```
W <= D*|H| + sum_{x in H} nu_x
  <= D*(196-|T|) + sum_{x free} nu_x.
```

A strictly positive gap W-sum(nu)-D*(196-|T|) therefore excludes this branch.
All frozen leaves have zero surcharges, but the implementation checks and
subtracts the full penalty if present. It uses integer sums and Fraction,
never an LP objective or an infeasibility status. The standard-library
checker independently verifies every listed AP and point capacity.

|s|complete splits (color0 coordinates)|leaves|min strict gap / D|
|---|---|---:|---:|
|184|2548; then1803 in its edited child|3|293613/1000000|
|201|2065|2|315425/1000000|
|205|1791|2|212707/1000000|
|269|none|1|124056/1000000|

These are strict rational contradictions, not approximations to an integer
optimum. Both branches are explicitly checked even where the numerical
guidance favored one. Freshly regenerated weights can differ; they must
pass the same definition-level checks.

**Both colors.** R(x)=3703-x exchanges halves. On a nonpole its new residue
is the negative of the old one. Since 617=1 mod4, q(-r)=q(r), and therefore
T_s(R(x))=1-T_s(x). Reflection preserves integer APs and maps V_0 to V_1.
The checker replays every AP, cut, split state and capacity at its actual
reflected coordinates for c=1. This is symmetry of the reference and the
necessary constraint system, never an assumed symmetry of f. It excludes
e_1<=196 independently of e_0.

Finally complementation of f preserves AP avoidance. Its edit counts against
the same partial reference are e'_c=M_s-e_c. Reflection pairs the reference
colors; each has M_s=1848 positions at s=1 (eight poles total) and1849 at
every other phase (six poles total). Applying the lower bound to f and its
complement gives 197<=e_c<=M_s-197, hence 394<=e_0+e_1<=2*M_s-394.

Only the family (s,1-s,1), s=0,...,616 is quantified. The other incompatible
affine references, fixed aligned QR words and period618 column constructions
are outside this theorem. Earlier class196 geographic inequalities are not
promoted to class197 by this argument. No coloring witness or new van der
Waerden number bound follows from these necessary edit constraints alone.
