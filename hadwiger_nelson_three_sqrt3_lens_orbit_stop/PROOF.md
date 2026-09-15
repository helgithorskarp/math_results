# Proof of the exact three-colour stopping theorem

Use scaled triangular coordinates `(s,t)` for the plane point
`(s*sqrt(3)/2,t/2)`.  The three centres

```text
c0=(0,0), c1=(2,0), c2=(1,3)
```

have pairwise squared distance three, so they are distinct and independent in
the strict unit graph.  Direct substitution in

```text
4 |p-q|^2 = 3*(delta s)^2 + (delta t)^2
```

shows that the listed two points for each centre pair are unit distance from
both owners.  Two distinct circles have at most two intersection points, so
each list is complete.

Multiplication of a relative vector by
`(1+i*sqrt(3))/2` gives the displayed integer rotation formula.  Iterating it
six times returns the input vector.  The verifier applies this recurrence to
both intersections and both owners for every lens, unions the resulting
formal addresses with the centres, and compares the exact set with the 16
certificate rows.  It then tests all 120 unordered physical pairs by the norm
formula.  Exactly 33 satisfy the unit equation; these and only these are the
strict edges.

For a unit edge, the integer equation

```text
3*(delta s)^2 + (delta t)^2 = 4
```

implies `delta t` is nonzero modulo three: reducing modulo three gives
`(delta t)^2=1`.  Therefore `t mod 3` is a proper three-colouring.  The three
vertices `(0,0),(0,2),(1,1)` are pairwise unit-separated, so two colours do
not suffice.  The chromatic number is exactly three.

Finally, three independent labelled terminals have five equality patterns up
to global colour permutation.  The certificate gives a proper four-colouring
for each canonical word `000,001,010,011,012`, and the checker tests each word
on all 33 edges and at the exact centre indices.  Every bare centre pattern
therefore extends, so the unrestricted centre relation is neutral.

The result supplies neither ordinary non-four evidence nor a candidate for the
record problem.  Its mathematical consequence for the campaign is the exact
retirement of this frozen first-orbit construction.
