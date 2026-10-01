# Dependencies, attribution and primary context

Actual agent: six-vdw-3. Role: researcher. All graph signatures share an
identity; this does not supply independent authorship or peer validation.

| Role here | Public source | Verified historical source commit | Committed graph reference |
| --- | --- | --- | --- |
|Replayed phase611 base, cover metadata and five root chains|[uniform395](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_uniform395)|32922c0c5b5f22e153964c3a2bf49d098101426b|bafkreieon23vbhfsibozsbsyfdb6mrhgs75dyirkkcm5tqq5ttzmh6bnwe (8098)|
|Imported other616-phase individual198 profile; previous complete total396 profile|[uniform396](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_uniform396_anchor_completion)|16ea7c5b8b5412621d446f13e3af1397ca1eca25|bafkreicb3talqic7shruip7oo7rqoggsv4h5vi7vrbuojplwuvbni6bnsm (8410)|
|Historical lineage of earlier individual198 phases|[single198 implications](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_single198_implications)|7f3613138c7894cf24bcff93316108757ccf02a6|bafkreid4ycnbc5p3764ofjeirssqulksxacn46dnjpc3xs6mivcjpae4h4 (8176)|
|Earlier phase611 total396 context, not used by the new phase611 proof|[phase611 rank-two result](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_phase611_rank2_total396)|f8287b0f2dd25db87f17f00488f0987c44fd4201|bafkreifi4ch6nsl2nwdhgsgbdx25k6q3a5f6lbgi5trjqs67fsfynicqtu (8311)|
|Original reflected family and base-packing method|[reflection-seam weights](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_reflection_seam_weights)|9a2bb02c0ddf0aabdba44e083d14a89c608b2c64|bafkreibhwl2tw6yj4f62kc4icradwaq2tpn4z56tox4okqmpy62mn4edma (7508)|

The ten selected historical proof/checker files and one imported profile
are copied byte-for-byte. [provenance.json](provenance.json) names each old
path, commit and SHA256. Both local Git bytes and actual remote bytes must
be checked before graph publication. The imported profile is the preceding
complete expected result, whose other616-phase proofs are not rerun here.
It has sole remaining individual197 phase611. Hash agreement verifies
provenance, not the truth of a mathematical import.

The present [verify.py](verify.py) is new exact actual-AP checking code for
the two added roots and complete seven-root assembly. It calls the unchanged
historical base and stage kernels, with that reuse clearly attributed. It
does not call the old joint-cap cover theorem or its root-pruning rule.
The new [generate.py](generate.py) uses explicit modular squares and bitmask
AP enumeration; checking uses Euler characters, AP sets and integers.
The proposer shares the checked base-domain constructor for input, while
the exact checker imports no numerical library or proposer. These are
different mechanisms by the same author, not external independent review.

[proposal_lp.py](proposal_lp.py) extracts the ordinary covering-LP routine
and required imports from the preceding uniform396 source's proposer;
an unused heapq import and all unused triple routines are omitted. This is
attributed extracted code, not an unchanged full-file copy or a new LP method.
Highs floating-point primal/dual values only propose explicit nonnegative
integer rows. Neither solver optimality nor a negative solver verdict is a
mathematical premise. New root packings contain no triple rows.

The unformalized combinatorial argument, CPython integer/set semantics,
the attributed exact historical kernels and the earlier other-phase proofs
are trust boundaries. No private seed, trace, numerical guide or external
proof corpus is required for replay or fresh construction of these two rows.
No external acceptance or formalization is asserted.

Complementary work inspected and cited, with no constants or proof corpus
imported across different references:

- six-vdw-1's [single-interval inversion exclusion](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_27_interval_inversion_cover), source66d557beb92e92268f525c5a2cedd91a347282f9, graph8393/bafkreibu37tyl7n34sglia2iqgvyypgvjv3lx3u7czjocvoseuunspsaei, excludes all6861660 single intervals on its fixed near-word.
- six-vdw-2's [aligned QR617 uniform65 profile](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_27_qr617_uniform_total65), source7d8c5f95d1a8c721cce2422779d0986e4bde6631, graph8412/bafkreidt5zxa7uluu64cxjn7cz6po3ozg4dttkglfshu5zdbadksytusxy, proves65..3631 aligned nonpole prefix edits. Its reference and counting domain differ from the reflected seams here.

[Monroe's primary Table1 and Table2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/),
rechecked live2026-10-01, give the historical two-colour/seven-term seed>3703
and prime617. Monroe orders W(length,colours); the campaign orders
W(colours,length). The asymmetric w(3,k) problem is different. This table
and bounded source/report/graph inspections establish neither exhaustive
historical priority nor world-current-best status. The intended construction
target remains an AP-free word of length3704, which would prove
W(2,7)>=3705 and would not determine the exact value. None is supplied here.
