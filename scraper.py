import pandas as pd
import requests
import io
import time

def scrape_hospital_data():
    # We add a unique timestamp (?v=) to the URL. 
    # This forces the government server to give us a fresh file.
    timestamp = int(time.time())
    url = f"https://www.msss.gouv.qc.ca/professionnels/statistiques/documents/urgences/urgences_live.csv?v={timestamp}"
    
    print(f"Fetching data from: {url}")
    
    try:
        # 1. Fetch the data
        response = requests.get(url)
        
        # Use 'iso-8859-1' to handle Quebec's specific French characters (é, ê, ô)
        response.encoding = 'iso-8859-1' 
        
        if response.status_code == 200:
            # 2. Read the CSV using 'latin1' to match the government's encoding
            df = pd.read_csv(io.StringIO(response.text), encoding='latin1')
            
            # 3. Save it to your repo as a clean UTF-8 CSV
            # This is the file your Google Script will read
            df.to_csv("urgences_live.csv", index=False, encoding='utf-8')
            
            # Print the last update time from the data to your GitHub log
            if 'Mise_a_jour' in df.columns:
                last_update = df['Mise_a_jour'].iloc[0]
                print(f"Success! Data timestamp in file is: {last_update}")
            else:
                print("Successfully updated urgences_live.csv (Timestamp column not found)")
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    scrape_hospital_data()
