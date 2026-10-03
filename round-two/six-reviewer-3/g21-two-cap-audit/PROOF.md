# Independent proof of the twelve-label capacity theorem

Actual reviewer: **six-reviewer-3**, independent mathematical reviewer. Target: committed LEMMA10012/0, `bafkreianoziph3cxsy2dwrxggk4hhkinwt2l3uzcx4xlozxxtidynjrwna`, actual author six-tammes-2. The written original theorem and proof were visible. This is not a blind review. Current target executable source, generated certificate and expected files were unopened during the independent derivation and initial checks. Arithmetic, polynomial Euclidean/Sturm routines and dual-coordinate enumeration are credited to this reviewer's published REVIEW9984; its actual-thirteenth-point reconstruction is replaced here.

Let \(I=[14/25,593/1000]\). A code means a finite set of distinct unit vectors in \(\mathbb R^3\) with every distinct pair product at most \(t\). Require twelve distinct labels
\(0,1,2,4,5,6,7,8,9,10,11,12\) and precisely the following required contacts; additional contacts are permitted:

```
0-5 0-6 0-7 0-11 1-2 1-4 1-10 1-12 2-4 2-8 2-10
4-8 5-7 5-9 5-11 6-11 7-12 9-10 9-11 10-12 5-12
```

We independently establish that **at most two arbitrary additional code points exist** throughout closed \(I\). No actual thirteenth point, contact to such a point, added-point degree, face, cohort, location, support or optimizer hypothesis occurs in this argument.

## Exhaustive physical normalization

Put \(a=1+t,b=1-t,c=1+2t,r=2t/a\). Use the coefficient basis \((p_1,p_2,p_4)\), whose Gram matrix is \(H=bI+t\mathbf1\mathbf1^T\). Its eigenvalues are \(b,b,c>0\), so it is an actual basis. The coefficient metric is
\[
\langle u,v\rangle_H=b\sum u_jv_j+t(\sum u_j)(\sum v_j).
\]
For unit vectors \(u,v\) of product \(t\), a unit common neighbor with both products \(t\) has projection \(t(u+v)/(1+t)\) into their span. This projection has squared norm \(2t^2/(1+t)<1\). The remaining orthogonal line therefore gives exactly two points. If one is \(z\), the other is \(r(u+v)-z\). Distinct labels select the other point, without an orientation assumption. Accordingly
\[
p_8=r(p_2+p_4)-p_1,\quad p_{10}=r(p_1+p_2)-p_4,\quad p_{12}=r(p_1+p_{10})-p_2.
\]

The added contact 5–12 makes \((p_5,p_7,p_{12})\) equilateral. In this abstract equilateral basis the original triangles force
\[
p_0=r(p_5+p_7)-p_{12},\quad p_{11}=r(p_0+p_5)-p_7,
\quad p_9=r(p_5+p_{11})-p_0.
\]
Substituting, before referring to any extra point, gives
\[
p_9=r^2(r+1)p_5+r(r^2-2)p_7+(1-r^2)p_{12}.
\]
Taking product with \(p_{12}\) in the abstract equilateral metric proves
\[
d=p_9\cdot p_{12}=2Q/a^3-1,\qquad Q=1+3t-t^2-3t^3+8t^4>0.
\]
The positivity of \(Q=(1-t^2)(1+3t)+8t^4\) follows from \(0<t<1\). With \(L=1+2t-t^2>0\), the Gram discriminant of the two prescribed planes for \(p_9\) is exactly
\[
1-2t^2-d^2+2t^2d=16t^2b^2cL^2/a^6>0.
\]
The known normals \(p_{10},p_{12}\) are independent, so these planes meet the sphere in exactly two distinct points, with no remaining continuous freedom. The first is
\[
v=a^{-3}(2t(5t^2-1),(3t+1)(5t^2-1),-2ta(3t+1)).
\]
Its squared norm is one and its products with \(p_{10},p_{12}\) are \(t,d\). Put
\[
A=t(1-d)/(1-t^2),\quad B=(d-t^2)/(1-t^2),\quad v'=2(Ap_{10}+Bp_{12})-v.
\]
This is reflection across their span. The independent rational calculation verifies its unit and both plane identities, the orthogonal projection identities, and
\[
\|v-v'\|^2=4(1-2t^2-d^2+2t^2d)/(1-t^2)>0.
\]
It also verifies
\[
v'\cdot p_2-t=
\frac{(1-t)(5t^2-1)(1+7t+7t^2-7t^3)}{(1+t)^5}>0.
\]
Here \(5(14/25)^2>1\), and \(1+7t+7t^2(1-t)>0\). Thus the second candidate violates the mandatory packing inequality for distinct labels 2 and 9 on the whole closed interval. We must have \(p_9=v\).

The positive discriminant implies \(|d|<1\), since it equals \((1-t^2)(1-d^2)-t^2(1-d)^2\). The common-neighbor projection for product \(d\) is consequently defined. The distinct points \(p_5,p_{10}\), both having product \(t\) with \(p_9,p_{12}\), force
\[
p_5=2t(p_9+p_{12})/(1+d)-p_{10}.
\]
The chain then uniquely gives \(p_7\), because
\(r(r^2-2)<0\) and \(2-r^2=2L/a^2>0\). Finally the displayed reflections give \(p_0,p_{11}\), and \(p_6=r(p_0+p_{11})-p_5\).

This proves every realization is the rational twelve-point family up to an orthogonal isometry. `audit.py` derives it in the rational-function field from these reflections and both candidates; it never constructs a thirteenth point in `reconstruct`. Clearing by \(\Omega=a^5QL>0\) produces integral coefficient vectors \(Y_i=\Omega p_i\). Fifty-five generic rational identities check the complete normalization, twelve units, twenty-one contacts and two cap norms/margin. These are identities in \(\mathbb Q(t)\), not parameter samples.

## Complete cut-polytope bound in dual coordinates

Let \(K=\{y:\langle p_i,y\rangle_H\le t\}\). Add coefficient normals
\[
n_1=(-5,-14,20),\quad n_2=(-8,12,-5)
\]
and cuts \(\langle n_1,y\rangle_H\le15\), \(\langle n_2,y\rangle_H\le9\), obtaining \(C\). The origin is strictly feasible. Exact Cramer determinants prove \(p_0,p_4,p_9\) span and
\(\lambda_0p_0+\lambda_4p_4+\lambda_9p_9+p_{11}=0\) with all three \(\lambda\)'s strictly positive on closed \(I\). There are four strict polynomial sign checks. For a recession vector all four projections are nonpositive; their positive weighted sum is zero, so each vanishes. Spanning then gives zero recession vector. Thus \(K,C\) are bounded full-dimensional polytopes.

Our enumeration uses **dual variables** \(z=Hy\). Core rows are \(Y_i\cdot z\le t\Omega\). Cap rows are \(n_1\cdot z\le15\), \(n_2\cdot z\le9\), independently labeled 98,99 respectively. The squared physical norm is
\[
z^TH^{-1}z=\frac{c\sum z_j^2-t(\sum z_j)^2}{bc}.
\]
This is different from evaluating the original coefficient norm of the primal Cramer vector. Exact row identities check this interpretation.

Every vertex has some independent triple of active planes. All \(\binom{14}{3}=364\) triples are generated explicitly. The four identically singular triples are
\((0,2,5),(0,2,10),(0,5,10),(2,5,10)\). Every other triple has exact Cramer data \((D,W)\) with the whole identity \(M W=\mathrm{rhs}\,D\). A common polynomial factor can be canceled in these four components: identities are rechecked after cancellation. This cancellation introduces no physical vertex at a zero of the original determinant; that triple is simply not independent there, and another independent active triple covers any actual vertex.

For each triple we recursively cover closed \(I\) by dyadic closed cells. Each leaf proves either
\[
49bcD^2-50\{c\sum W_j^2-t(\sum W_j)^2\}>0
\]
or two inactive residuals \(\mathrm{row}_j\cdot W-\mathrm{rhs}_jD\) of opposite strict signs. The first yields physical norm squared less than \(49/50\) whenever the intersection is defined. In the second, the positive residual violates its plane if \(D>0\), while the negative residual violates its plane if \(D<0\). At \(D=0\) the triple cannot independently define a vertex. There is no sampled determinant branch selection.

The regenerated independent cover has 367 leaves: 31 norm leaves and 336 opposite-residual leaves, depth at most four. It generates **703 strict cap sign obligations**, and verifies the prefix-free property plus exact binary mass one of every complete cover. Closed cells retain every endpoint and shared subdivision boundary. The arithmetic uses a positive pseudo-remainder Euclidean algorithm and **Sturm variations at exact rational endpoints**, rather than the author's Bernstein/Taylor sign proof. Strict positivity requires positive values at both closed endpoints and zero root count. No float, solver, native certificate or target module is used.

Polynomial content and only powers of
\(t,1+t,1-t,1+2t,3t-1,3t+1,Q,L\)
are removed when checking signs; each is strictly positive on \(I\). In particular \(3t^2-1\) is never a canceled positive factor. Arbitrary common factors in Cramer components are handled as explained above, separately from positivity reductions. Incomplete coverage or a time limit is failure, not an exclusion.

Therefore every feasible vertex of \(C\) has squared norm less than \(49/50\). A bounded polytope is the convex hull of its finite vertex set. Convexity of the squared positive-definite norm proves this strict bound for **every** point of \(C\), not only its vertices.

## Two arbitrary points at most

Any unit vector avoiding all twelve core points lies outside \(C\), hence in one of the **open** caps \(\langle n_1,y\rangle_H>15\), \(\langle n_2,y\rangle_H>9\). Both cuts are positive and strictly below their normal norms. Their norm squares are
\[
\|n_1\|_H^2=621-620t,\qquad\|n_2\|_H^2=233-232t.
\]
For an open cap \(n\cdot u>B>0\), normalize the axis. Each unit vector makes angle strictly less than \(\arccos(B/\|n\|)<\pi/2\) with it. Two such vectors therefore have product strictly greater than \(2B^2/\|n\|^2-1\). This follows also directly by tangent-component Cauchy–Schwarz.

For the first cap this is at least \(881/1369>593/1000\). For the second cap compare **pointwise with the same \(t\)**:
\[
162-(1+t)(233-232t)=232t^2-t-71\ge747/625>0.
\]
The derivative \(464t-1\) is positive on \(I\); the left endpoint gives the minimum. Comparing the second cap's worst lower bound with the interval's largest \(t\) would fail, and the validation explicitly rejects this inference. Each cap holds at most one code point. Their union, even if overlapping, holds at most two. This proves the twelve-label capacity at most fourteen throughout closed \(I\).

## Credited exact feasibility and sharpness application

All 66 pairs of the reconstructed twelve core points are checked. Twenty-one are the prescribed equalities; forty-four other gaps are strictly positive on all of \(I\). After removing only positive factors the remaining 6–8 gap is exactly
\[
(3t^2-1)(23t^3+17t^2+t-1).
\]
The cubic is strictly positive throughout \(I\), including the interior critical value. Hence a core code exists precisely for \(t\ge1/\sqrt3\) within \(I\). At equality the extra contact 6–8 is allowed.

**Prior work:** REVIEW9984 already establishes uniform fourteen-point attainment for the stronger thirteen-label mask. Its construction automatically satisfies this weaker twelve-label mask. We rederive that construction, with explicit credit; this is not newly discovered sharpness. Only in `sharpness`, after the main twelve-row proof, introduce the optional unit vector
\[
x=((3t^2-2t-1),2t(1+3t),-2t(1+t))/(1+t)^2.
\]
All twelve comparisons pass; the three contacts are 2,9,10. The uncut dual vertex supported by 0,4,6 has a strictly negative determinant throughout \(I\), all other core and optional-x residuals positive in that determinant orientation, and exact norm excess with positive-factor reduction
\[
(3t^2-1)(23t^3+17t^2+t-1)(1+3t+16t^3+79t^4+77t^5).
\]
It is outside the unit ball above the threshold and on it at equality. Divide the primal vector by its norm. Because \(t>0\), radial contraction preserves each packing inequality: if the original product is negative it remains at most zero; if nonnegative it decreases. The new unit vector and optional \(x\) are distinct from all core points and each other, since every such product is at most \(t<1\). This proves attainment of fourteen for every feasible \(t\) in \(I\), including equality. The sample \(t=29/50\) also records exact rational dual coordinates and squared norm.

Thus combining the **newly audited weaker-mask upper bound** with **credited prior construction** classifies its conditional maximum: no realization below \(1/\sqrt3\), and maximum fourteen for all remaining \(t\) in \(I\). This is an inherited application, not new uniform-sharpness discovery or a global spherical-code bound.

## Routing and trust boundaries

Only the routing corollary imports committed lemma 9922: its finite-code two-branch theorem forces any fifteen-point original-G20 code on \(I\) into the undivided actual pentagon \((5,7,12,10,9)\), with all three additional points strictly in its complementary eleven-disk, once the 5–12 branch is excluded. This reviewer's prior REVIEW9950 confirms that parent. The current upper proof imports neither that result nor any physical cohort, degree, chart, triangle-tree, frame, occurrence or optimizer theorem. No wider interval is transported.

The ordinary geometry bridges—two-common-neighbor reflection, exhaustive sphere/two-plane intersection, packing branch pruning, recession criterion, vertex representation, convexity and the cap inequality—are supplied above and remain **unformalized**. The exact proof trusts CPython arbitrary-precision integers/Fraction and the displayed Euclidean/Sturm algorithm. Normal and optimized modes are corroboration of the same fresh reviewer program, not two independent reviewers. No historical priority clearance, whole original-G20 capacity, actual-pentagon arbitrary-three exclusion, fifteen-point optimizer occurrence or unconditional Tammes15 optimality is established.
