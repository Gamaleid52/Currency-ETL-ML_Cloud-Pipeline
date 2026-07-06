# 📈 Enterprise Cloud Big Data & ML Currency Pipeline


An enterprise-grade, fully automated Cloud Data Engineering and Machine Learning pipeline. The system extracts daily and historical global currency exchange rates, processes high-volume time-series data, and utilizes predictive modeling to forecast market trends.

### 📊 Real-World Data Sources
To ensure production-grade accuracy, this pipeline utilizes 100% real-world financial data:
* **Historical Data:** Extracted multi-year historical daily closes (Big Data Scale) directly from **Yahoo Finance** via `yfinance` to train the ML model on true market behaviors and seasonality.
* **Live/Real-Time Data:** Fetched continuously from **ExchangeRate-API** to provide instantaneous up-to-date currency valuation on the dashboard.

### 🏗️ Architecture Overview
The architecture is designed following modern cloud data warehousing guidelines:
1. **Data Extraction (ETL):** Ingests live data and historical daily ticks using `pandas` & financial APIs.
2. **Cloud Data Warehouse (Supabase / Postgres):** Structured remote storage leveraging optimized schemas, connection pooling via Supabase Cloud Pooler (Port 6543) to bypass DNS/network bottlenecks.
3. **Predictive Analytics (ML Engine):** A time-series forecasting engine powered by **Facebook Prophet**, optimized for capturing seasonality (daily, weekly, and yearly trends), outputting a 30-day future horizon.
4. **Cloud Automation:** Fully orchestrated using **GitHub Actions** to awake daily at 00:00 UTC, run the ETL, retrain the model, and update the cloud warehouse completely serverless.
5. **Data Visualization:** An interactive data application developed via **Streamlit Community Cloud** and **Plotly**, rendering real-time metrics and live forecasting charts.

### 🛠️ Tech Stack
* **Language:** Python 3.x
* **Data Engineering:** Pandas, SQLAlchemy, Psycopg2, yFinance
* **Cloud Database:** Supabase (PostgreSQL Cloud)
* **Automation:** GitHub Actions (CI/CD workflows)
* **Machine Learning:** Prophet (FbProphet)
* **BI & Analytics:** Streamlit Cloud, Plotly

---



مشروع متكامل بمواصفات الشركات الكبرى (Enterprise-Grade) لبناء خط أنابيب بيانات سحابي (Cloud Data Pipeline) مع دمج تقنيات تعلم الآلة (ML). يقوم النظام بسحب أسعار العملات العالمية التاريخية واللحظية الحقيقية، ومعالجتها كبيانات زمنية ضخمة، ثم التنبؤ باتجاهات السوق المستقبلية.

### 📊 مصادر البيانات الحقيقية
لضمان محاكاة بيئات العمل الحقيقية، يعتمد النظام بنسبة 100% على مصادر بيانات مالية دولية:
* **البيانات التاريخية:** يتم سحب أسعار الإغلاق اليومية الحقيقية لسنوات سابقة مباشرة من **Yahoo Finance** عبر مكتبة `yfinance` لتدريب موديل تعلم الآلة على سلوك السوق الحقيقي وتقلباته.
* **البيانات اللحظية:** يتم جلب أسعار الصرف الفورية والمباشرة من خلال **ExchangeRate-API** لتحديث لوحة التحكم أولاً بأول بأسعار البورصة الحالية.

### 🏗️ نظرة عامة على هندسة النظام
تم تصميم النظام بناءً على أفضل الممارسات في هندسة البيانات والموديلات الإنتاجية السحابية:
1. **مرحلة سحب ومعالجة البيانات (ETL):** سحب البيانات اللحظية والتاريخية بدقة (Big Data Scale) من واجهات برمجة التطبيقات المالية باستخدام `pandas`.
2. **مستودع البيانات السحابي (Supabase / Postgres):** تخزين البيانات في قاعدة بيانات سحابية مُحسّنة، مع ربطها عبر الـ Supabase Cloud Pooler (بورت 6543) لضمان استقرار الاتصال وتخطي عقبات الـ DNS.
3. **التحليلات التنبؤية (تعلم الآلة):** محرك تنبؤ زمني معتمد على موديل **Facebook Prophet**، تم تدريبه لتحليل الأنماط الموسمية (اليومية، الأسبوعية، والسنوية) وتوقع حركة العملات لـ 30 يوماً قادمة.
4. **الأتمتة السحابية الكاملة:** دمج أداة **GitHub Actions** لتشغيل كامل الـ Pipeline والموديل تلقائياً كل يوم الساعة 12 منتصف الليل بتوقيت جرينتش لتحديث البيانات بدون أي تدخل بشري وجهازك مغلق.
5. **عرض البيانات (Dashboard):** لوحة تحكم تفاعلية حية مرفوعة على **Streamlit Community Cloud** ومبنية بـ **Plotly** لعرض التوقعات والمؤشرات مباشرة للمستخدمين 24/7.

### 🛠️ التقنيات المستخدمة
* **لغة البرمجة:** Python 3.x
* **هندسة البيانات:** Pandas, SQLAlchemy, Psycopg2, yFinance
* **قواعد البيانات السحابية:** Supabase (PostgreSQL Cloud)
* **الأتمتة سيرفرليس:** GitHub Actions
* **تعلم الآلة:** Prophet (FbProphet)
* **واجهات العرض:** Streamlit Cloud, Plotly