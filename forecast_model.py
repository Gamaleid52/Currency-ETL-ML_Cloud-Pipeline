import pandas as pd
from sqlalchemy import create_engine, types
from prophet import Prophet
import urllib.parse
import os

# Fixed Connection Settings
SERVER = "."
DATABASE = "FinancialDB"
#connection_string = f"mssql+pyodbc://@{SERVER}/{DATABASE}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
# Connection Settings for Supabase Cloud (Postgres)

# ==========================================
# 🛠️ DATABASE CONNECTION SETTINGS (CLOUD)
# ==========================================
raw_password = "theblueskyG@123"
encoded_password = urllib.parse.quote_plus(raw_password)
connection_string = f"postgresql+psycopg2://postgres:{encoded_password}@db.wzxaotzomwlkrudvmpwy.supabase.co:5432/postgres"


def train_and_forecast():
    print("🤖 Fetching historical data from Supabase Cloud for ML Training...")
    engine = create_engine(connection_string)
    
    # استخدام علامات التنصيص المزدوجة "" لأن PostgreSQL حساسة لحالة الأحرف (Case-Sensitive)
    query = 'SELECT "Date", "CurrencyCode", "ExchangeRate" FROM "Fact_HistoricalExchangeRates"'
    
    try:
        df = pd.read_sql(query, engine)
    except Exception as e:
        print(f"❌ Failed to fetch data: {e}")
        return
    
    if df.empty:
        print("⚠️ No data found in 'Fact_HistoricalExchangeRates'. Exiting...")
        return

    # قائمة العملات المستهدفة للتوقع
    # ملحوظة: تم تعديل رمز الريال السعودي إلى USDSAR=X في سكريبت السحب، وهنا نفلتر بالرمز النظيف المخزن
    target_currencies = ['EGP', 'EUR', 'SAR', 'GBP', 'AED', 'KWD', 'JPY']
    forecast_results = []
    
    print(f"🧠 Training Machine Learning Model (Prophet) for available currencies...")
    
    for code in target_currencies:
        # فلترة الداتا لكل عملة على حدة
        currency_df = df[df['CurrencyCode'] == code].copy()
        
        if currency_df.empty:
            print(f"⚠️ No historical data found for {code}, skipping...")
            continue
            
        # مكتبة Prophet تشترط تسمية الأعمدة كالتالي: الـ Date اسمه 'ds' والـ Value اسمها 'y'
        currency_df = currency_df.rename(columns={'Date': 'ds', 'ExchangeRate': 'y'})
        
        # إزالة منطقة التوقيت (Timezone) إن وجدت لضمان توافق الداتا مع الموديل
        currency_df['ds'] = pd.to_datetime(currency_df['ds']).dt.tz_localize(None)
        
        try:
            # إنشاء وتدريب الموديل مع تفعيل الأنماط الزمنية المختلفة
            model = Prophet(daily_seasonality=True, yearly_seasonality=True, weekly_seasonality=True)
            model.fit(currency_df)
            
            # تجهيز تايم لاين للمستقبل (30 يوم قادمين)
            future = model.make_future_dataframe(periods=30, freq='D')
            
            # عملية التوقع
            forecast = model.predict(future)
            
            # الفلترة لأخذ الأيام المستقبلية فقط (الـ 30 يوم الجداد)
            future_forecast = forecast[forecast['ds'] > currency_df['ds'].max()].copy()
            
            # تجهيز الأعمدة النهائية بالشكل المطابق لقاعدة البيانات
            output_df = pd.DataFrame()
            output_df['Date'] = future_forecast['ds']
            output_df['PredictedRate'] = future_forecast['yhat']        # الرقم المتوقع الأقرب للواقع
            output_df['RateUpperBoundary'] = future_forecast['yhat_upper'] # أعلى سعر متوقع (الأمان)
            output_df['RateLowerBoundary'] = future_forecast['yhat_lower'] # أقل سعر متوقع
            output_df['CurrencyCode'] = code
            output_df['BaseCurrency'] = 'USD'
            
            forecast_results.append(output_df)
            print(f"✅ ML Forecast completed successfully for: {code}.")
            
        except Exception as err:
            print(f"❌ Error training model for {code}: {err}")

    if not forecast_results:
        print("⚠️ No predictions generated. Table update canceled.")
        return

    # دمج كل التوقعات في DataFrame واحد
    final_forecast_df = pd.concat(forecast_results, ignore_index=True)
    
    # ========================================
    # 🗄️ LOAD STAGE: حفظ التوقعات في Supabase
    # ========================================
    print("🗄️ Saving Predictions into Cloud Database [Fact_Predictions]...")
    try:
        # تحديد أنواع البيانات بدقة لتتوافق مع Postgres
        data_types = {
            'Date': types.DateTime(),
            'PredictedRate': types.Float(precision=53),
            'RateUpperBoundary': types.Float(precision=53),
            'RateLowerBoundary': types.Float(precision=53),
            'CurrencyCode': types.VARCHAR(length=10),
            'BaseCurrency': types.VARCHAR(length=10)
        }
        
        # رفع البيانات مع استبدال الجدول إن وجد (replace) لمنع تكرار التوقعات القديمة
        final_forecast_df.to_sql(
            name='Fact_Predictions', 
            con=engine, 
            if_exists='replace', 
            index=False,
            dtype=data_types
        )
        print("⚡ SUCCESS: Machine Learning Predictions updated successfully in Supabase Cloud!")
        
    except Exception as e:
        print(f"❌ FAILED TO SAVE PREDICTIONS TO CLOUD: {e}")

if __name__ == "__main__":
    train_and_forecast()