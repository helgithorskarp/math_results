# Every four-colouring of H extends to H+M+M

For the fixed 21-point heptagon set H and aligned seven-point Moser spindle M specified below, set N=M+M and Z=H+N. Graphs on point sets always include **every** Euclidean unit-distance edge.

**Exact computer-assisted theorem.** N has 26 vertices and 69 unit edges. Z has **522 vertices and 2,436 unit edges**, and is exactly four-chromatic. More strongly, **every proper colouring of H with the palette {0,1,2,3} extends to a proper colouring of Z**. Equivalently, restriction from four-colourings of Z to four-colourings of the embedded H is surjective.

Thus this enlargement imposes no new four-colour constraint on H. Every subgraph of Z is four-colourable. In particular, all 210 specified target supports

\[
 Z_{ij}=(H\setminus\{h_i,h_j\})+(M+M),\qquad 0\le i<j<21,
\]

are four-colourable. They are distinct supports with 470–494 vertices. Each contains a spindle, so each is exactly four-chromatic. This closes these candidates and all their vertex- or edge-deleted subgraphs. No five-chromatic graph on at most 508 vertices is established.

The theorem concerns these exact factors and this double sum. It does not cover rotated or translated second summands, a third spindle sum, changed hosts, or arbitrary enlargements.

## Exact coordinates and why the cohort fits the target order

Use t=e^(pi i/21), s=i sqrt(11), with

\[
 \Phi_{42}(t)=t^{12}+t^{11}-t^9-t^8+t^6-t^4-t^3+t+1=0,
 \qquad s^2=-11.
\]

The 21 H points are ordered P_0,...,P_6,Q_0,...,Q_6,R_0,...,R_6, where

\[
 P_j=\frac{t^{6j}}{t^{24}-t^{-24}},\quad
 Q_j=-\frac{t^{6j-7}}{t^6-t^{-6}},\quad
 R_j=-\frac{t^{6j+7}}{t^{12}-t^{-12}}.
\]

Set u=h_7−h_0, v=h_14−h_0, rho=(5+s)/6, and order

\[
 M=(0,u,v,u+v,\rho u,\rho v,\rho(u+v)).
\]

H has 42 unit edges. The unit graph of M has the 11 edges

```
01 02 04 05 12 13 23 36 45 46 56
```

The [inherited field proof](../hadwiger_nelson_heptagon_moser_sum/PROOF.md) justifies the injective 24-coefficient representation in Q(t,s), and the [parent geometry source](../hadwiger_nelson_heptagon_difference_lifts/geometry.py) fixes H exactly.

There are 28 unordered spindle pairs with repetition. Their only nontrivial equality classes are

\[
 m_0+m_3=m_1+m_2,\qquad m_0+m_6=m_4+m_5.
\]

Hence N has exactly 26 points. Even the two displayed relations alone give the a priori bound |N|≤26. Omitting two H points therefore gives |Z_ij|≤19 times 26=494, before any favourable geometric coincidences are counted. This defines the bounded 210-case target cohort independently of a search result.

The full H+N support was checked first because any proper colouring of it restricts to every target. The test changes the Minkowski factor from one spindle displacement to the sum of two. Its 522-point support is not the previously closed [513-point five-orientation union](../hadwiger_nelson_heptagon_coupled_sums/TRIPLE_GLUING.md).

## Universal extension proof

Represent the four colours by F_2 squared, with XOR as addition. Fix the spindle row

```
q = 0 1 2 3 2 3 1
```

The prescription

\[
 \psi(m_a+m_b)=q_a\mathbin{\mathrm{XOR}}q_b
\]

is well-defined on N, is proper on all 69 of its unit edges, and has psi(0)=0. These facts are verified on all ordered representations and the complete exact N graph.

Let p be any proper four-colouring of H. The H labels 0,7,14 form a unit triangle, so their colours are distinct. Relabel the palette so that

\[
 p_0=0,\quad p_7=1,\quad p_{14}=2.
\]

We claim that

\[
 c(h_i+n)=p_i\mathbin{\mathrm{XOR}}\psi(n)
\]

is a proper colouring of Z. The exact geometry audit establishes:

1. The 546 formal H+N pairs form 522 geometric points: 505 singleton fibres, ten double fibres and seven triple fibres. **Every H label in a nontrivial fibre belongs to {0,7,14}.** Thus all coincidence conditions use only the three normalized colours, not the other 18 entries of p.
2. Exactly 2,434 unit edges are images of factor edges: a unit H edge with a fixed N point, or a unit N edge with a fixed H point. These are properly coloured for any proper p, by cancellation in XOR and properness of psi.
3. There are exactly two additional unit edges. All their H labels belong to {7,14}, so their colour inequalities also use only the normalized triangle.

Explicit formal representatives for those two edges are

\[
 \{h_7+2m_5,\ h_{14}+m_2+m_4\},\qquad
 \{h_7+m_1+m_5,\ h_{14}+2m_4\}.
\]

With the displayed q row their endpoint colours are respectively {1,2} and {3,2}. The audited witness verifies consistency on every nontrivial fibre. Because those fibres use only the normalized triangle, the consistency holds for every p with the three displayed values. All factor edges are proper by item 2 and the two extra edges by item 3. The prescription is therefore well-defined and proper for every such p.

Since psi(0)=0 and M contains 0, H is embedded in Z and c restricts to p there. Finally undo the initial palette permutation. A palette permutation need not preserve XOR: the construction is made after normalization and the inverse permutation is applied only to the finished proper colouring. This proves surjectivity for arbitrary original colour names.

For a concrete full-graph certificate, the [90-byte JSON witness](certificate.json) supplies q together with

```
p = 0 1 0 2 0 1 3  1 3 3 0 2 2 0  2 2 1 1 3 0 2
```

No completeness assumption about the earlier H-colouring library is used. The universal statement follows from the support of the exact coincidence and extra-edge constraints, not enumeration of all H colourings.

Every Z_ij contains h+M for any retained h, because 0 belongs to M. The checker verifies a spindle embedding in each restriction and rejects all 81 normalized hypothetical three-colourings of M, fixing its triangle 0,1,2. This gives the lower bound four for the full graph and every target support. Upper bounds follow by restriction of the full colouring.

## Exact target census

Omitting a host label removes a summand family, not necessarily all global vertices in that family: a point may still have a representation using another retained H label. Both implementations construct the retained geometric supports correctly and compare them entrywise.

| Vertices | Unit edges | Omitted H pairs |
|---:|---:|---:|
| 470 | 2,090 | 120 |
| 470 | 2,116 | 33 |
| 482 | 2,174 | 32 |
| 482 | 2,188 | 4 |
| 487 | 2,207 | 16 |
| 487 | 2,216 | 2 |
| 494 | 2,259 | 2 |
| 494 | 2,269 | 1 |

All 210 supports are distinct as subsets of the specified coordinate plane. No claim about the number of isometry classes is made. The exact support/edge stream is regenerated locally rather than published as a bulky exhaustive dump.

## Reproduction and trust boundary

[build.py](build.py) generates the full point set and all unit edges in the t,s basis. Its two validated finite-field homomorphisms reject pairs only when their norm residual cannot be zero. All survivors are checked exactly. It then produces the colour certificate, structural constraint support and all 210 restriction graphs.

[verify.py](verify.py) imports neither the producer nor its field arithmetic. It uses the earlier independent tensor basis zeta^a omega^b w^c, with zeta a primitive seventh root, omega squared=omega−1 and w squared=w−3. The conversions are t=zeta^6 omega and s=2w−1. Arithmetic comes from [audit.py](../hadwiger_nelson_heptagon_moser_sum/audit.py) and [contacts_audit.py](../hadwiger_nelson_heptagon_moser_sum/contacts_audit.py).

The new checker uses **no modular distance filter**. It computes all 135,981 full-support pair norms directly in characteristic zero, reconstructs and compares the complete edge list, and checks all 1,029 ordered H+M+M labels and all 546 H+N labels. It independently enumerates the 28 unordered M pairs, compares their equality classes, verifies the normalized-triangle support of every nonfactor constraint, and checks psi on all 69 N edges.

It reconstructs every target support from its retained exact coordinates and compares all 210 vertex and edge lists entrywise. The full witness has 2,436 edge checks; its target restrictions add 445,479 checked inequalities. Five controls reject malformed incidences, invalid or truncated colour rows and an improper full colouring. The prototype and final producer also agree entrywise on the full graph and colouring.

From the repository root, with Python 3.11.2, standard library only, assertions enabled:

```bash
python3 -B hadwiger_nelson_heptagon_double_spindle/build.py --out /tmp/hn-double-spindle
python3 -B hadwiger_nelson_heptagon_double_spindle/verify.py --work /tmp/hn-double-spindle
```

The output directory must be new. Generation took 1.039 seconds and the direct audit 43.427 seconds, each on one thread; peak memory was not measured. Compact expected results are in [expected.json](expected.json); versions and dependency hashes are in [validation.json](validation.json). Full graphs, the restriction stream, exploratory output and logs stay local and regenerate from source. No native solver, negative proof trace or floating-point geometry is used.

- Certificate SHA256: `e78e84aa92418bc110d7826fc32705587e71086b40fae777c0e32fbfc1ce20bc`.
- Full graph SHA256: `2f86b31bcc3741f9facc89ea484648ee08267722cb6e6c6ab8f91e3338638806`.
- Restriction stream SHA256: `bda4ff683b21fc880bcd97ac867cb55671ce8896f74092518f0fda372a284088`.

The new claim relies on the injective exact field model, Python integer arithmetic, finite-loop completeness, faithful decoding, and the stated universal-extension argument. Separate implementations were run by the author; external review of this new theorem is pending. The [accepted single-sum review](../hadwiger_nelson_heptagon_moser_rotation_family_review1/README.md) validates inherited geometry and its original scope, not the new double-sum theorem.

## Decision and shared context

This fixed aligned double-spindle sum and all its subgraphs are closed. It also fails as a gadget for imposing a new four-colour restriction on H, because every H colouring extends. A further construction should justify how it escapes this surjective extension before another nearby sum is enumerated. No third spindle sum, new host size, translated or rotated second factor, or next solver phase has begun. The bounded milestone is complete.

HN2's separate [H517 whole-support reduction](../hadwiger_nelson_heule517_whole_cover/README.md), source `d593c9ae774d6b296f73aa4a2c71f55158bde776`, was inspected at Discovery Net height 3162. Its 39,453 library residuals are unresolved target graphs, not known obstructions, and provide no premise here. The prior [four-large closure review](../hadwiger_nelson_heule517_large4_review1/README.md) at source `f93567218dc046d2c22d068fd15741e85ff63e4e` was also inspected. The lanes remain separate.

[Parts's primary paper](https://arxiv.org/abs/2010.12665) gives the 509-vertex record, also identified as current by [Haugland's August 2026 manuscript](https://arxiv.org/html/2608.04542v4), whose Section 2 supplies H. Both sources were checked live on 2026-09-06. This family exclusion does not improve the record.
