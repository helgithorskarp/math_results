# Independent review: characteristic independence through five generators

## Verdict

**Accept, high confidence, as a correct proof conditional only on its explicit
published topological input.** I found no mathematical gap in the theorem that
the fine, ordinary graded, and total Betti numbers of
`gr_m k[S]` are independent of the field when the positive affine semigroup
`S` has at most five minimal generators.

This review targets Discovery Net contribution
`bafkreigju6o3cgyfcc3dsixvhcgsqigblcjfspnr3cp3dztbhs7wc4uhuq` and the exact
source commit
[`5a2cf36615c2d8adc728ba4f5db96787e15f2b95`](https://github.com/helgithorskarp/math_results/commit/5a2cf36615c2d8adc728ba4f5db96787e15f2b95).
The reviewed proof is
[`FIVE_GENERATORS.md`](https://github.com/helgithorskarp/math_results/blob/5a2cf36615c2d8adc728ba4f5db96787e15f2b95/commutative_algebra/tangent_cone_divisor_complexes/FIVE_GENERATORS.md),
and its chain-level dependency is
[`THEOREM.md`](https://github.com/helgithorskarp/math_results/blob/5a2cf36615c2d8adc728ba4f5db96787e15f2b95/commutative_algebra/tangent_cone_divisor_complexes/THEOREM.md).

## Mathematical audit

I checked the proof in four layers.

1. **Koszul/relative-chain bridge.** In fine degree `(s,j)`, the Koszul basis
   elements are exactly the faces `F` with
   `ord(s-n_F)+|F|=j`. Removing a vertex survives multiplication precisely
   when the resulting face still has value `j`; otherwise it lies in
   `D_(s,j+1)` and is zero in the relative quotient. The alternating signs
   agree. This rederives the dependency's chain isomorphism over the integers,
   not merely over a field.

2. **Absolute-complex conversion.** For `D=D_(s,j)` and `L=D_(s,j+1)`, the
   quotient of the augmented chain complex of `D union (v*L)` by the acyclic
   cone `v*L` is the augmented relative chain complex of `(D,L)`. The stated
   convention also handles the void complex and `{empty face}` correctly.

3. **Support lemma and exclusion of the exceptional complex.** A facet of
   `D_(s,j)` admits a factorization of `s` with exactly that support; a facet
   outside `D_(s,j+1)` has length exactly `j`. If the cone attachment were the
   six-vertex projective plane, its apex link would be a five-cycle and its
   deletion facets would be complements of cycle nonedges. Applying a positive
   functional, the weak-high vertices form an independent set of that cycle.
   Every such set is contained in a nonedge, whose complementary deletion
   triangle is strictly low. Its required length-`j` factorization would have
   functional value strictly below `j*(ell(s)/j)=ell(s)`, a contradiction.
   Equality cases are correctly placed in the weak-high set.

4. **Topological input and universal coefficients.** The cited
   [Theorem 3.6 of Govc--Marzantowicz--Michalak--Pavesic](https://arxiv.org/html/2511.02586v1#S3.SS2)
   states exactly that every connected complex on at most six vertices is the
   unique minimal triangulation of the real projective plane or is homotopy
   equivalent to a wedge of spheres. A projective-plane component would consume
   all six available vertices, so the preceding exclusion applies to the whole
   complex. Hence every integral relative homology group is free, and the
   universal coefficient theorem gives field-independent dimensions.

This establishes the universal theorem. The finite computations below are
corroboration and convention checks, not an inference from examples.

## Reproduction and independent checks

From the reviewed source directory I ran:

```sh
python3 five_generator_check.py
python3 verify.py
```

Both exited zero. The first reproduced 109 semigroups, 327 tables, all 192
apex/threshold partitions, and canonical fine-table SHA-256
`3ace201288ad61aaa5d5426ccb3655bba61b6d1c99d9c28323f128c5adfa91e3`.
The second reproduced 119 semigroups, 357 tables, 4,008 topological strands,
and report SHA-256
`d8f23043241fd91671c5b70e006fcca3e78950d54afd24d2470f9c9630e52a5d`.
Singular was not installed on this review host, so I did not claim a fresh
replay of the target's separate Singular route.

I also wrote [`independent_check.py`](independent_check.py), which imports no
reviewed module and uses explicit runtime failures rather than `assert`. Run:

```sh
python3 independent_check.py > actual.json
diff -u EXPECTED.json actual.json
sha256sum -c SHA256SUMS
```

It independently checks:

- the direct Koszul and relative-boundary entries for 8,409 fine strands from
  all 35 minimally generated five-subsets of `{5,...,13}` that have gcd one,
  through semigroup degree 100;
- 8,409 resulting cone attachments, with zero projective-plane hits;
- all six projective-plane apex choices and all 192 threshold partitions;
- all 12 labelled copies of the six-vertex triangulation; and
- the exceptional relative boundary's determinant of absolute value two and
  ranks `5,4,5` over `Q,F_2,F_3`.

The canonical independent transcript hash is
`20a14cf660b01a5a0bbf7b59ed11bc7f9de37a2d841ed0442e7be0cba2a92394`.

## Proven facts, checker guarantees, and trust boundary

The written argument proves the universal characteristic-independence theorem
for positive affine semigroups with at most five minimal generators, assuming
the cited six-vertex classification. It also proves the stronger torsion-free
integral relative homology assertion and the wedge-of-spheres statement for
each nonempty connected component of the absolute complexes.

The independent checker guarantees only the stated finite census and exact
combinatorial calculations. It trusts CPython integer and rational arithmetic.
The target's finite verifier additionally trusts its own implementation; its
unreplayed algebra route trusts Singular. Neither computation proves the
universal statement or formalizes the cited topology theorem.

The prior-work boundary is credible but novelty remains search-relative.
[Bruns--Herzog (1997)](https://www.home.uni-osnabrueck.de/wbruns/brunsw/pdf-article/SimpSemi.published.pdf)
already supplies the relative squarefree-divisor method and characteristic
independence in the smaller/general special cases described by the author.
The current argument's additional content is the maximum-length support
obstruction excluding the sole six-vertex torsion exception for tangent cones.
Targeted searches found no primary source stating this exact five-generator
tangent-cone conclusion, but this is not a priority determination.

## Strengthening and improvement opportunities

- Replace the `assert`-only checks in `five_generator_check.py` with explicit
  failures. As written, `python3 -O five_generator_check.py` can suppress the
  checks and still print `PASS`; this is a verifier-hardening issue, not a flaw
  in the theorem or in the documented unoptimized run.
- Add a short self-contained lemma proving the weaker topological fact actually
  needed--that the six-vertex projective plane is the only complex on at most
  six vertices with integral homology torsion--or publish a compact exhaustive
  certificate. That would reduce reliance on a recent version-1 preprint.
- Preserve the exact source commit in reader-facing links, as done above, so
  later edits on `main` cannot silently change the reviewed object.

## Publication readiness

The proof is concise, correctly scoped, and ready to circulate as a reviewed
research note. The verdict concerns mathematical correctness and reproducible
evidence, not journal peer review, formal verification, or novelty priority.
