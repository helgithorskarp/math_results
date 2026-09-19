# Independent review: the eighteen-vertex Charney--Davis reduction

## Verdict

**ACCEPT, high confidence.** I independently reconstructed the proof that every
finite flag generalized homology 5-sphere on 18 vertices has a vertex of
one-skeleton degree at least 14, and that if the maximum degree is exactly 14,
at least nine vertices have degree 14. I found no mathematical or source error.

The reviewed source is commit
[`b6bd0ee2789ee17b6293e60472518eb1d7e2444a`](https://github.com/helgithorskarp/math_results/tree/b6bd0ee2789ee17b6293e60472518eb1d7e2444a/charney_davis_18_nine_high_degree).
Its intended Discovery Net lemma is
`bafkreibfyvnr7lfkqod4wcabenso4ovmgz2qy65a3nhtklruqmnmf5ikye`.
At review time that reference was still an uncommitted CheckTx receipt, so this
review does not call it committed graph evidence.

The conclusion is a necessary structural reduction, not the full
eighteen-vertex Charney--Davis inequality. It does not establish the existence
of a negative example, and it does not assert that nine is sharp.

## Independent reconstruction

Let `H` be the complement of the one-skeleton, let `q_v=deg_H(v)`, let
`m=|E(H)|`, and let `T` count triangles of `H`. Put

```text
a=gamma_2(Delta),  b=gamma_3(Delta),
L_v=gamma_2(lk_Delta(v)).
```

I checked the following steps without importing the target checker.

1. A vertex link is a flag homology 4-sphere on `17-q_v` vertices, so the
   cross-polytope lower bound gives `1<=q_v<=7`. Inclusion--exclusion on
   independent triples in `H`, followed by coefficient extraction, gives

   ```text
   a=39-m,
   b=230+(1/2) sum_v q_v(q_v-11)-T,
   S:=sum_v L_v
    =846+(1/2) sum_v q_v(3q_v-37)-3T.                 (1)
   ```

2. If `N_H(u)` and `N_H(v)` are disjoint and `uv` is not an edge of `H`,
   direct counting in the vertex and edge links gives

   ```text
   L_v=a+8+q_v(q_v-19)/2+sum_{x in N_H(v)}q_x-t_v,   (2)
   E_uv=L_u+L_v-a+(q_u-1)(q_v-1)-z_uv.               (3)
   ```

   Here `t_v` counts edges inside `N_H(v)`, `z_uv` counts edges between the
   two neighborhoods, and `E_uv=gamma_2(lk_Delta(uv))`. The checker proves
   (2)--(3) as equalities of affine forms, rather than testing them on sampled
   graphs.

3. Davis--Okun gives `E_uv>=0` for rational homology 3-spheres. Also, applying
   it to all vertex links of a flag homology 4-sphere `Y` and using
   `sum_x gamma_2(lk_Y(x))=2 gamma_2(Y)` gives `L_v>=0`. The normalization is
   `gamma_2(Y)=8 sum_x kappa(lk_Y(x))`.

4. If all `q_v>=4`, (1) gives `S<=846-18*50=-54`, so the minimum complement
   degree is at most three. If it is three, write `n_j=#{v:q_v=j}`. Then

   ```text
   S=90-8n_4-13n_5-15n_6-14n_7-3T >= 0.             (4)
   ```

   Equation (4) and degree-sum parity first force `n_3>=8`. When `n_3=8`,
   exact enumeration leaves only

   ```text
   3^8 4^8 5^2, T=0;
   3^8 4^9 6,   T=0 or 1;
   3^8 4^10,    0<=T<=3.
   ```

   Every one has `b<0`.

5. The `3^8 4^9 6` profile fails immediately: at the sextic vertex (2) has
   upper bound `-25+6*4=-1`.

6. In the `3^8 4^8 5^2` profile, triangle-freeness and (2) force the two
   quintic vertices to be adjacent, their quartic neighborhoods to partition
   the eight quartic vertices, and the cubic--quartic edges to form a perfect
   matching. All `L_v` vanish. Choosing a matched cubic/quartic pair across
   the partition forces `z>=3`, so (3) gives `E<=2-z<=-1`.

7. In the `3^8 4^10` profile, let `J=H[C]` on the eight cubic vertices.
   Formula (2) implies that each quartic vertex meets at most one cubic vertex
   and that no mixed triangle exists. Thus `|E(J)|>=7`. A triangle component
   contradicts (3). A 4-cycle would make a vertex of a cubic vertex-link have
   complement degree at most one, making that link a cone or suspension; the
   suspension case is excluded by Labbé--Nevo because `b<0`. If a vertex had
   degree three in `J`, four remaining vertices would have degree sum 12 but
   girth and the attachment restriction bound it by `2*3+4=10`.

   Therefore `J` has maximum degree two, girth at least five, eight vertices,
   and at least seven edges. Its only component types are

   ```text
   P8, C8, C7+P1, C6+P2, C5+P3.
   ```

   Each contains two degree-two vertices with disjoint neighborhoods. For
   that pair, (3) gives `E<=1+1-7+4=-1`, the final contradiction.

These contradictions prove at least nine complement-degree-three vertices
when the minimum is three. Translating back to the one-skeleton proves the
stated theorem. The join `C6*C6*C6` has complement degree sequence `3^18`, so
the maximum-degree-at-least-14 part is sharp.

## Published-input and coefficient-field audit

The source uses the following results with their hypotheses intact:

- Davis--Okun, Theorem 11.2.1, proves the needed nonnegativity for flag
  rational homology 3-spheres:
  https://arxiv.org/abs/math/0102104
- Labbé--Nevo, Lemma 2.1, Lemmas 3.2 and 3.4, and Theorem 3.5 supply the
  induced-link facts, antipode cases, and suspension/join structure:
  https://arxiv.org/abs/1612.01169

The theorem is stated over an arbitrary coefficient field. This is valid.
For every finite face link, vanishing lower homology over the stated field
forces all lower integral free ranks to vanish. Euler characteristic is
coefficient-independent, so the top rational Betti number is one. Thus every
link needed by Davis--Okun is a rational homology sphere. This argument does
not assert that integral torsion vanishes.

Targeted live searches on 19 September 2026 found no primary source stating
this eighteen-vertex refinement. That supports only search-relative novelty,
not a historical-priority claim.

## Strengthening and improvement opportunities

1. **Next theorem, now available but not reviewed here.** The subsequent
   `charney_davis_18_ten_high_degree` package claims to exclude exactly nine
   cubic complement vertices, strengthening nine to ten degree-fourteen
   vertices. Its new external boundary is the Labbé--Nevo classification of
   12-vertex flag homology 4-spheres with gamma-polynomial `1+2t`. A separate
   review must reconstruct that classification bridge and all eight new
   degree profiles; this verdict does not extend automatically to it.
2. **Higher assurance, feasible.** Formalize identities (1)--(3), the degree
   profile enumeration, and the coefficient-field bridge in Lean. The main
   value would be narrowing the remaining trust to Davis--Okun and the cited
   structural topology results, not strengthening the numerical bound.
3. **Broader frontier, conjectural.** Any move from ten high-degree vertices
   toward the full eighteen-vertex Charney--Davis inequality needs a new
   invariant for complement graphs with at least ten cubic vertices. The
   present degree moment alone grows less restrictive there; a useful next
   lemma would combine edge-link nonnegativity with an attachment or
   classification constraint that is stable across those profiles.

## Reproduce the independent audit

CPython 3.11, standard library only:

```sh
python3 verify_review.py > /tmp/charney18-review.json
cmp EXPECTED.json /tmp/charney18-review.json
python3 -O verify_review.py > /tmp/charney18-review-opt.json
cmp EXPECTED.json /tmp/charney18-review-opt.json
sha256sum -c SHA256SUMS
```

The code uses exact integer affine forms and complete finite enumeration.
It does not import the target package, use randomness, call a solver, or use
floating point. The topological inputs and the prose implications remain a
human proof obligation; the script is an independent audit of the algebra and
finite combinatorics, not a homology-sphere recognizer or formal proof.
