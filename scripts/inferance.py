import argparse
import csv
from pathlib import Path

import numpy as np
import onnxruntime as ort
from sklearn.datasets import load_iris


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run inference with the latest exported ONNX model."
    )
    parser.add_argument(
        "--model-dir",
        default="downloaded-model",
        help="Directory containing the ONNX model artifact files.",
    )
    parser.add_argument(
        "--input-csv",
        default="",
        help="Optional CSV path with feature rows (float values).",
    )
    parser.add_argument(
        "--output-dir",
        default="artifacts/inference",
        help="Directory where predictions are written.",
    )
    return parser.parse_args()


def find_model_file(model_dir: Path) -> Path:
    model_files = sorted(model_dir.glob("*.onnx"))
    if not model_files:
        raise FileNotFoundError(f"No ONNX model found in {model_dir}")
    return model_files[0]


def load_features(input_csv: str) -> np.ndarray:
    if input_csv:
        data = np.loadtxt(input_csv, delimiter=",", dtype=np.float32)
        if data.ndim == 1:
            data = data.reshape(1, -1)
        return data

    # Fallback demo data for manual runs without external input.
    iris = load_iris()
    return iris.data[:5].astype(np.float32)


def run_inference(model_path: Path, features: np.ndarray) -> np.ndarray:
    session = ort.InferenceSession(
        model_path.as_posix(),
        providers=["CPUExecutionProvider"],
    )
    input_name = session.get_inputs()[0].name
    outputs = session.run(None, {input_name: features})
    return np.array(outputs[0]).reshape(-1)


def write_predictions(output_dir: Path, predictions: np.ndarray) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "predictions.csv"
    with output_path.open("w", newline="", encoding="utf-8") as file_obj:
        writer = csv.writer(file_obj)
        writer.writerow(["row_index", "prediction"])
        for idx, prediction in enumerate(predictions):
            writer.writerow([idx, int(prediction)])
    return output_path


def main() -> None:
    args = parse_args()

    model_dir = Path(args.model_dir)
    model_path = find_model_file(model_dir)
    features = load_features(args.input_csv)
    predictions = run_inference(model_path, features)
    output_path = write_predictions(Path(args.output_dir), predictions)

    print(f"Loaded model: {model_path}")
    print(f"Input rows: {features.shape[0]}")
    print(f"Predictions saved to: {output_path}")


if __name__ == "__main__":
    main()
