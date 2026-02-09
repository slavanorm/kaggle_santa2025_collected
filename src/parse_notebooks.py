import json
import csv
import re
from pathlib import Path

def parse_notebook(path: Path) -> dict:
    ipynb = list(path.glob("*.ipynb"))
    if not ipynb:
        return {}

    content = ipynb[0].read_text()
    if not content.strip():
        return {}

    try:
        nb = json.loads(content)
    except json.JSONDecodeError:
        return {}
    cells = nb.get("cells", [])

    code = []
    for cell in cells:
        if cell.get("cell_type") == "code":
            source = cell.get("source", [])
            if isinstance(source, list):
                code.extend(source)
            else:
                code.append(source)

    text = "\n".join(code)
    lines = [l for l in text.split("\n") if l.strip() and not l.strip().startswith("#")]
    sloc = len(lines)

    imports = set()
    for match in re.findall(r"(?:from|import)\s+([a-zA-Z_][a-zA-Z0-9_]*)", text):
        imports.add(match.lower())

    common = {"numpy", "pandas", "matplotlib", "shapely", "numba", "scipy",
              "torch", "tensorflow", "jax", "polars", "cv2", "PIL", "sklearn",
              "pygad", "ortools", "cython", "pyomo", "multiprocessing", "joblib"}
    import_tags = sorted(imports & common)

    approaches = []
    lower = text.lower()
    if "simulated_annealing" in lower or "temperature" in lower and "cooling" in lower:
        approaches.append("SA")
    if "sparrow" in lower:
        approaches.append("Sparrow")
    if "genetic" in lower or "mutation" in lower and "crossover" in lower:
        approaches.append("GA")
    if "translation" in lower and ("dx" in lower or "dy" in lower):
        approaches.append("Translation")
    if "ensemble" in lower or "blend" in lower:
        approaches.append("Ensemble")
    if "gravity" in lower or "physics" in lower or "force" in lower:
        approaches.append("Physics")
    if "reinforcement" in lower or "ppo " in lower or " rl " in lower or "rl_" in lower:
        approaches.append("RL")
    if "greedy" in lower:
        approaches.append("Greedy")

    is_fork = "fork" in ipynb[0].stem.lower() or "fork" in text.lower()[:500]

    has_optimizer = any(x in lower for x in ["optimize", "minimize", "anneal", "iteration", "temperature"])
    is_analysis = any(x in lower for x in ["visualiz", "plot", "matplotlib", "fig,", "ax."]) and not has_optimizer
    is_solution = "submission" in lower or "to_csv" in lower
    is_ensemble = "ensemble" in lower or "blend" in lower or "merge" in lower

    parent_ref = ""
    fork_match = re.search(r"fork[- ]of[- ]([a-z0-9-]+)", ipynb[0].stem.lower())
    if fork_match:
        parent_ref = fork_match.group(1)

    return dict(
        sloc=sloc,
        import_tags=";".join(import_tags),
        approach_tags=";".join(approaches),
        is_fork=is_fork,
        parent_ref=parent_ref,
        has_optimizer=has_optimizer,
        is_analysis=is_analysis,
        is_solution=is_solution,
        is_ensemble=is_ensemble
    )

def main():
    base = Path("downloaded")
    api_data = {}

    with open("/tmp/notebooks_api.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            api_data[row["ref"]] = row

    fields = ["ref", "author", "title", "votes", "language", "has_gpu", "has_tpu",
              "approach_tags", "import_tags", "sloc", "is_fork", "parent_ref",
              "has_optimizer", "is_analysis", "is_solution", "is_ensemble",
              "url", "local_path"]

    with open("notebooks.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()

        for ref, row in api_data.items():
            slug = ref.replace("/", "_")
            path = base / slug

            parsed = parse_notebook(path) if path.exists() else {}

            out = dict(
                ref=ref,
                author=row["author"],
                title=row["title"],
                votes=row["votes"],
                language=row["language"],
                has_gpu=row["has_gpu"],
                has_tpu=row["has_tpu"],
                approach_tags=parsed.get("approach_tags", ""),
                import_tags=parsed.get("import_tags", ""),
                sloc=parsed.get("sloc", 0),
                is_fork=parsed.get("is_fork", False),
                parent_ref=parsed.get("parent_ref", ""),
                has_optimizer=parsed.get("has_optimizer", False),
                is_analysis=parsed.get("is_analysis", False),
                is_solution=parsed.get("is_solution", False),
                is_ensemble=parsed.get("is_ensemble", False),
                url=row["url"],
                local_path=row["local_path"]
            )
            writer.writerow(out)

    print("Done. notebooks.csv updated")

main()
