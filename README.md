# **ColorSync - Style Made Easy**

![Project Banner](https://www.hongkongda.com/wp-content/uploads/2024/05/aim_18741_1.jpg) 

**ColorSync** is a web application that helps users discover personalized fashion and style recommendations based on their uploaded images. By analyzing features like skin tone, hair color, and eye color, ColorSync provides tailored feedback and shopping suggestions to enhance your style.

---

## **Features**

- **Image Upload**: Upload an image to analyze your features.
- **Personalized Feedback**: Get feedback on your style based on the uploaded image.
- **Shopping Recommendations**: Receive curated product recommendations tailored to your features.
- **Camera Integration**: Capture an image directly using your device's camera.
- **Responsive Design**: Works seamlessly on both desktop and mobile devices.

---

## **Future Enhancements**

- **Advanced Recommendation Engine**: Integrate RAG (Retrieval-Augmented Generation) models to provide more precise and context-aware product recommendations.

- **Virtual Try-On**: Add Augmented Reality (AR) support to let users virtually try on recommended clothing and accessories.

- **Seasonal Trends**: Incorporate real-time fashion trend data to offer recommendations aligned with the latest styles and seasons.

- **E-Commerce Integration**: Partner with online stores to provide direct purchase links for recommended products.

- **Multi-Language Support**: Expand the app’s accessibility by adding support for multiple languages.

---

## **Technologies Used**

- **Frontend**:
  - HTML, CSS, JavaScript
  - [Font Awesome](https://fontawesome.com/) for icons
- **Backend**:
  - Python (Flask)
  - OpenCV for image processing
  - OpenAI API for generating recommendations
  - Cosine_similarity for product recommendations
- **Other Tools**:
  - Git for version control
  - JSON for data exchange

---

## **Installation**

Follow these steps to set up the project locally:

### **Prerequisites**
- Python 3.x
- Flask
- OpenCV
- OpenAI API key

### **Steps**

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/ColorSync.git
   cd ColorSync
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   Create a `.env` file in the root directory and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

5. **Run the Application**:
   ```bash
   python app.py
   ```

6. **Access the Application**:
   Open your browser and navigate to `http://localhost:8080`.

---

## **Usage**

1. **Upload an Image**:
   - Click on **Choose File** to upload an image or use the **Open Camera** button to capture one.
   - Click **Let's Style** to process the image.

2. **View Feedback**:
   - After processing, the **Feedback** section will display personalized style recommendations.

3. **Explore Shopping Suggestions**:
   - The **Shopping** section will show curated product recommendations based on your features.

4. **Clear and Reset**:
   - Use the **Clear** button to reset the application and upload a new image.

---

## **Project Structure**

```
ColorSync/
├── app.py                  # Flask application entry point
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── views/                  # HTML templates
│   └── index.html
├── data/                   # csv data
│   └── fashion_catalog.csv
├── featureextractor/       # Feature extraction module
│   └── featureExtraction.py
├── agents/                 # AI agent module
│   └── agent.py
├── graph/                  # Graph builder module
│   └── graph_builder.py
├── recommender/            # Product recommender module
│   └── product_recommender.py
└── prompts/                # Prompt files for AI
    ├── plan_prompt.txt
    ├── expert_prompt.txt
    └── recommender_prompt.txt
```

---

## **Contributing**

I welcome contributions! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeatureName`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeatureName`).
5. Open a pull request.

---

## **License**

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## **Acknowledgments**

- **OpenCV** for image processing capabilities.
- **OpenAI** for providing the API for generating recommendations.
- **Font Awesome** for the icons used in the project.
- **ChatGpt** for structuring UI code.
- **DeepSeek** for general code fixing.

---

## **Contact**

For questions or feedback, feel free to reach out:

- **Email**: uswamy@hawk.iit.edu
- **GitHub**: [udaykumarswamy](https://github.com/udaykumarswamy)
- **Project Link**: [https://github.com/your-udaykumarswamy/ColorSyncAI](https://github.com/udaykumarswamy/ColorSyncAI)

---

Enjoy using **ColorSyncAI**! 🎉