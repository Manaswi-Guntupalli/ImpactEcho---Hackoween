# ImpactEcho AI Verification (Simulated)

This version runs a **simulated AI verification model** that mimics the CLIP-based verifier but without heavy dependencies.
It generates random yet realistic confidence scores and flags donations as verified, flagged, or rejected.

## How to Run

1️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

2️⃣ Start the simulated AI server
```bash
python ai_verification.py
```

3️⃣ In another terminal, run the dataset integration
```bash
python impact_data_integration.py
```

4️⃣ Results will appear in the `data/` folder:
- `impact_data_verified.csv`
- `impact_data_verified.json`
