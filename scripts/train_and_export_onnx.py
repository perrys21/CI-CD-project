from pathlib import Path

from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression


def main() -> None:
    output_dir = Path("artifacts")
    output_dir.mkdir(parents=True, exist_ok=True)

    iris = load_iris()
    model = LogisticRegression(max_iter=500)
    model.fit(iris.data, iris.target)

    initial_type = [("float_input", FloatTensorType([None, iris.data.shape[1]]))]
    onnx_model = convert_sklearn(model, initial_types=initial_type, target_opset=17)

    model_path = output_dir / "iris_logreg.onnx"
    model_path.write_bytes(onnx_model.SerializeToString())

    metadata_path = output_dir / "model_metadata.txt"
    metadata_path.write_text(
        "\n".join(
            [
                "model_name=iris_logreg",
                "framework=scikit-learn",
                "format=onnx",
                f"feature_count={iris.data.shape[1]}",
                f"class_count={len(iris.target_names)}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    print(f"Saved ONNX model to: {model_path}")
    print(f"Saved metadata to: {metadata_path}")


if __name__ == "__main__":
    main()
