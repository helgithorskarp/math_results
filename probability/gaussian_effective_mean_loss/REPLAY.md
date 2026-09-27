# Historical replay of the original mean-loss packet

The original ten files in this directory remain byte-for-byte as published
at source commit f171c499bc0ed272d1b6fd5f78d57968d1578b62. The new replay
files are outside its original SHA256SUMS.

R8's later commit 9117b9b64127df8ee18337d9205e4aa7a9b70960 added acceptance
and continuation links to the header of its mean-loss PROOF.md. Its
mathematical body did not change, but the original INPUTS.json correctly
detects that byte change. Running the original verify.py against current
main therefore fails that pin. Do not replace the historical pin.

The [replay helper](replay.py) extracts the original packet and all ten
pinned inputs from the recorded commit into a temporary directory. It
checks their hashes and runs the unchanged verifier. It needs Python 3.11+
and Git with that commit available locally; there is no network request
or checkout mutation.

~~~
python3 probability/gaussian_effective_mean_loss/replay.py
python3 probability/gaussian_effective_mean_loss/replay.py --optimized
~~~

Both commands must report EFFECTIVE_MEAN_LOSS_PASS and HISTORICAL_REPLAY_PASS.
Expected record SHA-256:
1fed1586ae3915c7410387cbd68551c26dd9479d17b922092f02563b37a79e31.

The changed upstream PROOF.md had SHA-256
dd7620f1e3db97a497fd0806b18b89df7ea06e93e40a06da5ab960ae8890a0ee;
its new header gives
6725d26ad282b74447a6ee4e93f08b0fe91adae32bfecf85e11d32446cc9e20d.
This is a provenance repair, not a mathematical correction or an independent
review. The original argument has independent acceptance at graph6432; see
the [review](../gaussian_effective_mean_loss_review_r4/REVIEW.md). The follow-on [small-loss defect proof](../gaussian_small_loss_defect/PROOF.md)
uses versioned input pins so future header changes retain reproducibility.
