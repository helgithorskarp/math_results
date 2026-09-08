# The C13 triple-sum one-step shell is four-colourable

**Exact computer-assisted theorem.** Define

```text
omega = (1+i sqrt(3))/2
v     = (sqrt(33)+i sqrt(3))/6
rho   = (7+i sqrt(15))/8.
```

Let

```text
M = {0,1,omega,1+omega,v^2,v^2 omega,v^2(1+omega)},
C = M union rho M,
D = {omega^j v^k, rho omega^j v^k : 0<=j<6, -2<=k<=2},
B = C+C+C.
```

Repeated points are identified. Thus `C` has 13 points, `D` has 60 unit
vectors, and the triple Minkowski sum `B` has 403 points. Let `S` contain every
point `x` outside `B` such that `x=b+d` for some `b in B`, `d in D`, and `x`
has at least two unit-distance neighbours in `B`.

There are exactly **2,940** points in `S`. The strict unit-distance graph on
`B union S` has **3,343 vertices, 21,044 edges, and chromatic number exactly
four**. Consequently, for every one of the `2^2940` subsets `T` of `S`, the
strict unit-distance graph on `B union T` has chromatic number exactly four.
In particular, every candidate in this complete one-step shell family through
order 508 (at most 105 shell additions) is four-colourable.

This is a negative construction gate. It does not produce a five-chromatic
graph or improve the 509-vertex record. It closes simultaneous selection from
the entire first exact two-contact shell around the structured 403-point base;
it makes no claim about later shells, different direction dictionaries, or
points outside this rule.

## Proof

The verifier reconstructs `C`, `D`, `B`, and `S` exactly. It checks every
unordered pair in the 3,343-point host and then checks the stored 3,343-symbol
four-colour word on all 21,044 strict unit edges. Restricting that word to any
`B union T` proves the upper bound simultaneously for every `T subset S`.

The original seven points `M` occur in `B`, because `0` belongs to `C`.
The verifier reconstructs the 11 spindle edges and exhausts all `3^7=2,187`
three-colour assignments, finding no proper one. Therefore every `B union T`
has chromatic number at least four, which proves the equality claim.

Coordinates lie in

```text
Q[t,r,s]/(t^2-5, r^2+3, s^2+11),
t=sqrt(5), r=i sqrt(3), s=i sqrt(11).
```

The verifier first derives `omega`, `v`, and `rho` in this tensor algebra. It
then converts every coordinate to an integer numerator with denominator 96:

```text
x=(a+b sqrt(5)+c sqrt(33)+d sqrt(165))/96,
y=(e sqrt(3)+f sqrt(15)+g sqrt(11)+h sqrt(55))/96.
```

For a difference labelled `(a,b,c,d,e,f,g,h)`, squared distance one is tested
by exact integer equality of all four coefficients in the real radical basis.
The test is

```text
A = a^2+5b^2+33c^2+165d^2+3e^2+15f^2+11g^2+55h^2 = 96^2,
B = 2(ab+33cd+3ef+11gh) = 0,
C = 2(ac+5bd+eg+5fh) = 0,
D = 2(ad+bc+eh+fg) = 0.
```

The three independent square classes give a faithful degree-eight embedding,
so tuple equality and the four coefficient tests are exact.

The numbers of shell points with 2, 3, 4, 5, 6, and 8 base contacts are,
respectively,

```text
2108, 576, 156, 80, 18, 2.
```

The coordinate and strict-edge stream SHA-256 values are

```text
3218b1de50ca1a0b89a9e0df5c607962c60116f5892344cd83d051b2f5ca403b
a073f52548897b2e6018267040cd4b25893eea9cdd2f390b6c96d3c518cf0043
```

## Reproduction

The theorem needs only Python 3 and its standard library:

```bash
python3 -B hadwiger_nelson_c13_triple_sum_shell/verify.py
python3 -O -B hadwiger_nelson_c13_triple_sum_shell/verify.py
python3 -B hadwiger_nelson_c13_triple_sum_shell/controls.py
python3 -O -B hadwiger_nelson_c13_triple_sum_shell/controls.py
```

The verifier output is recorded in `expected.json`; the control output is recorded in `controls.json`.
On the validation machine, a verifier run took about 24 seconds and a controls
run about 36 seconds. `produce.py` can regenerate the compact certificate when
given a Kissat-compatible executable, but solver soundness is outside the trust
boundary: `verify.py` directly checks the resulting colour word.

The spindle and 60-direction dictionary are the familiar ingredients described
in [de Grey's 2018 construction](https://arxiv.org/html/1804.02385v2). They were
also used in this repository's earlier bounded contact-growth pilot (source
commit `07b9c3bcf71abb317d68ed410d8e0802e23c74e9`). The result here is the
complete triple-sum shell theorem, not a novelty claim for those ingredients.
