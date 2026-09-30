# Exact necessary conditions for phase201

All assertions concern arbitrary binary functions `f:{0,...,3703}->{0,1}`
without a monochromatic nonconstant seven-term integer AP. Put `C=1852`,
`p=617`, and let `q(r)=0` for a nonzero square modulo617, `q(r)=1` for a
nonsquare, and leave `q(0)` undefined. The partial reference is

```
T(x) = q(x-C+201)                      (x<C),
       q(x-C+417) XOR 1                (x>=C).
```

Its six poles are free and uncounted. Each nonpole reference class has1849
points. Write `E_c={x:T(x)=c and f(x)!=c}` and `e_c=|E_c|`. Any actual
original monochromatic AP of reference color `c` must meet `E_c`.
Reflection interchanges the reference classes; no reflection assumption is
made about `f`. The checker separately validates every reflected AP using
Euler's criterion.

## 1. A removed zero edit forces the old residual screen

The unchanged base packing has integer denominator `D0=1000000`, total
weight `S=195802847` in each class, and loads `0<=l(x)<=D0`. Summing mandatory
AP-hit inequalities gives `sum(E_c) l(x)>=S`.

Let `K_c={x:T(x)=c and l(x)=0}`. Exactly78 points lie in each `K_c`.
Suppose `e_c<=197` and choose any `z in E_c intersect K_c`. Removing it gives
`H=E_c\{z}` with `|H|<=196` and unchanged total base load. Thus

```
sum(H) (D0-l(x)) <= 196*D0-S = 197153 = delta0.
```

Every summand is nonnegative, so
`H subset V_c={x:T(x)=c and D0-l(x)<=delta0}`. Each `V_c` has1086 points and
is disjoint from `K_c`. This argument covers the possibility of multiple
zero edits too; no prior uniqueness assumption about `z` is used.

## 2. Exact loss replay in BOTH leaves of a complete cover

The frozen class196 tree splits color0 at2065, or actual color1 at1638.
Both membership cases for `H` are present. At a leaf let `F` denote its
forced residual edits and `X` its forbidden edits. Then
`J=H\F subset V_c\(F union X)` and `|J|<=196-|F|`.

For a checked actual AP `A`, let `P=A intersect V_c`. Its old residual
right-hand side is `b=1` if `P intersect F` is empty, otherwise0. Removing
`z` can decrease it by at most `b*[z in A]`.

For three checked original monochromatic APs with nonempty screened petals
`P1,P2,P3` and empty common intersection, a hitting set in `V_c` needs at
least two points. Put `U=P1 union P2 union P3` and `b=max(0,2-|F intersect U|)`.
The removed point can reduce the two-hit requirement by

```
ell(z) = 2 if z belongs to all three ACTUAL APs,
         1 if z belongs to one or two ACTUAL APs,
         0 otherwise.
```

Consequently `|J intersect U|>=b-min(b,ell(z))`. Losses use actual APs,
including their points outside the screen. Screen-only loss counting would
be invalid. The new checker computes this bound for every `z in K_c` and
every weighted row, respecting all inherited forced and forbidden states.

Let `W` be the weighted old residual right-hand side, `rho(z)` its total
loss and `nu` the sum of checked point surcharges. Exact capacities at
every free point imply

```
W-rho(z) <= sum(J) packed_load(x) <= (196-|F|)*D+nu.
```

Both frozen leaves have `D=1000000` and `nu=0`:

| Leaf in color0 | W | Old gap | Worst loss over ALL78 zeros | Remaining strict gap |
|---|---:|---:|---:|---:|
|2065 unchanged|196806996|806996|574772|232224|
|2065 edited|195315425|315425|101686|213739|

The reflected actual-color1 replay gives the same integers. Both strict
gaps are positive. Every candidate `z` is therefore impossible, and
`e_c<=197` implies `E_c intersect K_c` is empty. The other edit class and
all pole colors are unrestricted. Completeness comes from retaining both
tree children, not from accepting numerical search exhaustion.

## 3. Editing root1427 yields a smaller opposite-class domain

Now suppose `f(1427)=1` although `T(1427)=0`, and `e_1<=197`. By the first
condition `E_1` avoids `K_1`, so its full possible domain is
`U1={x:T(x)=1}\K_1`, of size1771. No cap on `e_0` is used here.

Each original color1 AP must meet `E_1`. An actual AP with1427 as its sole
original color0 point and all six other terms of reference color1 also
forces an edit among those six terms: otherwise the trial edit makes the
AP monochromatic1. These activated petals are reconstructed in **all of
U1**. Checked triples of original color1 APs with nonempty petals and empty
common intersection in this same full domain force two edits in their union.

The frozen root certificate has889 positive AP weights (including11
activated rows),20 positive triple weights and no surcharges. The checker
validates949 actual AP occurrences. Its total weighted right-hand side is

```
D1 = 1000000,
S1 = 196892545,
0 <= L(x) <= 999999 < D1                    for EVERY x in U1.
```

Thus `sum(E_1) L(x)>=S1`. Since `S1>196*D1`, integrality gives `e_1>=197`,
so the assumed cap makes `e_1=197`. The nonnegative defects satisfy

```
sum(E_1) (D1-L(x)) <= 197*D1-S1 = 107455.
```

Every edit lies in the exactly recomputed screen
`V1={x in U1:D1-L(x)<=107455}`, which has1023 positions, explicitly listed in
`expected.json`. This removes748 more positions from `U1`. It is a necessary
condition, not a contradiction: `S1<197*D1`. Neither the full phase201 repair
box nor this root case has been excluded by this source.

## Trust and scope

The solver uses square enumeration and floating LP guidance. New exact
checkers use Euler colors, actual integer APs, set intersections, complete
case coverage and unbounded Python integers. The only imported earlier
proof component is the unchanged base checker. No native solver status is
a mathematical premise. Corruption controls and small exhaustive logical
models check concrete failure modes; the displayed general inequalities
remain written, unformalized proof bridges. Source authorship is shared
between generation and checking; this is implementation independence, not
external review or proof-assistant formalization. No coloring, new `W` bound,
attainability claim, or exhaustive current-literature novelty claim is made.
