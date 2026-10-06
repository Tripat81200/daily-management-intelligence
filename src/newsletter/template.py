"""HTML and text email templates for Daily Management Intelligence."""

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{ edition_name }} - {{ formatted_date }}</title>
  <style>
    body {
      margin: 0;
      padding: 0;
      background-color: #f1f5f9;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      color: #1e293b;
      -webkit-font-smoothing: antialiased;
      line-height: 1.6;
    }
    table {
      border-collapse: collapse;
    }
    .wrapper {
      width: 100%;
      background-color: #f1f5f9;
      padding: 24px 8px;
    }
    .container {
      max-width: 660px;
      margin: 0 auto;
      background-color: #ffffff;
      border-radius: 12px;
      overflow: hidden;
      box-shadow: 0 4px 16px rgba(15, 23, 42, 0.06);
      border: 1px solid #e2e8f0;
    }
    .header {
      background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
      color: #ffffff;
      padding: 32px 28px;
      text-align: left;
      border-bottom: 3px solid #3b82f6;
    }
    .edition-badge {
      display: inline-block;
      background-color: #2563eb;
      color: #ffffff;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1px;
      padding: 4px 10px;
      border-radius: 4px;
      margin-bottom: 12px;
    }
    .header h1 {
      margin: 0 0 8px 0;
      font-size: 24px;
      font-weight: 800;
      letter-spacing: -0.5px;
      line-height: 1.25;
      color: #ffffff;
    }
    .header-meta {
      font-size: 13px;
      color: #94a3b8;
      display: flex;
      justify-content: space-between;
      margin-top: 8px;
    }
    .content-body {
      padding: 28px;
    }
    .big-picture-box {
      background-color: #f8fafc;
      border-left: 4px solid #2563eb;
      padding: 16px 20px;
      border-radius: 0 8px 8px 0;
      margin-bottom: 28px;
    }
    .big-picture-title {
      font-size: 13px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      color: #2563eb;
      margin-bottom: 6px;
    }
    .big-picture-text {
      font-size: 15px;
      color: #334155;
      margin: 0;
      line-height: 1.6;
    }
    .section-header {
      border-bottom: 2px solid #e2e8f0;
      padding-bottom: 8px;
      margin: 32px 0 18px 0;
    }
    .section-title {
      font-size: 17px;
      font-weight: 800;
      letter-spacing: -0.3px;
      color: #0f172a;
      display: inline-block;
      margin: 0;
      text-transform: uppercase;
    }
    .section-badge {
      font-size: 11px;
      font-weight: 600;
      padding: 2px 8px;
      border-radius: 4px;
      margin-left: 8px;
      vertical-align: middle;
    }
    .badge-ops { background-color: #e0f2fe; color: #0369a1; }
    .badge-mkt { background-color: #fef3c7; color: #b45309; }
    .badge-strat { background-color: #ede9fe; color: #6d28d9; }
    .badge-tech { background-color: #ecfdf5; color: #047857; }
    .badge-india { background-color: #ffedd5; color: #c2410c; }
    .badge-global { background-color: #f1f5f9; color: #475569; }

    .card {
      background-color: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      padding: 18px;
      margin-bottom: 18px;
      transition: all 0.2s ease;
    }
    .card-headline {
      font-size: 16px;
      font-weight: 700;
      color: #0f172a;
      margin: 0 0 10px 0;
      line-height: 1.4;
    }
    .card-block {
      margin-bottom: 8px;
      font-size: 14px;
      line-height: 1.55;
      color: #334155;
    }
    .card-block strong {
      color: #0f172a;
      font-weight: 600;
    }
    .card-adv {
      background-color: #eff6ff;
      border-radius: 6px;
      padding: 10px 12px;
      margin-top: 10px;
      font-size: 13px;
      color: #1e40af;
      line-height: 1.5;
    }
    .source-tag {
      display: block;
      margin-top: 10px;
      font-size: 12px;
      color: #64748b;
    }
    .source-tag a {
      color: #2563eb;
      text-decoration: none;
      font-weight: 500;
    }
    .source-tag a:hover {
      text-decoration: underline;
    }

    .lesson-box {
      background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
      color: #ffffff;
      padding: 24px;
      border-radius: 10px;
      margin: 36px 0 24px 0;
      border-left: 5px solid #10b981;
    }
    .lesson-tag {
      color: #10b981;
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 6px;
    }
    .lesson-title {
      font-size: 18px;
      font-weight: 800;
      color: #ffffff;
      margin: 0 0 10px 0;
    }
    .lesson-text {
      font-size: 14px;
      color: #cbd5e1;
      margin: 0;
      line-height: 1.6;
    }

    .scan-box {
      background-color: #f8fafc;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      padding: 18px 20px;
      margin: 28px 0;
    }
    .scan-item {
      font-size: 13px;
      padding: 6px 0;
      border-bottom: 1px dashed #e2e8f0;
      color: #334155;
    }
    .scan-item:last-child {
      border-bottom: none;
    }
    .scan-pillar {
      font-weight: 700;
      color: #0f172a;
      display: inline-block;
      width: 100px;
    }

    .footer {
      background-color: #0f172a;
      color: #94a3b8;
      padding: 24px;
      text-align: center;
      font-size: 12px;
      border-top: 1px solid #1e293b;
    }
    .footer a {
      color: #60a5fa;
      text-decoration: none;
    }
  </style>
</head>
<body>
  <div class="wrapper">
    <div class="container">
      
      <!-- HEADER -->
      <div class="header">
        <span class="edition-badge">Executive Daily Briefing</span>
        <h1>{{ edition_name }}</h1>
        <div style="font-size: 14px; color: #cbd5e1; margin-bottom: 8px;">{{ tagline }}</div>
        <div class="header-meta">
          <span>📅 {{ formatted_date }}</span>
          <span>⏱️ ~{{ reading_time_minutes }} min read</span>
        </div>
      </div>

      <div class="content-body">
        
        <!-- TODAY'S BIG PICTURE -->
        <div class="big-picture-box">
          <div class="big-picture-title">🌐 Today's Big Picture</div>
          <p class="big-picture-text">{{ big_picture }}</p>
        </div>

        <!-- TOP 5 — MUST KNOW -->
        <div class="section-header">
          <h2 class="section-title">🔥 TOP 5 — MUST KNOW</h2>
        </div>
        {% for item in top_5 %}
        <div class="card">
          <h3 class="card-headline">{{ loop.index }}. {{ item.headline }}</h3>
          <div class="card-block"><strong>What happened:</strong> {{ item.what_happened }}</div>
          <div class="card-block"><strong>Why it matters:</strong> {{ item.why_it_matters }}</div>
          <div class="card-block"><strong>Management takeaway:</strong> {{ item.management_takeaway }}</div>
          {% if item.competitive_advantage %}
          <div class="card-adv">
            <strong>💡 Second-Order Implication:</strong> {{ item.competitive_advantage }}
          </div>
          {% endif %}
          <span class="source-tag">Source: <a href="{{ item.source_url }}" target="_blank">{{ item.source_name }}</a></span>
        </div>
        {% endfor %}

        <!-- OPERATIONS INTELLIGENCE -->
        <div class="section-header">
          <h2 class="section-title">⚙️ OPERATIONS INTELLIGENCE</h2>
          <span class="section-badge badge-ops">Special Focus</span>
        </div>
        {% for item in operations %}
        <div class="card">
          <h3 class="card-headline">{{ item.headline }}</h3>
          <div class="card-block"><strong>What happened:</strong> {{ item.what_happened }}</div>
          <div class="card-block"><strong>Operational impact:</strong> {{ item.why_it_matters_operationally }}</div>
          <div class="card-block"><strong>Operational lesson:</strong> {{ item.operational_lesson }}</div>
          <span class="source-tag">Source: <a href="{{ item.source_url }}" target="_blank">{{ item.source_name }}</a></span>
        </div>
        {% endfor %}

        <!-- MARKETING INTELLIGENCE -->
        <div class="section-header">
          <h2 class="section-title">📣 MARKETING INTELLIGENCE</h2>
          <span class="section-badge badge-mkt">Special Focus</span>
        </div>
        {% for item in marketing %}
        <div class="card">
          <h3 class="card-headline">{{ item.headline }}</h3>
          <div class="card-block"><strong>What happened:</strong> {{ item.what_happened }}</div>
          <div class="card-block"><strong>Marketing/Customer impact:</strong> {{ item.why_it_matters_marketing }}</div>
          <div class="card-block"><strong>Marketing lesson:</strong> {{ item.marketing_lesson }}</div>
          <span class="source-tag">Source: <a href="{{ item.source_url }}" target="_blank">{{ item.source_name }}</a></span>
        </div>
        {% endfor %}

        <!-- STRATEGY & FINANCE -->
        <div class="section-header">
          <h2 class="section-title">📊 STRATEGY & FINANCE</h2>
          <span class="section-badge badge-strat">Core</span>
        </div>
        {% for item in strategy_finance %}
        <div class="card">
          <h3 class="card-headline">{{ item.headline }}</h3>
          <div class="card-block"><strong>Development:</strong> {{ item.what_happened }}</div>
          <div class="card-block"><strong>Strategic takeaway:</strong> {{ item.strategic_takeaway }}</div>
          <span class="source-tag">Source: <a href="{{ item.source_url }}" target="_blank">{{ item.source_name }}</a></span>
        </div>
        {% endfor %}

        <!-- TECHNOLOGY & AI -->
        <div class="section-header">
          <h2 class="section-title">🤖 TECHNOLOGY & AI</h2>
          <span class="section-badge badge-tech">Enterprise Impact</span>
        </div>
        {% for item in tech_ai %}
        <div class="card">
          <h3 class="card-headline">{{ item.headline }}</h3>
          <div class="card-block"><strong>Development:</strong> {{ item.what_happened }}</div>
          <div class="card-block"><strong>Business implication:</strong> {{ item.business_implication }}</div>
          <span class="source-tag">Source: <a href="{{ item.source_url }}" target="_blank">{{ item.source_name }}</a></span>
        </div>
        {% endfor %}

        <!-- INDIA BUSINESS -->
        <div class="section-header">
          <h2 class="section-title">🇮🇳 INDIA BUSINESS</h2>
          <span class="section-badge badge-india">Emerging Market</span>
        </div>
        {% for item in india_business %}
        <div class="card">
          <h3 class="card-headline">{{ item.headline }}</h3>
          <div class="card-block"><strong>Development:</strong> {{ item.what_happened }}</div>
          <div class="card-block"><strong>Market insight:</strong> {{ item.india_market_insight }}</div>
          <span class="source-tag">Source: <a href="{{ item.source_url }}" target="_blank">{{ item.source_name }}</a></span>
        </div>
        {% endfor %}

        <!-- GLOBAL BUSINESS -->
        <div class="section-header">
          <h2 class="section-title">🌎 GLOBAL BUSINESS</h2>
          <span class="section-badge badge-global">Macro</span>
        </div>
        {% for item in global_business %}
        <div class="card">
          <h3 class="card-headline">{{ item.headline }}</h3>
          <div class="card-block"><strong>Development:</strong> {{ item.what_happened }}</div>
          <div class="card-block"><strong>Macro impact:</strong> {{ item.macro_impact }}</div>
          <span class="source-tag">Source: <a href="{{ item.source_url }}" target="_blank">{{ item.source_name }}</a></span>
        </div>
        {% endfor %}

        <!-- THE MANAGEMENT LESSON OF THE DAY -->
        {% if lesson_of_the_day %}
        <div class="lesson-box">
          <div class="lesson-tag">🧠 THE MANAGEMENT LESSON OF THE DAY</div>
          <div class="lesson-title">{{ lesson_of_the_day.title }}</div>
          <p class="lesson-text">{{ lesson_of_the_day.explanation }}</p>
        </div>
        {% endif %}

        <!-- 60-SECOND SCAN -->
        {% if sixty_second_scan %}
        <div class="scan-box">
          <div style="font-size: 14px; font-weight: 800; text-transform: uppercase; margin-bottom: 12px; color: #0f172a;">
            ⚡ 60-SECOND SCAN
          </div>
          {% for scan in sixty_second_scan %}
          <div class="scan-item">
            <span class="scan-pillar">[{{ scan.pillar }}]</span>
            <span>{{ scan.takeaway }}</span>
          </div>
          {% endfor %}
        </div>
        {% endif %}

      </div>

      <!-- FOOTER -->
      <div class="footer">
        <p style="margin: 0 0 6px 0; font-weight: 600;">Daily Management Intelligence</p>
        <p style="margin: 0 0 6px 0;">Curated and synthesized via cloud-native AI pipeline for MBA leaders.</p>
        <p style="margin: 0; color: #64748b;">Automated daily execution • Zero manual intervention required</p>
      </div>

    </div>
  </div>
</body>
</html>
"""
