# An arithmetic gap in every even-uniform unequal-core AHT template

The [full proof](THEOREM.md) completes the even-uniform numerical part of the
unequal-core Abbott--Hanson--Toft (AHT) template theorem.

For even `r >= 4`, let the core ground set have size `2r-3`, and allow the
`r` core families to be arbitrary and different.  Every non-two-colorable
template in this class has at least

```text
binom(2r-3,r-2) + 2^(r-1) + binom(r,r/2)/2 + epsilon_r
```

edges, where `epsilon_r = r/2` if `r` is a power of two and
`epsilon_r = 1` otherwise.  Thus equality in the previously displayed
counting-plus-cover bound is impossible at every even uniformity.  The bound
is sharp for `r=4`, where it gives 23 edges.

The folded-cube vertex-cover formula used here is classical, not new.  The
increment is the parameter-uniform arithmetic gap obtained by combining that
formula with the unequal-core cross-cover inequalities and equality rigidity.
No claim about unrestricted `m(r)` is made, and sharpness for even `r>4` is
not asserted.

This package is proof-only: no computation, solver, external dataset, or
omitted certificate is needed.
