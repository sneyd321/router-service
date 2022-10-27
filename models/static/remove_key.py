import json, os

with open("./models/static/ServiceAccount.json") as serviceAccount:
    key = json.load(serviceAccount)

os.system(f"gcloud iam service-accounts keys delete {key['private_key_id']} --iam-account=cloud-run-admin@roomr-222721.iam.gserviceaccount.com --quiet")  