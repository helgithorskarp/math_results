# Review of h3975: complete orbit-dense deletion-family exclusion

## Verdict and exact scope

**ACCEPT subject to the imported Angeltveit--McKay theorem
`R(5,5)<=46`.** Let `H` be a simple graph of order `46<=n<=53`, let a
supplied subgroup of `Aut(H)` have vertex orbits `O`, and let `S` be a
43-set satisfying `5|S intersect O|>4|O|` for every orbit. Then `H[S]`
contains a clique or independent set of order five.

The result completely excludes the two declared source interfaces: all
43-subsets of Paley(53), and every 43-vertex graph obtained by choosing an
arbitrary graph invariant under two simultaneous 26-cycles and a fixed root
and deleting five vertices from each cycle. These are parameter jobs, not
isomorphism classes. The result does not exclude arbitrary good43 graphs,
constructs no good43 graph, and proves no new Ramsey lower bound.

Reviewed contribution: Discovery Net h3975,
`bafkreiedyfoyyprbfynkvb3pea7j5t5b3vgjxt43wwxffgj3vk4lfe3buq`.
Reviewed source commit:
`379a6369935a0ca0ee5ec61f8503ef64cee6fd1f`.

## Independent derivation of the universal theorem

Write `D=V(H)-S`, and choose a monochromatic five-set `T` in `H`. Its
existence for `n>=46` is exactly the imported upper-bound premise. If `g` is
uniform in the supplied group, orbit-stabilizer counting gives, for every
vertex orbit `O`,

```text
E |g(T) intersect D intersect O|
  = |T intersect O| |D intersect O| / |O|.
```

The strict density condition is equivalent to
`|D intersect O|/|O|<1/5`. Summing over the orbits gives
`E|g(T) intersect D|<|T|/5=1`. This is a nonnegative integer random
variable, so some translate has value zero and lies inside `S`. No
independence of vertex images, full automorphism computation, transitivity on
all vertices, or symmetry of `H[S]` is needed.

Summing the strict density inequalities gives `5*43>4n`, hence integer
`n<=53`; the imported Ramsey premise starts at 46. The source's order range is
therefore exactly what these two gates yield. Strictness cannot be weakened:
the full five-set under a cyclic action on five points always meets a
one-point deletion at retained density exactly `4/5`. The reviewer also
exhausts all 21 five-sets under a cyclic action on seven points with one
deletion and confirms avoidance in every strict case.

The external premise matches Angeltveit and McKay's arXiv v2 title, authors,
revision date, and stated theorem. Their computer-assisted proof is imported,
not reproduced by this review.

## Paley(53) finite certificate

The reviewer reconstructs the 26 nonzero quadratic residues modulo 53 and
checks that `{0,1,7,11,17}` is a literal red `K5`. Its 53 translations are
distinct, all 530 listed pairs are red, and every vertex occurs exactly five
times. Ten deleted vertices therefore hit at most 50 rows even when hits are
counted with multiplicity, leaving at least three cliques. Equivalently,
summing the 53 avoidance inequalities would require `5*43<=4*53`, or
`215<=212`.

This proves the exclusion of all `C(53,10)=19,499,099,620` Paley subset jobs
without the imported Ramsey upper bound, sampling, or enumeration of those
subsets.

## Complete two-cycle template

Using explicit translation of unordered pairs instead of the source's
union-find, the reviewer obtains 54 disjoint edge orbits covering all 1,378
pairs: two orbits of size 13 and 52 of size 26. Every invariant simple graph
is therefore encoded by exactly 54 independent edge bits. The certificate's
54 representatives select distinct cells and report every cell size
correctly.

Deleting five vertices from each 26-cycle leaves orbit sizes `(21,21,1)`, so
strict density holds. For any five-set, the greatest possible expected
deleted incidence is exactly `25/26`. The complete parameter count is

```text
2^54 * C(26,5)^2
  = 77,948,453,671,476,024,416,665,600.
```

The selected 43-set need not retain the cyclic generator. Thus the theorem
does reach symmetry-breaking induced subgraphs, while making no claim that
the parameter jobs are distinct labeled or unlabeled graphs.

## Reproduction and fresh receiving check

The pinned 19-entry source manifest, certificate, and reduction hashes all
match. The source replay passes in normal and `python3 -O` modes, regenerates
the certificate byte for byte, checks seven literal fixtures per mode, and
rejects its malformed controls.

The reviewer imports no source module and runs in both modes. Besides the
static certificate checks, it supplies a fresh cyclic graph of order 47 with
376 red edges and four deletions. The exact average is `20/47`. The source
receiver returns the surviving blue five-set `{1,4,7,12,15}`; a separate
highest-first reviewer search returns `{32,35,40,43,46}`. Both are checked
pair by pair. A fresh input violating strict orbit density receives no Ramsey
verdict.

Reproduction command:

```sh
python3 -B ramsey_r55_orbit_dense_deletion_review1/reproduce.py \
  . /scratch/research-team-v2/tmp/reviewer-1/review-h3975
```

Expected status: `REPRODUCED_ACCEPT_REVIEW_H3975`.

## Imported and residual trust

The universal theorem imports V. Angeltveit and B. D. McKay,
[`R(5,5)<=46`, arXiv:2409.15709v2](https://arxiv.org/abs/2409.15709).
The paper's large computer-assisted proof is outside this review. The
Paley(53) cover does not share that boundary; the two-cycle family uses the
universal theorem here, although the source also records a separate classical
order-53 route.

Residual trust comprises the imported upper bound for the universal claim,
the written expectation argument, source and reviewer implementations,
certificate bytes, exact Python integer/rational and SHA-256 semantics, Git
archive semantics, CPython, the operating system, and hardware. No external
solver, floating-point predicate, group catalog, or graph-isomorphism package
is used. Historical novelty is not assessed.
