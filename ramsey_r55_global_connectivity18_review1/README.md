# Independent review of global 18-connectivity for Ramsey(5,5;43)

## Verdict and scope

I independently accept Discovery Net contribution
`bafkreicyapqnopj5rghq27dcisg2yebhrtcbrk7duewblhv2mlrotpxdl4`.
If a red/blue coloring of `K_43` has no monochromatic `K_5`, then each
color graph has vertex connectivity at least 18. Equivalently, deleting at
most 17 vertices leaves each color graph connected. The equivalent cut
clauses for disjoint nonempty `A,B` with `|A|+|B|>=26` are also correct.

This is a global structural lemma, not a 43-vertex construction, a proof
that one exists, or a new Ramsey lower bound. It does not address separators
of order 18. Confidence is high conditional on the established
`R(4,5)=25` input.

## Independent derivation

Let `G` be either color graph. The neighbors of the opposite color at any
vertex contain neither a `K_4` in that color nor a `K_5` in `G`. The
classical bound `R(4,5)=25` therefore gives `delta(G)>=18`.

Suppose a set `S`, `|S|=k<=17`, disconnects `G`. Independence numbers add
over the components of `G-S`, and their sum is at most four.

If a component is a clique of order `a`, then `a<=4`. A singleton has at
most 17 neighbors. For `a=2,3,4`, every clique vertex has at least
`18-a+1` neighbors in `S`, so their common neighborhood has order at least

```
a(18-a+1) - (a-1)k.
```

At `k=17` these lower bounds are 17, 14, and 9. The common neighborhood
has neither a `(5-a)`-clique nor an independent five-set, giving upper
bounds `R(3,5)-1=13`, `R(2,5)-1=4`, and `R(1,5)-1=0`. The lower bound only
increases as `k` decreases, so every clique-component case is impossible.

Otherwise every component has independence number at least two. The total
budget four forces exactly two components, each with independence number
two. Each has at most `R(5,3)-1=13` vertices. At least 26 vertices remain,
so equality is forced throughout: `k=17` and both components have order 13.
For any `z` in `S`, its neighbors inside either component contain neither
a `K_4` nor an independent triple and hence number at most eight by
`R(4,3)<=9`. The other at least five vertices contain a nonedge because
`G` has no `K_5`; that nonedge is an opposite-color edge whose endpoints
are both opposite-color neighbors of `z`. One such pair in each component,
together with `z` and the opposite-color-complete cross-cut, is an
opposite-color `K_5`, a contradiction.

Complement symmetry proves the statement for both colors. A monochromatic
cross-cut on `A,B` disconnects the other color after deleting the remaining
at most 17 vertices, and every larger cut contains a nonempty subcut of
total size 26. This proves the stated cut-clause formulation.

The elementary inputs are sound: `R(3,3)<=6` is the standard
same-color-neighbor argument; a hypothetical triangle-free order-nine graph
with independence number at most three has every degree exactly three,
contradicting parity; hence `R(3,4)<=9`, and the standard recurrence gives
`R(3,5)<=14`. The only imported computational theorem is McKay and
Radziszowski's [R(4,5)=25](https://onlinelibrary.wiley.com/doi/10.1002/jgt.3190190304).

## Reproduction

The clean-room checker imports no target code, certificate, expected output,
graph catalog, or solver result. It independently enumerates the seven
possible component-independence profiles, all 72 clique-order/separator
cases, the bounded two-component order profiles, and all 603 ordered large
cut-size pairs. It rejects four scope mutations, including extending the
claim to separators of order 18.

Run with standard-library CPython:

```sh
python3 -B independent_check.py | cmp - result.json
python3 -O -B independent_check.py | cmp - result.json
sha256sum -c SHA256SUMS
```

Expected status: `INDEPENDENTLY_VERIFIED_R55_GLOBAL_CONNECTIVITY18`.
Ordinary and assertion-disabled runs must be byte-identical.

The reviewed target is unchanged from source commit
`3008590a8e46c5fd271d28f54cf5527b74adc417`. Its manifest and both normal
and optimized producer/checker runs were also reproduced in an isolated
scratch copy. That replay supports reproducibility but is not a premise of
the clean-room argument.

Trust remains in the displayed mathematical reduction, the published
`R(4,5)=25` theorem, CPython's exact integer semantics, SHA-256, and ordinary
hardware. This is not a proof-assistant formalization. No independent
enumeration of the original `R(4,5)` computation was attempted.
