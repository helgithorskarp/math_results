# A fixed colouring extends across all 252 specified coupled heptagon–spindle sums

For the fixed heptagon set H of 21 points and aligned Moser spindle M of 7 points below, define

\[
 C=\{a\overline b:a\in\Delta_1H,\ b\in\Delta_1M\},\qquad
 X_r=(H+M)\cup(H+rM),\quad r\in C,
\]

where \(\Delta_1Y=\{y-y':y,y'\in Y,\ |y-y'|=1\}\). All differences in this definition are actual complex unit vectors. Let G(X) be the complete unit-distance graph on the distinct points of X.

**Exact computer-assisted theorem.** C has 252 elements, and every G(X_r) is exactly four-chromatic. There is one fixed four-colouring of G(H+M) that extends to every G(X_r), separately for each r. These 252 exact supports are distinct as subsets of the specified coordinate plane; no claim of252 isometry classes is made. They have 143–268 vertices and 512–1022 edges. Consequently every subgraph of any of these252 graphs is four-colourable.

This tests an actual union construction after the [continuous single-sum family was closed](../hadwiger_nelson_heptagon_moser_sum/ROTATION_FAMILY.md). Edges with one endpoint in each exclusive component are included. There are 420 such edge occurrences across the cohort, with a maximum of 40 in one placement. The theorem does not follow just by colouring the two components independently.

The result excludes this finite coupled family. It does not cover arbitrary relative rotations, larger unions, translated components, or a simultaneous extension to the union over several r. No five-chromatic graph with at most 508 vertices is established.

## Exact construction and the cohort

Use the embedding

\[
 t=e^{\pi i/21},\quad s=i\sqrt{11},\qquad
 L=\mathbb Q(t,s),\quad
 \Phi_{42}(t)=t^{12}+t^{11}-t^9-t^8+t^6-t^4-t^3+t+1=0.
\]

For j=0,...,6 define, in order, the 21 points

\[
 P_j=\frac{t^{6j}}{t^{24}-t^{-24}},\qquad
 Q_j=-\frac{t^{6j-7}}{t^6-t^{-6}},\qquad
 R_j=-\frac{t^{6j+7}}{t^{12}-t^{-12}}.
\]

Set u=Q_0−P_0, v=R_0−P_0, rho=(5+s)/6, and

\[
 M=(0,u,v,u+v,\rho u,\rho v,\rho(u+v)).
\]

The exact field and geometry derivations are in the [single-sum proof](../hadwiger_nelson_heptagon_moser_sum/PROOF.md) and [parent heptagon source](../hadwiger_nelson_heptagon_difference_lifts/geometry.py). H has 42 unit edges, and M has the 11 unit edges

```
01 02 04 05 12 13 23 36 45 46 56
```

The directed unit-difference sets have sizes 84 and 14. Their 1176 ratios give exactly 252 distinct unit rotations. This C is also the full collision-angle set of the single-sum map, as established in the [earlier collision theorem](../hadwiger_nelson_heptagon_moser_sum/COLLISIONS.md). That characterization explains the cohort choice; the present full-graph audit reconstructs C directly from unit differences and does not require importing the collision proof to establish the finite theorem.

The producer expands all 36 inherited representatives by each of the seven powers of t^6. The checker independently enumerates all 1176 unit-difference ratios and compares the resulting 252 angles entrywise as an exact set. **No C7 quotient is applied to the coupled configuration:** the first spindle remains fixed at orientation 1 throughout. Both components contain H, so the initial general bound is147+147−21=273 vertices. Exact reconstruction gives the stronger maximum268 here. The baseline H+M has 143 vertices.

## Fixed baseline and the certificate

Name the four colours by the elements 0,1,2,3 of the group \(\mathbb F_2^2\), with XOR as addition. Use the H row

```
0 1 0 2 0 1 3  1 3 3 0 2 2 0  2 2 1 1 3 0 2
```

and the baseline M row

```
0 1 2 3 1 2 0
```

For every r the [791-byte certificate](certificate.json) specifies one of nine seven-entry rows q_r. On the 294 formal labels of the two components prescribe

\[
 c(h_i+m_j)=p_i\mathbin{\mathrm{XOR}}q_{0,j},\qquad
 c(h_i+r m_j)=p_i\mathbin{\mathrm{XOR}}q_{r,j}.
\]

The checker proves that all formal representations of any one geometric point receive the same colour, including coincidences between components. It then checks the colour inequality on **every** exact unit edge of the union. This establishes a well-defined proper colouring and a fixed restriction to H+M. The H row is an explicit witness; no completeness assumption about a library of H colourings is used.

Every union contains P_0+M. The checker reconstructs its embedding and rejects all 81 normalized three-colour assignments for M: the triangle 0,1,2 may be fixed to colours 0,1,2 without loss of generality. Hence chi(G(X_r)) is at least4, completing the equality. Restricting a proper colouring proves the subgraph corollary.

## Exhaustiveness and independent arithmetic

[build.py](build.py) generates all distinct points using exact coefficient arithmetic in the 24-dimensional basis t^i s^j, 0≤i<12 and j∈{0,1}. It tests every unordered point pair. Two validated homomorphisms to finite fields reject pairs whose squared distance cannot be 1. All surviving pairs are checked exactly in L. The producer encounters four modular false positives and correctly rejects all four in exact arithmetic. The checker encounters none with its different maps.

[check.py](check.py) imports neither the producer nor its field or graph functions. It constructs the factors in the tensor basis

\[
 \zeta^a\omega^b w^c,\quad 0\le a<6,\ b,c\in\{0,1\},\qquad
 \zeta^6=-\sum_{j=0}^5\zeta^j,\quad \omega^2=\omega-1,\quad w^2=w-3,
\]

with t=\(\zeta^6\omega\), s=2w−1. Its arithmetic dependencies are [audit.py](../hadwiger_nelson_heptagon_moser_sum/audit.py) and [contacts_audit.py](../hadwiger_nelson_heptagon_moser_sum/contacts_audit.py). It uses different finite fields and exact norm checks on all survivors. Field maps are used only for sound rejection: a nonzero image proves a norm residual is nonzero, while a zero image proves nothing until the exact check.

The audit independently reconstructs every support, all 294 formal labels per case, every full edge list, the component intersections, and every edge outside both component-induced graphs. It compares full lists, not just counts or hashes. It verifies every colour inequality and every spindle embedding, and exercises six rejection controls for malformed or invalid witnesses. These are separate implementations run by the author; external review of this new coupled theorem is pending. The inherited collision and unit-contact work has an [accepted separate-author review](../hadwiger_nelson_heptagon_moser_sum_collisions_review1/README.md).

## Reproduce

From the repository root, with Python 3.11.2, standard library only, and assertions enabled:

```bash
python3 -B hadwiger_nelson_heptagon_coupled_sums/build.py --out /tmp/hn-coupled-252
python3 -B hadwiger_nelson_heptagon_coupled_sums/check.py --work /tmp/hn-coupled-252
```

The output directory must not already exist. The complete graph files and rotation stream are regenerated locally. They are omitted from publication; the public certificate, expected totals and validation record are compact. Hashes identify the streams actually compared:

- Certificate SHA256: `68e7ee26a8605ad972b253f31d408fc0e83c4f26f6f5074170cc791766ee9564`.
- Ordered full graph stream SHA256: `146101cd89354af5d9af1f38910937cc30a1f6b572e59b4bd58af1fe9cae702b`.
- Ordered rotation stream SHA256: `2bc467e998fc638691a78cb327350606dfb0e2a840bea3592afc2dfada766d8b`.

[expected.json](expected.json) gives the complete 22-row histogram of vertices, edges, exclusive cross-edges, intersection size and rotation count. Both implementations scan 8,786,736 point pairs. The checker verifies 74,088 formal representations and 247,878 edge-colour inequalities, including all 420 new cross-edge inequalities. Generation took 49.998 seconds and the audit 68.080 seconds, each using one thread; peak memory was not measured. See [validation.json](validation.json) for dependency hashes and audit totals. The exploratory prototype and producer also agree entrywise on all 252 complete graphs. No native solver, floating-point geometric predicate, unfinished certificate or background search is involved.

## Campaign decision and source calibration

End this 252-angle two-component cohort and its deletion-only subfamilies. The common baseline extension removes a proposed obstruction caused by incompatible restrictions on the shared H or on the full baseline sum. It leaves a distinct possible mechanism: constraints between several attached components may prevent their separate extensions from coexisting. Such a construction would require a new bounded phase and full new edge reconstruction. It has not been started here; this theorem supplies no conclusion about it.

The source geometry comes from Section 2 of [Haugland's August 2026 manuscript](https://arxiv.org/html/2608.04542v4). That manuscript still identifies 509 as the record; [Parts's primary paper](https://arxiv.org/abs/2010.12665) gives 509 vertices and 2442 edges. Both sources were checked live on 2026-09-06. The present result is a finite family exclusion in the alternative geometric lane, separate from HN2's [H517 deletion certificates](../hadwiger_nelson_heule517_large3/README.md). The general record problem remains open.

The final shared-work refresh inspected HN2 source `6dcd0080ce1004ab86d743ce9498a9a065e0ccd9`, Discovery Net height 3136. Its three-large/six-small H517 family is closed; any remaining H517 obstruction on at most 508 vertices must retain at least 137 small vertices and omit at least four large vertices. The order restriction is essential. This result supplies no mathematical premise for the coupled geometric theorem.

## Completed simultaneous follow-up

The subsequent [six-triple gluing theorem](TRIPLE_GLUING.md) proves that the five explicit rotations 1, eta*rhobar, eta, etabar*rhobar and etabar admit a common colouring. Their whole union has 513 vertices and 2,097 edges and is four-chromatic. All its subgraphs are four-colourable. This closes the selected compatibility test without asserting a result for arbitrary multi-component unions.
