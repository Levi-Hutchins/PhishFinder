import onnx
import logging

import onnxruntime as rt
import numpy as np
from scripts.config.paths_config import MODEL_PATH

logger = logging.getLogger("Link-ML-Service")

def make_prediction(predict_me):
    try:

        session = rt.InferenceSession(MODEL_PATH)

        input_data_np = np.array([predict_me], dtype=np.float32)

        input_name = session.get_inputs()[0].name

        input_dict = {input_name: input_data_np}

        output = session.run(None, input_dict)
    except Exception as e:
        print(e)
        logger.error("An error occurred while making a prediction: ", str(predict_me))
        return 500

    predicted_output = output[0]
    logger.info(f"Successful Prediction")
    return predicted_output

