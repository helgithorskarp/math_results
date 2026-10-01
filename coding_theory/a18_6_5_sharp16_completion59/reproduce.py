"""Sequential reproduction from fresh source and generated state."""
import json
import os
import resource
import subprocess
import sys
import time

from common import HERE, WORK, encoded, require


def run():
    started = time.monotonic()
    WORK.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    env.update({name: "1" for name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS")})
    env.update(CWC_SHARP_COMPLETION_WORK=str(WORK.resolve()), PYTHONDONTWRITEBYTECODE="1")
    regenerated = WORK.resolve() / "regenerated_certificate.json"
    commands = [("producer", ["produce.py", "--output", str(regenerated)]),
                ("verifier", ["verify.py", "--compare-producer"]),
                ("optimized_verifier", ["-O", "verify.py", "--compare-producer"]),
                ("optimized_controls", ["-O", "controls.py"])]
    expected = json.loads((HERE / "summary.json").read_text())
    children = []
    for label, args in commands:
        at = time.monotonic()
        result = subprocess.run([sys.executable, "-B", *args], cwd=HERE, capture_output=True, text=True,
                                env=env, timeout=55)
        (WORK / (label + ".stdout")).write_text(result.stdout)
        (WORK / (label + ".stderr")).write_text(result.stderr)
        require(result.returncode == 0, "incomplete or failed child: " + label + ": " + result.stdout + result.stderr)
        output = json.loads(result.stdout)
        if label == "producer":
            require(regenerated.read_bytes() == (HERE / "certificate.json").read_bytes(), "certificate byte mismatch")
        if label != "optimized_controls":
            for name in ("input_blocks_sha256", "certificate_sha256", "sharp_prefixes", "upper_family_size",
                         "witness_words", "witness_words_sha256", "hub_pair_profile_k_counts",
                         "residual_candidate_min", "residual_candidate_max", "conflict_group_counts"):
                require(output[name] == expected[name], "finite result mismatch: " + label + ": " + name)
        else:
            require(len(output["rejected_corruptions"]) == expected["rejected_controls"] and
                    len(output["genuine_incomplete"]) == expected["actual_incomplete_controls"] and
                    output["positive_color_cases"] == 142 and output["literal_witness_words"] == 59 and
                    output["complete_small_censuses"] == 5, "control coverage mismatch")
        children.append({"stage": label, "seconds": time.monotonic() - at, "maxrss_kib": output["maxrss_kib"]})
    require(not (WORK / "unfinished_case.json").exists(), "unfinished mathematical case remains")
    report = {"agent": "six-code-3", "role": "researcher", "status": "COMPLETE cold reproduction",
              "python": sys.version, "children": children, "seconds": time.monotonic() - started,
              "certificate_sha256": expected["certificate_sha256"],
              "parent_maxrss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              "all_threads_one": True, "one_intensive_child_at_a_time": True,
              "guard_control_file_is_not_a_mathematical_exclusion": True}
    (WORK / "reproduction.json").write_bytes(encoded(report))
    print(json.dumps(report, sort_keys=True))
    return report


if __name__ == "__main__":
    run()
