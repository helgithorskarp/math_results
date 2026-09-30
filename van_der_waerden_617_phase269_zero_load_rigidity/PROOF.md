Author: six-vdw-3, researcher. Exact rational finite certificate with written
unformalized bridges; same-author independent checker, no external review.

Let N=3704,C=1852,p=617 and q(r)=0 for a nonzero square modp,1 for a
nonsquare. At zero it is undefined. The partial reference is

```
T(x)=q(x-C+269)          for x<C,
T(x)=q(x-C+349) XOR1     for x>=C.
```

All q arguments are reduced mod617; all poles are free, uncounted values.
Let f:{0,...,3703}->{0,1} have no monochromatic seven-term integer AP with
positive difference. E_c={x:T(x)=c,f(x)!=c}, e_c=|E_c|. The new theorem is:
for independently c=0,1, if e_c<=197 then E_c intersects Z_c=empty, where
Z_c is the complete zero-load set defined by the included base certificate.
The checker derives |Z_c|=73 and prints both coordinate lists.

Every nonpole AP monochromatic in original reference color c must contain
an element of E_c; otherwise it remains monochromatic in f. This necessary
AP-hitting implication requires no symmetry, periodicity, far-edit bound
or budget for the other reference-color class.

**General reduction by removing a zero-load edit.** Take any positive
weighted family of original-color APs, denominator D0, total weight S and
point loads l(x)<=D0. Define Z={x of that reference color:l(x)=0}. Assume
|E|<=B and choose z in E intersect Z. Every positive base AP avoids z, since its
positive weight contributes to l(z) if it contains z. Let H be E with z removed. It
still hits every positive base AP. Double counting gives

```
S <= sum_{x in H} l(x)
  = D0*|H| - sum_{x in H}(D0-l(x)).
```

Since |H|<=B-1 and all defects are nonnegative, H is contained in

```
V={x of that reference color:D0-l(x)<=(B-1)*D0-S}.
```

Any additional original AP A avoiding ALL of Z must be hit by H, regardless
of which zero-load edit z was chosen. Thus H hits its petal A intersects V.
This turns all choices of z into one necessary hitting problem. The
reduction is elementary; no historical novelty for the general principle
is asserted. Its exactly checked phase269 instance is the new restriction.

Here B=197,D0=1000000,S=195882130 and delta=(B-1)D0-S=117870. Exact base
replay verifies every original AP, both colors, positive weights and all
point capacities. It derives |V|=1012 and |Z|=73 in each reference color.
Because delta<D0, V avoids Z; a hypothetical second zero-load edit would
already be impossible in H. The proof does not assume a chosen z, supplied
mask, or a symmetry of f.

**One exact contradiction.** The new certificate lists positive integer
AP weights lambda_A and weights omega on unions of three petals, common
denominator D=1000000. Every listed actual AP is monochromatic in its
required reference color, crosses the actual seam and avoids ALL of Z.
For three nonempty petals with empty common intersection no one point
hits them all, so H must contain at least two distinct points in their
union. The checker verifies those hypotheses rather than accepting a cut
identifier or its claimed right-hand side.

Let W=sum(lambda)+2sum(omega). If the load at each x in V is at most D+nu_x,
then hitting all the rows requires

```
W <= D*|H| + sum_{x in H}nu_x <= 196D + sum_{x in V}nu_x.
```

Nonnegative vertex surcharges are subtracted in full. The frozen certificate
has869 positive AP weights,34 cover-two weights,zero surcharges and
W=196096042>196000000. Its exact surplus is96042/1000000=48021/500000.
Therefore H cannot exist, and neither can an edited point of Z under the
class197 budget. This is one uniform certificate with no position cases
or binary branches, not an inference from a numerical LP status.

**Both colors and dependent corollary.** R(x)=3703-x exchanges halves and
sends each residue to its negative. Since617=1 mod4, q(-r)=q(r), hence
T(R(x))=1-T(x). It preserves integer APs and reflects the base loads,
Z_0 to Z_1 and V_0 to V_1. The checker nevertheless replays every actual
reflected AP, avoidance test, triple intersection and capacity for color1.
The proof applies independently to either color and assumes no reflection
of f. If f changes any point of Z_c then e_c>=198.

The cited uniform reflection-seam profile gives e_0,e_1>=197. At total394
against this specific reference they must both equal197, so f agrees with
T at Z_0 union Z_1:146 explicitly listed nonpole positions. In particular,
f(0)=0 and f(3703)=1, because0 belongs to Z_0 and3703 belongs to Z_1.
These endpoint equalities follow from the new coordinate rigidity once
both class caps are known. The earlier class197 numerical profile is a
separate dependency of the total394 corollary; it is not
needed to deduce the new conditional zero-edit theorem. Neither the
corollary nor the certificate asserts that a394-edit repair exists.

The base certificate is fixed by SHA256
11357e254a79bb22b2ef5acde5ffbbef45afd16568f840eb50d05cdec8d695de.
Zero loads and the specified sets refer to these exact weights, not every
numerically regenerated dual for the same reference. Both base and new
certificate are included, so no private proof input is required. The new
frozen certificate SHA256 is
da470096764f2ee812d0ca4dd0f5ddaf96eb19ded35d5a2b822d29ebcfb789a8.

The theorem is conditional edit rigidity for phase269,key(269,349,1), not
all617 phases or arbitrary incompatible affine references. All six poles
stay free. No original class196 geographic constants are lifted to197.
No AP-free3704-point word, new van der Waerden bound, attainable optimum,
global nonexistence or exact W value is established.
