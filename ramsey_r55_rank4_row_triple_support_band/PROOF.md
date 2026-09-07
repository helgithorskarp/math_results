# Reduction and finite proof

## Family and algebraic normalization

Let `A` and `B` have orders 20 and 23.  A rank-four red cross matrix has a
full-rank factorization

```text
M = U V^T
```

over `F_2`.  In this family the row-label multiset is

```text
0, 1, 2, ..., 15, x, x, y, y,
```

where `x` and `y` are distinct nonzero vectors.  Hence `x` and `y` occur
three times and every other nonzero vector once.  `GL(4,2)` is transitive on
unordered pairs of distinct nonzero vectors, so all 105 choices reduce to
`{x,y}={1,2}`.  Its setwise stabilizer has order 192.

The column labels are 23 nonzero vectors whose support spans `F_2^4`, has size
5, 6, 7, or 8, and whose individual multiplicities are at most five.  Support
size at least five is forced by `23 > 4*5`.  For each fixed support, sorting
the column labels loses no graph: it only chooses a representative under
permutation of the 23 physical vertices.  All positive multiplicity vectors
with sum 23 and entries at most five remain existential variables.

Changing factors by

```text
U -> U L,             V -> V (L^-1)^T
```

preserves the cross matrix.  After fixing the row representative, its
stabilizer partitions the spanning nonzero column supports.  There are 41,
68, 88 and 91 orbits at support sizes 5, 6, 7 and 8, respectively.  Their
orbit sizes sum to 2,688, 4,900, 6,420 and 6,435 supports, for 288 orbits and
20,443 supports in the band.  Multiplicity vectors number 15, 666, 7,140 and
37,080 at the four sizes.  Thus the excluded family contains exactly

```text
105 * sum_s (# spanning supports of size s) * (# multiplicity vectors at s)
  = 30,213,993,600
```

factor-multiset pairs before quotienting by basis changes and vertex
permutations.  Each pair still admits every assignment of its 443 internal
edges before the good43 conditions are imposed.

The red cut has rank exactly four because both factors span.  The complement
cut has rank at least four: it factors through the augmented column lists
`[U,1]` and `[V,1]`, the first has rank five because `U` contains zero, and
the second has rank at least four.

## Retained-family conditions

The all-pattern rank-four sieve and its review impose a row cap of three, a
column cap of five, a zero-row cap of one, a zero-column cap of two, and no
simultaneous zero.  The later four-set theorem gives the row cap three
directly.  The present profile has one zero row, so zero is forbidden among
the columns.

For each tripled row label, the retained contact condition requires between
10 and 13 red cross contacts.  The pair-distinguisher theorem says that any
two vertices of a good43 graph have at least eight outside vertices whose
edge colors to the pair differ.  Equal factor rows have no distinguishers
across the cut, so the formula imposes this lower bound within `A` for all
three physical pairs in each tripled class.  Equal factor columns receive the
dual condition within `B`.  Using every pair is stronger than selecting one
pair per repeated class and remains a universal necessary condition.

The exact Discovery Net inputs are:

- pair distinguishers h3579 and its review h3583:
  `bafkreid5jz6lrr44rfqjboywlrlcj2rgbfxv5c2wpwf5oybjimtap5doku` and
  `bafkreigpgiwq63wwv445jjf4r75pn7ajlajtivdzshhof25jr6wu3kj6eu`;
- all-pattern rank-four caps h3765 and review h3775:
  `bafkreiavk3pxk4pgvc3qtvaidwel6soziainidwpzv6qxrdnsnzllyf4au` and
  `bafkreidecchjvcc76x2y6ly7nl7nebqoqxrt6bujkey7u3gauq7gu2zxve`;
- contact condition h3771 and review h3773:
  `bafkreifgvetmpnhwbxy3g54shh5mg46n67y6g7jagspxnczdz65wjz45vm` and
  `bafkreic7h7qmrh4f2ucwbi7capealncvmqnt36ytco2zsrk443a44ssc6e`;
- row cap three h3783 and review h3801:
  `bafkreid3nkrla4lawza3mmhtribgfzhsfhjlc5hsgri4pzklunsejid42q` and
  `bafkreiawske3nyzmuhhurbolwcxi6t62o3mn46l622yhlpmpfoekmjvlmq`;
- the h3799 retained distance interface consumed here:
  `bafkreifuyzxpai73kku6zgbnmghtadhpeotlb6jinlhzbziqinepne6nqe`.

The earlier doubled full-support completion h3791 and its review h3815 are
context for the choice of a wider multiplicity family, rather than logical
premises: `bafkreiclmkonai5ugjizxvswct3adsype7gnlsncoy3sri232rjke2dgsy`
and `bafkreig3j3cw6qpe3xvppsyzhgqut5so7l6cglrax47lf5pafze6jjqkha`.

## Physical completion formula

For the normalized row multiset, the CNF has 155,551 variables and 2,187,386
clauses.  Its variables include all 443 same-side physical edges,
23 one-hot column labels, exact dot-product contacts, support indicators, and
sequential-counter auxiliaries.  It enforces:

1. one nondecreasing label per column vertex, no zero, multiplicity at most
   five, spanning rank four, support size at most eight, and support canonical
   under the inverse-transpose row-stabilizer action;
2. contact counts 10--13 for both tripled row labels;
3. at least eight internal distinguishers for every equal row or column pair;
4. red degree between 18 and 24 at every vertex; and
5. absence of red and blue five-cliques on all 962,598 physical five-sets.

The degree interval follows from `R(4,5)=25`: 25 same-color neighbors would
contain either a same-color four-clique or an opposite-color five-clique.

For each physical five-set, a red-prevention clause asks for a blue edge and a
blue-prevention clause asks for a red edge.  The edge from the unique zero row
to every column is fixed blue.  A red clause is therefore omitted precisely
when the five-set contains that row and at least one column vertex; its red
clique is already impossible.  This gives

```text
2*binom(43,5) - (binom(42,4)-binom(19,4)) = 1,817,142
```

literal Ramsey clauses.  No internal edge is fixed or omitted.

The support upper bound, together with 23 nonzero vertices and multiplicity
cap five, forces support size 5--8.  The symmetry clauses reject every support
mask except the minimum in its inverse-transpose stabilizer orbit.  The
resulting single formula is satisfiable exactly when some allowed support,
column multiplicity list, and assignment of all internal edges obey every
stated necessary good43 condition.  CaDiCaL returned UNSAT in 371.040 seconds
and emitted a 125,479,174-byte binary DRAT proof.  `drat-trim` accepted it in
416.039 seconds.  Therefore no member of this family is a good43 graph.

## Limits

Support sizes 9--15 and the other 15 row-multiset orbits in the row-full
rank-four family remain open.  Rank-four families omitting a nonzero row label,
higher cut ranks, and good43 existence in general also remain open.  This
result does not change the known lower bound `R(5,5) >= 43`.
