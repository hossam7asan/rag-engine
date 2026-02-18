from helpers.config import get_settings, Settings
from pathlib import Path


class BaseController:

    def __init__(self):
        self.app_settings = get_settings()
        self.base_dir = Path(__file__).resolve().parent.parent
        self.files_dir = self.base_dir / "assets" / "files"
