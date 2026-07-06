import datetime
import pandas as pd
import urllib.parse
import yfinance as yf
from sqlalchemy import create_engine, types

# Fixed Connection Settings
SERVER = "."
DATABASE = "FinancialDB"
#connection_string = f"mssql+pyodbc://@{SERVER}/{DATABASE}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
# Connection Settings for Supabase Cloud (Postgres)
raw_password = "theblueskyG@123"
encoded_password = urllib.parse.quote_plus(raw_password)
connection_string = f"postgresql+psycopg2://postgres:{encoded_password}@db.wzxaotzomwlkrudvmpwy.supabase.co:5432/postgres"

def fetch_historical_rates():
    print("🚀 Starting Historical Data ETL Pipeline (Big Data Scale)...")
    
    # تحديد العملات اللي عايزين نراقبها ونجيب تاريخها مقابل الدولار
    # في Yahoo Finance، رمز العملة بيكتب كدة: EURUSD=X (معناه كم دولار لكل 1 يورو)
    # إحنا هنعكس الحسبة جوه الكود عشان تتماشى مع الـ API بتاعنا (كم عملة محلية لكل 1 دولار)
    currencies = {
        'EURUSD=X': 'EUR',
        'GBPUSD=X': 'GBP',
        'EGP=X': 'EGP',
        'USDSAR=X': 'SAR',
        'AED=X': 'AED',
        'KWD=X': 'KWD',
        'JPY=X': 'JPY'
    }
    
    start_date = "2020-01-01"
    end_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    historical_df_list = []
    
    print(f"🌐 Fetching daily data from {start_date} to {end_date} from Yahoo Finance...")
    
    for ticker, code in currencies.items():
        try:
            print(f"📥 Downloading historical data for: {code}...")
            # سحب الداتا من ياهو فاينانس
            data = yf.download(ticker, start=start_date, end=end_date, interval="1d")
            
            if data.empty:
                continue
                
            # إعادة ترتيب وتصحيح شكل الـ DataFrame القادم من yfinance
            df = data[['Close']].copy()
            df = df.reset_index()
            df.columns = ['Date', 'ExchangeRate']
            
            # تصحيح الحسبة للعملات المقلوبة في ياهو (زي اليورو والإسترليني)
            if ticker in ['EURUSD=X', 'GBPUSD=X']:
                df['ExchangeRate'] = 1 / df['ExchangeRate']
                
            # إضافة الـ Metadata
            df['CurrencyCode'] = code
            df['BaseCurrency'] = 'USD'
            
            historical_df_list.append(df)
            
        except Exception as e:
            print(f"⚠️ Error downloading {code}: {e}")
            
    if not historical_df_list:
        print("❌ No data was retrieved!")
        return
        
    # دمج داتا كل العملات في جدول واحد ضخم
    final_df = pd.concat(historical_df_list, ignore_index=True)
    
    # تنظيف سريع للداتا (مسح أي قيم فاضية)
    final_df = final_df.dropna()
    
    print(f"🧹 Data Transformation complete. Total rows generated: {len(final_df)}")
    
    # ----------------------------------------
    # LOAD STAGE: ضخ ملايين/آلاف السطور في SQL Server
    # ----------------------------------------
    print("🗄️ Loading Historical Data into SQL Server...")
    try:
        engine = create_engine(connection_string)
        
        data_types = {
            'Date': types.DateTime(),
            'CurrencyCode': types.VARCHAR(length=10),
            'ExchangeRate': types.Float(precision=53),
            'BaseCurrency': types.VARCHAR(length=10)
        }
        
        # هنرمي الداتا في جدول جديد تماماً للمستندات التاريخية
        final_df.to_sql(
            name='Fact_HistoricalExchangeRates', 
            con=engine, 
            if_exists='replace', 
            index=False,
            dtype=data_types
        )
        print("⚡ SUCCESS: Table [Fact_HistoricalExchangeRates] created and populated successfully!")
        
    except Exception as e:
        print(f"❌ LOAD STAGE FAILED: {e}")

if __name__ == "__main__":
    fetch_historical_rates()