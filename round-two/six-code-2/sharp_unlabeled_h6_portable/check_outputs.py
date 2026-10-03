"""Stdlib whole-record checker, importing no mathematical producer or audit.

Physical complete-carrier/graph/point checks are separate preceding children.
Every generated carrier, row, color, witness, map and link packet is compared
whole, not by its scalar counts. Raw execution bindings are verified before
only their dependent hashes are excluded from the mathematical record.
"""
import argparse
import hashlib
import json
from pathlib import Path
import resource
import time
from operations import check_operations


def need(ok, message):
    if not ok:
        raise ValueError(message)


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def read(path):
    return json.loads(path.read_bytes())


def pin(path):
    raw = path.read_bytes()
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--work", type=Path, required=True)
    args = parser.parse_args()
    need(not args.work.exists(), "fresh whole-record output")
    args.work.mkdir(parents=True)
    begin = time.monotonic()
    expected = read(args.source / "EXPECTED.json")
    spec = read(args.source / "SPEC.json")
    case_records = []
    actual_audit_pins = {}
    for configuration, prior in zip(spec["cases"], expected["cases"]):
        check_operations()
        key = configuration["key"]
        need(key == prior["key"], "entire configured case order")
        root = args.root / key
        need(not (root / "carrier/PARTIAL.json").exists() and not (root / "graph/PARTIAL.json").exists() and
             not (root / "graph/POSITIVE_STOP.json").exists(), "complete scopes only")
        packets = {}
        for name, proposed in prior["packets"].items():
            packets[name] = pin(root / name)
            need(packets[name] == proposed, "entire regenerated packet differs: " + key + "/" + name)
        summaries = {}
        for stage in ("carrier", "graph", "colors"):
            summary = read(root / stage / "SUMMARY.json")
            need({"seconds", "peak_RSS_kib"} <= set(summary), "exact runtime summary schema")
            summaries[stage] = {k:v for k,v in summary.items() if k not in ("seconds", "peak_RSS_kib")}
        need(summaries == prior["summaries"], "entire regenerated mathematical summaries")
        point_path = root / "point-audit/EXACT_RESULT.json"
        body = read(point_path)
        need(body.pop("producer_summary_sha256") == pin(root / "graph/SUMMARY.json")["sha256"], "actual raw-summary binding before normalization")
        need(body == prior["body_math"], "entire independent physical mathematical record")
        actual_audit_pins[tuple(configuration["extras"])] = pin(point_path)["sha256"]
        point = read(root / "point-cover-audit/EXACT_RESULT.json")
        need(point.pop("known_seed_inventory_sha256") == pin(args.source / "SEED_PAIRS.json")["sha256"], "compact literal seed-list binding")
        need(point == prior["physical_point_cover"], "whole independent physical point-map record")
        case_records.append({"key": key, "packets": packets, "summaries": summaries, "body_math": body, "physical_point_cover": point})
    need(len(case_records) == len(spec["cases"]) == len(expected["cases"]) == 4, "entire four-case domain")
    labels = read(args.root / "labels/EXACT_RESULT.json")
    label_cases = labels.pop("cases")
    for case in label_cases:
        need(case.pop("complete_physical_audit_sha256") == actual_audit_pins[tuple(case["extra_pair"])], "label raw-audit binding")
    need(label_cases == [c["label_case"] for c in expected["cases"]], "whole physical label case records")
    need(labels.pop("state_units") == expected["label_states"], "entire label state units")
    packet = pin(args.root / "labels/CERTIFICATES.json")
    need(packet == expected["labels_packet"] and
         labels.pop("certificate_bytes") == packet["bytes"] and labels.pop("certificate_sha256") == packet["sha256"], "entire regenerated label packet")
    need(labels == expected["label_shared"], "entire shared label result fields")
    links = read(args.root / "links/EXACT_RESULT.json")
    for case in links["cases"]:
        need(case.pop("physical_audit_sha256") == actual_audit_pins[tuple(case["extra_pair"])], "link raw-audit binding")
    need(links == expected["links_math"], "entire sharp-link mathematical result")
    need(pin(args.root / "links/CERTIFICATES.json") == expected["links_packet"], "entire regenerated sharp-link packet")
    domain = read(args.root / "domain/EXACT_RESULT.json")
    need(domain == expected["domain"], "entire union-domain result")
    need(pin(args.root / "domain/FULL_DOMAIN.json") == {"bytes":domain["combined_domain_bytes"],"sha256":domain["combined_target_domain_sha256"]}, "whole40800-boundary domain packet")
    exact = {"agent":"six-code-2", "role":"researcher", "status":"COMPLETE_SOURCE_ONLY_SHARP_UNLABELED_PROFILES_FOUR_FAMILIES", "cases":case_records,
             "labels":{"shared":labels,"cases":label_cases,"packet":packet,"state_units":expected["label_states"]},
             "links":links,"links_packet":expected["links_packet"],"domain":domain,
             "private_generated_inputs":[],"ordinary_bridges_formalized":False,"independent_person_review":"pending","all_h6_or_global_endpoint_claim":False}
    check_operations()
    need(time.monotonic() - begin < 60, "INCOMPLETE original whole-record check guard")
    raw = encoded(exact)
    (args.work / "EXACT_RESULT.json").write_bytes(raw)
    execution = {"seconds":time.monotonic()-begin,"peak_RSS_kib":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,"exact_bytes":len(raw),"exact_sha256":hashlib.sha256(raw).hexdigest(),"original_math_seconds":60}
    (args.work / "EXECUTION.json").write_bytes(encoded(execution))
    print(json.dumps(execution,sort_keys=True),flush=True)


if __name__ == "__main__":
    main()
