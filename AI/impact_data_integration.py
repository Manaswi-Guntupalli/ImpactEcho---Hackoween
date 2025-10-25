import pandas as pd
import requests
import random
import time
from datetime import datetime, timedelta

AI_URL = "http://localhost:8003/api/verify"
SAVE_CSV = "./data/impact_data_verified.csv"
SAVE_JSON = "./data/impact_data_verified.json"

def generate_impact_data(num_records=50, fake_rate=0.2):
    ngo_ids = [f"NGO-{i:03d}" for i in range(1, 21)]
    projects = ["Tree Plantation", "Health Camp", "Food Distribution", "Education Drive"]
    locations = ["Delhi", "Mumbai", "Bangalore", "Hyderabad", "Chennai"]

    num_fake = int(num_records * fake_rate)
    num_real = num_records - num_fake
    base_time = datetime(2025, 10, 1, 9, 0, 0)

    data = []

    for i in range(num_real):
        project = random.choice(projects)
        location = random.choice(locations)
        desc = f"Successfully completed {project.lower()} in {location} for local community support."
        data.append({
            "ngo_id": random.choice(ngo_ids),
            "project_type": project,
            "location": location,
            "description": desc,
            "media_link": f"https://picsum.photos/300?random={i}",
            "is_fake": 0
        })

    for i in range(num_fake):
        project = random.choice(projects + ["Ghost Project"])
        location = random.choice(["Unknown", "Nowhere", "N/A"])
        desc = f"Claimed {project.lower()} in {location} with fake proof."
        data.append({
            "ngo_id": f"FAKE-{random.randint(100,999)}",
            "project_type": project,
            "location": location,
            "description": desc,
            "media_link": random.choice([
                "https://imgur.com/fakeproof123",
                "https://drive.google.com/brokenlink"
            ]),
            "is_fake": 1
        })

    df = pd.DataFrame(data)
    return df


def get_ai_confidence(image, text):
    try:
        res = requests.post(AI_URL, json={"imageUrl": image, "text": text}, timeout=5)
        if res.status_code == 200:
            return res.json().get("confidence", None)
    except Exception:
        return None


def run_pipeline():
    print("🚀 Generating dataset...")
    df = generate_impact_data()
    df["ai_confidence"] = None

    print("🤖 Verifying each record using simulated AI service...")
    for i, row in df.iterrows():
        conf = get_ai_confidence(row["media_link"], row["description"])
        df.at[i, "ai_confidence"] = conf
        time.sleep(0.2)

    df["ai_verdict"] = df["ai_confidence"].apply(
        lambda x: "verified" if x and x >= 75 else ("flagged" if x and x >= 40 else "rejected")
    )

    df.to_csv(SAVE_CSV, index=False)
    df.to_json(SAVE_JSON, orient="records", indent=2)

    print("\n✅ Results saved to:")
    print(f"  {SAVE_CSV}")
    print(f"  {SAVE_JSON}")
    print("\nSummary:")
    print(df["ai_verdict"].value_counts())


if __name__ == "__main__":
    run_pipeline()
