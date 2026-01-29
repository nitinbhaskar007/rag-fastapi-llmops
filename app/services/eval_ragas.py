from typing import List, Dict, Any

def run_ragas_eval(samples: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    samples: [{ "question": str, "answer": str, "contexts": [str], "ground_truth": str(optional) }]
    """
    try:
        import pandas as pd
        from ragas import evaluate
        from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
        from datasets import Dataset
    except Exception as e:
        return {"ok": False, "error": f"RAGAS not available: {e}"}

    ds = Dataset.from_dict({
        "question": [s["question"] for s in samples],
        "answer": [s["answer"] for s in samples],
        "contexts": [s["contexts"] for s in samples],
        "ground_truth": [s.get("ground_truth", "") for s in samples],
    })

    result = evaluate(ds, metrics=[faithfulness, answer_relevancy, context_precision, context_recall])
    return {"ok": True, "metrics": dict(result)}
