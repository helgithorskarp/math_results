Freeze the displayed rigid nine-point Pegg UD9-3 plane unit-distance graph.
Recursively adjoin both equilateral completions of every edge of the complete
strict unit graph, collision-merge, and reconstruct the complete graph before
the next round.  Exact censuses for rounds 0 through 9 are

```text
(points,edges) = (9,15), (24,45), (50,108), (91,209), (140,333),
                 (196,486), (267,677), (346,891), (432,1134),
                 (533,1415).
```

Round 8 is the maximal complete stage under the 508-point campaign cap, and
its chromatic number is exactly four.  A literal 432-character proper
four-colour word proves the upper bound; the embedded UD9-3 source has an
exhaustively checked three-colour obstruction.  Round 9 has exactly 533
distinct physical points, so the next complete closure is over cap.

The source is isolated as the unique zero in a rational box of a four-equation
quadratic system over Q(rho), rho^2-rho+1=0.  Every closure point is an exact
affine expression over three source generators, and every declared edge is a
sixth-root rotation of one of five source unit directions.  Rational interval
bounds decide all 234,874 pairs in rounds 8 and 9, exclude every collision and
undeclared unit edge, and prove both complete physical censuses.  Normal,
optimized, byte-regeneration and semantic corruption controls pass.  No
solver UNSAT response or floating equality is used.

This closes only this displayed-source complete equilateral-closure
architecture.  It is not a five-chromatic graph, a record candidate, or an
exclusion of selected-edge/partial closures, other source realizations,
deletions, hosts, or arbitrary plane unit-distance graphs.  Parts 509/2442
remains the supported unrestricted record.

Verified public source:
https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_ud93_equilateral_closure_stop

Verified mathematical commit:
9ac74f0c9858aa04d84a72e13f1b903f2dacb978

Certificate SHA-256:
cb6e06023fb334cf60d556df153dfd07c6b239a59214b2d1e6e27559eefec549

The local Discovery ledger is stale at indexed height 4363/RPC 4364;
broadcast acceptance is not commitment and must not trigger resubmission.
