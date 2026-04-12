import pandas as pd
import requests
import io

def scrape_hospital_data():
    # Official Quebec Government Open Data URL for Emergency Room Wait Times
    url = "https://www.msss.gouv.qc.ca/professionnels/statistiques/documents/urgences/urgences_live.csv"
    
    try:
        # 1. Fetch the data
        response = requests.get(url)
        response.encoding = 'utf-8' # Ensure French characters are handled
        
        if response.status_code == 200:
            # 2. Read the CSV
            df = pd.read_csv(io.StringIO(response.text))
            
            # 3. Save it to your repo
            # This overwrites the old 12:45 file with fresh data
            df.to_csv("urgences_live.csv", index=False)
            print("Successfully updated urgences_live.csv")
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    scrape_hospital_data()
