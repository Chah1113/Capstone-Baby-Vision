"""
논문용 YOLOv8 성능 벤치마크 스크립트

사용법:
  # 모델 품질 + 속도 (data.yaml 있을 때)
  python benchmark.py --model weights/best.pt --data data.yaml

  # 속도만 (이미지 폴더로)
  python benchmark.py --model weights/best.pt --images path/to/images/

  # 전체 옵션
  python benchmark.py --model weights/best.pt --data data.yaml --images path/to/images/ \
                      --conf 0.5 --imgsz 640 --n 100 --out results/
"""

import argparse
import csv
import json
import os
import time
from datetime import datetime
from pathlib import Path

import numpy as np
from ultralytics import YOLO


# ──────────────────────────────────────────────
# 출력 헬퍼
# ──────────────────────────────────────────────

def _hr(char="─", width=60):
    print(char * width)

def _table(headers: list[str], rows: list[list], col_width: int = 14):
    sep = "┼".join("─" * col_width for _ in headers)
    top = "┌" + "┬".join("─" * col_width for _ in headers) + "┐"
    mid = "├" + sep + "┤"
    bot = "└" + "┴".join("─" * col_width for _ in headers) + "┘"

    def fmt_row(cells, left="│", right="│"):
        return left + right.join(str(c).center(col_width) for c in cells) + right

    print(top)
    print(fmt_row(headers))
    print(mid)
    for row in rows:
        print(fmt_row(row))
    print(bot)


# ──────────────────────────────────────────────
# 1단계: 모델 품질 지표 (yolo val)
# ──────────────────────────────────────────────

def run_val(model: YOLO, data: str, conf: float, imgsz: int) -> dict:
    print("\n[1/2] Model Quality — yolo val")
    _hr()
    val = model.val(data=data, conf=conf, imgsz=imgsz, verbose=False)

    rd = val.results_dict
    class_names = list(model.names.values())

    # 전체(all) 지표
    metrics = {
        "all": {
            "precision": round(rd.get("metrics/precision(B)", 0), 4),
            "recall":    round(rd.get("metrics/recall(B)", 0), 4),
            "mAP50":     round(rd.get("metrics/mAP50(B)", 0), 4),
            "mAP50_95":  round(rd.get("metrics/mAP50-95(B)", 0), 4),
        }
    }

    # 클래스별 지표
    if hasattr(val, "ap_class_index") and val.ap_class_index is not None:
        for i, cls_idx in enumerate(val.ap_class_index):
            cls_name = model.names.get(int(cls_idx), f"class_{cls_idx}")
            metrics[cls_name] = {
                "precision": round(float(val.box.p[i]) if hasattr(val.box, "p") else 0, 4),
                "recall":    round(float(val.box.r[i]) if hasattr(val.box, "r") else 0, 4),
                "mAP50":     round(float(val.box.ap50[i]) if hasattr(val.box, "ap50") else 0, 4),
                "mAP50_95":  round(float(val.box.ap[i]) if hasattr(val.box, "ap") else 0, 4),
            }

    # 테이블 출력
    headers = ["Class", "Precision", "Recall", "mAP@0.5", "mAP@0.5:0.95"]
    rows = []
    for cls, m in metrics.items():
        rows.append([cls, m["precision"], m["recall"], m["mAP50"], m["mAP50_95"]])
    _table(headers, rows, col_width=14)

    return metrics


# ──────────────────────────────────────────────
# 2단계: 런타임 속도 측정
# ──────────────────────────────────────────────

def _collect_images(data_yaml: str | None, images_dir: str | None, n: int) -> list[Path]:
    """이미지 경로 목록 수집 — data.yaml val split 또는 이미지 폴더."""
    candidates = []

    if images_dir and Path(images_dir).exists():
        exts = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
        candidates = [p for p in Path(images_dir).rglob("*") if p.suffix.lower() in exts]

    elif data_yaml:
        import yaml
        with open(data_yaml) as f:
            cfg = yaml.safe_load(f)
        base = Path(data_yaml).parent
        val_path = base / cfg.get("val", "valid/images")
        if not val_path.exists():
            val_path = base / cfg.get("path", "") / cfg.get("val", "valid/images")
        exts = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
        candidates = [p for p in val_path.rglob("*") if p.suffix.lower() in exts]

    if not candidates:
        raise FileNotFoundError(
            "속도 측정에 사용할 이미지를 찾을 수 없습니다.\n"
            "--images <폴더> 또는 올바른 --data data.yaml을 지정하세요."
        )

    rng = np.random.default_rng(42)
    selected = rng.choice(candidates, size=min(n, len(candidates)), replace=False)
    return list(selected)


def run_speed(model: YOLO, data: str | None, images_dir: str | None,
              conf: float, imgsz: int, n: int) -> dict:
    print(f"\n[2/2] Runtime Speed — {n} images")
    _hr()

    imgs = _collect_images(data, images_dir, n)
    print(f"  측정 대상: {len(imgs)}장")

    pre_list, inf_list, post_list = [], [], []

    # 워밍업 (첫 3장은 제외)
    warmup = imgs[:3]
    for p in warmup:
        model(str(p), conf=conf, imgsz=imgsz, verbose=False)

    for p in imgs:
        res = model(str(p), conf=conf, imgsz=imgsz, verbose=False)
        spd = res[0].speed
        pre_list.append(spd["preprocess"])
        inf_list.append(spd["inference"])
        post_list.append(spd["postprocess"])

    pre  = np.array(pre_list)
    inf  = np.array(inf_list)
    post = np.array(post_list)
    total = pre + inf + post

    fps = 1000.0 / np.mean(total)

    result = {
        "preprocess_mean":  round(float(np.mean(pre)),   2),
        "preprocess_std":   round(float(np.std(pre)),    2),
        "inference_mean":   round(float(np.mean(inf)),   2),
        "inference_std":    round(float(np.std(inf)),    2),
        "postprocess_mean": round(float(np.mean(post)),  2),
        "postprocess_std":  round(float(np.std(post)),   2),
        "total_mean":       round(float(np.mean(total)), 2),
        "total_std":        round(float(np.std(total)),  2),
        "fps":              round(fps, 1),
        "n_images":         len(imgs),
    }

    print(f"  Preprocess : {result['preprocess_mean']:6.1f} ms  (±{result['preprocess_std']:.1f})")
    print(f"  Inference  : {result['inference_mean']:6.1f} ms  (±{result['inference_std']:.1f})")
    print(f"  Postprocess: {result['postprocess_mean']:6.1f} ms  (±{result['postprocess_std']:.1f})")
    print(f"  ─────────────────────────────")
    print(f"  Total      : {result['total_mean']:6.1f} ms  (±{result['total_std']:.1f})")
    print(f"  FPS        : {result['fps']:6.1f}")

    return result


# ──────────────────────────────────────────────
# 3단계: 결과 저장
# ──────────────────────────────────────────────

def save_results(out_dir: str, model_path: str, val_metrics: dict | None,
                 speed: dict | None, config: dict):
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    ts = datetime.now().isoformat(timespec="seconds")

    payload = {
        "model":       model_path,
        "timestamp":   ts,
        "val_metrics": val_metrics,
        "speed_ms":    speed,
        "config":      config,
    }

    json_path = Path(out_dir) / "benchmark_results.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    # CSV (val_metrics 행 + speed 행)
    csv_path = Path(out_dir) / "benchmark_results.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if val_metrics:
            writer.writerow(["[Val Metrics]"])
            writer.writerow(["class", "precision", "recall", "mAP50", "mAP50_95"])
            for cls, m in val_metrics.items():
                writer.writerow([cls, m["precision"], m["recall"], m["mAP50"], m["mAP50_95"]])
            writer.writerow([])

        if speed:
            writer.writerow(["[Speed]"])
            writer.writerow(["preprocess_mean", "inference_mean", "postprocess_mean",
                             "total_mean", "fps", "n_images"])
            writer.writerow([speed["preprocess_mean"], speed["inference_mean"],
                             speed["postprocess_mean"], speed["total_mean"],
                             speed["fps"], speed["n_images"]])

    print(f"\nSaved → {json_path}")
    print(f"Saved → {csv_path}")


# ──────────────────────────────────────────────
# main
# ──────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(description="YOLOv8 논문용 성능 벤치마크")
    p.add_argument("--model",  required=True, help="모델 경로 (예: weights/best.pt)")
    p.add_argument("--data",   default=None,  help="data.yaml 경로 (val 지표 측정용)")
    p.add_argument("--images", default=None,  help="속도 측정용 이미지 폴더")
    p.add_argument("--conf",   type=float, default=0.5,  help="신뢰도 임계값")
    p.add_argument("--imgsz",  type=int,   default=640,  help="입력 이미지 크기")
    p.add_argument("--n",      type=int,   default=100,  help="속도 측정 이미지 수")
    p.add_argument("--out",    default="results", help="결과 저장 폴더")
    return p.parse_args()


def main():
    args = parse_args()

    if not args.data and not args.images:
        print("오류: --data 또는 --images 중 하나는 필요합니다.")
        return

    print("=" * 60)
    print(f"  EyeCatch AI — YOLOv8 Benchmark")
    print(f"  Model : {args.model}")
    print(f"  conf={args.conf}  imgsz={args.imgsz}  n={args.n}")
    print("=" * 60)

    model = YOLO(args.model)

    val_metrics = None
    if args.data:
        val_metrics = run_val(model, args.data, args.conf, args.imgsz)

    speed = None
    if args.data or args.images:
        speed = run_speed(model, args.data, args.images, args.conf, args.imgsz, args.n)

    config = {"conf": args.conf, "imgsz": args.imgsz, "n_images": args.n}
    save_results(args.out, args.model, val_metrics, speed, config)

    print("\n완료.")


if __name__ == "__main__":
    main()
