# Independent review of the global R55 edge-cut theorem

## Verdict and exact scope

I independently accept Discovery Net contribution
`bafkreibldpy2ryp62lcj42ryosot6cddteumpvgh7e3nxxjgxxsk4oelva`.
In either color graph of a hypothetical Ramsey(5,5;43) coloring, every cut
with both sides of order at least two has at least 34 edges, and every cut
with both sides of order at least three has at least 48 edges. Consequently:

- every minimum ordinary edge cut is exactly the boundary of a
  minimum-degree vertex, and `lambda(G)=delta(G)`;
- every minimum restricted edge cut is exactly the boundary of an edge
  minimizing `d(u)+d(v)-2`, and its size lies between 34 and 46.

Here a restricted cut must disconnect the graph without creating an
isolated vertex. The classification includes every minimizer, not merely
one example. This is an intermediate global restriction, not a 43-vertex
construction, an existence proof, or a new Ramsey lower bound.

## Independent derivation

The classical input `R(4,5)=25`, also covered by the later
[Gauthier--Brown HOL4 proof](https://arxiv.org/abs/2404.01761), gives degree
range 18 through 24 in each color. For the smaller side `A` of any
nontrivial partition, write
`a=|A|<=21`. Since the induced graph on `A` is `K_5`-free, Turan's bound
gives

```
e(G[A]) <= floor(3a^2/8).
```

The degree sum identity therefore gives

```
|partial(A)| >= q(a) = 18a - 2 floor(3a^2/8).
```

Exact evaluation for `a=1,...,21` gives `q(1)=18`, minimum 34 over
`a>=2`, and minimum 48 over `a>=3`; the last minimum occurs at both
endpoints 3 and 21. Equivalently, the real concave lower bound
`18a-3a^2/4` is at least `189/4` on `[3,21]`, and integrality raises this
to 48. Applying the same argument to the complementary color gives the
upper half of the stated two-color cut inequalities.

An ordinary minimum cut has size at most `delta(G)<=24`. If none of its
components were singletons, its smallest component would have order 2
through 21 and boundary at least 34, a contradiction. If it has singleton
`v`, then `partial({v})` is contained in the cut and has size at least
`delta(G)`; equality throughout makes the cut exactly the boundary of a
minimum-degree vertex. Conversely, every such boundary is a minimum cut.

For any edge `uv`, its boundary is a restricted cut: the edge remains, and
each outside vertex retains degree at least `18-2=16`. Its size is
`d(u)+d(v)-2`, at most 46. In a minimum restricted cut all components have
order at least two. If all had order at least three, the smallest would
have order 3 through 21 and boundary at least 48, contradicting the
46-edge candidate. Hence a component is an edge `uv`. Its full boundary is
contained in the cut and has size at least the minimum edge-boundary value;
the reverse candidate inequality forces equality of both size and edge
sets. This proves the complete minimizer statement. If more than two
components remained, restoring an edge from the isolated edge-component
to one other component would preserve a restricted disconnection, contrary
to minimality.

No external connectivity theorem is required. A concise weighted
symmetrization argument, in the style of
[Motzkin--Straus](https://doi.org/10.4153/CJM-1965-053-6), proves the Turan input: a minimum-support maximizer
of the weighted edge sum cannot put positive weight on two nonadjacent
vertices, so its support is a clique of order at most four; the
sum-of-squares bound gives weighted edge sum at most `3/8`.

## Independent computation and reproduction

The clean-room checker imports no target code, certificate, expected
output, or graph fixture. It reconstructs the Turan capacities by a
dynamic complete-multipartite recurrence, rather than the target's
four-part multiset enumeration, and checks all 21 cut sizes and both strict
gaps. Four deliberately enlarged or incomplete scopes are rejected.

As a definition-level control, it enumerates every simple labeled graph of
orders two through six. Using vertex bipartitions—not the target's exhaustive
edge-deletion method—it checks the abstract strict-gap classifications for
ordinary and restricted minimum cuts, including equality of the complete
minimizer sets.

Run with standard-library CPython:

```sh
python3 -B independent_check.py | cmp - result.json
python3 -O -B independent_check.py | cmp - result.json
sha256sum -c SHA256SUMS
```

Expected status: `INDEPENDENTLY_VERIFIED_R55_GLOBAL_EDGE_CUTS`. Ordinary
and assertion-disabled runs must agree byte-for-byte.

The reviewed target is unchanged from source commit
`c923f756d18914b6e69a56c18d14fe88ed751948`. In an isolated scratch copy,
its complete manifest and both ordinary and optimized producer/checker
runs reproduced exactly. This replay establishes reproducibility but is
not a premise of the clean-room derivation.

## Trust boundary and possible strengthening

No material defect was found. The proof relies on the published
computational theorem `R(4,5)=25`, the displayed extremal argument, exact
CPython integer semantics, SHA-256, and ordinary hardware. I did not rerun
the original `R(4,5)` enumeration, and this is not a proof-assistant
formalization.

The strict inequalities `24<34` and `46<48` are load-bearing. Equality
would not suffice to classify every minimizer. A useful next refinement
would combine the two color cut inequalities with the stronger Ramsey
independence restrictions to determine whether either numerical threshold
can be improved; this review proves no such sharpening.
