Actual author and executing agent: **six-sorting-1, researcher**, 2026-10-03.
Status: completed scoped author proof with independent algorithms by this
same author. Independent-person review and formalization remain pending.

Let a standard comparator `(a,b)`, a<b, write min to a. Ports are 0..12.
The literal seed P28 is B23 followed by L4 and two disjoint HIGH merges:

```
B23=(0,11),(1,7),(2,4),(3,5),(8,9),(10,12),
    (0,2),(3,6),(4,12),(5,7),(8,10),
    (0,8),(1,3),(2,5),(4,9),(6,11),(7,12),
    (0,1),(2,10),(4,8),(3,6),(9,11),(11,12).
L4=(3,4),(1,2),(1,3).
P28=B23;L4;(5,6);(7,10).
```

**Lemma.** Put M=(2,3,4,5,7,8). Let F be any finite standard comparator
word using only M, including the empty word and words with repeated gates.
Let u=(0,0,0,1,1,0) in this port order and let v=F(u). Define

```
p(F) = min { p in {5,7,8} : v[p]=0 }.
```

This set is nonempty. No standard thirteen-input sorting network with at
most 44 comparators has the literal prefix

```
P28; F; (p(F),9); (6,10); (9,11); (10,11).
```

The suffix is unrestricted in length, repeated gates, ports and parallel
depth. There is no imposed bound on the length of F. The statement excludes
one specified head/tail choice for every preparation; it does not exclude
the entire (5,6)/(7,10) route or the unrestricted size-44 problem. The
[current table](https://bertdobbelaere.github.io/sorting_networks.html)
continues to report the thirteen-input size bounds 44..45.

Fix the immutable original HIGH inputs 1 and 2 to distinct ranks 2 and 3.
Let all other eleven original inputs vary independently over 0/1. This
is an entire original clamped cube, not a tag representative or a selected
subset. At P28 the seven marked-touch deletions are independent of these
2048 assignments, there are zero whole-cube unmarked identities, and the
marks are rank 2 at port 10 and rank 3 at port 12. Ports 9 and 11 are
unmarked Boolean values r and s, with r<=s on every assignment.

Among the assignments with s=0, the complete dead-port input set on M is

```
000000, 000100, 000010, 000110
```

where each string lists coordinates in M order, so its integer encoding
is respectively 0,8,16,24, with coordinate j using bit j. Its attained
coordinatewise greatest member is u=(0,0,0,1,1,0), of weight two. Exactly
12 of the 2048 original assignments have s=0; assignment 38 in the
documented original free-port order attains u. The source independently
reconstructs every full seed row, this complete conditional set, both
distinct marker ranks and every deletion/identity count.

Every comparator is coordinatewise monotone and preserves Boolean
Hamming weight. The same properties hold for an arbitrary finite word
F by induction, regardless of its length. Hence v=F(u) has exactly two
ones, so at least one of the three coordinates 5,7,8 is zero. For the
chosen p=p(F), every conditional dead input x satisfies x<=u, and thus
F(x)[p]<=F(u)[p]=0. This proves existence of p and the needed zero on the
ENTIRE s=0 conditional region. More generally, a monotone weight-preserving
map applied below a weight-k upper input has at least |J|-k fixed zero
coordinates in any set J of more than k output coordinates. This elementary
monotonicity/conservation observation is not asserted as a new generic
theorem; the new result is its explicit sorting-prefix application here.

F touches neither original mark nor ports 9/11. After the head `(p,9)`,
port 9 contains max(F(x)[p],r). If s=0, both terms are zero. If s=1,
both terms are Boolean and at most one. Therefore the new port 9 value
is at most port 11 on EVERY original assignment. The next gate `(6,10)`
does not touch 9/11. It is a marked passage because original rank 2 is
at 10. Thus `(9,11)` is unmarked and an identity on the whole original
cube. Finally `(10,11)` is another marked passage and moves rank 2 to
11. Rank 3 stays at 12. The displayed prefix has at least nine marked
deletions and at least one whole-original unmarked identity: D=9, R>=1.
Any identities inside F or at the head only strengthen the inequality.

The whole-original pruning inequality from [8539 and its public
proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sorting-2/semantic-pruning/PROOF.md)
states that a sorting completion of total size m satisfies

```
m >= D_original + R_original + S(11).
```

Deleting marked passages gives an eleven-wire generalized comparator
network, and an unmarked gate that is an identity on the entire Boolean
cube is an identity on arbitrary ordered free inputs by thresholding.
Those identities can be removed jointly without changing later functions.
Generalized orientations and the induced free-wire/output permutation can
be standardized without increasing size. These are the credited pruning
bridges, not assumptions about a selected depth or an incomplete search.
With [Harder's S(11)>=35](https://arxiv.org/abs/2012.04400), the displayed
prefix therefore forces m>=9+1+35=45. This proves the lemma.

The required parameter rule is constructive: evaluate F once at u and
choose its first zero coordinate among 5/7/8. The proof does not enumerate
all words F or depend on the 8351-function private preparation catalogue.
It also does not require a promised future CLASS-depth reserve: both
future marked passages appear explicitly in the displayed tail. The
discussion with six-sorting-2 in campaign message 2655 suggested testing
HIGH activity at head/tail steps. The attained conditional maximum
reduction and this literal application were developed by six-sorting-1.

`generate.py` uses packed truth columns and distinct symbolic ranks.
`verify.py` imports no producer or campaign numerical helper. It replays
all 2048 original assignments with scalar values, compares every defining
finite field, and reconstructs the fifteen possible weight-two outputs
and their zero choices. It also checks 960 local weight-conservation cases,
10935 comparable-input monotonicity cases, and the complete five-row
conditional-zero head truth table. These corroborate the elementary
induction; they are not bounded samples offered in place of that induction.

For F empty, p=8. A separate full 2048-input replay of its actual 32-gate
prefix has D=9 and exactly the identity bit at gate index 30, `(9,11)`.
The genuine weight-three pattern 56 has ones at all three candidate ports,
so the strict hypothesis |J|>k is necessary for the generic zero argument.
Four semantic corruptions with repaired complete transport hashes reject
both normally and with -O: a false seed deletion count, an omitted actual
conditional assignment, a false greatest input, and selection of actual
nonzero coordinate 5 for output pattern 24. Valid proposal bytes remain
unchanged. Complete normal/O finite records agree.

The cold entry point reads only this directory's compact fixture and
source. No previous negative corpus, preparation catalogue, private data,
solver, floating point or proof trace is required. Imported S(11)>=35 and
the whole-original pruning bridges remain external literature/theorem
dependencies; their large proof corpora are not re-proved. The argument
and its exact certificate are unformalized and independently unreviewed.
