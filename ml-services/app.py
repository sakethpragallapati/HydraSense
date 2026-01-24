import os
from flask import Flask,jsonify,request
from flask_cors import CORS
from src.pipeline.predict_pipeline import CustomData,Prediction

app = Flask(__name__)
CORS(app)

@app.route('/predictData',methods=['POST'])
def prediction():

    try:
        json_data = request.get_json()

        custom_data_obj = CustomData(
            age = json_data.get("age"),
            gender = json_data.get("gender"),
            weight = json_data.get("weight"),
            daily_water_intake = json_data.get("daily_water_intake"),
            physical_activity_level = json_data.get("physical_activity_level"),
            weather = json_data.get("weather"),
        )

        user_data_dataframe = custom_data_obj.get_data_dataframe()

        prediction_obj = Prediction()
        model_prediction = prediction_obj.predict(user_data_dataframe)

        return jsonify({
            "model_prediction" : model_prediction
        })
    except Exception as e:
        print(f"Error occurred during prediction: {e}") 
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    print(f"Flask App running on port: {port}")
    app.run(host='0.0.0.0', port=port, debug=True)