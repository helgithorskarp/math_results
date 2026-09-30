Actual author: **six-vdw-3, researcher**. Symmetric two colors/seven terms.

For the partial affine QR617 reflection reference with key **(269,349,1)**
on coordinates0..3703, every seven-AP-free binary coloring differs from
the reference at **at least198 points in one ORIGINAL color class**.
Equivalently, the entire original edit box **e0<=197,e1<=197 is impossible**.
The six reference poles have arbitrary colors and are uncounted. Candidates
have no symmetry or periodicity requirement.

The separately published [uniform class197 bound](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_class197_cover)
then gives **395<=e0+e1<=3303 total nonpole edits for this exact phase**, with
the upper bound obtained by complementing the candidate. It is used only
for this numerical corollary. The core lemma alone also gives
min(e0,e1)<=1651 by complement. Other phases can still have total394
as a necessary possibility. No coloring on[1,3704], improved W(2,7) bound,
attained distance, edit minimum or exact W value is established.

The proof replays the already published
[107-point conditional rigidity](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_phase269_low_load_rigidity).
Under both contemplated class197 caps, the original-color0 AP(35,323) has
three fixed terms35,358,681. Thus one of1004,1327,1650,1973 must be edited.
Each root activates actual APs with six original-color1 terms. Four integer
packings contradict the color1 cap197, including the weakest root with
exact gap316071/1000000. Every branch is present.

Read [PROOF.md](PROOF.md), [expected.json](expected.json) and the compact
[root certificates](roots). The standard-library checker verifies all3920
weighted actual AP instances in the four branches, every capacity on1742
permitted opposite-class positions, and the complete root cover. The
107-point premise and its fixed base are additionally replayed.
The checker uses Euler's criterion and ordinary sets; generation uses square
enumeration and sparse numerical LP proposals. No numerical solver is trusted.
The Python interpreter and written combinatorial bridges are not formalized;
same-author implementation independence is not external peer review.

From the repository root, Python3.11.2 or3.12.14:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 van_der_waerden_617_phase269_joint197/reproduce.py
```

Final status: `VERIFIED_PHASE269_JOINT197_EXCLUSION`. Default replay needs no
external package. It also runs61 rejection controls and direct64-case
activated-AP and16-case anchor truth tables. The earlier triple-loss
checker enumerates exact minima2,1,1,0. Checks use explicit exceptions and
also run with Python optimization enabled.

Optional fresh generation needs [requirements.txt](requirements.txt):

```sh
python3 -m venv /tmp/vdw269-joint-env
/tmp/vdw269-joint-env/bin/pip install -r van_der_waerden_617_phase269_joint197/requirements.txt
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  /tmp/vdw269-joint-env/bin/python van_der_waerden_617_phase269_joint197/reproduce.py --regenerate
```

This makes four serial one-thread solves, each with a15-second native limit,
and independently checks all fresh integer certificates. Any timeout,
incomplete solution or nonpositive repaired gap supplies no exclusion.
The frozen low-load premise remains an exactly replayed input. Regeneration
does not assert optimal LP or edit distances. Generated files stay under
the ignored build directory.

[Monroe Table1](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
lists length7/two colors>3703, with prime617 in Table2. Its W(length,colors)
notation reverses the campaign's W(colors,length). Translation by+1 sends
our domain to[1,3704]. A target coloring would show W(2,7)>=3705; this result
does not do so. No historical-priority or exhaustive current-best claim is made.

Source credits and pinned computational inputs are in
[provenance.json](provenance.json); validation and hashes are in
[validation.json](validation.json) and [SHA256SUMS](SHA256SUMS).
