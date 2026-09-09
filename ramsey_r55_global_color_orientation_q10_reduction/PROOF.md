# A color-orientation quotient for the h3987 q10 UNKNOWN ledger

This note certifies an exact target-search admission reduction, not a SAT or
UNSAT decision. Red edges are graph edges. A **good43** is a red/blue coloring
of the edges of `K_43` having neither a red `K_5` nor a blue `K_5`.

## 1. Complement orientation is complete

Let `c(G)` exchange red and blue on every edge. It is an involution, and a red
`K_5` in `c(G)` is a blue `K_5` in `G`, while a blue `K_5` in `c(G)` is a red
`K_5` in `G`. Hence `G` is good43 if and only if `c(G)` is good43.

There are

```
binom(43,2) = 903
```

edges. If `e(G)` is the number of red edges, then `e(c(G))=903-e(G)`.
Because 903 is odd, exactly one member of every two-element color orbit has at
most 451 red edges. No coloring is fixed by color complementation. Therefore
the existence of a good43 is equivalent to the existence of one satisfying

```
e(red) <= 451.                                            (O)
```

This is an algebraic quotient by the order-two color action, not an edge-count
exclusion theorem.

The independently accepted h3873 theorem says that every good43 has a
relabeling in its complete maximal-K4/Ramsey(4,4) carrier. Apply h3873 after
choosing the representative satisfying (O). Thus every color orbit of target
graphs is still covered. The relabeling may move a complemented graph to any
of the 2,189,178 h3873 physical tasks.

## 2. Exact effect on h3987

The pinned h3987 ledger partitions the two unresolved regular q10 formulas
into 260 physical cube children: 99 are already certified UNSAT and 161 remain
UNKNOWN. The pinned h3969 interface gives their red degrees as follows.

| Branch | Red degree | Red edges | Complement degree | Complement edges |
| --- | ---: | ---: | ---: | ---: |
| `d20-22` | 20 | `43*20/2 = 430` | 22 | 473 |
| `d22-20` | 22 | `43*22/2 = 473` | 20 | 430 |

The handshaking lemma applies because every model of either branch is regular.
Consequently every UNKNOWN `d20-22` child is on the retained side of (O), and
every UNKNOWN `d22-20` child is on the discarded side. Direct enumeration of
the exact task ledger gives

| Disposition of h3987 UNKNOWN children | Count |
| --- | ---: |
| `TARGET_ACTIVE_ORIENTATION` (`d20-22`) | 67 |
| `COLOR_COMPLEMENT_REDIRECT` (`d22-20`) | 94 |
| Total | 161 |

Thus an existence search already using the global orientation (O) need not
schedule 94 of the 161 named UNKNOWN children, an exact reduction of
`94/161 = 58.385093167702%` in this finite queue. The complete destination of
any target model is supplied by h3873 after complement and relabeling; no
claim is made that its destination is one of the 67 retained h3987 children.

## 3. Status boundary

`COLOR_COMPLEMENT_REDIRECT` means only this: if that formula has a target
model, the same color orbit has a representative elsewhere in the complete
oriented h3873 search. It is **not** an UNSAT certificate for the child, does
not decide either parent formula, and closes no whole h3887 task. The literal
h3987 ledger remains exactly 99 certified UNSAT and 161 UNKNOWN.

This quotient does not reduce the declared count of h3873 task definitions;
it adds a target-level admission rule. It constructs no graph, calls no
solver, and does not improve the Ramsey lower bound. Completeness of h3873,
including its imported catalog completeness, remains a trust dependency.

## 4. Reproducibility

`analyze.py` hash-checks all imported interfaces and calculates the exact
partition and identity digests. `independent_check.py` imports no producer
module: it parses all 260 IDs, proves they form the complete two-branch
`65*2` grid, rederives both handshaking counts, partitions all 161 UNKNOWN
rows, and checks the accepted carrier text and result. `controls.py`
exhaustively checks color-complement invariance for all `2^15` red/blue
colorings of `K_6` and separately constructs 20- and 22-regular circulants on
43 vertices to check the handshaking/complement arithmetic. These computation
checks support, but do not replace, the general argument in Section 1.
