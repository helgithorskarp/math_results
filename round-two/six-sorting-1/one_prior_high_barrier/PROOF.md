# One preceding HIGH merge cannot repair the L4 thirteen-input prefix

Author and executing agent: **six-sorting-1, researcher**, 2026-10-02.
Status: conditional author proof with exact finite premises checked by separate
same-author algorithms. The written reductions are unformalized and no
external-person review verdict is claimed. The unrestricted interval remains
[44..45](https://bertdobbelaere.github.io/sorting_networks.html).

Ports are `0..12`. A standard comparator `(a,b)`, `a<b`, puts the minimum
at `a`. A completion means any sequential standard comparator word, with
arbitrary depth, repeated gates and preparations.

## Exact statement

Let B23 be the literal word

```
(0,11),(1,7),(2,4),(3,5),(8,9),(10,12),
(0,2),(3,6),(4,12),(5,7),(8,10),
(0,8),(1,3),(2,5),(4,9),(6,11),(7,12),
(0,1),(2,10),(4,8),(3,6),(9,11),(11,12).
```

Put `L4=(3,4),(1,2),(1,3)` and `P=B23;L4`, of size 26.
For each original pair of HIGH inputs fix distinct large ranks above all
eleven free Boolean inputs. At a prefix, count the comparisons touching a
HIGH mark. For each current unordered marked-port configuration take the
maximum original count `d`; its weight is `2^d`. The sum is the ordinary
HIGH pair mass. LOW is the dual original-pair family.

A binary event touches two live secondary HIGH ports; a singleton touches
one. A preparation touches none. An equal binary merge preserves mass.
At P the HIGH mass is 448. Its first strict increase is the first gate
whose resulting mass is greater than 448.

**Lemma.** No sorting completion of P with total size at most 44 has a
singleton first strict HIGH increase preceded by **exactly one** equal
binary HIGH merge. Any number of preparations before and after that merge
or the singleton is allowed. No suffix depth bound is assumed.

This does not exclude P's zero-, two- or three-preceding-merge singleton
cases, other LOW prefixes, or unrestricted thirteen-input size 44. The
[earlier conditional binary barrier](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sorting-1/both_first_binary_barrier/PROOF.md)
already excludes a binary first strict HIGH increase after P. The present
lemma advances its singleton construction frontier.

## Tight domains, frozen ports and ordinary costs

We import `S(11)>=35` from
[Harder's primary paper](https://arxiv.org/abs/2012.04400), together with the
size-preserving standardization interface for oriented pruned comparators.
The original lower-bound corpus is not replayed. The generic ordinary and
semantic pruning interface is
[lemma8539](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sorting-2/semantic-pruning/PROOF.md).
For a putative total-size-`m<=44` sorter the ordinary pair masses are at
most `2^(m-S(11))<=512` at every prefix.

The independent scalar base check follows **all 78 original LOW pairs and
all 78 original HIGH pairs on their complete 2048-assignment cubes**.
P has the sole LOW class `{0,1}` with ordinary and semantic cost 9.
Exactly 39 original LOW pairs have `D=9,R=0`, and both marks are sorted at
physical ports 0/1. Here D counts marked touches and R counts free gates
that are identities on the entire original cube. Each such original
restriction is retained separately. The HIGH secondary classes are

```
port:  5  6  7  9 10 11
cost:  6  6  6  6  6  7
```

The held HIGH port is 12. LOW ports 0/1 cannot be touched again: a touch
on any tight LOW restriction gives D at least 10 and hence total size at
least `10+35=45`. Likewise touching 12 doubles every HIGH class, making
HIGH mass at least 896. Thus every suffix gate avoids 0/1/12.

On every one of the 39 original tight LOW cubes, every future unmarked
comparison must be active on some input. If a gate is the identity on
even one whole original cube, its extra free deletion gives `D+R>=10`
and again forces size at least 45. Activity means an inversion actually
occurs on that original cube; current marker ports alone cannot establish
it.

A HIGH singleton doubles its candidate's weight. An ordinary HIGH binary
event of costs u,v replaces their weights with `2^(1+max(u,v))`. Mass is
nondecreasing and equality holds precisely for an equal-cost binary merge.
The one preceding merge must join two of the five cost-6 ports, giving
ten possible literal gates g. A cost-7/cost-6 merge would already be a
strict binary increase, outside the lemma's hypothesis.

After g there are three cost-6 ports and two cost-7 ports, still of mass
448. The first singleton must use a cost-6 port: it raises mass by 64 to
512, whereas a cost-7 singleton would overshoot. Its other endpoint is
one of the five dead ports among `2..11`. After the singleton, the mass
is saturated, so every remaining HIGH event is an equal binary merge.
There are five live secondary classes and exactly four such tail events.

## Commutation and exact function closure cover arbitrary preparations

Before g the dead preparation ports are `{2,3,4,8}`. Every earlier
preparation avoids g's two endpoints, which are still live. Move g to the
front immediately after P by disjoint-comparator commutations. Keep the
preparations in their original mutual order. The complete ordered-input
function and comparison count are unchanged. Every preparation now before
the singleton is on the five dead ports `D_g`: the original four plus
g's released smaller endpoint.

The singleton is **not** moved across preparations of its free endpoint.
Write the resulting prefix as `P;g;F;s`, with F an arbitrary standard
comparator word on `D_g`. As necessary conditions, each gate of F is
active on each of the 39 whole original tight LOW cubes.

For each g, breadth-first closure starts with the identity function on
all 32 Boolean assignments of the five dead inputs. A state contains the
entire five-output function, not a marker profile or a restricted image.
For each of its ten possible next standard comparators, project every
original LOW cube through `P;g;F` and test activity separately. Keep an
edge exactly when all 39 tests pass. Thus the next admissible moves depend
only on the stored full function and the fixed original cube images.

The producer and checker use different representations: packed five
output columns versus a 32-row table of integer outputs. The checker
enumerates the full closure without a word-length bound. It independently
matches the entire function set, every admissible transition, shortest
representative lengths and every representative's complete function.
The ten function counts, in lexicographic gate order, are

```
78,68,49,67,92,92,112,92,68,44; total 762.
```

Their maximum shortest length is six. The producer's operational
12-comparator preparation cutoff is never reached; the checker has no
such cutoff. No incomplete enumeration or timeout is a proof premise.

Replacing an arbitrary F by its shortest representative preserves all
five-output Boolean functions and does not increase total size. Thresholding
min/max functions lifts this equality to arbitrary totally ordered inputs,
including marked original domains. The unchanged suffix still sorts if
the original one did. It is therefore enough to exclude the 762 canonical
preparation functions. This reduction covers repeated comparisons and
arbitrary preparation depth.

After s, the HIGH live support only decreases. A preparation before a
future tail event avoids both of its endpoints: these endpoints are
still live and released ports never return. Move all four tail events
before the intervening preparations, preserving the preparations' order
and the complete ordered-input function. The post-singleton weights are
`6,6,7,7,7`. The two cost-6 leaves must pair. Their cost-7 parent joins
the three other cost-7 roots, which have three possible unordered
pairings. This gives exactly three four-gate tail functions.

The independent checker enumerates all legal tail event orders and compares
their complete 32-row five-output functions with the three canonical words.
It checks 16,839 orders and 130,970 local event controls across all active
heads. Tail normalization is consequently a complete function cover,
not a selected fixed-depth search.

## Original-domain minimum locks remove 501 functions

The obstruction used here is
[lemma9525](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sorting-1/conditional_minimum_lock/PROOF.md).
For any one tight original LOW restriction, suppose physical port 2 is
the minimum of all eleven free values after `P;g;F`. A later first touch
of 0/1 adds a marked deletion. A later first touch of 2, after arbitrary
preparations on the other free ports, is the free identity `(2,q)`:
the unchanged minimum is at most every other free value. Either touch
therefore gives a pruned eleven-input sorter of size at most `44-10<35`.
Thus any putative size-at-most-44 suffix avoids 0/1/2 altogether. If port
2 is already wrong on some full original Boolean input, that fixed suffix
cannot repair it.

For every one of the 762 functions the producer tests all 39 full original
eleven-input cubes and all 8192 full original Boolean inputs. The independent
scalar checker reconstructs those original cubes as full eleven-bit images,
applies each complete 32-row preparation table and directly checks the literal
full-input witness. It does not infer a minimum from a current marker class.
The exact outcomes are

```
501: some tight original minimum and a wrong full-input third statistic;
 12: a tight original minimum, but the full third statistic is already correct;
249: no tight original cube has the required minimum.
```

The first 501 admit no standard size-at-most-44 suffix of any HIGH type or
depth. All other 261 functions are retained, including the 12 already-correct
ones. The classified-record SHA256 is
`e49c1a14f113adbc5e643c9781e959b73a729020c88566cfade40d67b48dfd67`.

## Complete remaining fronts

For each retained F there are three unit-cost HIGH candidates and five dead
singleton partners, hence 3,915 heads. A free identity on a whole original
tight LOW cube rejects 2,044 of these heads. The remaining 1,871 heads
have all three canonical four-gate tails. None introduces another tight
LOW identity or minimum-lock rejection. Thus **all 5,613 fronts** are
retained for the nested bound. Each is the literal word

```
P;g;F;s;T, of length 32+length(F).
```

The remaining comparison budgets are 7..12. Their nine-wire images on
physical ports `2..10` have 36..84 states; there are 5,354 distinct images.
Their complete front-record SHA256 is
`8e18f17dbd27d7b0943a4c98170c039ea8521ad176c40031e80e5f9db96fb366`.

The independent cover check reconstructs P on all 8192 original inputs,
checks held original ranks 0/1/12 and obtains the exact 157-state ten-core
image. Every normalized front touches only those ten core ports. Replaying
its literal gates on every one of these 157 states therefore covers every
original input exactly, with multiplicities unnecessary. For every front
the checker verifies the held second-largest rank, all nine-wire states,
literal word, budget and hashes. Its 881,241 complete scalar core replays
cover all 5,613 fronts. Every LOW identity witness is checked on its actual
whole original cube, regardless of witness enumeration order.

## Selected original-domain nested bounds exclude every front

For a selected original clamping f with three LOW and three HIGH inputs,
retain all seven free Boolean inputs. Count marked deletions D and
whole-cube free identities R. Transport carriers through marked exchanges,
delete those two disjoint sets of gates and globally relabel by output
ports to obtain an oriented seven-input prefix `Q_f`. A reversed oriented
pair is kept as such; it is not silently sorted by its labels.

Use the general nested theorem of
[lemma9007](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sorting-2/native24-kernel-cover/NESTED.md)
and semantic anchor theorem
[lemma8604](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sorting-2/semantic-pruning/ANCHORS.md).
They apply to arbitrary oriented pruned prefixes; no native-prefix negative
application is transferred. For the selected original domains let

```
B7(Q) = max(16, LOW semantic anchor, HIGH semantic anchor),
lambda_f = D_f+R_f+B7(Q_f),
lambda_z = max(lambda_f over selected originals with current mask pair z),
M = sum_z 2^lambda_z.
```

Any full sorting extension of total size m satisfies `M<=2^m`. The
argument transports each original domain separately. A marked touch or
conditional identity adds one deletion and leaves Q unchanged up to a
global relabelling; an active free gate appends an oriented comparison.
The inner lower bound is nondecreasing under extension. A current tag-pair
transition has at most two preimages; a double fibre charges both, giving
a new label at least `1+max` of the old labels and hence at least their
combined dyadic weight. At a full sorter the final free circuits sort
their whole cubes, so the final single-class label is at most m. This is
the cited general nested proof, not an assertion that equal current
marker classes have equal free-domain functions.

For inner anchors the imported small lower bounds are `S(5)>=9`,
`S(6)>=12`, and `S(7)>=16`. Each original one-minimum, one-maximum,
two-minima, two-maxima and mixed-pair domain is computed separately on
all of its free assignments. Anchored class weights use their actual
`D+R` maxima. The packed producer computes the dyadic anchored sum;
the independent scalar checker computes all original numeric records
and uses a heap of `1+max` Huffman merges, checking the two formulas
agree. No lower-bound corpus for these known small sizes is re-proved.

The 99 proposal domains are credited published data. A selected subset
is sufficient; exhaustive enumeration of all original3+3 domains is not
a premise. Constant `B7=16` gives valid certificates for 5,254 fronts.
The remaining 359 use independently checked inner bounds 17 or 18.
Across all fronts the certificate selects **25,630 original outer
occurrences**. Within each front their current LOW/HIGH mask pairs are
distinct; the checker explicitly rejects duplicate-class accounting.

For every selected outer occurrence the checker recomputes the whole
128-assignment original cube, its exact D/R/identity mask, the free-carrier
word, and the complete retained function on all 128 inputs. An inner bound
greater than 16 additionally requires all original inner cubes and the
independent heap anchor calculation. It checks every selected label and
the exact strict sum. Normal Python and Python `-O` agree on every finite
mathematical record; correctness checks use explicit exceptions.

Every front has `M>2^44`. The smallest selected mass is

```
17729624997888 = (129/128)*2^44,
2^44 = 17592186044416.
```

Therefore none of the complete normalized fronts has a total-size-at-most-44
sorting extension. Minimum locks, whole-original-cube identities,
unrestricted-length exact function closure, and disjoint-gate commutation
cover all words in the lemma's stated branch. This proves the lemma.

## Reproduction and limits

[README.md](README.md) gives the serial standard-library command.
[certificate.json](certificate.json) is a compact finite summary; it is
not used instead of the mathematical replay. All complete preparation
functions, original domains, nine-wire images and selected records are
regenerated in ignored `work/` and checked before the summary is compared.
There is no private input, solver, network or graph dependency at runtime.
[SOURCE-CREDITS.md](SOURCE-CREDITS.md) identifies exact copied primitives,
published mathematical dependencies and proposal-data provenance.

The largest checked finite branch used fewer than 80 MiB and completed
under the unchanged per-child 45-second internal/55-second external
limits. A failed stage, timeout, incomplete queue or operational cutoff
terminates reproduction; it is never an exclusion. The historical large
Harder certificate corpus is imported rather than replayed, and the
written pruning, threshold and commutation bridges remain unformalized.
Shared signing identity supplies no independent-person review.
