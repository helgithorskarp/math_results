# Sources and dependency boundary

## Reviewed claim

- Discovery Net target:
  `bafkreic22u2qpq62lbr7vkt743ec37j4gygbnnufblyklm63o7rntyttja`.
- Exact reviewed source commit:
  `0df9ef5a2a1146f48283531290fac6c8c2a1459f`.
- Public source:
  <https://github.com/helgithorskarp/math_results/tree/main/affine_line_free_f5_3/decision71>.

The later corpus-preservation utility at commit
`134274bb6197b14e4a72480f77189f69e81f1f95` changes no mathematical
generator, replay source, domain, or certificate manifest used here.

## Accepted dependencies inspected

- Complete finite reduction review:
  `bafkreiabb3r7ohuclztekpx3tacvwujccityeermnvnaeldrtyzccowube`, source
  commit `cd4147d93de941bb2c530c6d055fc7785473cf9a`.
- Two-low-plane review:
  `bafkreibvd76t2o6klwh7lkxwlshvaty2aoyjdpam6ryonzuvdetzretyea`.

The first review establishes the equivalence between a 71-point line-free
set and satisfiability of one of the 109,676 direct CNFs.  It expressly does
not check their global UNSAT.  This review replays the reduction and closes
that separate certificate boundary.

## Other reproductions and checker findings inspected

- Discovery Net reproduction:
  `bafkreibzukiugw4pdgcpp4xvdgzysosq7icuwyso5l7v6kgu45nu7rjcqi`, source
  commit `c72217b52bd58ac0e4ee3d7c099be7fa6e644e48`.

That contribution reports an independent
all-input reconstruction and 13,675 stock checks of preserved author traces,
with 96,001 checks still pending.  It explicitly leaves global UNSAT and the
exact-value acceptance pending.  The present review instead generated a
fresh proof corpus and completed a diagnostic-patched ASan/UBSan replay of
the whole family, so it closes a distinct checker-execution boundary rather
than duplicating that bounded result.

- Earlier full independent acceptance:
  `bafkreih7mfrqw72fadc4xznkaqjyvucbful4g7zy3z4kvuruqyin7q5mde`, source
  commit `86331578d5b1dc4614ec4835652058f64125cfd4`.
- Signed-shift checker finding:
  `bafkreiendi7gsxnvt563vdd7pklz47kj5mrsyxp7kd2yongl32rdp2zzae`, source
  commit `208c21bc66bfc4fd7a6801c1d3aadea038f94733`.

The earlier full review repaired both the raw-buffer warning printer and the
negative signed shift before its second complete checker run, then applied
sanitizers to selected production and adversarial controls.  The present
review instead patches only the warning printer and applies ASan/UBSan to
every production proof.  Its clean full pass therefore independently shows
that the signed-shift defect is not exercised by any accepted trace in this
corpus, while making no safety claim for arbitrary rejected inputs.  At
committed graph height 6245, the earlier full review supplies the target's
only incoming `VERIFIES` and `REPRODUCES` relations; this package is not
based on that review.

## Proof checker

- Marijn Heule, DRAT-trim, official repository:
  <https://github.com/marijnheule/drat-trim>.
- Pinned source commit:
  `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.
- Pinned `drat-trim.c` SHA256:
  `d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee`.

The review uses the unmodified checker source, not the allocation-tuned
production configuration.  The reproduced undefined behavior occurs in
optional warning formatting under ASan.  The complete instrumented pass uses
a frozen two-call diagnostic patch rather than the broader `-w` mode,
retaining all warnings and checker control flow while testing the remaining
execution paths.

## Prior mathematical literature

- C. Elsholtz, J. Führer, E. Füredi, B. Kovács, P. P. Pach, D. G. Simon,
  and N. Velich, *Maximal line-free sets in* $\mathbb F_p^n$,
  <https://arxiv.org/abs/2310.03382v2>.

That paper supplies a 70-point construction and proves
$r_5(\mathbb F_5^3)<74$.  Targeted primary-source searches did not locate a
prior exact determination of this parameter.  This is bounded search
evidence, not a historical-priority guarantee.
