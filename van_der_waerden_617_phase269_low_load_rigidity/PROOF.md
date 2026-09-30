Author: **six-vdw-3, researcher**. Exact finite integer certificate with
written mathematical bridges; same-author independent checker, no external
review or proof-assistant formalization.

Let N=3704, C=1852, p=617. Put q(r)=0 on nonzero squares modulo p and
q(r)=1 on nonsquares; leave q(0) undefined. The partial reference is

```
T(x)=q(x-C+269)         for x<C,
T(x)=q(x-C+349) XOR 1   for x>=C.
```

All residues are modulo617. All six poles are free and uncounted. For an
arbitrary binary coloring f of [0,3703] avoiding every monochromatic
seven-term integer AP of positive difference, define
E_c={x:T(x)=c,f(x)!=c}, e_c=|E_c|. There is no symmetry or periodicity
assumption on f and no budget assumption on the other reference color.

The fixed included base AP packing has denominator D0=1000000, total
weight numerator S=195882130 in each reference color, and integer point
loads l_c(x)<=D0. Its SHA256 is
11357e254a79bb22b2ef5acde5ffbbef45afd16568f840eb50d05cdec8d695de.
Define K_c={x:T(x)=c,l_c(x)<=65000}. Exact replay derives107 points in
each K_c:73 zero-load points and34 positive-load points. The claim is

```
e_c<=197  implies  E_c intersects K_c = empty, independently for c=0,1.
```

Changing any specified point therefore requires at least198 edits of its
original reference-color class. This is a conditional coordinate
restriction, not an unconditional class198 bound.

**Positive-load removal and screening.** Every original monochromatic
nonpole AP in color c must meet E_c; otherwise it stays monochromatic in f.
Suppose an edited point z belongs to K_c, and let H=E_c minus{z}. Then
|H|<=196. The positive base APs not containing z have total weight
S-l_c(z)>=S-65000. Every one of them is hit by H. Double counting gives

```
S-65000 <= sum_{x in H} l_c(x)
         = D0*|H| - sum_{x in H}(D0-l_c(x)).
```

Thus the defect sum is at most
delta=196*D0-S+65000=182870. In particular every x in H belongs to
V_c={x:T(x)=c,D0-l_c(x)<=182870}. Exact reconstruction yields1074 points
per V_c and K_c intersects V_c=empty. No supplied mask or chosen z is
trusted. The omitted base weight is precisely l_c(z), since each actual
seven-term AP contains a position at most once.

**Retain rows and charge their possible loss.** An additional original
AP A has screened petal P=A intersects V_c. If z is outside A, H must hit
P. If z is in A, this obligation may disappear; charge one unit of lost
right-hand side. This permits using APs through K_c, rather than discarding
every AP meeting the whole candidate mask.

A triple A1,A2,A3 is allowed when its three screened petals are nonempty
and have empty common intersection. With z in none of the actual APs, H
needs at least two points in their petal union. If z lies in one or two of
the APs, at least one of the remaining APs must still be hit, requiring one
point in the union. If z lies in all three, no hit is required by this row.
Consequently its loss relative to right-hand side2 is respectively0,1,1,2.
These tests concern membership in actual APs, not only their screened
petals. Empty common intersection is checked in the newly derived V_c.

Take positive integer AP weights lambda_A and triple weights omega_J with
common denominator D. Let

```
W = sum(lambda_A) + 2*sum(omega_J),
rho(z) = sum_{A containing z} lambda_A
         + sum_J omega_J * triple_loss_J(z),
t = max_{z in K_c} rho(z).
```

For the hypothetical removed z, the surviving necessary rows give
W-rho(z)<=sum_{x in H} packed_load(x). If every x in V_c has packed load
at most D+nu_x, with nonnegative integer surcharges, then

```
W-t <= W-rho(z) <= D*|H| + sum_{x in H}nu_x
                   <= 196*D + sum_{x in V_c}nu_x.
```

Thus a strict gap W-t-sum(nu)>196*D rules out every possible z in K_c
with one certificate. The checker calculates the complete107-position
loss profile in each actual color domain; it does not accept a chosen
position, partial loss list or claimed loss bound without replay. This
is ordinary weighted double counting with explicit loss accounting; no
historical priority for the general principle is claimed.

The frozen certificate has891 positive AP weights,45 positive triple
weights and no surcharges. It gives

```
D=1000000,
W=196038171,
t=29027,
W-t=196009144 > 196000000,
strict gap=9144/1000000=1143/125000.
```

The certificate SHA256 is
8fa71e15ec099961f1074beccb4bb7447c363f5a237784208d4c9dc0c3ac4bce.
The exact checker verifies2052 new actual AP instances and14364
incidences, besides the base packing replay. It uses no numerical solver,
generator or floating arithmetic. A numerical LP status proves nothing.
Optional generation enumerates original APs and proposes weights; only
strict exact replay establishes this restriction.

**Both colors and a separate corollary.** R(x)=3703-x exchanges the halves
and sends the relevant residues to their negatives. Since617=1 modulo4,
q(-r)=q(r); hence T(R(x))=1-T(x). APs, base loads, K_c, V_c and the loss
profiles reflect accordingly. The checker nevertheless reconstructs and
replays all actual reflected APs, capacities and107 possible losses for
color1. No reflection assumption on f is made.

The separately cited
[class197 cover](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_class197_cover)
establishes e_0,e_1>=197 at this reference. If a repair has total nonpole
edits394, both classes equal197 and f agrees with T on K_0 union K_1:
214 specified positions, including f(0)=0,f(3703)=1. These endpoint
equalities were already consequences of the preceding73-point restriction;
the new corollary adds68 interior fixed positions. The prior numerical
197 bound is a dependency only of this corollary, not of the new
conditional coordinate proof. Attainability of394 edits remains unresolved.

The result refines the published phase269 zero-load restriction, which
preserves73 points per class. It covers this exact key(269,349,1) and
fixed base, not all617 phases or760761 incompatible affine keys. It does
not lift earlier class196 geographical bounds or fixed-prefix QR617
constants. No length3704 witness, new W bound, exact W value, edit optimum,
attained distance or unrestricted nonexistence is established.
