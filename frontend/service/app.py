from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_restplus import Api, Resource, fields
from sklearn.externals import joblib
from sampleParser import parseInput, makeSample
import tensorflow as tf
from tensorflow import keras
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from blitz.modules import BayesianLinear
np.random.seed(171)

flask_app = Flask(__name__)
app = Api(app = flask_app, 
		  version = "1.0", 
		  title = "ConductorML", 
		  description = "Predict critical temperature of a superconductor")

CORS(flask_app)

name_space = app.namespace('prediction', description='Prediction APIs')

model = app.model('Prediction params', 
				  {'formula': fields.String(required = True, 
				  							   description="Chemical formula of superconductor",
    					  				 	   help="Text Field 1 cannot be blank")
					}
				)

class BayesianRegressor(nn.Module):
    def __init__(self, input_dim, output_dim):
        super().__init__()
        #self.linear = nn.Linear(input_dim, output_dim)
        #2 layers only
        self.blinear1 = BayesianLinear(input_dim, 100) #100 is effectively hyperparam-- size of only hidden layer
        self.blinear2 = BayesianLinear(100, output_dim)
        
    def forward(self, x):
        x_ = self.blinear1(x)
        return self.blinear2(x_)

# Load ML model
# prediction_model_keras = keras.models.load_model('test_model')
prediction_model = BayesianRegressor(81, 1)
optimizer = optim.Adam(prediction_model.parameters(), lr=0.001)

checkpoint = torch.load('regressor_checkpoint.tar')
prediction_model.load_state_dict(checkpoint['regressor_state_dict'])
optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
epoch = checkpoint['epoch']

prediction_model.eval()

@name_space.route("/")
class MainClass(Resource):

	def options(self):
		response = make_response()
		response.headers.add("Access-Control-Allow-Origin", "*")
		response.headers.add('Access-Control-Allow-Headers', "*")
		response.headers.add('Access-Control-Allow-Methods', "*")
		return response

	@app.expect(model)		
	def post(self):
		try:
			# Take input and pass into model
			formData = request.json
			data = [val for val in formData.values()]
			formula = data[0]
			parsed_formula = parseInput(formula)
			sample = makeSample(parsed_formula)
			tensor_sample = torch.FloatTensor(sample)
			output = prediction_model(tensor_sample)
			result = output.detach().numpy()
			response = jsonify({
				"statusCode": 200,
				"status": "Prediction made",
				"result": "Predicted critical temperature: " + str(result[0]) + " K"
				})
			response.headers.add('Access-Control-Allow-Origin', '*')
			return response
		except Exception as error:
			return jsonify({
				"statusCode": 500,
				"status": "Could not make prediction",
				"error": str(error)
			})