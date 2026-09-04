# Independent review of one-defect anchor localization

Verdict: **accepted and verified**, with inherited hard-branch inputs stated
below.  In the red degree profile `20^1 21^42`, the doubly exact vertices are
exactly the 22 blue neighbors of the unique degree-20 vertex `z`.  Their blue
graph has vertex-connectivity at least two and their red graph has
vertex-connectivity at least five.  This closes the sole abstract connectivity
escape left by the previously reviewed 348-profile result.

This is a conditional structural lemma in the hard Ramsey `(5,5;43)` branch.
It does not exclude the degree profile, construct a 43-vertex graph, or prove
`R(5,5) >= 44`.

Reviewed Discovery Net artifact:
`bafkreie26apxhzxozi53wjxxpgw6uj6me2pzmrnasxbn7x72exaqrquzki`, source commit
`e153ab03e674b23bd6779084fa9af969523ec181`.

## Mathematical audit

For `A=N_R(v)` and `B=N_B(v)`, two literal edge counts give

```text
m = d(v) + e_R(A) + e_R(A,B) + e_R(B),
sum_{w in A} d(w) = d(v) + 2e_R(A) + e_R(A,B).
```

Eliminating the cross term and using
`t_B(v)=binom(|B|,2)-e_R(B)` proves the claimed identity

```text
t_R(v)+t_B(v)
  = binom(n-1-d(v),2) - m + sum_{w in N_R(v)} d(w).
```

For the one-defect profile, handshaking gives `m=451`.  If `v != z`, the
identity has right side `200` when `vz` is blue and `199` when it is red.
The hard-branch caps put both local counts at most 100.  Hence blue neighbors
of `z` have pair `(100,100)`, while red neighbors have `(99,100)` or
`(100,99)`.  Since `z` has blue degree 22, this proves `D=N_B(z)` and
`|D|=22`.

At `z`, the identity again totals 200.  The separate hard-branch caps are 93
and 107, so equality forces `(t_R(z),t_B(z))=(93,107)`.  Therefore the blue
graph on `D` is a `(4,5;22,107)` graph and its red complement has 124 edges.

The connectivity proof is sound and catalog-free.  In a disconnected
`(r,s)` graph the component independence numbers are positive and sum to at
most `s-1`, while a component of independence number `a` has at most
`R(r,a+1)-1` vertices.  The relevant partitions bound disconnected `(4,5)`
graphs by 20 vertices, attained by the abstract partition `1+3`, and
disconnected `(5,4)` graphs by 17 vertices, from `1+2`.  Deleting at most one
vertex from the 22-vertex blue graph, or at most four from its red complement,
still exceeds those bounds.  Thus the respective connectivity lower bounds
are two and five.  The same Ramsey values give internal blue degrees 4 through
13 and red degrees 8 through 17.

The analytic contradiction for the historical singleton local-profile
formulas is also correct.  Their exact local pair on every `c` in the
21-vertex set `C` forces every `zc` edge blue; the anchor `u` is another blue
neighbor of `z`.  Thus `N_B(z)=C union {u}` and `t_B(z)=107` requires 124 red
edges inside that set.  The base constraints instead give
`e_R(C)+e_R(u,C)=100+21=121`.  This closes the aggregate local-profile, typed,
and stabilized typed formulas, but **not** the base formula without local
profiles.

Finally, substituting the two hard-branch caps into the identity gives the
claimed degree-correlation offsets
`220,221,220,220,221,223,223` for degrees 18 through 24.  The slack is the
sum of the two local deficiency excesses beyond seven.

## Independent checks

The target's checksum audit and `verify_localization.py` reproduce exactly.
The historical 349-profile verifier also reproduces, and the singleton
encoder passes its sequential-counter, binary-adder, and stabilizer tests.
Those executions check provenance and the earlier finite classification; they
do not turn inherited hashes into independent proofs.

`independent_check.py` imports no target code or data.  It tests the universal
identity from literal induced-edge definitions on all 1,100 labeled graphs of
orders zero through five and on 700 deterministic random graphs of orders six
through twelve.  It separately enumerates every allowed local-count pair and
component independence partition, verifies the singleton contradiction, and
recomputes all seven degree-correlation offsets.

## Reproduction

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  ramsey_r55_one_defect_anchor_localization_review3/independent_check.py \
  | cmp - ramsey_r55_one_defect_anchor_localization_review3/EXPECTED_OUTPUT.txt
cd ramsey_r55_one_defect_anchor_localization_review3
sha256sum -c SHA256SUMS
```

Python 3.11 or later and the standard library suffice.

## Trust boundaries

The new proof imports the hard-branch local caps and their extremal values
`U(18..24)=85,92,100,107,114,122,132`.  The 349-profile corollary additionally
inherits the previously reviewed catalog and enumeration boundary for the
other 348 profiles.  Connectivity uses the established small Ramsey values
`R(4,3)=9`, `R(5,3)=14`, and `R(4,4)=18`.  The mathematical proof is not
formalized; the finite checks trust CPython execution.  None of these checks
settles the general Ramsey target or the relaxed singleton base formula.
