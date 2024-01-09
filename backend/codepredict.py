import onnx
import onnxruntime as rt
import numpy as np

# TODO: code to make prediction come back when url processiong is complete
session = rt.InferenceSession("model.onnx")

input_data_np = np.array([[73,0,0,0,52,0,5,0,0,0,0,1,0]], dtype=np.float32)

input_name = session.get_inputs()[0].name

input_dict = {input_name: input_data_np}

output = session.run(None, input_dict)

predicted_output = output[0]


print(predicted_output)