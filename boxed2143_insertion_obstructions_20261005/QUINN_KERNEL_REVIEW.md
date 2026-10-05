# Internal full-scope review of Quinn's maximum-insertion kernel

Reviewer: Theo, literature-researcher-4. Author: Quinn, literature-researcher-3. Date:2026-10-05. Verdict: accept the exact insertion/occurrence Claims1–3 and the stated legal-gap-only state obstruction, at the reviewed bytes below. This is an internal team check of partial structural mathematics, not external peer review, a novelty judgment, or a solution of decision410.

Reviewed proof SHA256: `e1a1e1f2604d6692b4e54484a971d3772c101b73925fb680988ba79eba5a376d`.
Reviewed kernel SHA256: `546db68acf8a12532397608e48afa617415b6cc7b405851434a5ea9020040fe5`.
Reviewed state-obstruction SHA256: `9926fdeef70be67658ebfc75afe93fe071466334ce840c02f1944918d5270ff7`.
The reproduction JSON pins all10 author manifest files and the manifest itself; every size/hash matched and was unchanged at the end of the run. The coordinator's retained packet has the same initial source scope. Hashes establish byte identity, not truth.

## Independent argument from canonical value intervals

My checker was independently designed around value-boundary rectangles, before reading Quinn's kernel. Its full occurrence sets have already been compared with Lyra's direct four-index/interior checker. I use that known interval characterization to derive the insertion rule independently.

Insert a new maximum M=n+1 into gap g of a parent p. Any occurrence using that point has it third in selected order. Fix the selected minimum B=p_j. Restrict the child to values in [B,M]. Rectangle emptiness is equivalent to its four selected points being a consecutive factor in this restricted word. Removing the new maximum leaves the three consecutive points x,B,z. In the parent, x and z are therefore the closest points on either side of B with value greater than B. These are exactly Quinn's l(j),r(j); no closer qualifying point may be skipped. The pattern order requires B<x<z<M, equivalently p_l<p_r. The new maximum lies immediately after B in the restricted word exactly when its original gap satisfies j<=g<r in one-based parent indexing. Every parent point between B and z in position is below B, so any such gap works. Conversely these conditions construct the consecutive [B,M]-factor x,B,M,z and hence an actual boxed occurrence. This proves the complete iff and its explicit witnesses for arbitrary parents, without assuming they avoid.

Indices are sound: l,j are on or left of gap g and keep their one-based indices; the new maximum has index g+1; r is right of the gap and shifts to r+1. In zero-based code the blocked gap interval is [j+1,r] and the child tuple is (l,j,g,r+1). Empty or one-sided greater-neighbor sets produce no eligible triple. The minimum-to-maximum value interval is nondegenerate and distinctness follows from permutation validation.

Old occurrences persist: their selected maximum is at most n, so the new point M is above every old rectangle and cannot obstruct one. Translating old indices accounts for all old occurrences. Thus the author function legal_maximum_gaps correctly returns gaps creating no *new* occurrence. It characterizes avoiding children only when the parent avoids, a condition stated explicitly in the proof and API. A nonavoiding parent has no avoiding child, regardless of that function's output. Deleting a global maximum likewise cannot create an occurrence among remaining entries, because the removed point lies above every such candidate rectangle. Every avoiding child consequently has one avoiding maximum-deletion parent. Recording maximum positions recovers the complete insertion history, proving the exact full-class generating tree and its object-level counting recurrence.

For the complete occurrence checker, assign each occurrence to its selected largest value M. Deleting all values above M changes no emptiness condition for its rectangle. In the restriction to values<=M, deleting M gives a valid permutation of [M-1], and the preceding insertion rule finds exactly the occurrences using M. Restoring larger entries changes none of them because those entries are vertically outside the rectangle. Translating retained positions back to the original permutation is therefore correct. The largest selected value uniquely assigns each occurrence to one loop iteration, and distinct minimum positions distinguish occurrences within that iteration. There are no missing or duplicated occurrences.

The proposed state obstruction is also correct independently of the kernel: at parent size2,12 and21 both have three legal gaps because all children have size3. Appending3 gives123 and213. Of the four insertions of4 into each, only inserting at gap2 into213 gives the entire permutation2143. Hence the next legal sets differ. At length4, boxed2143 containment is exactly equality to2143. Parent sizes0 and1 have only one permutation each, proving the stated same-size collision minimality. This excludes the legal-gap set alone as a deterministic state; it does not exclude other encodings or prove any asymptotic result.

## Code and finite replay

The monotone-stack routine retains right-to-left maxima of the scanned prefix. Its indices increase and values decrease. An omitted index is dominated by a later, larger entry; it cannot be the nearest greater predecessor whenever a dominating entry is available. Popping values below the next value and reading the surviving top therefore finds the closest greater predecessor. The reverse scan is symmetric. Strict comparison is sufficient because inputs have distinct values. The difference-array marks the exact union of valid closed gap intervals, and the complete checker performs the value restriction and position translation described above. Explicit validation rejects nonpermutations, noninteger entries including bool, and invalid gap indices. Mathematical acceptance in the reviewed kernel does not depend on assertions or floating point.

`check_quinn_kernel.py` compares the author outputs against my separately derived rectangle representation and against naive neighbor scans; it imports no author verifier or expected table. It checks:

- complete occurrence sets on all5914 labelled parents of sizes0 through7;
- all46233 maximum-insertion instances, comparing the complete new-point occurrences and all shifted old occurrences against the actual child rectangles;
- the forbidden-gap union, the parent-avoidance qualification, and nearest greater indices entry by entry;
- nine malformed-input controls and the minimal state collision reconstructed directly from length-four permutations.

The replay passed. Exact child-occurrence stream SHA256 is `896b9bf0d7ae78603ac8cdd500df0b3b232d1dad94cf4cd55bc379beedff185a`. Runtime was about4.57 seconds on CPython3.11.2, peak Linux RSS19592KiB. No solver, parallel native job, external package, or approximate mathematical computation was used. Reviewer evidence is `quinn-kernel-reproduction.json`.

Reproduce from this directory:

```sh
python3 -B check_quinn_kernel.py --max-n 7 --output quinn-kernel-reproduction.json
```

The default author path names the transferred campaign workspace. It can be overridden with `--author-dir` to replay the coordinator's unchanged snapshot. A changed manifest/source is an explicit failure. Timings may vary; source and deterministic occurrence-stream hashes are the reproducibility evidence.

The finite replay tests implementation, indexing and normalization. The written argument above supplies the checked arbitrary-size reduction; finite agreement cannot replace it. The trust base consists of the written arguments, inspected source, Python/stdlib and exact permutation representations. Neither this review nor the author packet supplies the missing uniform entropy bound or high-branching construction. Decision410 remains unsolved, and no public source verification or completion-stop request is justified.
