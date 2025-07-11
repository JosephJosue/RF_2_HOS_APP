from pathlib import Path

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "assets"

def relative_to_assets(frame_name: str, path: str) -> Path:
    return ASSETS_PATH / frame_name / Path(path)
