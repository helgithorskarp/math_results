# RID rigidity on an entire closed inner receiving triangle

six-rupert-3, researcher; 2026-10-02. Author checked, unformalized and independently unreviewed.

For the standard edge-two rhombicosidodecahedron K, put phi=(1+sqrt(5))/2 and s=2-phi. Every receiver in the closed raw triangle

    conv((0,0,1),(s/2,0,1),(s/2,s^2/2,1))

has only scale-one, zero-translation equal-shadow fits: for every original proper rotation R, physical planar translation t and scale lambda>=1, inclusion holds exactly when lambda=1, t=0 and R belongs to G union H_n G. The statement retains arbitrary rolls, original halfturns, closed boundaries and signed proper-group receiving images. Read [PROOF.md](PROOF.md) for the complete ordinary bridges and exact scope. The global RID question remains open.

The new annular local collar and all-source shell certificates are reproduced here. The pole uses the explicitly cited earlier published P theorem9037; its checker is an external published proof dependency and was not newly replayed. That earlier review does not cover this new lemma.

Python3.11+ and the standard library, from this directory:

```bash
python3 reproduce.py
python3 reproduce.py --optimized --compare .generated/normal
```

Each invocation requires a fresh output directory. The second regenerates every product and compares all mathematical fields and every coefficient with the first execution. Both modes use strictly sequential child jobs with20-second guards and numeric threads1. Each mode runs48 complete18-root source products,3 complete closed receiving collar layers,8 whole-cell assemblers and1 closed receiver join. A failed or timed-out child leaves the execution incomplete.

Expected source result:8,730 midpoint nodes;9,594 leaves (8,705 physical,889 gauge);428,210 exact joint controls greater than1/100000. The exact minimum is

    -217/22528+(1477/247808)*phi.

The whole-annulus collar has36 actual signed contact duals,2880 bicubic controls, coordinate masses(19,42,7), radius1/53 and squared closure88047/89888<1. All closed seams and the overlap with P are checked.

[forests.json](forests.json) contains108 literal prefix trees per receiving cell. Tokens0..5 denote midpoint bisections of edges in lexicographic order:01,02,03,12,13,23. A branch is followed by its two closed child trees. S0..S539 are actual physical rows (support index times60 plus original vertex); G0..G59 are the sign-paired actual binary gauges in freshly rebuilt order. Commas separate tokens. This is a small literal certificate, with no coordinate or sign dump. [collars.json](collars.json) contains only actual endpoint contact triples and rational bounds. Every sign is recomputed.

[expected.json](expected.json) binds the entire coefficient streams, literal forests, geometry, margins and counts. [DEPENDENCIES.json](DEPENDENCIES.json) pins every runtime source and compact input before import. [VALIDATION.json](VALIDATION.json) records actual source and relocated executions, exact summaries and deliberate damaged-input checks. All large coefficient records and execution journals stay in the ignored .generated directory. No private scratch, ledger or external numerical library is a runtime input.
