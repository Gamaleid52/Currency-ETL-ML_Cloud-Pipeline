# 📈 Enterprise Cloud Big Data & ML Currency Pipeline

---


An enterprise-grade, fully automated Cloud Data Engineering and Machine Learning pipeline. The system extracts daily and historical global currency exchange rates, processes high-volume time-series data, and utilizes predictive modeling to forecast market trends.

### 🏗️ Architecture Overview
The architecture is designed following production-grade ML and modern cloud data warehousing guidelines:
1. **Data Extraction (ETL):** Ingests live data from Exchange Rate API and historical daily ticks (Big Data Scale) from Yahoo Finance using `pandas` & `yfinance`.
2. **Cloud Data Warehouse (Supabase / Postgres):** Structured remote storage leveraging optimized schemas, case-sensitive identifiers, and efficient query pooling to eliminate performance bottlenecks.
3. **Predictive Analytics (ML Engine):** A time-series forecasting engine powered by **Facebook Prophet**, optimized for capturing additive and multiplicative seasonality (daily, weekly, and yearly trends), outputting a 30-day future horizon.
4. **Data Visualization:** An interactive data application developed via **Streamlit Community Cloud** and **Plotly**, rendering real-time metrics and live forecasting charts.

### 🛠️ Tech Stack
* **Language:** Python 3.x
* **Data Engineering:** Pandas, SQLAlchemy, Psycopg2, yFinance
* **Cloud Database:** Supabase (PostgreSQL Cloud)
* **Machine Learning:** Prophet (FbProphet)
* **BI & Analytics:** Streamlit Cloud, Plotly

---


مشروع متكامل بمواصفات الشركات الكبرى (Enterprise-Grade) لبناء خط أنابيب بيانات سحابي (Cloud Data Pipeline) مع دمج تقنيات تعلم الآلة (ML). يقوم النظام بسحب أسعار العملات العالمية التاريخية واللحظية، ومعالجتها كبيانات زمنية ضخمة، ثم التنبؤ باتجاهات السوق المستقبلية.

### 🏗️ نظرة عامة على هندسة النظام
تم تصميم النظام بناءً على أفضل الممارسات في هندسة البيانات والموديلات الإنتاجية:
1. **مرحلة سحب ومعالجة البيانات (ETL):** سحب البيانات اللحظية والتاريخية بدقة (Big Data Scale) من Yahoo Finance و APIs المعتمدة باستخدام دمج ذكي بين `pandas` و `yfinance`.
2. **مستودع البيانات السحابي (Supabase / Postgres):** تخزين البيانات في قاعدة بيانات سحابية مُحسّنة بالكامل، مع مراعاة العلاقات وحالة الأحرف (Case-Sensitivity) لضمان أعلى سرعة استعلام.
3. **التحليلات التنبؤية (تعلم الآلة):** محرك تنبؤ زمني معتمد على موديل **Facebook Prophet**، تم تدريبه لتحليل الأنماط الموسمية (اليومية، الأسبوعية، والسنوية) وتوقع حركة العملات لـ 30 يوماً قادمة مع تحديد حدود الأمان العلوية والسفلية.
4. **عرض البيانات (Dashboard):** لوحة تحكم تفاعلية حية مرفوعة على **Streamlit Community Cloud** ومبنية بـ **Plotly** لعرض التوقعات والمؤشرات مباشرة للمستخدمين 24/7.

### 🛠️ التقنيات المستخدمة
* **لغة البرمجة:** Python 3.x
* **هندسة البيانات:** Pandas, SQLAlchemy, Psycopg2, yFinance
* **قواعد البيانات السحابية:** Supabase (PostgreSQL Cloud)
* **تعلم الآلة:** Prophet (FbProphet)
* **واجهات العرض:** Streamlit Cloud, Plotly