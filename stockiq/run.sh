# 1️⃣ Create environment
conda env create -f environment.yaml
conda activate stockiq

# 2️⃣ Set Gemini API key
#export GEMINI_API_KEY="your_real_gemini_api_key"

# 3️⃣ Run the dashboard
streamlit run app.py
