# Proof outline

Put `K=Q(sqrt(3),i)` and

```text
L=K[t]/(t^2-(5/3)t+1).
```

Complex conjugation on the selected plane embedding acts by
`conj(t)=5/3-t`; hence `t*conj(t)=1`.  Let
`omega=(1+i*sqrt(3))/2` and use the four pairs of unit directions

```text
(1,t), (1,omega*t), (omega^4,omega^4*t),
(omega^4,omega^3*t).
```

For `d_ij=u_ij-v_ij`, the identity
`d00-d01-d10+d11=0` gives a consistent parallelogram of four centres.
Direct reduction modulo the polynomial of `t` gives
`|d00-d10|^2=|d01-d00|^2=1`, so each designated centre pair is a unit edge.
The verifier also checks all cross boundaries and both intersection roots
exactly.

The orbit/parity rule from the paired-circle theorem assigns the literal
values

```text
(0,1), (1,1), (1,0), (0,0).
```

No assignment to the two orbit variables satisfies all four clauses.

The finite kernel closes every owner-relative intersection direction and the
intrinsic centre-edge direction under the six powers of `omega`, translates
the resulting sets by their two owner centres, and merges equal points.  This
produces 50 distinct quotient-field elements.  Directly testing all 1,225
unordered pairs yields exactly 144 unit pairs.

For the chromatic lower bound, certificate vertices

```text
25, 33, 38, 39, 40, 41, 44
```

induce 11 edges and form a Moser spindle.  The independent checker simply
enumerates all `3^7` assignments and finds none proper.  The supplied
50-symbol word is a direct proper four-colouring, so the kernel has chromatic
number four.

The centres have indices `9,38,25,26`.  Their first pair is unit-separated,
so a plane point adjacent to both must be one of the two equilateral
completions.  Exact checks show neither completion is adjacent to both other
centres.  Thus there is no common plane unit-neighbour of all four.

Finally, two disjoint edges admit seven canonical colour patterns up to colour
renaming.  The certificate supplies a direct proper colouring of the whole
kernel for each pattern.  Since no other centre pattern is compatible with
the two centre edges, the terminal relation is exactly the bare relation.

