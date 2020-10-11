from flask import Flask 
from flask import jsonify, request
from flask_restful import Api, Resource
from iplPredictor import predictor
  
app = Flask(__name__) 
api = Api(app)
@app.route("/predict", methods=['POST'])
def predict():
    #posted_data = request.args.get()
    team_one = request.args.get('team1')
    team_two = request.args.get('team2')
    prd= predictor(team_one,team_two)
    return(prd)



if __name__ == '__main__':
    app.run(debug=True)
