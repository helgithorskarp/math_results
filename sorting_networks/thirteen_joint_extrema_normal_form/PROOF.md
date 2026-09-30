# A coupled extreme-profile normal form for the selected B11 branch

Author and executing agent: **six-sorting-1, researcher**. Standard
comparators (a,b), a<b, send the smaller value to a. Internal labels
0..10 correspond to original thirteen-input wires1..11.

Let P20 be the literal twenty-comparator prefix in `fixture.json`, and
put Q20=P20[:-1];(10,12). The prefix Q20;(0,5);(0,1) has length22,
holds the global minimum on original0 and maximum on original12, and
has the 158-state Boolean image B11 on the eleven active wires. This
is the selected binary-minimum branch of the
[parent P19 normal form](https://github.com/helgithorskarp/math_results/tree/main/sorting_networks/thirteen_twenty_prefix_exclusion),
source commit `c40dcc78d772c2ab1fd1991d8f89e4c270491673`, graph7813
`bafkreifrmmc5ztlhitir24jn2lqdy6iekdndejcf2auf7limrwind5ydby`.

**Theorem.** Any 22-comparator sorter of B11, hence any full44 sorter
with this literal22-comparator prefix, satisfies the following conditions.

1. The first comparator on internal10 has its partner in
   {1,2,3,4,5,6,8}. Before it, every effective minimum or maximum profile
   event is a binary merge of equal weights.
2. At that first10 comparator, both profile weight sums become512,
   and the two active supports become disjoint. Every subsequent
   effective event is an equal-weight binary merge in one profile.
3. On deleting comparators that change neither profile, its effective
   word has exactly10 or11 comparators. Every such word lies in the
   complete coupled profile automaton of2214 states and22536 labelled
   transitions, including self loops. That automaton has751950 terminal
   effective words of length10 and2266650 of length11, and no other
   terminal effective lengths.

Every standard pair, repeated comparison, interleaving and arbitrary
depth is allowed. Comparators that preserve both profiles can still
change other values and may occur anywhere in the word. The catalog
is a necessary relaxation. It supplies neither a B11 sorter nor an
exclusion. The B11 completion interval stays22..23, and S(13) stays44..45.

## Imports and exact initial weights

We import S(11)=35 from [Harder](https://arxiv.org/abs/2012.04400v3),
the current S(13)>=44 lower bound in the
[maintained table](https://bertdobbelaere.github.io/sorting_networks.html),
and the parent theorem that P20 requires exactly25 further comparators
at arbitrary depth. The parent theorem is an explicit dependency, rather
than a proof corpus replayed here. The table was checked on2026-09-30.

For each of the78 original pairs of positions, mark the two smallest
values. At a prefix, retain each marked output pair z with depth
d(z), the maximum number of prefix comparators touching at least one
mark among original witnesses reaching z. Touching both counts once;
stationary comparisons count. Define W=sum_z 2^d(z). Define the dual
profile for the two largest values in the same way.

Marked-pair transport depends only on the current pair. Each output
fiber has at most two preimages; when two occur both are charged. Thus
the fiber inequality 2^(1+max(d1,d2))>=2^d1+2^d2 proves that W does not
decrease. In a full44 sorter, deleting the two marked extremes leaves
an eleven-input sorting circuit with44-D comparators. Standardization
adds no comparator, so S(11)=35 gives D<=9. Each complete profile ends
at its single extreme pair with W<=2^9=512. Therefore W<=512 at every
intermediate prefix, separately for the minima and maxima.

Deletion/standardization and weighted extreme profiles are established
methods. The
[anchored transport source](https://github.com/helgithorskarp/math_results/tree/main/sorting_networks/thirteen_anchored_minimum_exclusion),
commit `e5ade1718ca337f84d219e23b47405444505cfea`, graph7765
`bafkreiareuniowhyogbqesy3xdnfku724x3dcxp7fdg3gneggykvj3idhu`,
is the campaign's explicit method reference. No priority is asserted
for pruning, weighted methods or order reversal.

After the literal22-prefix, each minimum marked pair contains held0,
and each maximum marked pair contains held12. The other mark is on
an active internal port. The exact partner weights are:

| Internal port | Minimum weight | Maximum weight |
|---|---:|---:|
| 0 | 128 | 0 |
| 1 | 64 | 0 |
| 2 | 64 | 0 |
| 3 | 64 | 0 |
| 4 | 64 | 0 |
| 5 | 0 | 128 |
| 6 | 64 | 0 |
| 7 | 0 | 64 |
| 8 | 0 | 128 |
| 9 | 0 | 128 |
| 10 | 32 | 32 |

Both sums are480, leaving slack32. These are reconstructed from every
original marked pair, not inferred from only the single-extreme images.
The public checker independently obtains the158-row Boolean image
from all8192 original inputs and verifies the23-comparator control.

## The first comparison on internal10

A suffix comparator avoids held original0 and12. In either active
partner profile, its output weight is2*max(u,v) at the lower port for
minima and the upper port for maxima; the other endpoint becomes empty.
The increase in total weight is |u-v|. Thus a unary event, with v=0,
increases the sum by u; an equal-weight binary event increases it by0.

Before the first10 comparator, both weights on10 stay32. Every other
positive weight starts at least64 and can only stay unchanged or
double at an output endpoint. With slack32, a unary event elsewhere
costs at least64, and an unequal binary event elsewhere costs at least64
because the weights are powers of two. Neither is possible. Hence
every earlier effective event is an equal-weight binary merge. The
two supports remain disjoint off10, and their sums stay480.

Partner0 is impossible: the minimum weight there starts at128 and
cannot leave the lowest port, so merging with32 costs at least96.
Partner9 is impossible: the maximum weight there starts at128 and can
leave9 only via10, so before the first10 comparison it is still at
least128, again costing at least96.

Partner7 is also impossible, using the imported P20 theorem. The
maximum weight64 on7 cannot be touched beforehand: outside10 there
is no other maximum weight64, and the remaining maximum weights are
multiples of128; any attempted unary or unequal event costs at least64.
Thus all preceding suffix comparators avoid both7 and10. If the first10
event were(7,10), it would commute to the start of the suffix. In
original labels it is(8,11), disjoint from each of(10,12),(0,5),(0,1).
Commuting it before those three gates gives P20 followed by24 gates,
contradicting the parent's exact P20 suffix minimum25.

The surviving partners are exactly the stated seven labels. Immediately
before this event, its maximum partner must be empty: any positive
maximum there would be at least128, because the only64 port7 is excluded.
Its minimum partner must be empty or have weight64; a larger weight
would cost at least96. In the two profiles the event therefore has forms

    minimum: (0,32)->64 or (64,32)->128;
    maximum: (0,32)->64.

Each sum increases by exactly32, reaching512. The minimum weight moves
to the partner, and the maximum weight stays on10, so the supports
become disjoint. Partners5 and8 must not be discarded merely because
they initially carry maximum weights: earlier equal merges can vacate
them. For example,(5,8);(5,10) and(8,9);(8,10) are admitted profile
prefixes. No surviving unary event is assumed to commute to the front.

## Saturation and the10-or11 event count

Once both sums are512, any positive unary event or unequal merge would
increase a sum beyond512. Every subsequent effective event is therefore
an equal-weight binary merge. Disjointness persists: a merge in one
profile touches two ports empty in the other, and comparators empty in
both profiles change neither support. Consequently each later event
changes just one profile.

Initially the minimum profile has seven positive ports and the maximum
profile has five. Each binary merge decreases its support size by one;
a unary event preserves it. Terminal support sizes are one each, at
internal0 for minima and10 for maxima. Thus there are six minimum binary
events and four maximum binary events. The first10 event is the only
maximum unary event. If its minimum part is binary, it is counted among
the six minimum binary events and shared with that maximum unary event:
the union has6+4+1-1=10 events. If its minimum part is unary, there is
one additional minimum unary event, also shared with the maximum unary
event: the union has6+1+4+1-1=11 events. There are no other shared events.

Removing profile-preserving comparators changes neither the current
profiles nor the permissibility of the remaining profile word. This
removal is solely for the extreme-profile projection: it does not assert
that the shortened word sorts the full Boolean image. A full22 word
therefore has exactly12 or11 profile-preserving comparators, possibly
interspersed throughout the word.

## Complete finite closure and counting

Divide every weight by32. A state is two integer11-vectors and a Boolean
flag recording whether10 has been touched. The initial vectors are

    low  = (4,2,2,2,2,0,2,0,0,0,1),
    high = (0,0,0,0,0,4,0,2,4,4,1).

For every one of the55 standard active pairs, apply the exact partner
transport. Reject a successor if either sum exceeds16, or if it is the
first10 comparison and its partner is0,7 or9. All other successors,
including state self loops, are retained. Breadth-first closure from
the initial state ends with:

| Quantity | Exact value |
|---|---:|
| Reachable states | 2214 |
| Labelled edges, including self loops | 22536 |
| States before first10 touch | 204 |
| First10 edges | 973 |
| First10 edges with a minimum binary event | 380 |
| First10 edges with a minimum unary event | 593 |
| Terminal states | 1 |
| States from which the terminal is reachable | 2214 |
| Terminal effective words of length10 | 751950 |
| Terminal effective words of length11 | 2266650 |

The973 first10 edges have partner counts
1:124, 2:152, 3:164, 4:176, 5:102, 6:204 and8:51.
For every reached post-split state, both sums equal16 and the supports
are disjoint. Both programs check this invariant on the actual states,
and the hashes canonically commit to every state and labelled edge.

There is no depth bound or operational cutoff in either closure program.
Weights are integers in {0,1,2,4,8,16} and each sum is at most16, so the
state domain is finite. Induction on the number of suffix comparators
shows that every hypothetical B11 completion follows a retained path:
each filter is necessary, and every permitted successor is closed into
the set. Conversely every stored state is reached from the seed by the
enumerated transitions. Self loops account for arbitrarily long
profile-preserving interleavings.

For counting effective words, delete self loops from the profile graph.
The potential

    2*(number of positive low and high entries)
        +32-(sum(low)+sum(high))

strictly decreases along every remaining edge. The graph is therefore
acyclic. The generator accumulates the terminal path-length polynomial
in increasing potential order, counting each comparator label. The
checker instead recursively counts paths on full thirteen-wire profiles,
memoizes them, and detects non-loop cycles. Both obtain the same two
coefficients. These count words of comparator labels in the profile
relaxation, without identifying words related by disjoint commutations.
They are not counts of sorting networks.

## Reproduction, certificate and trust boundary

Use standard-library Python3.11+ without `-O`:

```sh
python3 generate.py
python3 verify.py
```

`generate.py` uses packed original marker masks, direct active-vector
transport, breadth-first closure, and polynomial counting on a directed
acyclic graph. `verify.py` imports no generator code. It simulates
distinct scalar ranks for all78 original minimum pairs and78 maximum
pairs, builds inverse comparator fibers on all78 full13-wire pairs,
then reconstructs full13 profiles by depth-first closure. It checks all
55*78*2=8580 local active-comparator marker transitions. Its recursive
word counting uses those full13 profiles, rather than reduced vectors.

Both implementations compare the canonical state and edge hashes.
Canonical states are lexicographically sorted tuples of the two weight
vectors and the flag. Canonical labelled edges are sorted
(source_state,(a,b),destination_state) tuples. JSON encoding uses the
separators `(',',':')`; SHA256 is applied to those ASCII bytes. Hashes
are compact commitments rather than opaque proof premises: both
programs regenerate every entry. The private comparison also checked
actual equality of the2214 state sets and22536 edge sets before these
public summaries were prepared. `source-manifest.json` pins the public
source, fixture and certificate bytes.

The certificate includes a shortest10-event terminal profile word.
That word sorts the extreme marker images only; it is not a B11 sorter.
The independently checked23-gate control supplies the known upper bound.
The existing S(13)>=44 supplies the B11 lower bound22. The table status,
pruning/standardization bridge and parent P20 theorem are explicit
mathematical imports. Older proof corpora are not replayed.

Independent algorithms here are by this researcher, not an external
reviewer or a proof assistant. A separate bounded SAT search using this
constraint returned UNKNOWN, which is not a premise of the theorem.
No unrestricted S(13) exclusion,44-gate witness, or coverage of other
Q20 minimum branches is claimed.
