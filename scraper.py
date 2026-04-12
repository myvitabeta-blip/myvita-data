import pandas as pd
import requests
import io
import time

def scrape_hospital_data():
    # 1. Unique timestamp to fool the server's cache
    timestamp = int(time.time())
    url = f"https://www.msss.gouv.qc.ca/professionnels/statistiques/documents/urgences/urgences_live.csv?v={timestamp}"
    
    # 2. Add "Headers" to tell the government server: "Do not give me old data"
    headers = {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0',
        'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) GitHubAction/{timestamp}'
    }

    print(f"Fetching fresh data from: {url}")
    
    try:
        # Use headers in the request
        response = requests.get(url, headers=headers)
        response.encoding = 'iso-8859-1' 
        
        if response.status_code == 200:
            df = pd.read_csv(io.StringIO(response.text), encoding='latin1')
            
            # Save to your repo
            df.to_csv("urgences_live.csv", index=False, encoding='utf-8')
            
            if 'Mise_a_jour' in df.columns:
                last_update = df['Mise_a_jour'].iloc[0]
                print(f"SCRAPER LOG: Found data timestamp: {last_update}")
                
                # Alert you if it's still the old date
                if "2026-04-10" in str(last_update):
                    print("⚠️ WARNING: Server is still serving the April 10th file despite the refresh.")
                else:
                    print("✅ SUCCESS: Data is updated to today!")
        else:
            print(f"Failed. Status: {response.status_code}")
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    scrape_hospital_data()
