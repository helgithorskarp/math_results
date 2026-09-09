# Finite proof details

Let `q(G)` be the total number of red or blue monochromatic five-cliques. For
an edge `e=uv`, let `R_e` be the number of red triangles in
`N_R(u) intersect N_R(v)` and define `B_e` analogously in blue. The
monochromatic five-cliques containing `e` are in bijection with these
triangles. Therefore

```text
q(G toggle e) - q(G) = -R_e + B_e, if e is red,
q(G toggle e) - q(G) =  R_e - B_e, if e is blue.
```

Applying this identity sequentially gives the exact objective after a
four-edge switch, including all interactions between its toggled edges.

For a four-set there are three perfect matchings and three unordered pairs of
matchings. A valid alternating pair has internally constant but opposite
colors. The primary enumerator loops over all `C(43,4)` four-sets and all
three pairs. Consequently it omits no alternating 2-switch and duplicates
none within a fixed source graph. It separately checks that the source has
objective 12 and red degrees in the necessary target interval.

The first census records, per source, the total number of switches, the
numbers with objective below or equal to 12, the minimum endpoint objective,
the multiplicity of that minimum, and one attaining move. Summation gives
12,056,241 switches, zero descending, zero neutral, and 502 minimum moves.

The two-level enumerator reconstructs all 502 minimum moves rather than
trusting only the stored examples. For every resulting middle graph it again
enumerates the complete alternating-switch neighborhood. Each middle graph
has an inverse switch to its source at objective 12. The census finds exactly
502 descending endpoints and exactly 502 objective-12 endpoints in total,
so these forced inverses are the unique descending moves and the unique
objective-12 moves. The remaining 25,423,990 second switches all have
objective greater than 12.

The independent programs reconstruct the physical graphs and switches from
the persisted input but use the displayed one-third edge-sum identity for
triangle counts. They verify all per-source rows and fixed aggregate values.
This leaves the C++ integer/bit semantics, the elementary identities above,
and the inherited completeness of the 238 input representatives as the
computational trust boundary.
