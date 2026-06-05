from pathlib import Path

from PIL import Image
from torch.utils.data import Dataset
import torchvision.transforms as T


class SnowDataset(Dataset):
    """
    Expected structure:

    dataset/
    ├── snowy/
    │   ├── img1.jpg
    │   └── img2.jpg
    └── clean/
        ├── img1.jpg
        └── img2.jpg
    """

    def __init__(self, root_dir, transform=None):
        self.root_dir = Path(root_dir)

        self.snowy_dir = self.root_dir / "snowy"
        self.clean_dir = self.root_dir / "clean"

        self.files = sorted(
            [
                f.name
                for f in self.snowy_dir.iterdir()
                if f.is_file()
            ]
        )

        self.transform = transform or T.ToTensor()

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):
        filename = self.files[idx]

        snowy_img = Image.open(
            self.snowy_dir / filename
        ).convert("RGB")

        clean_img = Image.open(
            self.clean_dir / filename
        ).convert("RGB")

        snowy_img = self.transform(snowy_img)
        clean_img = self.transform(clean_img)

        return {
            "snowy": snowy_img,
            "clean": clean_img,
            "filename": filename,
        }