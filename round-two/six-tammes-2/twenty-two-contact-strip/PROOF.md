# A parameter strip and critical-vertex barrier for the 22-contact core

Actual author: **six-tammes-2**, role **researcher**, 2026-10-02.
Complete conditional author proof; independent review and formalization pending.

Let `I=[14/25,593/1000]`. Suppose thirteen unit points with labels
`0,1,2,4,5,6,7,8,9,10,11,12,13` have all distinct pair products at most
`t in I`, and these 22 prescribed products equal t:

```
0-5 0-6 0-7 0-11 1-2 1-4 1-10 1-12 2-4 2-8 2-10 2-13
4-8 5-7 5-9 5-11 6-11 7-12 8-13 9-10 9-11 10-12
```

Both `(6,8)` and `(9,13)` are absent from the contact assumptions.
The labels are injective, as also follows from the packing inequalities.
No face, degree, contact-map completeness, optimizer occurrence or added
point assumption is imposed.

Use the complete frame and reciprocal circle parameter z of
[lemma9149](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-2/twenty-two-contact-frame/PROOF.md).
Its sole packing orientation is `(epsilon,eta)=(-1,+1)`.
The new conclusions are:

1. Every such packing has `t>577/1000` and `9/10<z<7/5`.
2. Throughout `J x [9/10,7/5]`, where `J=[577/1000,593/1000]`,
   the three planes `p1.x=p4.x=p7.x=t` have a unique intersection
   `x147`. Its squared norm strictly decreases with z. Put
   `A(t)=t^3-3t^2+t+1` and `z0(t)=2t^2/A(t)`.
   Then `||x147||^2<1` exactly when `z>z0(t)`.
3. Let tau be the unique root in J of the credited incumbent quintic
   `F(t)=13t^5-t^4+6t^3+2t^2-3t-1`.
   An actual packing with `t<tau` has `z>z0(t)`, and hence
   `||x147||^2<1`. At `t=tau` it has `z>=z0(t)` and
   `||x147||^2<=1`.

Conclusion3 concerns this particular intersection, even when it fails
some avoidance inequalities. It is a useful critical-vertex bound for
an extension polytope. The other polytope vertices and cap capacity are
not verified here, so no two-extension exclusion or new global Tammes-15
bound follows from this lemma alone.

## Frame used by the new checker

Anchor coordinates use `Q=(p1,p2,p4)` and positive definite Gram matrix
`H=(1-t)Id+tJ3`. Write `<a,b>_H=a^T H b` and
`D=(1-t)^2(1+2t)`. The coordinates B1,B2,B4 are the standard basis.
The reflection rule `new=r(first+second)-old`, `r=2t/(1+t)`, gives
B8 from B2,B4,B1; B10 from B1,B2,B4; B12 from B1,B10,B2; and
B13 from B2,B8,B4. Set

```
k=t(9t^2-2t-3)/(1+t)^2, gamma=k/(1+k),
mu=(t-1)(t+1)(2t+1)(3t-1)/(9t^3-t^2-t+1),
C=1+D z^2, d=H^-1(B12 cross B1),
W=t B12 +(D z^2-1)/C (B1-t B12)+(2Dz/C)d,
s=[D(tz^2-2z)+t(2t-1)]/C,
delta=1-s^2, g=delta-k^2-t^2+2skt,
V=[(k-st)W+(t-sk)B10-sqrt(Dg) H^-1(W cross B10)]/delta,
U=gamma(W+V)+mu H^-1(W cross V),
den=(2r-1)(r+1),
p0=(rU+rW+(1-r)V)/den,
p5=((1-r)U+rW+rV)/den,
p11=(rU+(1-r)W+rV)/den,
p6=U, p7=W, p9=V.
```

The imported lemma covers every packing with these contacts, including
chart endpoints, all original orientations and Gram tangencies. It
proves the packing-only bound `g>1/2`; that bound is **not** used to
justify differentiation on a whole parameter box. The executable
interval kernel and mathematical premise are pinned by commit and
SHA256 in [INPUTS.json](INPUTS.json). Their hashes identify the premise;
they do not replace its separate proof.

## Whole-box mean-value enclosure and the two strip covers

The imported scalar kernel uses outward rounding to the `2^-80` dyadic
lattice, specialized squaring including intervals crossing zero, and
integer-square-root bounds. [model.py](model.py) first computes the
**raw, unclipped** rational functions on the entire closed box and
requires `g.lower>0` and `delta.lower>0`. Every subsequent denominator
must exclude zero and every differentiated square-root argument must
have a strictly positive lower endpoint. These checks establish that
the displayed branch is differentiable along every segment from the
midpoint to a point of the box, without a feasible-subset assumption.

Every expression carries its value enclosure, both partial derivative
enclosures and its independently evaluated midpoint enclosure. For
half-widths `rt,rz`, if the derivative bounds are `dt,dz`, its value
enclosure is intersected with

`center + [-rt max|dt|,rt max|dt|] + [-rz max|dz|,rz max|dz|]`.

The segment mean-value theorem proves this enclosure. The sum, product,
quotient, power and positive-square-root rules preserve all three
enclosures. Narrowing a value does not narrow its derivatives by
assumption: it only supplies valid inputs to subsequent derivative
rules. Empty intersections reject. No clipping based on packing facts
occurs in this differentiated model.

The two prefix plans cover the **full closed** rectangle
`I x [-5/2,5/2]` for the sole retained orientation. Each T/Z token splits
its parent's t/z interval into both closed halves, and every two-digit
leaf token records one literal proof instruction. The verifier reads
every token, checks both children and rejects missing or trailing data.
It makes no adaptive witness selection.

A leaf may certify a strict packing violation by a specified pair using
the whole-box centered model. Alternatively it may use one literal
non-differentiated witness from lemma9149's pinned interval kernel:
chart violation, empty necessary intersection, impossible real V,
W-pair violation or another cross-pair violation. Those primitive
witnesses may use feasible-subset clipping, exactly as already proved
in9149; they are not fed into a derivative argument. The remaining leaf
type lies strictly inside the requested parameter strip and is outside
the exclusion target. Thus the boundary values `z=9/10,z=7/5` and
`t=577/1000` are included in the regions excluded by packing violations.

The z plan has374 leaves, maximum total depth14; the t plan has372
leaves, maximum depth18. Their full exact replay proves conclusion1.
The prior unsuccessful depth22 experiments are not inputs. This proof
changes the enclosure representation, retaining the same depth22 and
160-second limits.

## Exact critical-vertex identity

Put `L(t,z)=(t^2-6t-3)z-3t-1`. Algebra gives

```
det Gram(B1,B4,W) =
4t^2(t-1)^4(2t+1)L(t,z)^2 / [(t+1)^4 C^2],

||x147||^2-1 =
-8(t+1)(2t+1)((t-1)z-1)(A(t)z-2t^2)
 / [(t-1)L(t,z)^2].
```

The norm formula follows from `t^2 1^T Gram^-1 1`. The checker derives
both identities over `Q(t,z)` from W and the anchor Gram matrix. Exact
two-variable Bernstein coefficients prove that the displayed Gram
determinant is strictly positive on the full closed strip. In the norm
identity, `t-1<0`, `((t-1)z-1)<0`, `A(t)>0`, and all squared factors are
strictly positive. Its sign is therefore the opposite of
`A(t)z-2t^2`, proving conclusion2's threshold.

For completeness, the exact z derivative of the squared norm is

```
8(t+1)^3(2t+1)[3t^3 z-5t^2 z-5t^2+t z-2t+z-1]
 / [(t-1)L(t,z)^3].
```

Its numerator has strictly negative, and denominator strictly positive,
Bernstein coefficients on the full closed strip, proving strict
decrease. [ALGEBRA.json](ALGEBRA.json) records the exact expressions,
degrees and coefficient extrema; [algebra.py](algebra.py) recomputes them.

## Packing forces the strict critical-vertex barrier below tau

Define `h(t,z)=<U(t,z),B8(t)>_H-t`. The third literal plan covers the
**whole** closed rectangle `J x [9/10,19/20]`. Its1103 leaves all prove
`partial_z h<0` with the unclipped differentiable model above. None
of its leaves skips a point using a packing predicate. This also proves
regularity of the branch on that entire rectangle.

At `z=z0(t)` the radical is a perfect rational square. Write

```
P4=8t^4-3t^3-t^2+3t+1,
P5=4t^5-19t^4-2t^3+4t^2-2t-1,
Pq=2t^5+21t^4-4t^3-6t^2+2t+1.
```

Direct rational reconstruction of W,V,U gives

```
sqrt(Dg) = -(t-1)^2(2t+1)(3t+1)P5 / [(t+1)^2 P4],

h(t,z0(t)) =
2t(t-1)(2t+1)(3t+1)(5t^2-1)(7t^3+5t^2+9t+3) F(t)
 / [(t+1)^4 P4 Pq].
```

The first expression squares to the exact radicand and is strictly
positive on J. Bernstein signs check its branch, all raw boundary
denominators, `g>0`, and `delta>0`; a merely squared identity would
not select the needed root. The factor multiplying F in the second
identity is strictly negative on J. Also `F'>0` there and the exact
credited bracket for tau has opposite F signs:

`0.59260590292507377809642492233275 < tau < 0.59260590292507377809642492233276`.

Hence `h(t,z0(t))>0` for `t<tau`, and it equals0 at tau.
The checker further proves `A>0` and `(19/20)A-2t^2>0` on J, so
`z0(t)<19/20` throughout.

For an actual packing, conclusion1 gives `z>9/10` and `h(t,z)<=0`.
If `z0(t)<=9/10`, then already `z>z0(t)`. Otherwise any
`z<=z0(t)` belongs to `[9/10,19/20]`, and strict decrease in z gives
`h(t,z)>=h(t,z0(t))>0` below tau, a contradiction. At tau,
`z<z0(t)` gives a strict contradiction by the same derivative sign.
This proves conclusion3, including all endpoint cases.

## Verification, prior art and remaining work

Run [check.py](check.py) with Python3.11+ and SymPy1.14.0, from this
directory in the repository checkout. It verifies the pinned prerequisite
hashes, recomputes exact rational and Bernstein identities, selects the
positive radical by signs, and replays all1849 literal interval leaves.
[EXPECTED.json](EXPECTED.json) contains compact counts, strict margins
and hashes. [controls.py](controls.py) rejects seven deliberately damaged
proof inputs or invalid differentiation domains. Normal and optimized
Python checks and controls are required in the recorded validation.
The interval replay shares the pinned dyadic kernel; it is not an
independent researcher review. The geometric interpretation and
mean-value argument remain unformalized.

Lemma9149 is the sole mathematical dependency. The critical-vertex
approach and the incumbent root were already studied on the stricter
negative23-contact curve in
[lemma9003](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-2/negative-core-boundaries/PROOF.md),
and the associated cap proof in
[lemma9057](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-2/negative-core-extensions/PROOF.md).
This result removes the additional `(6,8)` contact from that critical
vertex conclusion, without importing the old curve parameter, its
lower boundary or its conditional vertex argument. It does not transfer
9057's complete polytope audit to the larger family.

The next mathematical obligation is a uniform audit of the remaining
avoidance-polytope vertices over the feasible two-dimensional domain,
with a proved cap bound for arbitrary additional unit points. The
optimizer/contact-map occurrence bridge is a separate unresolved
obligation. Existing global bounds and incumbent status are unchanged.
