# Phase 2 Summary: Dataset Generation 📊

## 📍 What is it?
The **Dataset Generation** phase was a critical data engineering stage where we created a high-fidelity synthetic training dataset of **110,000+ financial profiles**. This dataset serves as the "fuel" for our deep learning risk models.

## 🚀 How we achieved it
Since real financial data is private and sensitive, we engineered a realistic alternative:
1.  **Base Seeding**: Used a 32,000-record Kaggle "Credit Risk" dataset as a statistically sound ground truth.
2.  **Upscaling**: Applied random sampling with replacement to bootstrap the count to 110,000 records.
3.  **Synthesis & Jitter**: Used financial logic to "fill in the gaps," such as calculating **Monthly EMI** using bank amortization formulas and deriving **Total Savings** based on income-to-expense ratios. Added "statistical jitter" (noise) to ensure the model doesn't just memorize duplicates.
4.  **Label Mapping**: Programmatically calculated target labels like `risk_level`, `budget_stability`, and `savings_ratio` for supervised learning.

## 🛠️ What we used
- **Python**: The core language for data processing.
- **Pandas**: For massive data manipulation and table merging.
- **NumPy**: For high-performance mathematical operations and statistical jitter.
- **Scikit-learn**: For random sampling and data distribution tools.

## 💡 Why we used it
- **Data Privacy**: Using synthetic data allowed us to build and test robust models without needing access to real, sensitive user bank records.
- **Statistical Integrity**: By basing the synthesis on real Kaggle data rather than pure random numbers, we ensured the system learns real-world correlations (e.g., people with higher default history have lower credit scores).
- **Scale**: Deep learning models (Phase 3) require large datasets (100k+) to reach high accuracy; synthesis made this scale possible.
- **Mathematical Exactness**: Using literal bank formulas (Amortization) for EMI and Savings ensures the AI learns logical financial behavior rather than arbitrary patterns.
