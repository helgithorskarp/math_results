# Exact core-completion obstructions for the 69-word (18,6,5) code

Agent: **six-code-3**, role: **researcher**. This is a restricted computer-assisted
lemma about the published Aw--Chee--Ling incumbent. It supplies necessary cuts
for an unrestricted search for 70 words. It does not improve the located global
bounds **69 <= A(18,6,5) <= 72**.

## Statement and finite reduction

Let C be the 69 binary words in `acl69.txt`, interpreted as 5-subsets of
{0,...,17}: coordinate 0 is the leftmost character, and seed row indices start
at 0. The file is an exact copy of
[Brouwer's public certificate](https://aeb.win.tue.nl/codes/cwc/d6/a18.6.5.69),
with SHA-256
`cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d`.

For a coordinate subset I, put C_I = {B in C : B is disjoint from I}.
For every I in the following complete, explicitly specified cohort,

- I = {p}, for all 0 <= p < 18;
- I = {p,17}, for all 0 <= p < 17,

the largest family F of 5-subsets with pairwise intersections at most 2 and
with C_I contained in F has **exactly 69** members. In particular, all words
through one coordinate, or through coordinate 17 and any second coordinate,
may be discarded and reconstructed arbitrarily without producing 70 words
while retaining C_I. Replacement words need not meet I.

For each I, let R_I = C minus C_I, and let N_I consist of all 5-subsets outside
C that intersect each word of C_I in at most 2 points. Every F containing C_I
has F minus C_I contained in R_I union N_I. The certificate partitions this
entire residual family into exactly |R_I| classes; each two distinct words in
one class intersect in at least 3 points. Thus F uses at most one word from
each class, giving |F| <= |C_I| + |R_I| = 69. The incumbent C attains 69.

All 8,568 possible blocks are considered. This is a restriction on which
incumbent words remain present, not a symmetry assumption about an unknown
optimal code. There is no asserted exclusion for two-coordinate supports
that omit coordinate 17, or for arbitrary 70-word codes.

## Consequence for exact search

For binary variables x_B indicating the selected blocks, every code of size
at least 70 satisfies the following 35 conditional cuts:

    sum(x_B for B in C_I) <= |C_I| - 1

for the 35 supports above. These may be added to a search whose target size
is at least 70. They are not inequalities valid for all feasible codes: C
itself violates them. Each pair cut has a core of 38--43 incumbent words;
the singleton cores have 49--57 words.

Equivalently, for every coordinate p the omitted incumbent words cannot all
contain p. For every p < 17 the omitted words cannot all meet {p,17}.
In particular, the omitted incumbent words avoiding coordinate 17 must have
empty intersection. These restrictions remain valid after simultaneously
permuting every coordinate of the specified seed and the candidate code.

## Certificate format and independent check

`certificates.json` contains 35 strings. For each support I:

1. Seed rows meeting I are ordered by their row indices, and assigned local
   colors 0,...,|R_I|-1.
2. N_I is ordered lexicographically as increasing 5-tuples of coordinates.
3. The k-th character assigns the k-th new word to one of those colors,
   using the alphabet stored in the certificate. Each color class also
   contains its corresponding removed seed word.

The generator detects incompatibility through unique seed triples and finds
the class assignment by finite backtracking. The independent checker imports
no generator code: it validates the seed directly by Hamming distances,
enumerates all 5-subsets with direct set intersections against the retained
core, then checks every pair within every claimed class. The proof relies
on these exact checks and the elementary partition argument above, not on
the generator's search result, a solver, floating point, or a timeout.

The trust boundary is Python's standard library and these finite checking
routines, together with the stated mathematical reduction. There is no
proof-assistant formalization. A timeout or failed coloring search has no
nonexistence meaning.

## Reproduction

Python 3.11 or later, standard library only. Checked with CPython 3.11.2 and
3.12.14; one thread. From the repository root:

```sh
python3 coding_theory/a18_6_5_coordinate_cores/verify.py --expect coding_theory/a18_6_5_coordinate_cores/expected.json
python3 coding_theory/a18_6_5_coordinate_cores/generate.py --check coding_theory/a18_6_5_coordinate_cores/certificates.json
python3 coding_theory/a18_6_5_coordinate_cores/audit.py
```

The first command reports all 35 exact maximum completion sizes as 69;
`expected.json` gives the candidate counts and certificate hash. The second
regenerates the compact certificate exactly. The third rejects six malformed
or mathematically invalid certificates, including an incomplete cover and
a compatible pair assigned to one class. The checker and generator each
take approximately one second on the campaign machine and use well below
the 2 GiB scope cap. No large outputs or external solver are required.

## Prior work and scope

- Aw, Chee, and Ling, *Six New Constant Weight Binary Codes*, Ars
  Combinatoria 67 (2003), 313--318,
  [Theorem 1 and Appendix A](https://ymchee66.github.io/home/PDF/6cwc.pdf),
  provide the known 69-word construction; that lower bound is reproduced,
  not claimed as new.
- [Brouwer's maintained table](https://aeb.win.tue.nl/codes/Andw.html),
  checked 2026-09-30, gives 69--72 for (18,6,5).
- The located recent primary papers
  [Rosin, arXiv:2603.00174](https://arxiv.org/html/2603.00174v1) and
  [Echols, arXiv:2608.13906](https://arxiv.org/html/2608.13906v1) supply new
  constructive bounds in other parameter cases. Their displayed result
  tables do not improve (18,6,5).

The new contribution here is the precisely quantified core-completion
obstruction and its compact exact certificates. No priority claim is made;
this obstruction was not located in the searched sources. The checker can
be reused for further specified cores by extending the certificate schema
and explicitly proving complete coverage of the chosen new cohort.
