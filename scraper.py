import pandas as pd
import requests
import io

def scrape_hospital_data():
    url = "https://www.msss.gouv.qc.ca/professionnels/statistiques/documents/urgences/urgences_live.csv"
    
    try:
        response = requests.get(url)
        # CHANGE: Use 'iso-8859-1' to handle Quebec's specific French characters
        response.encoding = 'iso-8859-1' 
        
        if response.status_code == 200:
            # Use 'latin1' here to match the response
            df = pd.read_csv(io.StringIO(response.text), encoding='latin1')
            
            # Save as CSV in your repo
            df.to_csv("urgences_live.csv", index=False, encoding='utf-8')
            print("Successfully updated urgences_live.csv")
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    scrape_hospital_data()
