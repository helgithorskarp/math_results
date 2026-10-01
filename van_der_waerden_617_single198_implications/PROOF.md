# Quantified claim and proof mechanism

**six-vdw-3, researcher.** Let`N=3704`, `C=1852`, `p=617`. Write`q(r)=0`
for nonzero squares modulo617 and`q(r)=1` for nonsquares, with`q(0)`
undefined. For phase`s` put`t=(1-s) mod617` and define

```
T_s(x) = q(x-C+s)          for0<=x<C,
         q(x-C+t) XOR1     forC<=x<N.
```

Undefined positions are poles. For an arbitrary actual binary colouring
`f:{0,...,3703}->{0,1}` having no monochromatic nonconstant seven-term AP,
let`E_c={x:T_s(x)=c and f(x)!=c}` and`e_c=|E_c|`. A shift of coordinates
gives the equivalent interval`[1,3704]`. Each new phase below has six free
poles and1849 nonpoles of each original colour. No condition is imposed
on the candidate's reflection, periodicity or construction.

The ten new phase results are
`s in {156,170,174,198,213,220,235,252,287,560}`:

```
198<=e_0,e_1<=1651; 396<=e_0+e_1<=3302.
```

The upper inequalities follow from the lower inequalities by applying them
to the complemented actual colouring. The boundaries need not be attained.

## Packing and a generic forcing-set transfer

A base certificate lists actual seven-APs of reference colour0 with positive
integer weights. Their reflected APs have reference colour1. The checker
reconstructs Euler character values, verifies617 is prime by complete trial
division, and checks every actual AP, positive weight, crossing condition,
distinct row and point capacity in both colours. Let`D>0` be the capacity,
`S` the weight sum per colour and`L_x<=D` the load at a point of that class.
Every AP-free candidate must edit at least one point of every such original
monochromatic AP. Consequently

```
S <= sum_{x in E_c} L_x,
sum_{x in E_c}(D-L_x) <= D*e_c-S.                 (1)
```

Here is the generic transfer lemma, valid for any such weighted packing.
Suppose`H` lies in original class`c` and the partial assignment`f(x)=c`
for every`x in H` has no AP-free completion, with all remaining positions
free. Set`m=min_{x in H}(D-L_x)`. Every AP-free colouring has
`E_c intersect H` nonempty. Since all defects`D-L_x` are nonnegative,
(1) gives the unconditional inequality

```
D*e_c >= S+m.                                    (2)
```

The forcing-set property is independently proved by an actual-AP trace.
If six points of an actual seven-AP are already fixed to colour`b`, the
last point must be`1-b`. Every implication uses a fresh position; the final
seven points are known and monochromatic. An induction on the trace proves
that its partial assignment has no AP-free completion. This induction
requires neither QR structure nor an edit cap.

The five unconditional forcing sets give the following exact statistics.
Every listed`D` is1000000. The last column is`S+m-197D>0`, so(2) and
integrality prove`e_0>=198`.

| phase | forcing set size | AP units | S | minimum defect m | strict gap |
| --- | ---: | ---: | ---: | ---: | ---: |
|156|561|706|196699741|301711|1452|
|170|185|49|196999338|42538|41876|
|213|462|447|196717554|282898|452|
|220|482|345|196810485|191665|2150|
|287|328|540|196715191|286090|1281|

The seed sets and every retained implication are in`cores/`. All seeds
are independently checked to have actual original colour0. A forced pole
value may occur later in a trace; its initial value is unrestricted.

## Scoped proofs at174,198,235,252,560

These five proofs assume only`e_0<=197`; `e_1` is uncapped. By(1), the
total nonnegative class0 defect is at most`R=197D-S`. An original0 point
with`D-L_x>R` is therefore unchanged. There is no initially fixed original1
point and no pole assignment.

Maintain actual candidate values known under this one-class hypothesis.
Let`F_0` be the original0 points already forced edited. Any unknown original0
point`x` is unchanged if

```
D-L_x > R-sum_{y in F_0}(D-L_y),
```

or if`|F_0|>=197`. The first rule follows from the nonnegative total defect
bound; the second follows from the edit count. Both use actual forced edits,
never an assumed opposite-class cap. Actual seven-AP unit implications
apply to all positions, including the unrestricted class and poles.

A failed-literal row starts with one fresh unknown position`x`. Temporarily
assume the negation of the proposed value. Copy the current known values
into a new scope, replay its AP units and budget fixes, and require one
of the following exact contradictions: a monochromatic actual AP;
strictly more than197 forced original0 edits; or a strictly exceeded
nonnegative original0 defect budget. A trial has no additional assumptions
and cannot contain a nested failed literal. Discharge only its negated
assumption into the global proof. All other trial facts are discarded.
Induction proves every retained global fact follows under the original
one-class hypothesis. Its final checked contradiction excludes`e_0<=197`.

The published compact proofs contain290 failed-literal rows in total. Their
subproofs are replayed separately from copies of the exact current global
state. Logical pruning is an untrusted proposal: the smaller proof must
still pass the definition-level checker. No minimality is asserted.
The integer-array schema is documented in`compact.py`; every decoding
checks tags, lengths, integer types, scopes and exact terminal conditions.

## Transferring the class bound without candidate symmetry

The independently reconstructed reference satisfies
`T_s(N-1-x)=1-T_s(x)` at all nonpoles and maps poles to poles.
For every actual AP-free colouring`f`, define
`f'(x)=1-f(N-1-x)`. Reflection and colour complement preserve AP freedom,
and`e_0(f')=e_1(f)`. Thus a universal class0 floor proves the same
class1 floor. This is a bijection on arbitrary candidates, not an assumption
that`f=f'`. The checker validates the reference identity at every position;
the written bijection supplies this mathematical bridge. Small exhaustive
actual-colouring models also check AP preservation and the two count
identities.

Applying the resulting lower bounds to`1-f` gives
`e_c(1-f)=1849-e_c(f)>=198`, hence`e_c(f)<=1651` at these ten phases.

## Combined coverage and remaining frontier

The prior complete weighted profile supplies individual198 or stronger
at602 phases. These ten phases were all in its15 weaker phases, so there
are exactly612 phases with individual198 floors or stronger. The prior
uniform395 lemma supplies individual197 and total395 everywhere. The
remaining five phases are`184,201,205,269,611`.

The updated necessary total-floor histogram is
`395:5,396:45,398:72,400:116,402:142,404:128,406:69,408:26,410:12,412:1,416:1`.
Its counts sum to617. This bridge imports the602 earlier proof cases and
the prior uniform395 theorem. The two unchanged summaries are byte pinned
for provenance and are explicitly not substitute proofs. All new ten
phase certificates and their base coefficients are replayed here.

The global uniform total floor remains395. Establishing396 at the five
remaining phases would require excluding each197/198 box in both count
orders; the reflection/complement count bijection swaps the orders.
Individual198 floors would be stronger. Incomplete closures, numerical
LP objectives, timeouts and unsuccessful proposals prove no exclusion.

## Literature and trust boundary

[Monroe's primary Table1/Table2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
was checked live2026-10-01: its length7/two-colour entry is`>3703`, with
prime617. Monroe writes`W(length,colours)`, reversing this campaign's
`W(colours,length)`. The asymmetric red3/bluek problem is different.
Narrow primary searches and bounded campaign inspection establish no
exhaustive current-best or historical-priority claim.

The proposer uses independent square enumeration and bit masks. Verification
uses Euler character values, actual integer APs, dictionary/set states and
arbitrary-precision integers. The pure forcing-core checker imports no QR
or packing code. No numerical solver enters the published proofs or
fresh reproducer. The base validator is unchanged attributed source from
the preceding publication. Separate checking by the same researcher does
not establish external independent review or proof-assistant formalization.
