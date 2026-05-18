from fastapi import APIRouter, UploadFile, File, HTTPException
import os
from pathlib import Path
import tempfile

from app.services.code_explainer import explain_code
from app.services.bug_detector import detect_bugs
from app.services.repo_analyzer import analyze_repository
from app.services.ai_explainer import explain_with_ai

router = APIRouter()


def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent path traversal attacks."""
    # Get just the basename to prevent directory traversal
    safe_name = os.path.basename(filename)
    # Remove any remaining dangerous characters
    safe_name = "".join(c for c in safe_name if c.isalnum() or c in "._-")
    if not safe_name:
        raise ValueError("Invalid filename")
    return safe_name


@router.post("/analyze")
async def analyze_code(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")
    
    try:
        # Sanitize filename to prevent path traversal
        safe_filename = sanitize_filename(file.filename)
        
        # Use temporary directory for better cleanup
        os.makedirs("uploads", exist_ok=True)
        file_path = os.path.join("uploads", safe_filename)

        # Read file content
        content = await file.read()

        # Save file temporarily
        with open(file_path, "wb") as f:
            f.write(content)

        try:
            # Decode content
            code = content.decode("utf-8", errors="ignore")

            # Perform analysis
            explanations = explain_code(code)
            bugs = detect_bugs(code)
            summary = analyze_repository(code)
            ai_explanation = explain_with_ai(code)

            return {
                "filename": file.filename,
                "line_count": len(code.splitlines()),
                "summary": summary,
                "explanations": explanations,
                "bugs": bugs,
                "ai_explanation": ai_explanation
            }
        finally:
            # Clean up uploaded file
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception:
                    pass  # Best effort cleanup
                    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")