# Proof of the conditional nullary-minimum exclusion

Author: **six-sorting-1, researcher**. Definitions, literal prefixes,
reproduction and scope are in [README.md](README.md).

Write L(n) for the imported lower bounds in `known_lower_bounds`; in
particular L(7)=16, L(11)=35, L(12)=39 and L(13)=44.
If a proposed completion lifts to a44-gate thirteen-input sorter, fix
some original inputs to a block of largest or smallest distinct values.
Delete each gate touched by a marked extreme, counting a doubly touched
gate once. If the fixed prefix deletes D gates and k unmarked inputs
remain, the suffix can delete at most44-L(k)-D gates. Threshold colors
determine both the deleted-gate count and the remaining marker positions
independently of internal rank orders. The listed witnesses use all13
distinct ranks; their finite replay is in `verify.py`.
This is established extreme-value pruning, not a new general theorem.

A44-gate global sorter has no comparator redundant on its complete
Boolean domain: deleting one would contradict L(13)=44. Every partial
target here is a complete image of its literal global prefix, so redundancy
on that image also gives this contradiction.

## The complete second-minimum cover

Assume some Vj has an18-gate sorter. Its P26 lift has44 gates.
The one-zero leaves of Vj are precisely0,1,2,3,4,6,7. They cover every
non-all-one row: some one-zero leaf position is zero. The14 original-rank
witnesses give passage caps2 at leaf0 and3 at the other six leaves.
A passage counts a selected gate even when the zero remains stationary.

Track these seven single-zero paths to their common final position0.
Suppress every unary passage to obtain a binary merge tree with depths
di no greater than the path passage counts qi. Kraft gives

    1 >= sum(2^-di) >= sum(2^-qi) >= 1/4 + 6/8 = 1.

Equality forces qi=di=2,3,3,3,3,3,3, with no unary or post-merge passage.
The kernel therefore has six binary gates. Before any selected gate,
nonkernel gates avoid every occupied minimum position. Each endpoint of
a later kernel gate remains occupied until its merge, so a nonkernel
gate before it has disjoint endpoints. Adjacent commutation moves all
six kernel gates to the front without changing the Boolean map or cost.
The final minimum is then on original wire1 and can be removed.

There are exactly45 tree types. Choose two of the six other leaves to
join leaf0's three-leaf branch (15 choices), and pair the other four leaves
in its sibling four-leaf branch (3 choices). Comparators send each branch
minimum to its least wire. The fixture gives one word per tree. Independently,
`verify.py` enumerates all56,700 labelled binary merge histories, accepts
the900 cap-feasible histories and checks that they have exactly45 clade
signatures and commute to the fixture words. This enumeration checks the
finite classification; the Kraft/commutation argument excludes unary and
interleaved kernels, including arbitrary allowable depth.

Thus every V18 sorter would leave a12-gate sorter for one of the45
U images in its Y case. No case has been discarded by a timeout.

## A maximum kernel is forced in every one of the90 U12 cases

Fix one U case and assume a12-gate sorter Q. U contains the one-hot
leaves4,7,8 and contains the one-zero rows at0 and1. Write qi for the
passage count on the one-hot-i path. Its maximum8 path stays at8.
Each listed mixed witness has, after P32, exactly one residual high
mark at8 and one residual low mark at a leaf ell in0,1,2. The witnessed
union passage cap is2; initially every U row satisfies xell<=x8.

The low mark's position p only decreases. Its current Boolean value on
any U row is at most the initial value xell; the value at8 is at least
the initial x8. A gate jointly touched by these two markers would be
(p,8), already ordered on every U row, hence redundant. Such an overlap
is impossible in a44-gate lift. The two path counts therefore add and
satisfy q8+r_ell<=2. Both are at least one: another one-hot leaf must reach8;
if ell>0 its zero must reach0, while if ell=0 the one-zero row at1 forces
a gate on0, touching the stationary zero0. Consequently q8=r_ell=1.

Wire8 occurs in just one gate. The one-hot7 input can reach8 only through
(7,8), so this is that unique gate, denoted g. Every U has a listed
two-one row with initial x8=0. It must finish with ones at7/8. At g it
must transfer a one from7 to8, leaving7 zero, and since there is no later
gate on8, a later gate(p,7), p<7, must refill7. Call one such later gate h.

Now use the two-high rows A={4,8} and B={7,8}. Their separately checked
original-rank witnesses give high-passage caps3. Until g, the8 mark is
stationary and no gate touches8. On A the other mark follows exactly
the one-hot4 path and must arrive at7 before g. Thus A pays q4 high
passages through g. On B it pays q7 through g. At g both rows have ones
on7/8; without a later8 gate, their7 bit stays one. Both pay one further
high passage at the mandatory refill h. Therefore

    q4+1 <= 3,   q7+1 <= 3,   q8=1.

The three-leaf maximum tree now has caps2,2,1, whose Kraft sum is exactly1.
The same equality argument eliminates all unary passages. Since7 can
merge upward only at8, its binary kernel is uniquely

    (4,7),(7,8).

It commutes to the front by the occupied-position argument. Every nonzero
U row has a one among4/7/8, so this kernel finds the maximum on8, which
can be removed. A U12 sorter would thus yield a ten-gate sorter of its
eight-wire F image. The checker replays all180 two-high witnesses, all240
mixed witnesses, all90 reset rows and the complete original Boolean images.
This terminal-refill cut adapts the cited K18 idea, without transferring
any K18 hypothesis to U.

## Nine complete sequential F10 certificates

All45 F images are identical across the two Y cases. Each contains the
entire sorted Boolean chain. The certificate partitions the45 indices
among sources8,7,26,19,34,22,1,21,29, of sizes
38,44,46,48,48,49,50,52,52. Every supplied permutation maps its source
pointwise into the target; `verify.py` checks every row and inclusion.

The size monotonicity used here includes input permutations. Relabel a
target sorter to sort a permuted source, then standardize its generalized
comparators, propagating any exchanged output labels to the end. Gate
count is unchanged. The resulting standard word differs only by an output
permutation from sorting the source. A standard word fixes each sorted
chain row, and all those rows belong to the source. The residual output
permutation therefore fixes every chain row, hence every wire; the word
sorts the original source. This is the usual standardization argument,
not an unproved permission to relabel a standard network arbitrarily.

For each source, the complete P34 Boolean image and original-rank witnesses
give the `single_threshold_rows` passage caps. Each surviving mixed
witness extends through(4,7),(7,8): only the second gate is a deletion,
the final residual high mark retires, and the F minimum passage cap is1
at `minimum_leaf_cap1`. This extension is replayed independently.

The encoder represents ten sequential standard gates, with every one of
the28 wire pairs allowed in every slot. Each Boolean row has exact AND/OR
transitions and its sorted final state. High passages are input ORs and
low passages are the negations of input ANDs. Fixed initial leading zeros
and trailing ones stay fixed under all standard comparators. No layer
bound, future-interval, pure-side, kernel normal form or lexicographic
filter is used. Any ten-gate sorter for the source yields a44-gate global
sorter and must satisfy the witnessed pruning caps, so it gives a model
of this CNF.

Every one of the nine CNFs has a checked refutation. The manifest gives
the exact variable/clause counts and full-CNF/proof SHA256 hashes.
Glucose4 returned UNSAT with native proof output; DRAT-trim independently
verified each trace. A solver-free forward RUP implementation then checked
all84,339 additions against the full CNFs, ignoring deletions and accepting
the final empty clause only after unit propagation. Its finite control
tests and separate reference comparison are recorded in README.md.
The source regenerates exactly these CNFs/traces; the large generated
files stay in scratch. Solver answers alone do not establish exclusion.

Thus all nine source sets, all45 F images and all90 U cases have no
respective ten-/twelve-gate sorter. The complete minimum cover excludes
every V18 sorter. Shorter V sorters would lift to at most43 global gates,
already excluded by L(13)=44.

## Sharp upper bounds and the Y corollary

The fixture's eleven-gate word sorts the shared38-state image at tree8.
Its first two gates(0,2),(0,1) replace a three-gate control on wires0/1/2:
the only missing initial three-bit pattern is010, on which that two-gate
word would fail. Direct scalar verification checks the actual entire
word and both45-gate lifts on all8,192 inputs each; this is the upper
bound evidence, not merely the three-bit observation.

It follows that S(F38)=11. Prepending the maximum kernel gives13-gate
U sorters at tree8, so their51-/50-state images have exact size13.
Prepending the six-gate minimum tree gives19-gate V sorters, so
S(V1)=S(V2)=19. Thresholding commutes with comparison, giving the usual
zero-one implication for their full45-gate thirteen-input lifts.

Finally, in a Y20 sorter whose minimum1 path has one passage, a binary-only
minimum kernel on leaves0/1/5 must be(0,5),(0,1): any other first binary
merge makes leaf1 pay twice. Nonkernel gates commute past its occupied
positions, putting it at the front and producing a forbidden V18 sorter.
Hence that Y branch requires a unary passage. The cited interleaving lemma
then requires at least two nonkernel events before final merge(0,1).
Unary minimum kernels and the other maximum-route branch remain open.
None of these literal-prefix results excludes arbitrary thirteen-wire
networks or resolves S(13).
