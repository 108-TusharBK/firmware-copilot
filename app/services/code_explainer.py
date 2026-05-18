def explain_code(code: str):
    lines = code.splitlines()
    explanations = []

    for i, line in enumerate(lines, start=1):
        stripped = line.strip()

        if not stripped:
            continue

        explanations.append({
            "line": i,
            "code": stripped,
            "explanation": f"This line contains: {stripped}"
        })

    return explanations
