from pathlib import Path


class Paths:
    """
    Path resolution class for project directories.
    
    Provides computed properties for accessing various project directories
    relative to the project root.
    """

    def __init__(self, root_dir: Path):
        """
        Initialize Paths with a root directory.
        
        Args:
            root_dir: Absolute path to the project root directory.
        """
        self._root_dir = root_dir

    @property
    def root_dir(self) -> Path:
        """
        Returns the absolute path to the project root directory.
        """
        return self._root_dir

    @property
    def data_dir(self) -> Path:
        """
        Path to the top-level data directory.
        """
        return self.root_dir / "data"

    @property
    def raw_data_dir(self) -> Path:
        """
        Path to the directory containing original/raw datasets.
        """
        return self.data_dir / "raw"

    @property
    def processed_data_dir(self) -> Path:
        """
        Path to the directory containing preprocessed datasets.
        """
        return self.data_dir / "processed"

    @property
    def models_prod_dir(self) -> Path:
        """
        Path to the directory containing production-ready models.
        """
        return self.root_dir / "models" / "prod"

    @property
    def models_staging_dir(self) -> Path:
        """
        Path to the directory for models in staging/experimentation.
        """
        return self.root_dir / "models" / "staging"

    @property
    def assets_dir(self) -> Path:
        """
        Path to the assets directory (e.g., for mappings, configs, vocab).
        """
        return self.root_dir / "src" / "assets"


def get_project_paths() -> Paths:
    """
    Factory function to create Paths instance with project root.
    """
    root_dir = Path(__file__).parent.parent.parent
    return Paths(root_dir)

