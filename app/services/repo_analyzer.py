def analyze_repository(code: str):
    return {
        "total_lines": len(code.splitlines()),
        "contains_interrupt_handler": "IRQHandler" in code,
        "contains_freertos_task": "xTaskCreate" in code,
        "contains_while_loop": "while" in code,
        "contains_malloc": "malloc(" in code
    }
