# Dependencies and scope

Actual author: **six-vdw-2, researcher**. Every dependency below is in the
same source repository; exact file hashes are in [provenance.json](provenance.json).
All new direct cap exclusions are independent of older numerical bounds.

| Input | Verified source commit | Use |
| --- | --- | --- |
| [Mixed-edit implication/packing kernels](../van_der_waerden_27_qr617_mixed_edit_region/PROOF.md) | `45338b996411231c38ef2c5073c157911c15a427` | Square-list/bit-mask generator and independent Euler/actual-AP/set/integer checker |
| [Complete disjunction checker](../van_der_waerden_27_qr617_class29_disjunction/verify.py) | `9f183bdd6f0b78152dba63a5fc0ef8391e9d49ec` | Reconstruct full parent states, exact inherited child hypotheses and mandatory root/petal covers; its old numerical result is unused |
| [Uniform64 repair profile](../van_der_waerden_27_qr617_uniform_total64/PROOF.md) | `4e9b37fa71e682eccbe636c436f4050fbc95b5ed` | Only the dependent boundary corollary: class30..1818 and total64..3632 at both endpoints; old proof corpus is not rerun |

The graph references for these inputs are respectively
`bafkreibmh5mlwv34k2is34pnjmjonfr3tsb5dp2l43hy7kwxpp34iaahgu`,
`bafkreigdc2r7hp4snvr5h3sqwtzth6bcx7ocbtcpzabiodifflmb36ewrq`, and
`bafkreicb2jl2ktqnjw7yt7ocssglacmdib7a55z57xxzv6s6x5e6v4be2y`.
Older bounds cited transitively by uniform64 are not numerical premises of
the three new direct cap exclusions.

Monroe's [primary article](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
was checked live2026-10-01: Table1 gives length7/two colors `>3703`,
Table2 identifies prime617, and its notation puts length before colors.
Here W(2,7) puts colors first. A length3704 AP-free witness would give
W(2,7)>=3705. This package provides necessary repair cuts, with no such
witness or comprehensive current-record/priority claim. Asymmetric red3/bluek
results concern a different parameter.

Complementary published directions are context, not proof inputs:

* [Reflected-reference individual198 implications](../van_der_waerden_617_single198_implications/PROOF.md),
  source `7f3613138c7894cf24bcff93316108757ccf02a6`, graph
  `bafkreid4ycnbc5p3764ofjeirssqulksxacn46dnjpc3xs6mivcjpae4h4`.
  Its piecewise reflected QR617 reference and counted regions differ from
  the aligned reference here; its constants are not transferred.
* [Period622 degree3 character repairs](../van_der_waerden_622_degree3_character_repair/README.md),
  source `c768156dd53b9d25d45439ecf9e63334dadcaa7e`, graph
  `bafkreic7axpkcg2kybbz5ldy6xp4lumihkvoetygo7kk5s5obrbq56sjye`.
  This is a different construction template; no bound from it is imported.

The final source refresh also inspected the [new quartic family](../van_der_waerden_622_even_quartic_character_repair/PROOF.md),
source `fb05eeea151f199adcbc0d83f7d98c0dca4e34dc`: quartics that become
even after translation over F311. Its root-free repair constraints use
the different period622 template. The written proof and scope were read;
its proof corpus was not rerun and its constants are not imported.

The present cuts apply to any actual coloring compared against precisely
the displayed aligned reference and domain. An invalid intermediate search
word may remain inside an excluded box, but an AP-free completion must
leave it. No other worker's source, workspace or search instructions are
changed by this result.
