# An unrestricted four-branch CEGIS mechanism for a good43

## Scope

A **good43** is a simple graph on 43 vertices with neither a clique nor an
independent set of order five.  This directory establishes a complete
target-facing construction mechanism: every possible good43 occurs, up to
vertex relabeling and interchange of the two colors, in one of four SAT
branches processed by `cegis.cpp`.  There is no automorphism, regularity,
catalog, packing, seed graph, edit-radius, or local-repair assumption.

The pass-1 pilot did **not** find a good43 and did not prove any branch empty.
The result here is the unrestricted finite mechanism and its physical verifier,
not a Ramsey-number improvement or a candidate record.

## Literal target formula

For every physical pair `0<=i<j<n`, let `x_ij=1` mean that `ij` is a red
edge; zero means blue.  For every five-set `Q`, let `E(Q)` be its ten pairs.
The two Ramsey clauses are

\[
 B_Q=\bigvee_{e\in E(Q)}x_e,
 \qquad
 R_Q=\bigvee_{e\in E(Q)}\neg x_e.                 \tag{1}
\]

The first clause says that `Q` is not all blue, and the second says that it is
not all red.  Thus an assignment satisfies every clause in (1) if and only if
its physical graph is good.  There are

\[
 2\binom{43}{5}=1,925,196
\]

such clauses on 903 physical variables.

## Four branches cover the unrestricted target

The classical result `R(4,5)=25` gives

\[
                         18\le d(v)\le24             \tag{2}
\]

at every vertex of a good43.  Indeed, the neighborhood of `v` is a
`(4,5)`-graph and hence has at most 24 vertices.  Applying the same statement
to the other color gives `42-d(v)<=24`.

Choose any vertex.  If its red degree is at most 21, retain the color
orientation.  Otherwise interchange red and blue, giving degree `42-d(v)`,
which lies between 18 and 21 by (2).  Relabel the chosen vertex as zero and
its neighbors as `1,...,d`.  Consequently every good43 has a representative
in one of exactly four branches

\[
                         d(0)=18,19,20,21.             \tag{3}
\]

The unit clauses implementing (3) are only a relabeling normalization.  All
other pairs remain physical Boolean variables.  The degree clauses
`18<=d(v)<=24` are the sound global condition (2), encoded by sequential
counters.  The executable can also run with both filters disabled, over all
`2^903` labeled graphs.

This four-branch union is not a fixed-neighborhood or catalog family: the
internal graphs on the two root sides and every cross-edge are free.  No
claimed target would depend on the normalization, since its emitted 903-edge
word is checked after decoding as a literal labeled graph.

## Counterexample-guided clause generation

Fix a branch.  The engine begins with the root and degree filters and a
deterministically shuffled subset of five-set pairs from (1).  It repeatedly:

1. asks an incremental exact SAT solver for any assignment satisfying the
   clauses accumulated so far;
2. inspects **every** five-set in that physical assignment;
3. returns a good graph if there is no monochromatic five-set; and
4. otherwise adds the violated clause for each selected monochromatic
   five-set and solves the enlarged global formula.

Every SAT call ranges over all remaining edge variables.  The solver may
change any number of edges between rounds, so this is not a bounded-radius
repair, a matching move, or a walk around a reference graph.  Randomness only
permutes sound clauses and decision phases; it never restricts the solution
set.

### Finite-termination theorem

At a SAT round, a violated Ramsey clause cannot already be in the accumulated
formula, because the returned assignment satisfies that formula.  Unless a
target is returned, at least one previously absent clause is therefore added.
There are only `2*binom(n,5)` clauses.  With no round cap, and assuming each SAT
call returns SAT or UNSAT, a branch terminates after at most

\[
                       2\binom n5+1
\]

calls.  A returned zero-violation graph satisfies the target definition.  If
an accumulated subformula is UNSAT, then the full branch is UNSAT because
every full target satisfies that subformula.  Hence checked UNSAT proofs for
all four branches would prove that no good43 exists, while any SAT terminal
word would be the desired construction.

The present producer does not emit an UNSAT proof and this package claims no
UNSAT result.  Its immediate purpose is construction.  Any future branch
exclusion must add and independently replay a proof object before being
reported as a theorem.

## Resume boundary

At the end of each completed round, the producer atomically writes:

- all explicitly learned Ramsey-clause codes;
- the exact initial parameters and number of completed rounds;
- the best physical edge word and its exact red/blue violation counts; and
- the complete `mt19937_64` state controlling subsequent clause selection.

Restarting from that file reconstructs the same explicit mathematical
subformula and clause-selection state.  Internal solver lemmas are deliberately
not serialized, so wall time and the next satisfying assignment need not match
an uninterrupted process.  The checkpoint is an exact semantic continuation,
not a bit-for-bit snapshot of CaDiCaL's internal heap.

## Independent physical verifier

`verify.py` imports no producer code and invokes no SAT solver.  It decodes the
complete edge word into a dense adjacency matrix and examines all
`binom(n,5)` vertex sets, counting red and blue monochromatic copies.  It emits
`GOOD_GRAPH` only when both counts are zero.  For `n=43` that is exactly 962,598
literal five-set checks.

The verifier is calibrated on one published good42 record from McKay's data:
all 850,668 five-sets pass.  Red- and blue-clique corruptions are rejected with
physical witnesses.  `controls.py` independently compares its counts on all
33,867 labeled graph words through order six, checks hexadecimal round trips,
checks the complementation/root normalization on all small words, and rejects
malformed inputs.  The producer separately exhausts 3,584 signed sequential-
counter instances through seven inputs.

The deterministic no-witness-seed calibration constructs a good32 after 858 CEGIS
rounds and 66,011 admitted Ramsey clauses.  The independent verifier checks all
201,376 five-sets in its emitted physical word.  This is an implementation
calibration, not a new Ramsey bound.

## Trust boundary and pilot status

Exact graph arithmetic uses integers and Boolean literals.  The producer trusts
CaDiCaL 1.9.5, its C++ implementation, the compiler, and ordinary hardware for
SAT models.  Every claimed positive graph is nevertheless checked directly by
the independent Python verifier, so solver soundness is not a premise for an
existence claim.  An UNSAT claim would require a separately checked proof.

The pass-1 target pilot executed 120 completed rounds in each branch of (3),
starting only from deterministic random phases and clause order.  All four
outcomes are explicitly `INCOMPLETE`; no endpoint or defect-count claim follows.
The scratch checkpoints are retained outside Git because they are generated
operational state.  This run demonstrates that the complete normalization,
global degree filters, separation oracle, physical decoder, and restart
interface all execute at target size.

## Sources

- Brendan D. McKay and Stanislaw P. Radziszowski, *R(4,5) = 25*,
  J. Graph Theory 19 (1995), 309--322,
  https://doi.org/10.1002/jgt.3190190304.
- Vigleik Angeltveit and Brendan D. McKay, *R(5,5) <= 46*,
  J. Graph Theory (2026), https://doi.org/10.1002/jgt.70029;
  preprint arXiv:2409.15709v2.
- Brendan D. McKay and Stanislaw P. Radziszowski, *Subgraph counting
  identities and Ramsey numbers*, J. Combin. Theory Ser. B 69 (1997), 193--209.
- Brendan McKay's Ramsey graph data page, including the good42 records:
  https://users.cecs.anu.edu.au/~bdm/data/ramsey.html
