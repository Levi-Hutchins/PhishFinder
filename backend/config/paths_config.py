import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE_DIR, "../../dataset", "dataset.csv")
MODEL_PATH = os.path.join(BASE_DIR, "../onnx", "model.onnx")