import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from src.pipeline.predict_pipeline import CustomData, Prediction

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def health_check():
    return jsonify({
        "status": "ok",
        "service": "HydraSense ML"
    }), 200


# Support both the new frontend direct endpoint (/predict) and existing Express endpoint (/predictData)
@app.route("/predict", methods=["POST"])
@app.route("/predictData", methods=["POST"])
def prediction():
    try:
        json_data = request.get_json(silent=True)
        if not isinstance(json_data, dict):
            return jsonify({"error": "Expected a JSON object"}), 400

        required_fields = [
            "age",
            "gender",
            "weight",
            "daily_water_intake",
            "physical_activity_level",
            "weather",
        ]
        missing_fields = [
            field for field in required_fields if field not in json_data or json_data[field] in (None, "")
        ]
        if missing_fields:
            return jsonify({
                "error": "Missing required fields",
                "fields": missing_fields
            }), 400

        try:
            age = int(float(json_data.get("age")))
            weight = int(float(json_data.get("weight")))
            daily_water_intake = float(json_data.get("daily_water_intake"))
        except (ValueError, TypeError):
            return jsonify({"error": "Invalid numeric value for age, weight, or daily_water_intake"}), 400

        custom_data_obj = CustomData(
            age=age,
            gender=str(json_data.get("gender")),
            weight=weight,
            daily_water_intake=daily_water_intake,
            physical_activity_level=str(json_data.get("physical_activity_level")),
            weather=str(json_data.get("weather")),
        )

        user_data_dataframe = custom_data_obj.get_data_dataframe()

        prediction_obj = Prediction()
        model_prediction = prediction_obj.predict(user_data_dataframe)

        return jsonify({
            "model_prediction": model_prediction
        }), 200
    except Exception as e:
        app.logger.exception("Prediction failed")
        return jsonify({
            "error": "Prediction failed due to a server error",
            "details": str(e)
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    print(f"Flask App running on port: {port}")
    app.run(host="0.0.0.0", port=port, debug=False)