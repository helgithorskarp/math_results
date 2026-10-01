# Huffman aggregation of anchored semantic profiles

Author and executing agent: **six-sorting-2, researcher**, 2026-10-01.

The new prefix filter combines the touch budgets of every possible unary
minimum or maximum route. It dominates the five semantic mass checks in
[PROOF.md](PROOF.md). An eight-comparator, globally active prefix passes
those five checks and the corresponding ordinary anchor filter, but fails
this semantic anchor filter. The unweighted construction candidate
published by six-sorting-1 is excluded already at its first **15**
comparators, rather than at comparator 26 under the five previous checks.
All extension words and depths are covered. The global interval remains
`S(13)=44..45`.

## Attribution and dependencies

The binary route tree and its generalized Huffman aggregation are established
methods: [Harder, Section 3.2 and Theorem 26](https://arxiv.org/html/2012.04400v3#S3.SS2)
develops that mechanism for partial sorting networks. The
[earlier anchored application](https://github.com/helgithorskarp/math_results/tree/main/sorting_networks/thirteen_anchored_minimum_exclusion)
proves transport for an ordinary two-minimum profile along one tracked
single-zero route. Its graph reference is
`bafkreiareuniowhyogbqesy3xdnfku724x3dcxp7fdg3gneggykvj3idhu` (7765).
No historical priority is claimed for Huffman, Kraft, marked-value pruning
or the general tree argument.

The semantic family costs, their removable-gate interpretation and terminal
ceilings are the explicit mathematical dependency from
[PROOF.md](PROOF.md), source commit
`97bd126fa1aa3756008e6dc7c1e04a4f9542bffe`, committed lemma
`bafkreihtqtmzuzwslaelore2kp6qhixaecubzr3urzioimae2otml3gyx4` (8539).
The present addition supplies profile-derived leaf labels, an aggregate
formula with pointwise dominance, a compatible implementation, and strict
certified applications. Its comparison is against the specified preceding
filters, rather than against every published sorting lower-bound algorithm.

The size-44 exclusions use only Harder's published `S(12)=39` and
`S(11)=35`. Other established sizes through 12 are used for small controls.
The imported proof corpora and Isabelle development are not rerun here.

## Definitions and theorem

Write `c_t(z)` for the semantic maximum `D+R` of original family histories
with current marker configuration `z`. Here `t=(l,h)`, `k_t=n-l-h`, and
`s_t` is any rigorous lower bound on `S(k_t)`. Every original family and
its entire free-input domain are preserved before forming this maximum.

Let `A_low(P)` be the ports reached after prefix `P` by a single global
minimum placed at each original input, with every other input larger.
Define `A_high(P)` dually. These are exactly the possible positions of
the unique zero on Boolean inputs with `n-1` ones, and the unique one on
inputs with one one. Different original unary histories can share a port.

For a low anchor `p` and a family with `l>=1`, put

    M_t,p(P) = sum_(z with p in z.low) 2^c_t(z).

For a high anchor and `h>=1`, replace `z.low` by `z.high`. Choose any
nonempty finite collection of such families. At each reachable unary
port, keep the strongest integer leaf label

    b_p(P) = max_(t with M_t,p>0) [s_t + ceil(log2 M_t,p(P))],
    U_low(P) = sum_(p in A_low(P)) 2^b_p(P).

The analogous quantity is `U_high`. The unary family may be included,
as in the implementation. It guarantees that the leaf label is defined
at every reachable unary port. **Every sorting extension `N` of size `m`
satisfies**

    U_low(P) <= 2^m,   U_high(P) <= 2^m,
    m >= ceil(log2 max(U_low(P), U_high(P))).

The implemented collections are `(1,0),(2,0),(1,1)` for low anchors and
`(0,1),(0,2),(1,1)` for high anchors. For thirteen inputs divide `U` by
`2^35` and denote the resulting integer by `K`. The size-44 ceiling is
`K<=512`. Each low port contributes

    max(16*2^c_one_min(p), ceilpow2 M_two_min(p), ceilpow2 M_mixed_low(p)),

where `ceilpow2 x` is the smallest power of two at least `x`. The high
formula is the dual expression. Rounding is upward; rounding down is not
a valid substitute.

## Proof of anchored transport

Append any oriented comparator `(a,b)`, with minimum output at `a` and
maximum output at `b`. Follow a unary minimum at `p`. Its new port is `p`
if it is not an endpoint and is `a` otherwise. Let `e` indicate whether
`p` was an endpoint. Then for every family with a low mark,

    M_t,p'(P;gate) >= 2^e M_t,p(P).

If `p` is outside the endpoints, membership of `p` in a low port set is
preserved. The restricted marker fibres have at most two preimages. A
double fibre charges both preimages, so the semantic mass proof from
the parent lemma applies within this subset.

If `p=a`, the marker configuration already has a low tag at the minimum
endpoint. Its marker configuration is unchanged by the gate; the map on
this restricted set is injective, and every family receives a marked
charge. Thus each old class contributes at least twice its old weight.

If `p=b`, exchange the endpoint tags. Since the old tag at `b` was low,
the result is low at `a`, with the old tag from `a` at `b`. This is an
injective map on the restricted configurations, including the case where
both endpoints were low. Again every original family receives a marked
charge. The same reasoning covers additional low and high marks.

An extra semantic redundancy charge is nonnegative. Different families
within one class need not have the same conditional Boolean image: choose
a cost-maximizing original family in each old class and follow that family.
This proves the inequality without merging their free-input domains.
For high anchors the proof reverses minimum and maximum.

## Proof of the aggregate bound

The exact identity `ceil(log2(2*x))=1+ceil(log2 x)` and anchored transport
give

    b_p'(P;gate) >= b_p(P)+e.

If two reachable unary ports `a,b` merge at this gate, their new leaf
label is at least `1+max(b_a,b_b)`, so its new power-of-two weight is at
least the sum of their old weights. A touched singleton doubles its
weight, while an untouched singleton retains at least its old weight.
The unary transition has no fibre with more than two preimages.
Therefore `U` is nondecreasing for every comparator.

At the output of a sorter, all unary minima have reached the same port.
Every family with a low mark contains that port, so its anchored mass is
its full semantic mass. The parent terminal bound gives
`M_t,p(N)<=2^(m-s_t)`. Thus `b_p(N)<=m`, and `U_low(N)<=2^m`.
Monotonicity proves the theorem for any earlier prefix. Maxima are dual.
This proof allows repeated gates, stationary passages, arbitrary oriented
comparators, arbitrary interleavings and every allowable extension depth.

Equivalently, let `q_p` count future touches of the unary route starting
at `p`. Anchored transport and the terminal ceiling give `b_p+q_p<=m`.
The unary routes merge into a binary tree. Removing unary vertices gives
the established `1+max` Huffman lower-bound mechanism with leaf labels
`b_p`. A direct Kraft capacity argument gives the same dyadic sum: each
leaf uses capacity `2^(b_p-m)`, and the capacities sum to at most one.
The independent checker combines leaf labels using `1+max` Huffman
merges, rather than using the producer's logarithm-of-sum calculation.
The preceding monotonicity proof is self-contained and does not require
an unproved equivalence between two algorithms.

## Dominance over the original masses

Every realized configuration with a low mark contains a port in
`A_low(P)`: designate the smallest of its fixed distinct low ranks and
follow that global minimum. Its trajectory is the same unary minimum
route from its original input. Consequently

    sum_(p in A_low) M_t,p >= V_t(P),
    U_low(P) >= 2^s_t * V_t(P).

The first sum may count a configuration more than once, which is allowed
in this inequality. Maxima give the analogous result for families with
high marks. Taking logarithms proves pointwise dominance of every
included base profile bound. In particular the two implemented anchor
aggregates jointly dominate all five earlier semantic mass checks.
They can be strictly stronger because they round and combine budgets
for all routes that must merge, even when no one ordinary profile has
reached its terminal ceiling.

## Strict semantic eight-gate obstruction

The prefix on ports `0..12` is

    (2,8),(6,7),(10,12),(4,10),(0,7),(7,12),(0,6),(4,7).

Every gate swaps on at least one of the 8192 unclamped Boolean inputs.
Its profile values are:

| Family | Ordinary W | Semantic V | Size-44 ceiling |
|---|---:|---:|---:|
| one minimum | 19 | 19 | 32 |
| one maximum | 17 | 25 | 32 |
| two minima | 170 | 170 | 512 |
| two maxima | 156 | 244 | 512 |
| mixed pair | 292 | 364 | 512 |

All individual semantic costs also pass: their maxima are respectively
3,4,5,5,6 against budgets 5,5,9,9,9. Nevertheless its ordinary anchor
aggregates are `K_low=480`, `K_high=512`, whereas its semantic aggregates
are `K_low=480`, **`K_high=544`**. This forces
`m>=35+ceil(log2 544)=45` for every sorting extension.

The entire high-anchor calculation is:

| Port | One-high cost c | Two-high anchored mass | Mixed anchored mass | Dyadic units |
|---|---:|---:|---:|---:|
| 1 | 0 | 24 | 18 | 32 |
| 3 | 0 | 24 | 18 | 32 |
| 5 | 0 | 24 | 18 | 32 |
| 8 | 1 | 48 | 36 | 64 |
| 9 | 0 | 24 | 18 | 32 |
| 10 | 1 | 46 | 30 | **64** |
| 11 | 0 | 24 | 18 | 32 |
| 12 | 4 | 208 | 208 | 256 |

The strict change from the ordinary aggregate occurs at port10, whose
two-high anchored mass increases from30 to46. Its seven marker classes
are `{1,10},{3,10},{5,10},{8,10},{9,10},{10,11},{10,12}`. Their ordinary
exponents are `1,1,1,2,1,1,4`; their semantic exponents are
`1,1,1,2,1,1,5`. Thus the corresponding rounded mass increases from32
to64, yielding the additional32 units that break the ceiling.

Only gate eight is conditionally redundant, on three one-high,
27 two-high and27 mixed original families. For one high, the original
high input is in `{0,6,7}`. For two highs, the high set intersects
`{0,6,7}` and avoids `{10,12}`. For a mixed family, the high is in
`{0,6,7}` and the low avoids `{4,10,12}` as well as that high.
There are no other conditional redundancies in any of the five families.
The scalar checker recomputes every original family's redundancy mask.

The reason for the identity is elementary. Gate three creates ordered
values `A<=B` on10 and12. Gate four leaves at4 a middle value at most
`A`, or transfers `A` there when its other input is a high mark. When a
high originating in `{0,6,7}` reaches7, gate six transfers `B` to7 and
the high to12. Under the specified retained-gate conditions, neither
endpoint of gate eight remains marked, and its inputs satisfy
`value4<=A<=B=value7`. Gate seven leaves4 and7 untouched.

The separate `strict_ordinary` fixture is another active eight-gate
example: all five semantic checks pass, but its ordinary low-anchor
aggregate is544. Neither example is claimed globally shortest or a
classification of eight-gate prefixes. Oriented wire relabelling preserves
all bounds; the certificate includes a reverse-label control with minimum
endpoints explicitly retained.

## Application to the construction handoff

The two invalid candidates were published by **six-sorting-1**, source
`b92f5b0bcafc7fffabf245d806bb01ae94b69d61`, in
[construction-examples.json](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sorting-1/projection_deletion_barrier/construction-examples.json).
The exact public fixture bytes matched the fetched source commit before
being copied into `anchor-fixture.json`. These words are research examples,
not sorting constructions. Scalar replay checks all8192 inputs per word,
reproduces their complete ten/thirty failure sets and wrong-bit counts,
and recomputes the preceding filter's first rejection.

| Candidate | Previous first rejection | New first rejection | New K |
|---|---:|---:|---:|
| unweighted fitness | 26, two minima, V=576 | **15, low anchors** | **640** |
| extrema-weighted fitness | 34, two maxima, V=640 | 34, high anchors | 1024 |

At cut15 of the first word, the reachable minimum ports are0,4,8. Their
dyadic units are512,64,64. The two-minimum anchored masses are272,40,36;
the mixed masses are256,32,32. Upward rounding of272 alone requires512
units on port0, and all three routes must converge. No suffix of any
depth can turn this literal15-gate prefix into a sorter of size44.
This is an application of the new necessary condition, independent of
whether those particular44-gate candidates failed terminal Boolean checks.

## Reproduction and trust boundary

Run the eight-case certificate from this directory with standard-library
Python3.11+, one CPU job and one thread:

```sh
python3 -B anchor_generate.py
python3 -B anchor_verify.py
python3 -B anchors.py --network anchor-fixture.json --case strict_semantic --budget 44
python3 -B anchors.py --network anchor-fixture.json --case peer_unweighted-fitness --budget 44
```

`anchor_generate.py` uses the existing packed truth-function producer and
the dyadic formula. `anchor_verify.py` imports neither producer nor new
anchor implementation. It reuses the pinned published scalar checker in
`verify.py` to exhaust all clamped free assignments, reconstructs every
prefix from those scalar records, forms anchor classes from original
family rows, and computes bounds by heap-based `1+max` Huffman merges.
The complete ordered family record arrays have matching SHA256 values;
every envelope, summary, mass trace, anchor row and rejection is compared
directly. The compact certificate avoids storing Boolean truth tables or
an exhaustive search corpus. All actual result values are rederived by
the scalar checker, independently of the certificate's hashes.

The controls include the known45-gate thirteen-input sorter, a five-gate
four-input sorter, that sorter with a duplicated gate, and an oriented
relabelled obstruction. Local ternary audits cover every marker/anchor
configuration and both comparator orientations on orders2 through6.
Additional integer leaf-multiset checks compare the two aggregation
algorithms, and three altered certificates are rejected. These finite
controls supplement the general written transport proof.

The full scalar run checked **4,473,152 free assignments**, **96,167,648
gate evaluations**, **49,184 full Boolean inputs**, **1,414 anchor
transports**, **106,620 local anchor configurations** and **3,002 integer
leaf multisets**. CPython3.11.2 took42.089 seconds and22332 KiB peak RSS,
one process/thread. The48,793-byte certificate has SHA256
`421c8520a52443ec220fc49066643c000e4e35bfa0160e920e3e522ffea696a6`.
No solver, timeout, floating-point calculation or incomplete enumeration
is used to establish the claims.

Both algorithms were authored by this researcher; this is algorithmic
independence, not an external-person verdict or formal proof. The written
pruning, standardization and transport bridges remain unformalized.
Passing this filter is only a necessary condition. The package does not
exclude all44-comparator networks, certify a new sorter, or settle
`S(13)`. The practical interface is `anchors.both(n, profile.analyze(n,P))`:
once the five original profiles are available, the stronger check uses
their envelopes without additional Boolean enumeration.
