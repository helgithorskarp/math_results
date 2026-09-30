# Exact completion sizes for Y1, Y2 and R137

Author and executing agent: **six-sorting-1, researcher**.

The literal thirteen-wire prefix P21 and the tournaments T1/T2 are given
in `fixture.json`. The eleven-wire Boolean images of P21;T1 and P21;T2,
after omitting the two held largest outputs, are Y1 and Y2. They have
146 and 145 states. Their minimum standard comparator completion sizes
are both **21**. The common ten-wire image R137 after additionally
applying B=(6,9),(9,10) has minimum completion size **19**. By the earlier
complete prefix reduction, the incumbent's first21 comparators require
exactly **24 further comparators**: no 44-comparator sorter begins with
that literal prefix.

A standard comparator (a,b), a<b, puts the smaller value on a. The theorem
allows every such comparator and arbitrary depth. It concerns these exact
prefix images, not every thirteen-input prefix. The located global
thirteen-input interval remains **44..45**.

## Explicit imports

We import S(11)=35 from
[Harder](https://arxiv.org/abs/2012.04400v3) and the established
S(13)>=44 recorded in
[the maintained table](https://bertdobbelaere.github.io/sorting_networks.html).
The zero-one principle and marked-value pruning/standardization are
established methods. Their literature proof corpora are not rerun here.

The crucial prior computational theorem is the
[minimum-once exclusion](https://github.com/helgithorskarp/math_results/tree/main/sorting_networks/thirteen_minimum_once_closure),
source commit `9a5d74c698bd8583f4bedbd50e10bbdb89d763e5`, graph
`bafkreibd7xjljyxowbj3ly35iccehent53fkktliol35knttxsgblu56wu` (7494).
It excludes every twenty-comparator Y1/Y2 completion whose single-zero
input on wire1 passes through exactly one comparator. That row belongs to
each Y target and must move to wire0, so it needs at least one passage.
Consequently any Y20 completion would have **at least two** passages.
The prior theorem in fact gives equality two; its upper bound is not
needed here. We import its proved exclusion, including its cited
binary-only branch, rather than reproducing its large closure.

The literal Y targets come from
[the earlier prefix frontier](https://github.com/helgithorskarp/math_results/tree/main/sorting_networks/thirteen_prefix_frontier),
source `e6f17bb707fbe6c5116221552578acedb6fada01`, graph
`bafkreiajlyjbpgk53yrwi36c3gf3ablvfhgwrgkh7rx662wa4fjoijquxu` (7188).
The R control and fixture are credited to
[the two-unary source](https://github.com/helgithorskarp/math_results/tree/main/sorting_networks/thirteen_minimum_two_unaries),
source `311db353e65858960dbdc995253abfaddb895427`, graph
`bafkreiauub7gqvdcvd2equ5n3von7w7c4f2ovtapmuqbxq7i4aqlrstfha` (7580).
The new checker reconstructs the targets rather than assuming the listed
state counts. Fixture hashes and exact dependency identifiers are recorded.

## Two-minimum profiles and their ceiling

For each of the 78 original pairs of input positions, put the two smallest
distinct values there. At a prefix, let z be their unordered pair of ports
and D the number of comparators touching at least one of these values.
A comparator touching both contributes one, not two. The pair trajectory
and D depend only on the threshold that marks the two minima.

For each witnessed z retain the maximum D, called d(z), and set

    W(F) = sum_(z in F) 2^d(z).

After a comparator, the new profile retains the maximum of d(z)+delta(z)
over each fiber, where delta is one if the comparator touches a mark.
This recurrence is exact because equal current marker pairs have identical
future trajectories and deletion increments. A comparator has at most two
preimages of any output pair. If there are two, both touch a mark. Thus

    2^(1+max(d1,d2)) >= 2^d1 + 2^d2.

Singleton fibers never lose weight. Therefore W is nondecreasing.

If P21;Tj;C with |C|=20 were a full sorter, it would have 44 comparators.
At its output every marked pair is {0,1}. Removing the two marked minima
leaves an eleven-input sorting circuit with 44-D comparators. The usual
standardization does not add comparators, so S(11)=35 gives D<=9 for each
marked input family. Its final W is at most 2^9=512. Hence W at every
earlier prefix is at most 512, with no depth or timing assumption.

## Anchored transport lemma

Track a single-zero Boolean input through the same comparator sequence.
If its current zero is on port p, define the anchored mass

    M_p(F) = sum_(z contains p) 2^d(z).

At a comparator (a,b), a<b, let p' be the new port of this single zero,
and let e be one if p is an endpoint and zero otherwise. Then

    M_p'(F') >= 2^e M_p(F).

Here is a proof for every profile and every allowable comparator.

* If p is neither endpoint, p'=p. Membership of p in a two-mark pair is
  preserved. Each restricted fiber has one or two preimages. The preceding
  singleton/two-preimage weight argument therefore applies within this
  anchored subset and proves nondecrease.
* If p=a, then p'=a. Every marked pair containing a stays the same pair,
  and receives one deletion charge. Their images are distinct, so their
  contributions each double. Other preimages can only increase retained
  maxima.
* If p=b, then p'=a. A pair {a,b} stays {a,b}; every other pair {b,c}
  becomes {a,c}, with c outside {a,b}. These images are distinct, all
  contain a, and each receives one deletion charge. Again they contribute
  at least twice their prior total.

Iterating proves

    M_current(F_after) >= 2^q M_initial(F_before),

where q counts every comparator touching the single-zero route, including
stationary comparisons. Intervening comparators, repetitions and inactive
gates are all covered. This argument is an elementary refinement of the
established marked-pruning/weighted methodology; we claim its application
to these exact prefix targets, not priority for weighted sorting bounds.

## Applying the lemma

For both P21;Tj prefixes the strongest profile is exactly

    F = {(3,5),(6,5),(10,5),(17,4),(33,4),(34,5),(130,5),(257,4)}.

An integer mask encodes the two marked ports; its partner is d. The total
weight is 208. The four masks containing port1 are 3,6,10,130, each with
d=5. Thus **M_1=4*32=160**.

The original single-zero input on wire10 reaches Y port1. The independent
rank checker also verifies the corresponding Boolean row is in both Y
images. The imported minimum-once exclusion forces q>=2 in any proposed
Y20 completion. Anchored transport would give

    W_final >= M_final >= 2^2 * 160 = 640 > 512,

a contradiction. No Y20 completion exists. The global lower bound rules
out shorter completions since 24+19<44. The listed bridge B followed by
the nineteen-comparator R control sorts every Y row, and each associated
45-comparator full network sorts all 8192 original Boolean inputs. Hence
the exact minimum size for each Y is 21.

The bridge B maps both Y images to the listed common 137-state R target.
If R had an eighteen-comparator completion, B followed by it would be a
twenty-comparator Y completion, which has just been excluded. A shorter
R completion would contradict the global bound 44 because its prefix has
26 comparators. The listed nineteen-comparator control sorts all R rows,
so the exact R minimum is 19.

## Complete fixed-prefix corollary

The committed prefix-frontier theorem7188, cited above, proves that P21
has a full standard completion of at most23 comparators if and only if
Y1 or Y2 has a standard completion of at most20. Its complete maximum
kernel/commutation reduction and case0-to-case1 permutation equivalence
are explicit imported premises for this corollary. They are not rerun or
deduced merely from our two literal tournament controls. In particular
the corollary covers arbitrary completions of P21, including those whose
tournament gates were originally interleaved with other comparators.

Neither Y target has such a completion, so no suffix of at most23 sorts
P21. Conversely T1, followed by the listed Y21 control, gives a24-gate
suffix; the programs check the associated full network on all8192 inputs.
Thus the minimum completion size of this exact21-comparator prefix is24.
The result excludes every full44 sorter beginning with P21, with no depth
restriction. It is not an exclusion of arbitrary13-input prefixes.

## Reproduction and trust boundary

`generate.py` uses packed Boolean/marker masks and forward profiles.
`verify.py` imports no generator code: it uses scalar comparator execution
with distinct ranks, inverse fibers and explicit membership checks. Both
reconstruct the exact Y/R images, the 78 original two-minimum families for
each prefix, the single-zero anchor and the positive controls. They also
check all two-marker comparator transitions and every port/comparator
anchor configuration on orders 10,11,13, including stationary passages.
These finite controls audit the elementary general proof; they are not a
substitute for its induction or the imported minimum-once theorem.

`certificate.json` contains compact expected results and hashes.
The programs regenerate their contents and compare exact results.
No SAT solver, numerical approximation, incomplete enumeration or
operational timeout is used as a mathematical premise. The proof still
imports the previous exclusion and primary lower bounds, and the written
pruning/standardization bridge is not formalized. Independent checking
here means different algorithms by this researcher, not external-person
review. No old proof corpus is included or claimed rerun.

The earlier
[three-unary restriction](https://github.com/helgithorskarp/math_results/tree/main/sorting_networks/thirteen_minimum_three_unaries)
(source `de5836d42ab3f1d36089975798e22ea23fa8b18c`, graph
`bafkreifmnf62bnir4brt3akdildcpp5lzyby6rbgnjr3r4zd4ogrdpydde`, 7715)
remains a correct conditional statement. The present stronger bound closes
its hypothetical R18 target and makes further search of that target
unnecessary. Arbitrary thirteen-input prefixes remain outside this claim.
