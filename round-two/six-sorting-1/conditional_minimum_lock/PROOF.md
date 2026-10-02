# An original-domain minimum excludes the entire partner-1 prefix

Author and executing agent: **six-sorting-1, researcher**, 2026-10-02.
Status: scoped author-proved lemma, with exact finite premises checked by
separate same-author algorithms. The ordinary argument is written below;
it is not a proof-assistant theorem or an external-person review verdict.

## Statement

A standard comparator `(a,b)`, `a<b`, writes the minimum to physical port
`a` and the maximum to `b`. Ports are `0..12`. Let B23 be the literal word

```
(0,11),(1,7),(2,4),(3,5),(8,9),(10,12),
(0,2),(3,6),(4,12),(5,7),(8,10),
(0,8),(1,3),(2,5),(4,9),(6,11),(7,12),
(0,1),(2,10),(4,8),(3,6),(9,11),(11,12).
```

Put `L1=(1,3),(2,4),(1,2)` and `P=B23;L1`, a 26-comparator prefix.

**Lemma.** Every standard thirteen-input sorting network beginning with
this literal P has at least **45 comparators**. The suffix can have any
depth, order, repeated comparisons, preparation length or HIGH event type.

This is an exclusion of one conditional prefix, not an exclusion of all
44-comparator thirteen-input networks. No 45-comparator completion of P
is claimed. The [maintained table](https://bertdobbelaere.github.io/sorting_networks.html),
checked 2026-10-02, still gives `44 <= S(13) <= 45`.

## A general conditional minimum-lock obstruction

Fix r original inputs to r distinct ordered ranks below all k=n-r free
Boolean inputs. Suppose a prefix sends the marked ranks, in increasing
order, to physical ports `0..r-1`, touches a marked rank at exactly D gates,
and leaves physical port r equal to the minimum of all free inputs on
every assignment of the **entire original k-dimensional free cube**.
Suppose `S(k)>=L` is an established lower bound. If a full n-input Boolean
input has the wrong order statistic at port r after this prefix, then no
standard sorting completion has total size at most `D+L`.

To prove this, assume such a completion of total size m. By the zero-one
principle it sorts the clamped ranks as well as Boolean inputs. Marked
pruning transports free-wire labels through marked exchanges. Deleting
all gates touching a mark gives an oriented k-wire Boolean sorter.
The size-preserving standardization bridge gives its size at least L.
This is the ordinary pruning interface of
[lemma8539](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sorting-2/semantic-pruning/PROOF.md)
and [Harder's primary paper](https://arxiv.org/abs/2012.04400).

If any suffix gate touches a physical marked port, consider the first such
gate. The marks have remained at `0..r-1` up to that gate, so its marked
touch adds one to D. Pruning then leaves at most `m-D-1 < L` comparisons,
a contradiction. Consequently no suffix gate touches `0..r-1`.

If any suffix gate touches r, consider the first one. All preceding
suffix gates have avoided both r and the marked ports. They only compare
other free values; every one of these values is at least the unchanged
minimum at r. The gate is standard `(r,q)` with `q>r` and is therefore the
identity on the entire original free cube, even after arbitrary such
preparations. It is free, hence distinct from the D marked deletions.
Delete it as well. The resulting k-wire Boolean sorter again has at most
`m-D-1 < L` comparisons. This is impossible.

Thus the fixed suffix schedule contains no comparison incident to r.
It leaves r unchanged on **every** original full input, including the
specified Boolean input whose order statistic at r is wrong. Such a
schedule cannot sort. This proves the obstruction.

The only computational premise is the conditional minimum and marked
route at the prefix. Future preparation functions or suffix lengths are
not enumerated. Standard orientation matters: a reversed logical pair
could move an already minimal value away from physical r. Oriented free
circuits produced by pruning remain allowed in the lower-bound bridge;
the n-input completion in the lemma is standard.

## The tight original restriction

For P, fix **original** inputs 3 and 5 to `-2,-1`, respectively. All
eleven other original inputs vary independently in `{0,1}`. This is LOW
mask `40={3,5}`, HIGH mask zero. On every one of its 2048 assignments,
P ends with `-2,-1` at physical ports 0 and 1. Its exact record is

```
[original_LOW,original_HIGH,current_LOW,current_HIGH,D,R,R_mask]
= [40,0,3,0,9,0,0].
marked-touch mask = 50737800;
marked gates (one based) = 4,8,10,13,14,18,19,25,26.
```

Every touch counts, including stationary and shared-marker comparisons.
There are nine marked deletions and no free identity in the prefix.
The eleven surviving physical ports are `2..12`. The free-carrier route
maps the original free labels to output indices by

```
original free ports: 0,1,2,4,6,7,8,9,10,11,12;
input-to-output indices: 0,1,3,2,4,5,6,7,8,9,10.
```

After this global relabelling the retained oriented 17-gate prefix Q is

```
(0,9),(1,5),(3,2),(6,7),(8,10),
(0,3),(2,10),(6,8),(0,6),(2,7),(4,9),
(5,10),(2,6),(1,4),(7,9),(9,10),(0,1).
```

Here an oriented pair writes min to its **first** label; `(3,2)` is
deliberately retained. Output label 0 is physical port 2. The scalar
checker reproduces the full carrier function on all 2048 inputs.

There is also a short ordered-input identity. Write `x0..x10` for Q's
input labels. After Q's gate 9, wire 0 equals

```
A=min(x0,x9,x3,x2,x6,x7,x8,x10).
```

No gate changes wire 0 before the final `(0,1)`. After gate 14, wire 1
equals

```
B=min(x1,x5,x4,max(x0,x9)).
```

No gate changes wire 1 before the final gate either. Since
`max(x0,x9)>=min(x0,x9)>=A`, the last gate gives

```
min(A,B)=min(x0,x1,x2,x3,x4,x5,x6,x7,x8,x9,x10).
```

Thus physical port 2 is the minimum of the free values. Independently,
the checker propagates exact monotone DNFs through min/max gates,
distributing AND over OR and absorbing supersets. With a bitmask denoting
a conjunction of variables, Q gate 9 wire 0 has DNF `[1997]`, gate 14
wire 1 has DNF `[51,562]`, and final wire 0 has DNF `[2047]`. The final
term contains every one of the eleven variables. All 2048 clamped
assignments also verify the minimum directly.

Import `S(11)>=35` from Harder's paper. Its large lower-bound corpus is
not replayed here. Apply the obstruction with r=2, k=11, D=9 and L=35,
so `D+L=44`. Any additional marked or free-identity deletion would force
`m>=9+1+35=45`. It remains to exhibit the wrong full-input order statistic.

## The full Boolean witness and controls

Let original Boolean input integer 235 use bit i for physical input i:

```
input  = [1,1,0,1,0,1,1,1,0,0,0,0,0];
P(input)=[0,0,1,1,0,1,1,0,0,0,0,1,1];
sorted = [0,0,0,0,0,0,0,1,1,1,1,1,1].
```

Physical port 2 is 1 and must become 0. The suffix cannot touch it by
the preceding obstruction, so no size-at-most-44 completion can sort.

As finite controls, append each of the twelve possible standard gates
incident to physical 2. Gates `(0,2),(1,2)` give `D10,R0`; the ten
gates `(2,q)`, `3<=q<=12`, give `D9,R1`, with redundancy bit `2^26`.
Each has single-original-domain deletion count 10 and lower bound 45.
These controls test the count at the immediate prefix. Coverage of an
arbitrary future preparation is the invariant proof above.

Original LOW mask `5={0,2}` provides a necessary negative control. It
also has current LOW mask 3, D9 and R0 at P, but its physical port 2 is
**not** the free minimum. At free assignment 571, in ascending order of
the eleven original unmarked inputs, it gives

```
input  = [-2,1,-1,1,0,1,1,1,0,0,0,1,0];
P(input)=[-2,-1,1,1,0,1,1,0,0,0,0,1,1].
```

The free minimum is 0, whereas port 2 is 1. Equality of the current
marker configuration and deletion counts does not identify the original
conditional function. The semantic damage test switches to this valid
original restriction and rejects the minimum property itself, rather
than merely rejecting a fixture checksum or fixed-mask mismatch.

Positive controls check the primary 35-comparator eleven-input sorter on
all 2048 Boolean inputs. A 71-comparator completion of P, formed by
insertion-sorting physical ports 2 through 11 with 45 additional adjacent
comparisons, sorts all 8192 original Boolean inputs. This larger positive
completion shows the prefix is sortable; it supplies no size-45 witness.

## Consequence for the coordinated frontier

[Actual9325](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sorting-1/one_sided_low_binary_barrier/PROOF.md)
normalizes every B23 completion whose first strict ordinary LOW pair-mass
increase is binary to one of L1, L2 or
`L4=(3,4),(1,2),(1,3)`, without changing its function or comparator count.
That result already excludes L2. This lemma now excludes L1 completely.
Consequently **only L4 remains** in that first-LOW-binary branch.

[Actual9420](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sorting-1/both_first_binary_barrier/PROOF.md)
requires a first strict HIGH singleton after L4. The exact L4 ten-wire
image has 157 states and an 18-comparator budget. L4's free-operand
preparations, first-LOW-singleton cases, the changed ancestor and the
unrestricted 44..45 gap remain unresolved. This corollary imports the
published normalization and HIGH exclusion; the literal P lemma does
not require them.

## Reproduction and trust boundary

[README.md](README.md) gives exact commands. The compact certificate is
3637 bytes, SHA256
`afc2d7cab06f8574f78a5c4aedc5c28b3978847ad8a0ed942ea7c8b1e38137d2`.
Packed-column production and standalone scalar/lattice verification agree
in normal and optimized Python. All fourteen damaged premises reject.
[expected.json](expected.json) gives the exact finite record;
[SOURCE-CREDITS.md](SOURCE-CREDITS.md) identifies copied generic primitives
and imported mathematics. No solver or suffix search is required.

The finite checks establish the literal route, conditional free function,
minimum identity, Boolean witness and controls. The written invariant,
zero-one principle and size-preserving generalized-network pruning bridge
remain unformalized. Known `S(11)>=35` is imported primary literature, not
a newly proved lower bound. Independent algorithms here are executed by
the same researcher and do not constitute an independent reviewer verdict.
