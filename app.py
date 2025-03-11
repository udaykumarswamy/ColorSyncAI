from flask import Flask, render_template, jsonify, request
import subprocess
import configparser
import cv2
import numpy as np
import base64
from io import BytesIO
from flask_cors import CORS  
import featureextractor.featureExtraction as featureExtraction
from featureextractor import featureExtraction
from agents.agent import Agent
from graph.graph_builder import build_graph
from recommender import product_recommender
import logging
import logging.config

# Read the properties file
config = configparser.ConfigParser()
config.read('config.properties')


logConf = config.get('LogFile', 'logConfiguration')

logging.config.fileConfig(logConf)
logger = logging.getLogger('colorsync')

# Get the template folder path from the properties file
template_folder = config.get('Flask', 'template_folder')

open_api_key = config.get('OPENAI_API_KEY','open_api_key')

app = Flask(__name__, template_folder=template_folder)
CORS(app)


@app.route("/")
def index():
    """
    Renders the index.html template.

    This function is a Flask route that renders the index.html template
    when the root URL ("/") of the application is accessed.

    Returns:
        str: The rendered HTML content of the index.html template.
    """
    logger.info("rendering index.html file")
    return render_template("index.html")


@app.route('/process-image', methods=['POST'])
def process_image():
    try:
        logger.info("Entered process image")
        # Load the prompts from files
        with open("prompts/plan_prompt.txt", "r") as file:
            plan_prompt = file.read()
        logger.debug("Loaded plan_prompt")
            
    
        with open("prompts/expert_prompt.txt", "r") as file:
            expert_prompt = file.read()
        logger.debug("Loaded expert_prompt")
            
        with open("prompts/recommender_prompt.txt", "r") as file:
            recommender_prompt = file.read()
        logger.debug("Loaded recommender_prompt")
        
        # Check if the request contains JSON data
        if not request.is_json:
            return jsonify({"error": "Invalid request. Content-Type must be application/json."}), 400
        
        # Get the JSON data
        data = request.get_json()
        if not data or "image" not in data:
            return jsonify({"error": "Invalid request. 'image' field is missing."}), 400
        
        # Extract the base64 image data
        image_data = data["image"]

        # Decode the base64 image data
        try:
            # Remove the "data:image/png;base64," prefix if present
            if "," in image_data:
                image_data = image_data.split(",")[1]
            logger.debug("Decoding image base64 started")
            # Decode the base64 string to bytes
            img_data = base64.b64decode(image_data)
            np_arr = np.frombuffer(img_data, np.uint8)
            img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            logger.debug("Decoding image base64 completed")
            if img is None:
                logger.error("error:Failed to decode image")
                return jsonify({"error": "Failed to decode image."}), 400
        except Exception as e:
            logger.error(f"Error decoding image: {e}")
            return jsonify({"error": "Invalid image data. (Image Either has no human face or blurry Image or multiple faces), please try with good quality image!"}), 400
        
        # Process the image with OpenCV (example: extracting features)
        color_codes = featureExtraction.extractFeatures(img)
        
        # Check if extractFeatures returned an error
        if isinstance(color_codes, dict) and "error" in color_codes:
            logger.error(color_codes["error"])
            return jsonify({"error": color_codes["error"]}), 400
        # Example input lists
        labels = ["skin color", "hair color", "eye color"]

        # Use list comprehension to populate color_codes
        label_color_codes = [{"label": label, "code": code} for label, code in zip(labels, color_codes)]

        # Create a list of formatted strings for each color code
        formatted_codes = [f'{item["label"]} code: {item["code"]}' for item in label_color_codes]

        # Join the formatted strings with commas
        task_string = ', '.join(formatted_codes)

        # Wrap the result in the desired format
        task = f"'task': \"{task_string}\""
        
        # Initialize the agent
        agent = Agent(open_api_key)
        logger.info("Initialized Agent")
        
        # Build the graph
        graph = build_graph(agent, plan_prompt, expert_prompt, recommender_prompt)
        logger.info("Buit Graph")
    
        # Define the initial state
        initial_state = {
            'task': task,
            "max_revisions": 1,
            "revision_number": 1,
            "content": [],
        }
    
        result = {}

        for s in graph.stream(initial_state):
            if s:
                json_data = dict(s)
                #print(json.dumps(json_data, indent=2))
                result.update(json_data)

        json_data = result  
        logger.info("Final aggregated result generated")
        
        # Safely extract colors
        list_of_colors = json_data.get("extracter", {}).get("draft", "").split(", ")
        logger.debug(f"Extracted colors: {list_of_colors}")
        
        rec_res_list = product_recommender.checkRecommendation(list_of_colors)
        logger.info("Generated product recommendations")
        
        # Return the result as JSON
        return jsonify({"feedback": json_data, 
            "shopping_recommendations": rec_res_list}),200  # HTTP 200 OK
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    logger.info("Starting Flask application")
    app.run(debug=True, port=8080, use_reloader=True)