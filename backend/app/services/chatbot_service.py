"""
chatbot_service.py
==================
Module 3: MediBot AI Health Assistant Chatbot
Intelligent healthcare conversational engine with:
1. Online LLM API integration (Google Gemini / OpenAI Chat Completion)
2. Comprehensive multi-topic clinical & soft-computing AI knowledge engine fallback
3. Context-aware personalized prediction explanation (GA features, ANN probability, Fuzzy logic score)
4. Strict medical ethical safety protocols (educational clarity, no prescribing)
"""

import os
import json
import re
import urllib.request
import urllib.error

SYSTEM_PROMPT = """You are MediBot, an advanced AI Health Assistant for the MediHybrid intelligent healthcare platform.
Your mission:
1. Explain health concepts, medical terms, symptoms, lifestyle guidance, and clinical biomarkers clearly and calmly.
2. Explain how the soft computing algorithms (Genetic Algorithm, Artificial Neural Network, Mamdani Fuzzy Logic, and CNN Diabetic Retinopathy detection) work together.
3. Interpret user predictions accurately when user assessment context is provided.
4. Adhere strictly to medical safety rules:
   - State clearly that you are an educational AI assistant, NOT a medical doctor.
   - Never diagnose, prescribe medications, or alter clinical treatment plans.
   - For elevated risk scores or severe retinopathy, advise consulting a healthcare professional.
Keep answers structured, insightful, and formatted with clean markdown and bullet points."""

# Deep clinical & soft computing knowledge repository
KNOWLEDGE_TOPICS = {
    "ga": {
        "keywords": ["genetic algorithm", " ga ", "chromosome", "deap", "feature selection", "crossover", "mutation"],
        "title": "Genetic Algorithm (GA) Biomarker Selection",
        "content": (
            "**Genetic Algorithm (GA) in MediHybrid:**\n"
            "The Genetic Algorithm is an evolutionary metaheuristic inspired by Charles Darwin's theory of natural selection.\n\n"
            "- **Chromosome Representation**: Each individual chromosome is a binary mask (e.g., `[1, 0, 1, 1, 0]`) where `1` activates a clinical biomarker and `0` discards it.\n"
            "- **Population & Initialization**: A diverse population of candidate biomarker masks is initialized randomly.\n"
            "- **Fitness Function**: Evaluates each candidate subset using stratified **5-Fold Cross-Validation ROC-AUC** strictly within the training set, penalizing redundant features.\n"
            "- **Selection**: Employs Tournament Selection to favor higher-fitness feature masks without prematurely losing genetic diversity.\n"
            "- **Crossover & Mutation**: Uses Two-Point Crossover (recombining biomarker blocks) and Bit-Flip Mutation (flipping inclusion state at rate $p_m = 0.08$).\n"
            "- **Outcome**: Discards uninformative or colinear clinical variables, preventing neural network overfitting and maximizing generalization."
        )
    },
    "ann": {
        "keywords": ["neural network", " ann ", "mlp", "backpropagation", "relu", "sigmoid", "adam", "hidden layer"],
        "title": "Artificial Neural Network (ANN) Classifier",
        "content": (
            "**Artificial Neural Network (ANN) in MediHybrid:**\n"
            "- **Architecture**: Multi-Layer Perceptron (MLP) receiving exclusively the optimal biomarkers selected by the Genetic Algorithm.\n"
            "- **Hidden Layers**: Dense layers equipped with **ReLU** (Rectified Linear Unit) activations, enabling the network to capture complex non-linear metabolic relationships.\n"
            "- **Output Layer**: Single neuron with **Sigmoid activation function** producing a continuous posterior probability $P(\\text{Disease} | X) \\in [0, 1]$.\n"
            "- **Loss & Optimization**: Trained using Binary Cross-Entropy loss with the **Adam optimizer** and early stopping to prevent memorization.\n"
            "- **Output Scaling**: The neural probability is mapped to an intuitive 0–100 risk score."
        )
    },
    "fuzzy": {
        "keywords": ["fuzzy", "mamdani", "membership", "defuzzification", "centroid", "fuzzification", "linguistic", "rules"],
        "title": "Mamdani Fuzzy Inference System",
        "content": (
            "**Mamdani Fuzzy Inference System in MediHybrid:**\n"
            "Traditional clinical criteria struggle with boundary cases (e.g., is a fasting glucose of 101 mg/dL abruptly 'diseased' while 99 mg/dL is 'healthy'?). Fuzzy logic resolves this ambiguity.\n\n"
            "- **Fuzzification**: Converts crisp patient values into degrees of membership across linguistic terms: *Low*, *Normal*, *Moderate*, and *High* using triangular and trapezoidal curves.\n"
            "- **Rule Base**: Encodes human clinical knowledge into linguistic IF-THEN rules (e.g., *IF Glucose is High AND BMI is Obese THEN Diabetes Risk is High*).\n"
            "- **Rule Evaluation & Aggregation**: Uses fuzzy MIN for logical conjunction (AND) and fuzzy MAX for combining active rule outputs.\n"
            "- **Centroid Defuzzification**: Computes the center of gravity of the aggregated membership area to yield a continuous, interpretable 0–100 risk index."
        )
    },
    "hybrid_fusion": {
        "keywords": ["hybrid", "fusion", "formula", "weights", "0.7", "0.30"],
        "title": "Hybrid Risk Fusion Architecture",
        "content": (
            "**Hybrid Neuro-Fuzzy Fusion Formula:**\n"
            "MediHybrid integrates empirical statistical learning with deterministic clinical heuristics:\n\n"
            "$$\\text{Hybrid Risk Score} = (0.70 \\times \\text{ANN Risk Score}) + (0.30 \\times \\text{Fuzzy Risk Score})$$\n\n"
            "- **Rationale**: The ANN captures subtle multi-dimensional patterns from large patient cohorts, while the Fuzzy Inference System guarantees that established medical rules (like extreme glucose or cholesterol spikes) always anchor the prediction.\n"
            "- **Categorization**: Classified into transparent experimental tiers: *Low Risk* (<30%), *Moderate Risk* (30–60%), and *High Risk* (>60%)."
        )
    },
    "retinopathy": {
        "keywords": ["retina", "retinopathy", "aptos", "fundus", "dr", "microaneurysm", "exudate", "hemorrhage", "neovascularization"],
        "title": "Diabetic Retinopathy & 5 Clinical Severity Stages",
        "content": (
            "**Diabetic Retinopathy (APTOS 2019 International Classification):**\n"
            "Diabetic retinopathy is microvascular damage to the retina caused by prolonged systemic hyperglycemia.\n\n"
            "- **Class 0 (No DR)**: Completely healthy retina; clear vascular tree, sharp optic disc margins, and foveal reflex.\n"
            "- **Class 1 (Mild NPDR)**: Presence of isolated microaneurysms (tiny balloon-like capillary wall outpouchings).\n"
            "- **Class 2 (Moderate NPDR)**: Multiple dot-and-blot intraretinal hemorrhages and yellow hard lipid exudates.\n"
            "- **Class 3 (Severe NPDR)**: The '4-2-1' rule — extensive hemorrhages in all 4 quadrants, venous beading in 2+ quadrants, or microvascular abnormalities.\n"
            "- **Class 4 (Proliferative DR - PDR)**: Pathological neovascularization (fragile new vessel proliferation) on the optic disc or retina, posing imminent risk of vitreous hemorrhage or tractional retinal detachment.\n\n"
            "**Key Note**: Early detection and strict glycemic control can prevent over 90% of severe vision loss."
        )
    },
    "gradcam": {
        "keywords": ["gradcam", "grad-cam", "heatmap", "attention", "explainability", "visual attention"],
        "title": "Grad-CAM Retinal Attention Heatmaps",
        "content": (
            "**Grad-CAM (Gradient-Weighted Class Activation Mapping):**\n"
            "- **Function**: Illuminates the exact spatial regions inside the retinal fundus image that governed the CNN's classification.\n"
            "- **Mechanism**: Tracks the positive gradient flow from the predicted severity class back to the final convolutional feature maps.\n"
            "- **Interpretation**: Warm red/yellow zones mark pathological lesions (such as microaneurysm clusters, hemorrhagic patches, or hard exudates), while cool blue zones indicate healthy background tissue."
        )
    },
    "blood_pressure": {
        "keywords": ["blood pressure", "hypertension", "systolic", "diastolic", "mmhg", "hypotension", "bp"],
        "title": "Blood Pressure Stages & Cardiovascular Risk",
        "content": (
            "**Blood Pressure Clinical Classifications (AHA/ACC Standards):**\n"
            "- **Normal**: Systolic < 120 mmHg **and** Diastolic < 80 mmHg\n"
            "- **Elevated**: Systolic 120–129 mmHg **and** Diastolic < 80 mmHg\n"
            "- **Stage 1 Hypertension**: Systolic 130–139 mmHg **or** Diastolic 80–89 mmHg\n"
            "- **Stage 2 Hypertension**: Systolic ≥ 140 mmHg **or** Diastolic ≥ 90 mmHg\n"
            "- **Hypertensive Crisis**: Systolic > 180 mmHg **and/or** Diastolic > 120 mmHg (requires immediate medical intervention)\n\n"
            "**Management Advice**:\n"
            "- Follow the **DASH diet** (Dietary Approaches to Stop Hypertension) rich in potassium, calcium, and magnesium.\n"
            "- Restrict sodium intake to under 2,300 mg per day (ideally <1,500 mg).\n"
            "- Engage in 150 minutes/week of moderate-intensity aerobic exercise."
        )
    },
    "glucose": {
        "keywords": ["glucose", "blood sugar", "glycemia", "hyperglycemia", "hypoglycemia", "fasting glucose", "sugar level"],
        "title": "Blood Glucose Biomarkers & Interpretation",
        "content": (
            "**Fasting Plasma Glucose (FPG) Reference Ranges:**\n"
            "- **Normal**: 70 to 99 mg/dL\n"
            "- **Impaired Fasting Glucose (Pre-diabetes)**: 100 to 125 mg/dL\n"
            "- **Diabetes Threshold**: ≥ 126 mg/dL on two separate occasions\n\n"
            "**Postprandial (2 Hours Post-Meal) Target**:\n"
            "- Normal: < 140 mg/dL\n"
            "- Pre-diabetes: 140 to 199 mg/dL\n"
            "- Diabetes: ≥ 200 mg/dL\n\n"
            "**Clinical Significance**: Chronic elevation causes non-enzymatic glycation of proteins, microvascular damage (eyes, kidneys, nerves), and macrovascular accelerated atherosclerosis."
        )
    },
    "hba1c": {
        "keywords": ["hba1c", "a1c", "glycated hemoglobin", "hemoglobin a1c"],
        "title": "Hemoglobin A1c (HbA1c) Glycemic Memory",
        "content": (
            "**Hemoglobin A1c (HbA1c) Overview:**\n"
            "HbA1c measures the percentage of red blood cell hemoglobin chemically bonded to glucose, representing an average 3-month glycemic history.\n\n"
            "- **Normal**: Below 5.7%\n"
            "- **Pre-diabetes**: 5.7% to 6.4%\n"
            "- **Diabetes**: 6.5% or higher\n\n"
            "Every 1% reduction in HbA1c correlates with a ~37% reduction in microvascular complications such as diabetic retinopathy and nephropathy."
        )
    },
    "cholesterol": {
        "keywords": ["cholesterol", "ldl", "hdl", "triglycerides", "lipid", "atherosclerosis", "lipids"],
        "title": "Lipid Profile & Atherosclerotic Risk",
        "content": (
            "**Standard Lipid Profile Biomarkers (mg/dL):**\n"
            "- **Total Cholesterol**: Desirable < 200 | Borderline 200–239 | High ≥ 240\n"
            "- **LDL ('Bad' Cholesterol)**: Optimal < 100 | Near Optimal 100–129 | High 160–189 | Very High ≥ 190\n"
            "- **HDL ('Good' Protective)**: Low < 40 (men) / < 50 (women) | High/Protective ≥ 60\n"
            "- **Triglycerides**: Normal < 150 | Borderline 150–199 | High ≥ 200\n\n"
            "**Mechanics**: Elevated LDL particles permeate endothelial micro-tears in coronary arteries, oxidize, and trigger foam cell formation, leading to calcified plaques."
        )
    },
    "heart_disease_symptoms": {
        "keywords": ["heart attack", "heart disease symptom", "angina", "chest pain", "shortness of breath", "cad", "coronary"],
        "title": "Coronary Artery Disease & Warning Symptoms",
        "content": (
            "**Coronary Artery Disease (CAD) Warning Indicators:**\n"
            "- **Angina Pectoris**: Squeezing, heavy pressure, or fullness in the center of the chest.\n"
            "- **Radiation**: Discomfort radiating to the left shoulder, arms, neck, jaw, or upper back.\n"
            "- **Exertional Dyspnea**: Unexplained shortness of breath during routine light physical exertion.\n"
            "- **Ischemic Diaphoresis**: Sudden cold sweat, lightheadedness, or nausea.\n\n"
            "**Critical Safety Notice**: Chest pain lasting more than 5 minutes or accompanied by radiating jaw/arm ache requires immediate emergency medical services (Call 911 / 112 / 108)."
        )
    },
    "ecg_and_st": {
        "keywords": ["ecg", "st depression", "oldpeak", "thal", "exercise angina", "flouroscopy", "thalassemia"],
        "title": "Cardiovascular Stress & ECG Markers",
        "content": (
            "**Clinical Cardiac Markers in MediHybrid:**\n"
            "- **ST Depression ('Oldpeak')**: Measures horizontal or downsloping ST-segment depression induced by exercise relative to rest on an ECG. Depression > 1.0 mm indicates myocardial subendocardial ischemia.\n"
            "- **Max Heart Rate Achieved (thalach)**: Typically compared against the physiological formula $220 - \\text{age}$. Inability to reach 85% of target heart rate indicates chronotropic incompetence.\n"
            "- **Exercise-Induced Angina (exang)**: Occurrence of cardiac ischemia provoked directly by physical workload.\n"
            "- **Major Vessels Colored by Fluoroscopy (ca)**: Evaluates coronary angiographic narrowing across 0 to 3 major coronary arteries."
        )
    },
    "bmi": {
        "keywords": ["bmi", "body mass index", "obesity", "overweight", "weight", "underweight"],
        "title": "Body Mass Index (BMI) & Metabolic Load",
        "content": (
            "**Body Mass Index (BMI) Reference Categories ($kg/m^2$):**\n"
            "- **Underweight**: < 18.5\n"
            "- **Normal Weight**: 18.5 – 24.9\n"
            "- **Overweight**: 25.0 – 29.9\n"
            "- **Class 1 Obesity**: 30.0 – 34.9\n"
            "- **Class 2 Obesity**: 35.0 – 39.9\n"
            "- **Class 3 Severe Obesity**: ≥ 40.0\n\n"
            "**Impact**: Visceral adipose tissue releases pro-inflammatory cytokines (TNF-alpha, IL-6) and free fatty acids, directly inducing hepatic and muscular insulin resistance."
        )
    },
    "lifestyle": {
        "keywords": ["diet", "exercise", "prevention", "lifestyle", "food", "nutrition", "workout", "sleep", "stress"],
        "title": "Evidence-Based Cardiovascular & Metabolic Prevention",
        "content": (
            "**Evidence-Based Lifestyle Optimization:**\n"
            "- **Nutrition**: Emphasize the Mediterranean dietary pattern — abundant leafy vegetables, berries, legumes, extra virgin olive oil, and wild-caught oily fish (omega-3 fatty acids).\n"
            "- **Carbohydrate Quality**: Replace refined flours and simple sugars with high-fiber, low-glycemic complex carbohydrates.\n"
            "- **Physical Activity**: Minimum 150 minutes of moderate aerobic exercise (e.g., brisk walking, cycling) plus 2 days of resistance strength training weekly.\n"
            "- **Sleep Hygiene**: Maintain 7–9 hours of restorative sleep to prevent cortisol spikes and impaired overnight glucose regulation.\n"
            "- **Avoidance**: Total cessation of tobacco smoking and reduction of ultra-processed sodium-rich snacks."
        )
    },
    "metrics": {
        "keywords": ["accuracy", "precision", "recall", "f1", "auc", "roc", "kappa", "qwk", "confusion matrix"],
        "title": "Model Evaluation Metrics in Healthcare AI",
        "content": (
            "**Soft-Computing Evaluation Metrics Explained:**\n"
            "- **Recall (Sensitivity)**: $\\frac{TP}{TP + FN}$ — Critical in medicine to avoid False Negatives (missing a diseased patient).\n"
            "- **Precision (PPV)**: $\\frac{TP}{TP + FP}$ — Reflects the confidence that a positive diagnosis is genuinely diseased.\n"
            "- **F1-Score**: Harmonic mean of Precision and Recall, crucial for imbalanced medical cohorts.\n"
            "- **ROC-AUC**: Measures the model's discriminative ability across all classification decision thresholds.\n"
            "- **Quadratic Weighted Kappa (QWK)**: Standard benchmark for Diabetic Retinopathy (APTOS 2019) that penalizes misclassifications proportionally to the severity distance (e.g., classifying Class 0 as Class 4 is penalized far more heavily than Class 0 as Class 1)."
        )
    }
}

class ChatbotService:
    def __init__(self):
        self.gemini_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("AI_API_KEY")
        self.openai_key = os.environ.get("OPENAI_API_KEY")
        self.provider = "gemini" if self.gemini_key else ("openai" if self.openai_key else "knowledge_engine")

    def _call_gemini_api(self, prompt: str, context: str = ""):
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_key}"
        full_content = f"{SYSTEM_PROMPT}\n\nPatient Context:\n{context}\n\nUser Question:\n{prompt}"
        payload = {
            "contents": [{"parts": [{"text": full_content}]}],
            "generationConfig": {"temperature": 0.35, "maxOutputTokens": 750}
        }
        req = urllib.request.Request(
            api_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["candidates"][0]["content"]["parts"][0]["text"]

    def _call_openai_api(self, prompt: str, context: str = ""):
        api_url = "https://api.openai.com/v1/chat/completions"
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{prompt}"}
            ],
            "temperature": 0.4,
            "max_tokens": 750
        }
        req = urllib.request.Request(
            api_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.openai_key}"
            }
        )
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]

    def _context_aware_explanation(self, context_data: dict, user_msg: str) -> str:
        disease = context_data.get("disease", "Clinical Assessment")
        hybrid = context_data.get("hybrid", {})
        ann = context_data.get("ann", {})
        fuzzy = context_data.get("fuzzy", {})
        selected_feats = context_data.get("selected_features", [])
        explainability = context_data.get("explainability", [])

        score = hybrid.get("score", ann.get("score", "N/A"))
        cat = hybrid.get("category", "Evaluated")
        ann_score = ann.get("score", "N/A")
        fuzzy_score = fuzzy.get("fuzzy_score", "N/A")

        # Top risk drivers
        risk_drivers = [f for f in explainability if f.get("is_risk_factor")][:4]
        protective = [f for f in explainability if f.get("is_protective")][:3]

        driver_bullets = "\n".join([f"- **{f['label']}**: `{f['value']} {f['unit']}` ({f['summary']})" for f in risk_drivers]) if risk_drivers else "- All evaluated biomarkers were within standard demographic ranges."
        protective_bullets = "\n".join([f"- **{f['label']}**: `{f['value']} {f['unit']}` ({f['summary']})" for f in protective]) if protective else "- None explicitly classified as protective."

        return (
            f"### Comprehensive Review of Your {disease}\n\n"
            f"- **Overall Hybrid Risk Score**: **{score}%** ({cat})\n"
            f"- **Artificial Neural Network Probability**: `{ann_score}%`\n"
            f"- **Mamdani Fuzzy Logic Risk Index**: `{fuzzy_score}%`\n\n"
            f"**Biomarkers Selected by Genetic Algorithm ({len(selected_feats)} features):**\n"
            f"`{', '.join(selected_feats)}`\n\n"
            f"**Primary Risk Elevation Factors:**\n{driver_bullets}\n\n"
            f"**Protective / Optimal Biomarkers:**\n{protective_bullets}\n\n"
            f"**Algorithm Explanation**:\n"
            f"The Genetic Algorithm filtered out redundant variables, feeding only verified predictive factors into the Neural Network (70% weight). Simultaneously, the Mamdani Fuzzy System (30% weight) calculated clinical degrees of membership. "
            f"Because this system operates as an educational research prototype, please share this assessment with your physician for diagnostic interpretation."
        )

    def _knowledge_engine_response(self, message: str, context_data: dict = None) -> str:
        msg = message.lower().strip()

        # Check if user is asking to explain their assessment result
        if context_data and any(k in msg for k in ["my result", "my prediction", "my score", "my assessment", "why is my", "explain my", "my risk"]):
            return self._context_aware_explanation(context_data, msg)

        # Match query against extensive knowledge topics
        matched_topics = []
        for key, topic in KNOWLEDGE_TOPICS.items():
            for kw in topic["keywords"]:
                if kw in msg:
                    matched_topics.append(topic)
                    break

        if matched_topics:
            # If 1 topic matches, return in-depth explanation
            if len(matched_topics) == 1:
                return matched_topics[0]["content"]
            
            # If multiple topics match (e.g. "What is the relation between glucose and retinopathy?"), synthesize them
            combined_reply = [f"### {matched_topics[0]['title']} & Related Clinical Concepts\n"]
            for t in matched_topics[:2]:
                combined_reply.append(t["content"])
            return "\n\n---\n\n".join(combined_reply)

        # General conversational Q&A parsing for common medical questions
        if "what is diabetes" in msg or "type 2" in msg or "type 1" in msg:
            return (
                "**Understanding Diabetes Mellitus:**\n\n"
                "Diabetes is a chronic metabolic condition characterized by elevated blood glucose (hyperglycemia).\n\n"
                "- **Type 1 Diabetes**: An autoimmune condition where the body attacks insulin-producing beta cells in the pancreas. Requires external insulin therapy.\n"
                "- **Type 2 Diabetes**: Characterized by progressive insulin resistance combined with insufficient compensatory insulin secretion. Highly influenced by lifestyle, genetics, and visceral adiposity.\n"
                "- **Gestational Diabetes**: High blood sugar that develops during pregnancy and usually resolves after delivery, though it elevates future Type 2 risk.\n\n"
                "**Primary Organs Affected**: Blood vessels, eyes (retinopathy), kidneys (nephropathy), nerves (neuropathy), and the cardiovascular system."
            )

        if "heart disease" in msg or "cardiovascular" in msg or "heart attack" in msg:
            return (
                "**Cardiovascular Disease (CVD) Overview:**\n\n"
                "Cardiovascular disease encompasses disorders of the heart and blood vessel network, most notably **Coronary Artery Disease (CAD)**.\n\n"
                "- **Pathology**: Caused by atherosclerosis — the gradual deposition of cholesterol-rich plaques inside coronary arteries, narrowing luminal blood flow to the heart muscle.\n"
                "- **Major Modifiable Risk Factors**: High LDL cholesterol, elevated systolic blood pressure, smoking, diabetes, sedentary lifestyle, and high chronic stress.\n"
                "- **Screening Tools**: Resting & stress ECG, lipid panels, coronary calcium scoring, and fluoroscopy angiograms."
            )

        if "how does medihybrid work" in msg or "how it works" in msg or "how this project work" in msg:
            return (
                "**How MediHybrid Works (End-to-End Workflow):**\n\n"
                "1. **Input Phase**: Patient biometrics (glucose, BP, cholesterol, age, etc.) or retinal fundus photographs are entered into the platform.\n"
                "2. **Genetic Algorithm (GA)**: Evaluates billions of biomarker combinations to select the optimal subset with highest predictive ROC-AUC.\n"
                "3. **Artificial Neural Network (ANN)**: Evaluates the GA-selected features to calculate a probabilistic disease classification score (0–100%).\n"
                "4. **Mamdani Fuzzy System**: Converts crisp patient numbers into linguistic sets (Low, Normal, High) and defuzzifies active clinical IF-THEN rules via centroid calculation.\n"
                "5. **Hybrid Fusion**: Blends $(0.70 \\times \\text{ANN}) + (0.30 \\times \\text{Fuzzy})$ for balanced, explainable risk output.\n"
                "6. **Vision Module (RetinaScan)**: Evaluates retinal eye images using deep transfer learning with Grad-CAM visual heatmaps across 5 clinical severity classes."
            )

        # Default helpful assistant response
        return (
            "Hello! I am **MediBot**, your AI Clinical Health Assistant. I am equipped to assist you with:\n\n"
            "- **Your Predictions**: Ask *'Explain my diabetes result'* or *'Why is my hybrid score elevated?'*\n"
            "- **Soft-Computing AI**: Inquire about the *Genetic Algorithm*, *Artificial Neural Network*, *Fuzzy Logic*, or *Grad-CAM*.\n"
            "- **Retinal Health**: Ask about *Diabetic Retinopathy 5 severity stages* or *how to interpret fundus scans*.\n"
            "- **Clinical Biomarkers**: Inquire about *Fasting Glucose*, *HbA1c*, *Blood Pressure categories*, or *LDL Cholesterol*.\n"
            "- **Lifestyle & Prevention**: Ask about *dietary guidelines*, *exercise protocols*, and *cardiovascular risk factors*.\n\n"
            "Feel free to ask any medical, algorithmic, or platform question!"
        )

    def generate_reply(self, message: str, context_data: dict = None) -> str:
        """
        Coordinates AI response with fallback handling.
        """
        if not message or not message.strip():
            return "Please type a health or soft-computing question to begin."

        # 1. Try Gemini API if key is available
        if self.gemini_key:
            try:
                ctx_str = json.dumps(context_data, indent=2) if context_data else "No user assessment loaded."
                return self._call_gemini_api(message, ctx_str)
            except Exception:
                pass

        # 2. Try OpenAI API if key is available
        if self.openai_key:
            try:
                ctx_str = json.dumps(context_data, indent=2) if context_data else "No user assessment loaded."
                return self._call_openai_api(message, ctx_str)
            except Exception:
                pass

        # 3. Knowledge engine fallback (instant, rich, context-aware)
        return self._knowledge_engine_response(message, context_data)

chatbot = ChatbotService()
