import csv
import time
from app.pipeline import run_pipeline
INPUT_FILE = "data/final_eval.csv"
OUTPUT_FILE = "results/evaluation_results.csv"
def run_evaluation():
    results = []
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            start = time.time()

            # Run your full pipeline
            output = run_pipeline(row["prompt"])

            latency = int((time.time() - start) * 1000)
            # amended the orevious is commneted 
            # expected_ent = clean_row.get("expected_entities")
            # if expected_ent is None:
            #     expected_ent = clean_row.get("expected_entity", "")

            # results.append({
            #     "id": clean_row.get("id", "unknown"),
            #     "prompt": clean_row.get("prompt", ""),
            #     "language": clean_row.get("language", "en"),
            #     "attack_type": clean_row.get("attack_type", "NONE"),
            #     "has_pii": clean_row.get("has_pii", "0"),
            #     "expected_policy": clean_row.get("expected_policy", "ALLOW"),
            #     "actual_policy": output.get("decision", "ALLOW"),
            #     "rule_score": output.get("rule_score", 0.0),
            #     "semantic_score": output.get("semantic_score", 0.0),
            #     "final_risk": output.get("final_risk", 0.0),
            #     "latency_ms": latency,
            #     "expected_entities": expected_ent, # Logs perfectly now!
            #     "source": clean_row.get("source", "manual")
            # })

            results.append({
                "id": row["id"],
                "prompt": row["prompt"],
                "language": row["language"],
                "attack_type": row["attack_type"],
                "has_pii": row["has_pii"],
                "expected_policy": row["expected_policy"],
                "actual_policy": output["decision"],
                "rule_score": output["rule_score"],
                "semantic_score": output["semantic_score"],
                "final_risk": output["final_risk"],
                "latency_ms": latency,
                "expected_entities": row["expected_entities"],
                "source": row["source"]
            })

    # Save results
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print(f"Evaluation complete. Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    run_evaluation()