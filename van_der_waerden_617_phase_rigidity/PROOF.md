# Exact seam rigidity for affine quadratic-residue blocks modulo 617

Author: six-vdw-3, researcher. Status: exact computer-assisted lemma and
elementary corollaries; the two implementations are same-author checks, not
independent peer review.

Throughout, an arithmetic progression has seven terms and positive integer
common difference. All coordinates in the proof are zero based. Translating
by one gives the usual interval `[1,N]`.

Let `p=617`, and write `q(0)=*`, `q(x)=0` for nonzero quadratic residues
modulo `p`, and `q(x)=1` for nonresidues. A pole is a point at which the
argument of `q` is zero. Define the complete block of length `p`

```
B(s,e,h)(i) = q(i+s) XOR e,  if i+s != 0 modulo p;
             h,             otherwise,
0 <= i < p,  0 <= s < p,  e,h in {0,1}.
```

This includes every affine quadratic-character block `q(alpha*i+beta)`
with `alpha != 0`, up to a freely chosen pole color: put
`s=beta/alpha` and `e=q(alpha)`. Here
`q(x*y)=q(x) XOR q(y)` for nonzero field elements.

## Lemma 1: partial modular safety

For every `a` in the field and every nonzero `d`, the non-pole terms of
`q(a),q(a+d),...,q(a+6d)` contain both colors. There are exactly
`617*616=380072` parameter pairs.

Both programs check all these pairs directly. Alternatively,
multiplicativity reduces the check to `d=1`: multiplication by `d` changes
every non-pole color by the same bit. Thus arbitrary pole assignments in
any sequence having one fixed phase and orientation cannot create a
monochromatic progression with difference not divisible by `617`.

## Lemma 2: sharp seam rigidity

The concatenation
`B(s,e,h) B(t,f,g)` is progression free if and only if `s=t` and `e=f`.
The colors `h,g` are unrestricted. If the phase or orientation changes,
there is a monochromatic progression crossing the seam, using no pole,
with common difference at most `28`.

To prove necessity, complement the whole coloring when `e=1` and replace
`f` by `e XOR f`. It is enough to check the `2*617^2=761378` normalized
triples `(s,t,f)`. For `1 <= d <= 28`, take every crossing progression

```
(a,a+d,...,a+6d),  p-6d <= a < p.
```

Its span is less than `p`, so these are exactly the crossing progressions
of those differences in the two-block interval. The total is
`sum(d=1..28) 6d = 2436`. Compute the phase sets for which all left terms
have color `b` and all right terms have color `b`, after applying the
relative orientation. A set never includes a phase for which a term is a
pole. The corresponding Cartesian product is a certified set of
incompatible pairs, for every choice of both pole colors.

The Python computation unions these rectangles. For every left phase `s`,
it asserts that the full surviving row is exactly the singleton `(t,f)=(s,0)`.
This is an entry-level check, not an inference from the total. The separate
C++ program generates residues by squaring, builds ternary word tables,
enumerates every individual normalized triple, and directly rechecks all
seven terms of its chosen obstruction. Exactly `760761` triples have an
obstruction and exactly `617` survive. No pole colors are enumerated
because each obstruction avoids both poles.

For sufficiency, use Lemma 1 with the common phase and orientation. Any
progression in two complete blocks has `d <= floor(1233/6)=205`, and hence
`617` does not divide `d`. Therefore it contains both non-pole colors,
regardless of `h,g`.

The hole-free difference bound is sharp. At difference cutoff `27`, the
only additional normalized survivors are `(154,463,1)` and `(155,464,1)`.
Their first hole-free crossing obstructions have difference `28`. Both
programs check this assertion. It makes no assertion about progressions
that use a pole at cutoff `27`.

Restoring the global orientation and the two independent pole colors gives
exactly `617*2*4=4936` valid ordered two-block parameter choices out of
`(617*2*2)^2=6091024` choices.

## Lemma 3: a saturation witness

The six residues

```
1 - 47*j modulo 617,  j=1,...,6,
```

are `571,524,477,430,383,336`, all nonresidues. Consequently, for every
nonzero `r`, put `d=47*r modulo 617`, chosen in `[1,616]`. The six residues
`r-j*d` are nonzero and all have color `1-q(r)`. This follows from
multiplicativity, and both programs also check all `616` multiplier cases.

## Corollary: complete classification at lengths 3703 and 3704

Consider colorings whose first `6p=3702` points are six complete blocks,
each independently of the form `B(s_j,e_j,h_j)`, with all subsequent
points assigned arbitrary colors. Within this construction family:

* there are exactly `252` progression-free colorings of length `3703`;
* there are none of length `3704`.

Proof. Lemma 2 applies to every adjacent pair of complete blocks. Therefore
all six phases coincide with a single `s` and all orientations with a
single `e`; the six pole colors remain free.

Write `u=6p=3702` for the first additional point. If `s != 0`, set
`d=47*s modulo p` in `[1,616]`. The six predecessors `u-j*d`, `j=1,...,6`,
lie in the existing prefix, since `u-6d >= 6`. They avoid poles and have
color `1-q(s) XOR e`, by Lemma 3. Avoiding their completion forces
`c(u)=q(s) XOR e`. But `0,p,...,5p` already have this same color, so
`0,p,...,6p` is then monochromatic. Thus `s=0` is necessary.

With `s=0`, any progression of difference not divisible by `p` is safe by
Lemma 1. At length `6p+1`, the only progression of difference divisible by
`p` is `0,p,...,6p`. Its seven pole colors must not all agree. Conversely
this condition suffices. The two orientations and the `2^7-2=126`
nonconstant pole assignments give exactly `252` distinct colorings.

Now add `v=6p+1=3703`. The six points
`v-47, v-94, ..., v-282` all lie in the six-block prefix, avoid poles,
and have color `1 XOR e`. They force `c(v)=0 XOR e`. However,
`1,1+p,...,1+5p` all have color `0 XOR e`, so difference `p` forces the
opposite color at `v`. This is a contradiction. Neither obstruction uses
any of the seven free poles. QED.

## Scope, evidence, and trust boundary

The seam lemma is a finite exact claim supported by two algorithms with
different representations and quadratic-residue generation mechanisms.
Their completeness domains and all reductions are stated above. The
corollary uses elementary arguments plus the checked finite lemmas.
There is no SAT solver, external certificate, random search, floating
point arithmetic, or omitted proof corpus. The trust boundary comprises
the published code, Python's exact integer semantics, the C++ compiler
and runtime, and this unformalized proof. C++ arithmetic is bounded:
`x*x <= 616^2=379456`, and all indices and modular products fit in signed
32-bit integers; reported counts use unsigned 64-bit integers.

This excludes a specified construction family. It does not bound
`W(2,7)` above, and does not exclude edits inside the residue blocks,
other periods, interleaving/zipper transformations, or general colorings.
The included 3703-point seed reproduces an existing lower bound. A valid
3704-point coloring is still required to establish `W(2,7)>=3705`.
