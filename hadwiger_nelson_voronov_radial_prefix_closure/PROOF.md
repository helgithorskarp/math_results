# Exact closure theorem

Let `M1` be the 73-point generator set in the planar `L_{10,2}` series of
Voronov, Neopryatnaya, and Dergachev, and let

`M2 = {x+y : x,y in M1 and |x+y| <= 1}`.

For each radius `r`, write `K_r = {x in M2 : |x| <= r}`.  We call

`K_r union rho(K_s)`,

where `rho` is any rotation about the origin, a uniform-target-budget radial
assembly when `|K_r|+|K_s|-1 <= 508`.  The subtraction accounts for the
origin, which belongs to both copies.  Thus every such assembly physically
has at most 508 points, independent of any further coincidences.

The exact enumeration over `Q(sqrt(2),sqrt(3))` gives 865 points in `M2`.
After quotienting by exchange of the two copies, every admissible pair of
radial prefixes is contained componentwise in one of six maximal pairs:

```
(241,241), (289,217), (361,145),
(433,73), (457,25), (505,1).
```

For each maximal pair, the verifier proves exactly that `r+s<1`.  It does so
without adjoining square roots: for `a=r^2` and `b=s^2`, it checks

```
1-a-b > 0,
(1-a-b)^2-4ab > 0.
```

These inequalities are equivalent to `sqrt(a)+sqrt(b)<1`.  Therefore every
distance between a point of one copy and a point of the other is strictly
less than one, for every rotation.  No cross unit edge exists.

The largest relevant individual prefix, `K_505`, has exactly 216 unit edges.
The verifier enumerates all 127,260 point pairs with exact arithmetic and
checks the committed bipartition.  Every smaller prefix is an induced subset
of `K_505`, so it is bipartite as well.

Even if a rotation creates extra coincidences between the two copies, the
union is four-colourable: give a physical point the pair consisting of its
bipartition colour in the first copy and its bipartition colour in the second
copy (using an arbitrary bit when it is absent from one copy).  Every unit
edge belongs to one of the two copies and changes the corresponding bit.
This proves that no uniform-target-budget radial assembly in this family is
five-chromatic.

`exact_model.py` implements the field in the basis
`1,sqrt(2),sqrt(3),sqrt(6)`.  Radical comparisons use rational enclosing
intervals and increase their precision until the exact nonzero field element
is separated from zero.  Equality is coefficientwise.

The paper's displayed generator is used here.  The authors' public notebook
uses `phi0^4 conjugate(phi1)` instead.  Replacing `phi1` by that element leaves
`M1` unchanged: the exponent sign is reversed and its `phi0` exponent is
shifted modulo 24.
