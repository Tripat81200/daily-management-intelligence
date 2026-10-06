# Daily Management Intelligence 🚀
> **A fully automated, cloud-native daily executive intelligence briefing designed for MBA students, strategy analysts, and management leaders.**

---

## 🌟 Overview & Vision

**Daily Management Intelligence** is NOT a generic news aggregator. It is a **daily competitive-intelligence briefing** engineered to give you an unfair information and strategic advantage in boardrooms, case competitions, MBA classroom discussions, and executive roles.

Every morning, the system autonomously:
1. **Scours the Web**: Ingests fresh, verified business developments from the previous 24–48 hours across top publications (*LiveMint, Economic Times, Reuters, CNBC, Supply Chain Brain, Marketing Dive, Bloomberg, Financial Times*).
2. **Eliminates Noise**: Ruthlessly filters out clickbait, celebrity news, sports scores, and surface-level noise, selecting only stories with strategic, financial, operational, or marketing significance.
3. **Applies Multi-Factor Scoring**: Prioritizes **Operations** and **Marketing**, with balanced coverage across **Strategy, Finance, Economics, Enterprise Tech/AI, India Business, and Global Macro**.
4. **Applies Senior Consultant AI Synthesis**: Employs a McKinsey/BCG strategy partner + MBA professor persona to analyze each story across three deliberate tiers:
   - **Understand**: *What actually happened?* (2–3 concise sentences)
   - **Analyze**: *Why does this matter?* (Strategic mechanism, margin pressure, channel conflict)
   - **Teach**: *What is the enduring management takeaway?*
   - **Competitive Advantage Layer**: *What second-order implication did casual readers miss?*
5. **Renders & Delivers a Polished HTML Email**: Sends an executive, mobile-responsive briefing formatted for an **8–12 minute read**, complete with verified source links, **"The Management Lesson of the Day"**, and a **"60-Second Scan"**.

---

## ☁️ Architecture (100% Cloud-Only)

```
┌────────────────────────────────────────────────────────┐
│  GitHub Actions Scheduled Cron (Daily 7:00 AM IST)     │
│  [Runs in Cloud: No laptop or local server needed]     │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│ 1. News Ingestion (Google News RSS + Direct RSS)       │
│    • Ingests 150-250 candidate stories                 │
│    • Deduplicates against 14-day history storage       │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│ 2. Multi-Criteria Scoring & Bucketing                  │
│    • Weights: Impact (25%), Mgmt (20%), Ops (15%),    │
│      Mkt (15%), Strategy (10%), Recency (10%), Moat    │
│    • Buckets: Top 5, Operations, Marketing, Strategy,  │
│      Tech/AI, India, Global                            │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│ 3. AI Intelligence Synthesis (Google Gemini Flash API) │
│    • Structured JSON extraction                        │
│    • Second-order thinking & managerial mental models  │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│ 4. Executive Newsletter Rendering (Jinja2 HTML Engine) │
│    • Responsive, modern executive design               │
│    • Generates HTML + Plain-text fallback              │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│ 5. Automated Cloud Delivery (Resend API or Gmail SMTP) │
│    • Delivers straight to your primary inbox           │
│    • Uploads HTML preview artifact to GitHub Actions   │
│    • Commits updated history JSON back to repo         │
└────────────────────────────────────────────────────────┘
```

> [!IMPORTANT]
> **Zero Local Requirements**: Your computer can be powered off, asleep, or disconnected. The entire pipeline runs on GitHub's cloud runners and scheduled cron jobs.

---

## 💰 Cost Breakdown (Target: ₹0 / $0 per month)

| Service | Role | Free Tier Allowance | Our Daily Usage | Monthly Cost |
| :--- | :--- | :--- | :--- | :--- |
| **GitHub Actions** | Cloud Workflow Runner | 2,000 min/mo (private) / Unlimited (public) | ~1.5 min/day (~45 min/mo) | **₹0.00** |
| **Google Gemini API** | AI Analysis & Synthesis | 15 requests/min, 1,500 requests/day | 1–2 requests/day | **₹0.00** |
| **Google News & RSS** | Fresh News Collection | 100% Free & Open | No API keys needed | **₹0.00** |
| **Resend Email API** | Cloud Email Delivery | 3,000 emails/month (100/day) | 1 email/day | **₹0.00** |
| **Gmail SMTP (Alt)** | Alternative Delivery | 500 emails/day | 1 email/day | **₹0.00** |
| **TOTAL** | | | | **₹0 / month** |

---

## 🚀 Quick Setup Guide

### Step 1: Push Code to GitHub
1. Create a new repository on GitHub (e.g. `daily-management-intelligence`).
2. In your terminal inside this folder:
```bash
git init
git add .
git commit -m "Initial commit of Daily Management Intelligence pipeline"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/daily-management-intelligence.git
git push -u origin main
```

---

### Step 2: Add GitHub Secrets
Go to your repository on GitHub:
**Settings → Secrets and variables → Actions → New repository secret**

Add the following secrets:

#### 1. Required Secrets:
* `GEMINI_API_KEY`: Your Google Gemini API key.
  * Get one free in 30 seconds at [Google AI Studio](https://aistudio.google.com/).
* `EMAIL_TO`: Your email address where you want to receive the daily briefing (e.g., `you@gmail.com`).

#### 2. Email Delivery Secrets (Choose Option A or Option B):

**Option A (Recommended: Resend API)**:
* `EMAIL_SERVICE`: `resend`
* `RESEND_API_KEY`: Your API key from [Resend](https://resend.com) (Free 3,000 emails/month).
* `EMAIL_FROM`: `Management Intelligence <onboarding@resend.dev>` (or your verified domain).

**Option B (Standard Gmail SMTP)**:
* `EMAIL_SERVICE`: `smtp`
* `SMTP_HOST`: `smtp.gmail.com`
* `SMTP_PORT`: `587`
* `SMTP_USER`: Your Gmail address (e.g., `you@gmail.com`)
* `SMTP_PASS`: A 16-character [Google App Password](https://myaccount.google.com/apppasswords) *(Note: Use an App Password, not your normal password)*
* `EMAIL_FROM`: `Daily Management Intelligence <you@gmail.com>`

---

### Step 3: Grant Workflow Write Permissions (For History Tracking)
To allow GitHub Actions to save `data/history/sent_stories.json` automatically so stories are never repeated:
1. Go to repository **Settings → Actions → General**.
2. Scroll to **Workflow permissions**.
3. Select **"Read and write permissions"** and click **Save**.

---

### Step 4: Test Immediately (Manual Run)
You don't need to wait until tomorrow morning to test:
1. Go to your repository's **Actions** tab on GitHub.
2. Select **Daily Management Intelligence Briefing** from the left sidebar.
3. Click **Run workflow**.
4. Check your inbox after ~90 seconds!
5. In addition, every run uploads `daily-briefing-html` under the action's **Artifacts** section so you can inspect the exact HTML in your browser.

---

## ⏰ Changing the Daily Delivery Schedule

The schedule is controlled by the cron expression in [`.github/workflows/daily-newsletter.yml`](.github/workflows/daily-newsletter.yml#L18):

```yaml
on:
  schedule:
    - cron: '30 1 * * *'  # 1:30 AM UTC = 7:00 AM IST
```

### Timezone Conversion Reference (IST is UTC + 5:30):
| Desired Delivery Time (IST) | Equivalent UTC Time | Cron Syntax |
| :--- | :--- | :--- |
| **6:00 AM IST** | 00:30 UTC | `- cron: '30 0 * * *'` |
| **6:30 AM IST** | 01:00 UTC | `- cron: '0 1 * * *'` |
| **7:00 AM IST (Default)** | 01:30 UTC | `- cron: '30 1 * * *'` |
| **7:30 AM IST** | 02:00 UTC | `- cron: '0 2 * * *'` |
| **8:00 AM IST** | 02:30 UTC | `- cron: '30 2 * * *'` |

Simply change the cron string in the YAML file on GitHub to adjust your delivery time.

---

## ⚙️ Configuration & Customization

All editorial rules, section story quotas, ranking weights, and feed sources are centralized in [`config/config.yaml`](config/config.yaml):

```yaml
# Section quotas
content:
  top_stories_count: 5
  operations_stories_count: 3
  marketing_stories_count: 3
  strategy_finance_stories_count: 3
  tech_ai_stories_count: 2
  india_business_stories_count: 3
  global_business_stories_count: 2

# Scoring weights
ranking:
  weights:
    business_impact: 0.25
    management_relevance: 0.20
    operations_relevance: 0.15
    marketing_relevance: 0.15
    strategic_importance: 0.10
    recency: 0.10
    novelty: 0.05
  threshold_min_score: 0.35
  history_retention_days: 14 # Excludes stories covered in past 14 days
```

---

## 🧪 Local Development & Testing

If you ever wish to test or develop locally:

```bash
# 1. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run unit test suite
pytest tests/

# 4. Generate local briefing preview (without sending email)
python main.py --dry-run
# Preview saved to: data/sample_briefing.html
```

---

## 🛠️ Maintenance & Monitoring

- **Zero Daily Maintenance**: The cloud workflow triggers automatically every single day.
- **Deduplication Persistence**: After every successful run, the GitHub runner automatically commits `data/history/sent_stories.json` with `[skip ci]`, ensuring history persists in the repository across daily executions.
- **Artifact Backups**: Each workflow run archives the generated HTML briefing as a GitHub Actions Artifact for 7 days.
- **Fail-Safe Resilience**: If a particular RSS source is down or slow, the collector continues with other sources. If AI generation experiences a temporary network blip, exponential backoff retries automatically.
