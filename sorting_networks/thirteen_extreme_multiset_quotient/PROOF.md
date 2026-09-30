# Exact comparator-multiset quotient of the coupled B11 profiles

Author and executing agent: **six-sorting-1, researcher**, 2026-09-30.
Standard comparator (a,b), a<b, sends the smaller value to a. A network
is a sequential word of these comparators; no layer or depth restriction
is imposed.

## Target and imports

The literal prefix P20 is in `fixture.json`. Put P19=P20[:-1],
Q20=P19;(10,12), and P22=Q20;(0,5);(0,1). P22 holds the global minimum
on original port 0 and maximum on original port 12. Its projected
Boolean image on original ports 1..11, now labelled 0..10, is B11 with
158 states. The checker reconstructs this image from all 8192 original
Boolean inputs and verifies the included 23-gate completion.

The necessary coupled-profile normal form is imported from
[the parent source](https://github.com/helgithorskarp/math_results/tree/main/sorting_networks/thirteen_joint_extrema_normal_form),
commit `65a48340a24e9a4d8b294f590e12d4328a72808f`, graph7871
`bafkreiew3rysxid3p77hllln3pqhf7tyw7rift5gcx5qpy3pbaqtwlwwvy`.
Its proof imports the P20 suffix minimum25, weighted extreme pruning,
and S(11)=35 from [Harder](https://arxiv.org/abs/2012.04400v3).
The unrestricted S(13) interval is still44..45 in the
[maintained table](https://bertdobbelaere.github.io/sorting_networks.html),
checked2026-09-30. These are mathematical imports, not the new result.

The complementary
[P19 binary-minimum reduction](https://github.com/helgithorskarp/math_results/tree/main/sorting13_P19_binary_minimum_reduction),
by six-sorting-2, researcher, commit
`ca993bc042ba81442a4afccb0d374d142696d0e7`, graph7885
`bafkreiada56oxpnrld7oh7kxfouijytxi57gdnesul72jhdwcnxw7sdlla`,
excludes all other Q20 minimum words. It proves that a full44 sorter
starting with P19 exists if and only if B11 has a22-gate sorter.
This equivalence extends the scope of the present quotient to all P19
completions. Its source was read and its generator and separate checker
replayed privately, including all28 stored phase-profile sets. Its
transitive prefix/pruning dependencies remain imports.

## Parent profile system

For every original pair of minimum positions, retain at each current
marked pair the largest number d of prefix comparators touching either
mark. Define the maximum profile dually. Touching both marks counts
once; stationary comparisons are charged. With W=sum 2^d, the pruning
bound for a full44 sorter is W<=2^(44-S(11))=512 for each polarity.
The held extreme is outside the active ports. In units32 the active
partner weights after P22 are

    low  = (4,2,2,2,2,0,2,0,0,0,1),
    high = (0,0,0,0,0,4,0,2,4,4,1).

An active comparison (a,b) replaces its two low weights by
(2*max(u,v),0), and its two high weights by (0,2*max(u,v)). Each profile
sum is at most16. The first comparison involving port10 has partner
p in {1,2,3,4,5,6,8}; the parent excludes0,7,9. Earlier effective
events are equal-weight binary merges. At the first10 comparison both
sums reach16, and the low/high supports become disjoint. Its low part
is either binary or unary, and its high part is unary. Every later
effective event is an equal-weight binary merge in exactly one profile.

Here an event is effective if it changes at least one profile, including
the first10 flag. Every actual B11 completion gives a path in this
system. Comparators preserving both profiles may still change other
Boolean values and can occur anywhere. Projecting them out is solely
for extreme-profile analysis.

The complete parent graph has2214 reachable states and22536 labelled
edges including self loops. Its single terminal state is low weight16
on0, high weight16 on10, and the first10 flag set. Removing self loops
leaves an acyclic graph: the integer potential

    2*(number of occupied low and high entries)
        +32-(sum(low)+sum(high))

strictly decreases on every remaining edge. There are751950 terminal
effective words of length10 and2266650 of length11. These statements
and the parent state/edge hashes are independently reconstructed here.

## Repetition lemma

**Lemma.** Every terminal effective word of length10 has distinct
comparator labels. Every terminal effective word of length11 has at
most one repeated comparator, appearing exactly twice. If it repeats,
it is a minimum binary comparison (a,p), a<p, appearing once before
and once after the first (p,10) event.

**Proof.** A minimum binary merge on (a,b) removes b from its support;
a maximum binary merge removes a. Neither type introduces a new
occupied port. The maximum unary part of the first (p,10) event leaves
the already occupied port10 occupied. Thus maximum support only shrinks.
Minimum support also only shrinks except possibly at this single event:
if its minimum part is unary, the empty port p becomes occupied as10
becomes empty. Port p is the sole port that can reenter minimum support.

A repeated minimum binary label (a,b) would require b to reenter its
support after its first occurrence. Therefore b=p and the two
occurrences straddle the first10 event. The first occurrence removes p
before this event; at most one minimum binary comparison can remove p
in that phase. The second removes p irreversibly afterward. Hence there
can be only one repeated minimum label, and it occurs at most twice.
Maximum binary labels cannot repeat because their removed ports never
reenter maximum support.

A binary label other than the first (p,10) label cannot be effective
in opposite polarities at two different times. Before the first10
event the supports are disjoint
off10, and a preceding binary event avoids10. Afterward they are fully
disjoint. Both endpoints of a minimum binary event are absent from
maximum support then, and maximum support never grows. Both endpoints
of a maximum binary event are absent from minimum support then. Only
one of them could later acquire a minimum weight, namely p, whereas a
minimum binary event requires two occupied endpoints. Thus changing
polarity cannot cause repetition for these other labels.
The first (p,10) label itself cannot
repeat effectively: no earlier event uses10, and afterward its two
endpoints have disjoint low/high roles, with no support growth allowed.

In the length10 case the low split is binary, so minimum support never
grows and no label repeats. In the length11 case the low split is unary;
the preceding argument gives the assertion. QED.

Repetition really occurs in the necessary relaxation. The fixture's
following terminal effective word repeats (1,2) around split (2,10):

    (1,2),(2,10),(2,3),(1,2),(4,6),(0,4),
    (0,1),(7,10),(5,8),(9,10),(8,10).

Initially the first (1,2) minimum merge clears2. The unary split returns
a minimum weight to2, and (2,3) doubles it to equal the weight on1.
The second (1,2) is therefore allowed. Both programs check every step
and its terminal profiles. This profile word is not claimed to sort B11.

## Exact480-class quotient

Encode a comparator multiset by a base4 digit for each of the55 pairs
in lexicographic `combinations(range(11),2)` order. Each digit is its
effective occurrence count, at most2 by the lemma. The packed integer
uses two bits per comparator; JSON stores it as a decimal string.

At the terminal graph state assign the empty multiset count1. At every
other state, for each outgoing non-loop edge labelled g, add one g to
each suffix multiset and sum the suffix word counts. This recurrence
is exact by partitioning labelled paths by their first edge. Evaluating
it in increasing potential gives every terminal effective multiset
from the initial state, with its number of labelled words. The result is:

| Effective events | Repeated labels | Classes | Effective words, all classes at this length |
|---:|---:|---:|---:|
| 10 | 0 | 135 | 751950 |
| 11 | 0 | 297 | 2062440 |
| 11 | 1 | 48 | 204210 |

There are exactly480 classes and3018600 effective words. The certificate
contains the entire480-entry table of code, event length, and word count,
not only these totals. Its canonical class-table SHA256 is
`5ac42c7b2ec5cc5485ea107338ddd20eaf9f8e5a56a6cbb8aa3e87e803799042`.
It also records the parent state hash
`d9481729ef2857403f8ff6a39b5442e4cd2e98bf55a915e58070bc75046e888b`
and edge hash
`427c556cc7abd4c44fab58e70233f13820747ab3eac759aad10b0ab66f4fb585`.

The independent checker explicitly walks all terminal effective words
on full thirteen-wire inverse-fiber profiles. For every word it adds
one to that word's multiset count. It compares all480 codes and their
individual counts, not just the totals or hashes. It separately checks
the11690 distinct suffix-class entries across all graph states by a
recursive set computation with cycle detection. Neither program has
an operational cutoff. The finite graph and strict potential decrease
establish termination and complete coverage.

## Construction-search interface and scope

For a fixed certified multiset m, `build_class_graph` uses states
(profile,used), where used records consumed multiplicities. A profile
self loop leaves used unchanged. A non-loop edge labelled g is retained
exactly when used[g]<m[g], and then increases used[g] by1. Acceptance
requires the terminal profile and used=m. Induction on word length
shows that this recognizes precisely all full comparator words whose
effective projection belongs to m. Every profile-preserving comparison
and every permitted ordering remains available. Two-bit quotas handle
the repeated comparator correctly. Dead states may be retained; they
do not create accepting paths.

The helper is exercised on the repeated example class. Its graph has
158 states and1402 labelled edges including self loops; the checker
independently reconstructs these counts using full thirteen-wire
inverse profiles and quotas. This is an example class graph, not the
158-state Boolean target merely because their sizes coincide.

Adding all158 Boolean row constraints and an exact22-comparator budget
to any of these480 class graphs gives a complete partition of the B11
construction problem. The quotient does not make every multiset order
valid, justify moving events to the front, or assert that a profile
word sorts other values. No class has been excluded by this certificate.
No44 sorter or unrestricted lower bound45 is established.

The rank/inverse checker is algorithmically separate but written by the
same researcher. No external reviewer verdict or proof-assistant result
is asserted. The deletion/standardization bridge is unformalized;
primary size bounds and earlier prefix theorems remain explicit imports.
The present certificate replays the complete coupled graph and quotient,
not older large proof corpora. The separate search experiments are not
premises of this result.
