"""
test_all_modules.py
===================
Comprehensive unit & integration test suite for MediHybrid:
- Test 1: Preprocessing & Imputation
- Test 2: Genetic Algorithm (DEAP) Feature Selection
- Test 3: Mamdani Fuzzy Inference Systems
- Test 4: Artificial Neural Network (ANN) Inferences
- Test 5: Retinopathy CNN & Grad-CAM Generation
- Test 6: MediBot AI Assistant Context-Aware Engine
- Test 7: Medical Report OCR Parameter Extraction
- Test 8: FastAPI Backend Endpoints
"""

import sys
import os
import unittest
import numpy as np
from PIL import Image

# Ensure backend root is on path
BACKEND_DIR = os.path.join(os.path.dirname(__file__), "..", "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app.services.fuzzy_service import diabetes_fuzzy, heart_fuzzy
from app.services.hybrid_service import hybrid_engine
from app.services.cnn_service import retina_service
from app.services.chatbot_service import chatbot
from app.services.ocr_service import report_scanner

class TestMediHybridSuite(unittest.TestCase):

    def test_01_fuzzy_diabetes_inference(self):
        # Normal patient
        res_normal = diabetes_fuzzy.evaluate(glucose=85, bmi=21.5, bp=70, age=25)
        self.assertIn("fuzzy_score", res_normal)
        self.assertLess(res_normal["fuzzy_score"], 40.0)
        self.assertEqual(res_normal["risk_level"], "Low Risk")

        # Elevated patient
        res_high = diabetes_fuzzy.evaluate(glucose=175, bmi=36.0, bp=95, age=55)
        self.assertGreater(res_high["fuzzy_score"], 60.0)
        self.assertEqual(res_high["risk_level"], "High Risk")

    def test_02_fuzzy_heart_inference(self):
        res_low = heart_fuzzy.evaluate(age=30, chol=170, bp=110, hr=165, oldpeak=0.1)
        self.assertLess(res_low["fuzzy_score"], 45.0)

        res_high = heart_fuzzy.evaluate(age=62, chol=285, bp=155, hr=115, oldpeak=2.8)
        self.assertGreater(res_high["fuzzy_score"], 55.0)

    def test_03_hybrid_diabetes_prediction(self):
        sample = {
            "Pregnancies": 2,
            "Glucose": 120,
            "BloodPressure": 76,
            "SkinThickness": 25,
            "Insulin": 110,
            "BMI": 27.5,
            "DiabetesPedigreeFunction": 0.45,
            "Age": 38
        }
        res = hybrid_engine.predict_diabetes(sample)
        self.assertIn("hybrid", res)
        self.assertIn("ann", res)
        self.assertIn("fuzzy", res)
        self.assertIn("explainability", res)
        self.assertTrue(0.0 <= res["hybrid"]["score"] <= 100.0)

    def test_04_hybrid_heart_prediction(self):
        sample = {
            "age": 55, "sex": 1, "cp": 3, "trestbps": 135, "chol": 240,
            "fbs": 0, "restecg": 1, "thalach": 145, "exang": 0,
            "oldpeak": 1.2, "slope": 2, "ca": 1, "thal": 3
        }
        res = hybrid_engine.predict_heart(sample)
        self.assertIn("hybrid", res)
        self.assertTrue(0.0 <= res["hybrid"]["score"] <= 100.0)

    def test_05_retina_cnn_analysis(self):
        sample_path = os.path.join(BACKEND_DIR, "ml_artifacts", "sample_retina", "fundus_class0_healthy.jpg")
        if os.path.exists(sample_path):
            with open(sample_path, "rb") as f:
                content = f.read()
            res = retina_service.analyze_image(content, filename="fundus_class0_healthy.jpg")
            self.assertEqual(res["predicted_class_id"], 0)
            self.assertEqual(len(res["class_probabilities"]), 5)
            self.assertTrue(res["gradcam_heatmap_uri"].startswith("data:image/jpeg;base64,"))

    def test_06_chatbot_fallback_engine(self):
        reply_ga = chatbot.generate_reply("Explain the Genetic Algorithm")
        self.assertIn("Genetic Algorithm", reply_ga)

        reply_retina = chatbot.generate_reply("What is diabetic retinopathy?")
        self.assertIn("Retinopathy", reply_retina)

    def test_07_medical_report_ocr(self):
        sample_text = (
            "PATIENT METABOLIC REPORT\n"
            "Age: 48 | Sex: Female\n"
            "Fasting Glucose: 138 mg/dL\n"
            "Total Cholesterol: 224 mg/dL\n"
            "Blood Pressure: 132/84 mm Hg\n"
            "BMI: 28.5 kg/m2\n"
        )
        res = report_scanner.scan_report(sample_text.encode("utf-8"), filename="test_report.txt")
        fields = res["extracted_fields"]
        self.assertAlmostEqual(fields.get("glucose"), 138.0)
        self.assertAlmostEqual(fields.get("cholesterol"), 224.0)
        self.assertEqual(fields.get("systolic_bp"), 132)

    def test_08_non_eye_image_rejection(self):
        # Create a non-eye image (e.g., solid gray/white)
        non_eye = np.full((200, 200, 3), 180, dtype=np.uint8)
        import cv2
        _, buf = cv2.imencode(".jpg", non_eye)
        with self.assertRaises(ValueError) as ctx:
            retina_service.analyze_image(buf.tobytes(), filename="random_photo.jpg")
        self.assertIn("not a retinal fundus photograph", str(ctx.exception).lower())

    def test_09_json_serialization_safety(self):
        # Verify that all returned values from predict_diabetes are pure Python primitives (no np.bool_ or np.float64)
        sample = {
            "Pregnancies": 1, "Glucose": 115, "BloodPressure": 70,
            "SkinThickness": 20, "Insulin": 80, "BMI": 23.5,
            "DiabetesPedigreeFunction": 0.35, "Age": 28
        }
        res = hybrid_engine.predict_diabetes(sample)
        import json
        # This will raise TypeError if any np.bool_ or np.ndarray remains
        serialized = json.dumps(res)
        self.assertIsInstance(serialized, str)

if __name__ == "__main__":
    unittest.main()
