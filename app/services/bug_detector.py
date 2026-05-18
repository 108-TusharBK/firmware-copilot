def detect_bugs(code: str):
    bugs = []

    # Detect infinite loop waiting on a flag
    if "while(flag == 0)" in code or "while (flag == 0)" in code:
        bugs.append({
            "issue": "Possible missing volatile keyword",
            "severity": "High",
            "description": (
                "If 'flag' is modified inside an interrupt, it should be declared volatile."
            )
        })

    # Detect strcpy usage
    if "strcpy(" in code:
        bugs.append({
            "issue": "Unsafe string copy",
            "severity": "Medium",
            "description": "strcpy can overflow buffers. Consider strncpy or snprintf."
        })

    # Detect malloc usage
    if "malloc(" in code:
        bugs.append({
            "issue": "Dynamic memory allocation",
            "severity": "Medium",
            "description": (
                "Dynamic allocation may cause fragmentation in embedded systems."
            )
        })

    return bugs