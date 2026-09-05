import subprocess
import os
from config import PRICING_TIERS

def get_pdf_price(pdf_path: str) -> float:
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    try:
        result = subprocess.run(
            ["pdfinfo", pdf_path],
            capture_output=True,
            text=True,
            check=True
        )
        for line in result.stdout.splitlines():
            if line.startswith("Pages:"):
                pages = int(line.split(":")[1].strip())
                break
        else:
            pages = 1
    except Exception:
        pages = 1

    # Determine price based on config tiers
    for max_pages, price in PRICING_TIERS:
        if pages <= max_pages:
            return price
    return PRICING_TIERS[-1][1]  # fallback
