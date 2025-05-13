# 🚀 Fruits to Roots: Development Workflow

This guide explains the end-to-end development cycle for the **Fruits to Roots** project, including how to test locally, commit changes, and deploy automatically via Vercel.

---

## ✅ Local Development Workflow

### 1. Clone or Open the Project

Make sure you're in the root project folder:

```
fruits-to-roots/
├── backend/
├── frontend/
│   └── f2r/
```

### 2. Run Frontend Locally (Vite Dev Server)

```bash
cd frontend/f2r
npm install  # Run once to install dependencies
npm run dev  # Starts local server at http://localhost:5173
```

### 3. Make Code Changes

Edit files in your local IDE. You can live preview changes at `http://localhost:5173`.

### 4. Commit Changes

```bash
git add .
git commit -m "Describe your change"
```

### 5. Push to GitHub

```bash
git push origin main
```

### 6. Vercel Auto-Deploys

* Vercel will automatically build and deploy your app when you push to the `main` branch.
* You can monitor deployments at: [https://vercel.com/dashboard](https://vercel.com/dashboard)

---

## 🧠 When to Push

| Scenario                     | Push to GitHub? |
| ---------------------------- | --------------- |
| Feature complete & working   | ✅ Yes           |
| Small or untested change     | ❌ No            |
| Collaborating or debugging   | ✅ Yes           |
| Mid-development (use branch) | ✅ (on branch)   |

---

## 🛠 Manual Redeploy (Optional)

If auto-deploy fails or you want to trigger it again:

* Go to your [Vercel project dashboard](https://vercel.com/dashboard)
* Click **Deployments** → **Redeploy** next to the latest build

---

## 🌐 Live Site URL

Once deployed, your app is available at:

```
https://fruitstoroots.vercel.app
```

Or your custom domain, if configured.

---

## ✅ Summary: Local → Live Cheat Sheet

| Task                  | Command / Tool                                                       |
| --------------------- | -------------------------------------------------------------------- |
| Edit code             | Your IDE (VS Code, etc.)                                             |
| Run frontend locally  | `npm run dev`                                                        |
| Commit changes        | `git add . && git commit`                                            |
| Push to deploy        | `git push origin main`                                               |
| Trigger manual deploy | Vercel Dashboard → Redeploy                                          |
| View live site        | [https://fruitstoroots.vercel.app](https://fruitstoroots.vercel.app) |

---

For backend deploy instructions, see `backend/deploy.sh` and `rotate-openai-key.sh`.
