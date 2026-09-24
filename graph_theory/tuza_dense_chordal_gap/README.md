# A strict Tuza gap for dense chordal graphs

For every fixed `beta>0`, all sufficiently large chordal graphs with
`m>=beta n^2` satisfy

    2nu(G)-tau(G) >= m^2/(100n^2),
    tau(G) <= (2-3beta/100)nu(G).

Here `nu` counts edge-disjoint triangles and `tau` counts edges meeting
every triangle. The result includes dense split and interval graphs.
The [proof](PROOF.md) combines an explicit fractional bound

    2nu*(G)-tau(G) >= m^2/(50n^2)-2n/3

with the classical uniform Haxell--Rodl rounding theorem. The structural
step bounds zero-weight edges of an optimal fractional cover using a
perfect elimination ordering. The zero/unit LP framework itself is due
to prior work and is attributed in [SOURCES.md](SOURCES.md).

A sharper split-graph corollary holds for every fixed number `r` of active
neighborhood types and arbitrary multiplicities:

    2nu*(G)-tau(G) >= [k^2-2k-32(r+1)]/[8(8r+11)].

For sufficiently large clique order `k`, this gives
`2nu(G)-tau(G)>=k^2/[16(8r+11)]`. In particular it reaches unrestricted
three-type split graphs at every sufficiently large clique order.

**Status:** the [independent h5717 review](../tuza_dense_chordal_gap_review1/REVIEW.md)
accepts this result with high confidence. This original proof does not
evaluate the numerical cutoff for the integer statements. A later
[full-packing rounding argument](../tuza_bounded_type_full_rounding/README.md)
supplies an explicit cutoff for the bounded-type split corollary; that
new argument is awaiting independent review.
This does not prove Tuza for all chordal graphs or all three-type split
graphs. It does not establish the stronger experimental factor `3/2`.

The finite audit is supplementary, not the proof of the universal bounds:

```sh
python3 audit.py
```

It uses only the Python standard library and exact integer/rational
arithmetic. Its scope and expected output are described by the script and
[AUDIT.json](AUDIT.json); [RUN.json](RUN.json) records the invocation and
environment. No LP solver, floating-point tolerance, downloaded dataset,
or generated bulk certificate is required.
