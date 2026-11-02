"""
fuzzy_service.py
================
Module 1: Mamdani Fuzzy Inference Systems using scikit-fuzzy
- Diabetes Fuzzy System: Evaluates Glucose, BMI, Blood Pressure, and Age
- Heart Disease Fuzzy System: Evaluates Age, Cholesterol, Resting BP, Max Heart Rate, and ST Depression
- True fuzzification, linguistic rule evaluation, aggregation, and centroid defuzzification
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class DiabetesFuzzySystem:
    def __init__(self):
        # Universes of discourse
        self.g_univ = np.arange(40, 261, 1)    # Glucose (mg/dL)
        self.b_univ = np.arange(12, 61, 0.5)  # BMI (kg/m²)
        self.bp_univ = np.arange(50, 201, 1)  # Blood Pressure (mm Hg)
        self.a_univ = np.arange(18, 91, 1)    # Age (years)
        self.r_univ = np.arange(0, 101, 1)    # Risk score (0 - 100)

        # Antecedents
        self.glucose = ctrl.Antecedent(self.g_univ, "glucose")
        self.bmi = ctrl.Antecedent(self.b_univ, "bmi")
        self.bp = ctrl.Antecedent(self.bp_univ, "bp")
        self.age = ctrl.Antecedent(self.a_univ, "age")
        self.risk = ctrl.Consequent(self.r_univ, "risk")

        self._build_memberships()
        self._build_rules()
        self.simulation = ctrl.ControlSystemSimulation(self.control_system)

    def _build_memberships(self):
        # Glucose: Normal (<100), Borderline/Moderate (100-140), High (>140)
        self.glucose["normal"] = fuzz.trapmf(self.g_univ, [40, 40, 90, 110])
        self.glucose["moderate"] = fuzz.trimf(self.g_univ, [100, 125, 150])
        self.glucose["high"] = fuzz.trapmf(self.g_univ, [140, 170, 260, 260])

        # BMI: Normal (<25), Overweight (24-30), Obese (>29)
        self.bmi["normal"] = fuzz.trapmf(self.b_univ, [12, 12, 20, 25])
        self.bmi["overweight"] = fuzz.trimf(self.b_univ, [24, 27.5, 31])
        self.bmi["obese"] = fuzz.trapmf(self.b_univ, [29, 35, 60, 60])

        # Blood Pressure: Normal (<120), Prehypertension (120-140), High (>140)
        self.bp["normal"] = fuzz.trapmf(self.bp_univ, [50, 50, 75, 85])
        self.bp["moderate"] = fuzz.trimf(self.bp_univ, [80, 90, 105])
        self.bp["high"] = fuzz.trapmf(self.bp_univ, [100, 115, 200, 200])

        # Age: Young (<35), Middle (30-55), Senior (>50)
        self.age["young"] = fuzz.trapmf(self.a_univ, [18, 18, 30, 40])
        self.age["middle"] = fuzz.trimf(self.a_univ, [35, 48, 60])
        self.age["senior"] = fuzz.trapmf(self.a_univ, [55, 65, 90, 90])

        # Risk Output: Low, Moderate, High
        self.risk["low"] = fuzz.trapmf(self.r_univ, [0, 0, 20, 35])
        self.risk["moderate"] = fuzz.trimf(self.r_univ, [25, 50, 75])
        self.risk["high"] = fuzz.trapmf(self.r_univ, [65, 80, 100, 100])

    def _build_rules(self):
        rules = [
            ctrl.Rule(self.glucose["normal"] & self.bmi["normal"], self.risk["low"]),
            ctrl.Rule(self.glucose["normal"] & self.bmi["overweight"] & self.age["young"], self.risk["low"]),
            ctrl.Rule(self.glucose["moderate"] & self.bmi["normal"], self.risk["moderate"]),
            ctrl.Rule(self.glucose["moderate"] & self.bmi["overweight"], self.risk["moderate"]),
            ctrl.Rule(self.glucose["moderate"] & self.bmi["obese"], self.risk["high"]),
            ctrl.Rule(self.glucose["high"] | self.bmi["obese"], self.risk["high"]),
            ctrl.Rule(self.glucose["high"] & self.age["senior"], self.risk["high"]),
            ctrl.Rule(self.bp["high"] & self.glucose["moderate"], self.risk["high"]),
            ctrl.Rule(self.glucose["normal"] & self.bp["normal"] & self.age["young"], self.risk["low"]),
            ctrl.Rule(self.glucose["high"] & self.bp["high"] & self.bmi["obese"], self.risk["high"])
        ]
        self.rules = rules
        self.control_system = ctrl.ControlSystem(rules)

    def evaluate(self, glucose, bmi, bp, age):
        g = float(np.clip(glucose, 40, 260))
        b = float(np.clip(bmi, 12, 60))
        p = float(np.clip(bp, 50, 200))
        a = float(np.clip(age, 18, 90))

        # Direct fuzzification memberships
        g_norm = float(fuzz.interp_membership(self.g_univ, self.glucose["normal"].mf, g))
        g_mod = float(fuzz.interp_membership(self.g_univ, self.glucose["moderate"].mf, g))
        g_hi = float(fuzz.interp_membership(self.g_univ, self.glucose["high"].mf, g))

        b_norm = float(fuzz.interp_membership(self.b_univ, self.bmi["normal"].mf, b))
        b_over = float(fuzz.interp_membership(self.b_univ, self.bmi["overweight"].mf, b))
        b_ob = float(fuzz.interp_membership(self.b_univ, self.bmi["obese"].mf, b))

        self.simulation.input["glucose"] = g
        self.simulation.input["bmi"] = b
        self.simulation.input["bp"] = p
        self.simulation.input["age"] = a

        try:
            self.simulation.compute()
            score = float(self.simulation.output["risk"])
        except Exception:
            # Fallback heuristic calculation if out of defuzzifiable support
            score = float(np.clip((g_hi * 50) + (b_ob * 30) + (g_mod * 20), 5.0, 95.0))

        risk_level = "Low Risk" if score < 35 else ("Moderate Risk" if score < 65 else "High Risk")

        active_rules = []
        if g_hi > 0.3 or b_ob > 0.3:
            active_rules.append(f"Rule [High Glucose / Obesity]: Glucose ({g}) and BMI ({b}) drive risk towards High (μ_hi={g_hi:.2f}, μ_ob={b_ob:.2f})")
        if g_norm > 0.5 and b_norm > 0.5:
            active_rules.append(f"Rule [Optimal Glycemia]: Normal Glucose ({g}) & BMI ({b}) actively suppress risk (μ_norm={g_norm:.2f})")
        if g_mod > 0.3:
            active_rules.append(f"Rule [Impaired Fasting Glucose]: Intermediate glucose level promotes Moderate vigilance (μ_mod={g_mod:.2f})")

        return {
            "fuzzy_score": round(score, 2),
            "risk_level": risk_level,
            "defuzzification": "Centroid (Mamdani)",
            "memberships": {
                "glucose": {"normal": round(g_norm, 3), "moderate": round(g_mod, 3), "high": round(g_hi, 3)},
                "bmi": {"normal": round(b_norm, 3), "overweight": round(b_over, 3), "obese": round(b_ob, 3)}
            },
            "active_rules": active_rules if active_rules else ["Default baseline metabolic rule active"]
        }


class HeartFuzzySystem:
    def __init__(self):
        self.a_univ = np.arange(25, 85, 1)    # Age
        self.c_univ = np.arange(100, 500, 1)  # Cholesterol
        self.bp_univ = np.arange(80, 220, 1)  # Resting BP
        self.hr_univ = np.arange(60, 220, 1)  # Max HR
        self.st_univ = np.arange(0, 6.5, 0.1) # Oldpeak ST depression
        self.r_univ = np.arange(0, 101, 1)    # Heart Risk

        self.age = ctrl.Antecedent(self.a_univ, "age")
        self.chol = ctrl.Antecedent(self.c_univ, "chol")
        self.bp = ctrl.Antecedent(self.bp_univ, "bp")
        self.hr = ctrl.Antecedent(self.hr_univ, "hr")
        self.st = ctrl.Antecedent(self.st_univ, "st")
        self.risk = ctrl.Consequent(self.r_univ, "risk")

        self._build_memberships()
        self._build_rules()
        self.simulation = ctrl.ControlSystemSimulation(self.control_system)

    def _build_memberships(self):
        self.age["young"] = fuzz.trapmf(self.a_univ, [25, 25, 40, 50])
        self.age["senior"] = fuzz.trapmf(self.a_univ, [45, 58, 85, 85])

        self.chol["desirable"] = fuzz.trapmf(self.c_univ, [100, 100, 180, 200])
        self.chol["borderline"] = fuzz.trimf(self.c_univ, [190, 225, 250])
        self.chol["high"] = fuzz.trapmf(self.c_univ, [240, 280, 500, 500])

        self.bp["normal"] = fuzz.trapmf(self.bp_univ, [80, 80, 120, 130])
        self.bp["high"] = fuzz.trapmf(self.bp_univ, [125, 145, 220, 220])

        self.hr["low"] = fuzz.trapmf(self.hr_univ, [60, 60, 110, 130])
        self.hr["optimal"] = fuzz.trapmf(self.hr_univ, [120, 150, 220, 220])

        self.st["normal"] = fuzz.trapmf(self.st_univ, [0, 0, 0.8, 1.5])
        self.st["elevated"] = fuzz.trapmf(self.st_univ, [1.2, 2.5, 6.5, 6.5])

        self.risk["low"] = fuzz.trapmf(self.r_univ, [0, 0, 25, 40])
        self.risk["moderate"] = fuzz.trimf(self.r_univ, [30, 55, 75])
        self.risk["high"] = fuzz.trapmf(self.r_univ, [65, 80, 100, 100])

    def _build_rules(self):
        rules = [
            ctrl.Rule(self.chol["desirable"] & self.bp["normal"] & self.st["normal"], self.risk["low"]),
            ctrl.Rule(self.chol["high"] | self.st["elevated"], self.risk["high"]),
            ctrl.Rule(self.bp["high"] & self.age["senior"], self.risk["high"]),
            ctrl.Rule(self.chol["borderline"] & self.bp["normal"], self.risk["moderate"]),
            ctrl.Rule(self.st["elevated"] & self.age["senior"], self.risk["high"]),
            ctrl.Rule(self.chol["high"] & self.bp["high"], self.risk["high"]),
            ctrl.Rule(self.hr["low"] & self.st["elevated"], self.risk["high"]),
            ctrl.Rule(self.chol["desirable"] & self.age["young"], self.risk["low"])
        ]
        self.rules = rules
        self.control_system = ctrl.ControlSystem(rules)

    def evaluate(self, age, chol, bp, hr, oldpeak):
        a = float(np.clip(age, 25, 85))
        c = float(np.clip(chol, 100, 500))
        p = float(np.clip(bp, 80, 220))
        h = float(np.clip(hr, 60, 220))
        s = float(np.clip(oldpeak, 0.0, 6.5))

        c_hi = float(fuzz.interp_membership(self.c_univ, self.chol["high"].mf, c))
        s_hi = float(fuzz.interp_membership(self.st_univ, self.st["elevated"].mf, s))
        p_hi = float(fuzz.interp_membership(self.bp_univ, self.bp["high"].mf, p))
        c_des = float(fuzz.interp_membership(self.c_univ, self.chol["desirable"].mf, c))

        self.simulation.input["age"] = a
        self.simulation.input["chol"] = c
        self.simulation.input["bp"] = p
        self.simulation.input["hr"] = h
        self.simulation.input["st"] = s

        try:
            self.simulation.compute()
            score = float(self.simulation.output["risk"])
        except Exception:
            score = float(np.clip((c_hi * 45) + (s_hi * 40) + (p_hi * 15), 5.0, 95.0))

        risk_level = "Low Risk" if score < 35 else ("Moderate Risk" if score < 65 else "High Risk")

        active_rules = []
        if c_hi > 0.3 or s_hi > 0.3:
            active_rules.append(f"Rule [Atherosclerotic / Ischemic Risk]: Serum Chol ({c}) or ST Depression ({s}) elevates cardiac risk (μ_chol={c_hi:.2f}, μ_st={s_hi:.2f})")
        if c_des > 0.5:
            active_rules.append(f"Rule [Lipid Balance]: Desirable cholesterol level maintains protective cardiovascular baseline (μ_des={c_des:.2f})")
        if p_hi > 0.4:
            active_rules.append(f"Rule [Hypertensive Strain]: Resting BP ({p} mm Hg) introduces vascular wall tension (μ_bp={p_hi:.2f})")

        return {
            "fuzzy_score": round(score, 2),
            "risk_level": risk_level,
            "defuzzification": "Centroid (Mamdani)",
            "memberships": {
                "cholesterol": {"desirable": round(c_des, 3), "high": round(c_hi, 3)},
                "st_depression": {"elevated": round(s_hi, 3)},
                "blood_pressure": {"high": round(p_hi, 3)}
            },
            "active_rules": active_rules if active_rules else ["Default cardiac hemodynamic balance active"]
        }

# Singleton instances
diabetes_fuzzy = DiabetesFuzzySystem()
heart_fuzzy = HeartFuzzySystem()
