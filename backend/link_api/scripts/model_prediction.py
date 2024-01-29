import onnx
import onnxruntime as rt
import numpy as np
import scripts.config.paths_config 


def make_prediction(predict_me):
    session = rt.InferenceSession("/Users/levi_1/Desktop/PhishGuard/backend/scripts/onnx/model.onnx")

    input_data_np = np.array([predict_me], dtype=np.float32)

    input_name = session.get_inputs()[0].name

    input_dict = {input_name: input_data_np}

    output = session.run(None, input_dict)

    predicted_output = output[0]
    return predicted_output

