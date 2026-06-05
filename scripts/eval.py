import argparse
from pathlib import Path

import numpy as np
from PIL import Image


def compute_psnr(img1, img2):
    mse = np.mean((img1 - img2) ** 2)

    if mse == 0:
        return float("inf")

    return 20 * np.log10(255.0 / np.sqrt(mse))


def evaluate(pred_dir, gt_dir):
    pred_dir = Path(pred_dir)
    gt_dir = Path(gt_dir)

    scores = []

    for pred_file in pred_dir.iterdir():
        if not pred_file.is_file():
            continue

        gt_file = gt_dir / pred_file.name

        if not gt_file.exists():
            continue

        pred = np.array(Image.open(pred_file).convert("RGB")).astype(np.float32)
        gt = np.array(Image.open(gt_file).convert("RGB")).astype(np.float32)

        scores.append(compute_psnr(pred, gt))

    if not scores:
        print("No matching image pairs found.")
        return

    print(f"Average PSNR: {np.mean(scores):.2f} dB")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--pred_dir", required=True)
    parser.add_argument("--gt_dir", required=True)

    args = parser.parse_args()

    evaluate(args.pred_dir, args.gt_dir)