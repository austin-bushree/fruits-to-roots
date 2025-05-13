
## 🚀 Backend Deployment & API Key Management (GCP Cloud Run)

### 📁 Directory: `backend/`

This project uses [Google Cloud Run](https://cloud.google.com/run) to host the FastAPI backend, and [Secret Manager](https://cloud.google.com/secret-manager) to securely store your OpenAI API key.

---

### 🔨 `deploy.sh` – Build & Deploy Backend

This script builds your FastAPI backend Docker image and deploys it to Cloud Run with the latest config.

**To run:**

```bash
cd backend
./deploy.sh
```

#### What it does:

* Builds and tags your backend image using Cloud Build
* Deploys to Cloud Run in region `us-west2`
* Re-applies secret bindings (`OPENAI_API_KEY`) for production use

---

### 🔐 `rotate-openai-key.sh` – Upload & Apply a New OpenAI Key

Use this script whenever you need to rotate your OpenAI API key (for security or expiration).

**To run:**

```bash
cd backend
./rotate-openai-key.sh
```

#### What it does:

* Prompts for your new OpenAI API key (input is hidden)
* Uploads it as a **new version** of your `OPENAI_API_KEY` secret
* Re-deploys your backend to bind the latest key

---

### ✅ Prerequisites

* You’ve authenticated via `gcloud auth login`
* You’ve set your project with `gcloud config set project fruits-to-roots`
* Your secret `OPENAI_API_KEY` already exists in Secret Manager
* Your Cloud Run service is named `fruits-backend`

---

Would you like me to auto-generate a `README.md` file containing this content along with usage badges and project metadata?
