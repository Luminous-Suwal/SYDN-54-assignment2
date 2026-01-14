import csv
import os
import math
from collections import defaultdict

def analyze_weather_data():
    # Find the folder where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(script_dir, 'temperatures')
    
    # Season groupings based on your column names
    seasons_map = {
        'Summer': ['December', 'January', 'February'],
        'Autumn': ['March', 'April', 'May'],
        'Winter': ['June', 'July', 'August'],
        'Spring': ['September', 'October', 'November']
    }

    seasonal_all_temps = defaultdict(list) 
    station_all_temps = defaultdict(list)  

    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' not found.")
        return

    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    
    for filename in csv_files:
        file_path = os.path.join(folder_path, filename)
        with open(file_path, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            # Clean headers to remove any hidden spaces
            reader.fieldnames = [name.strip() for name in reader.fieldnames]
            
            for row in reader:
                station = row['STATION_NAME'].strip()
                
                # Iterate through each month column
                for month_name in ['January', 'February', 'March', 'April', 'May', 'June', 
                                  'July', 'August', 'September', 'October', 'November', 'December']:
                    try:
                        val = row[month_name].strip()
                        if not val or val.lower() == 'nan':
                            continue
                        
                        temp = float(val)
                        
                        # Add to station data for Range and Stability
                        station_all_temps[station].append(temp)
                        
                        # Add to seasonal data
                        for season, months in seasons_map.items():
                            if month_name in months:
                                seasonal_all_temps[season].append(temp)
                                
                    except (ValueError, KeyError):
                        continue

    # --- Task 1: Seasonal Average ---
    with open(os.path.join(script_dir, "average_temp.txt"), "w") as f:
        for s in ["Summer", "Autumn", "Winter", "Spring"]:
            temps = seasonal_all_temps[s]
            if temps:
                avg = sum(temps) / len(temps)
                f.write(f"{s}: {avg:.1f}°C\n")

    # --- Task 2: Temperature Range ---
    station_metrics = {}
    max_range = -1.0
    
    for station, temps in station_all_temps.items():
        r = max(temps) - min(temps)
        station_metrics[station] = (r, max(temps), min(temps))
        if r > max_range:
            max_range = r

    with open(os.path.join(script_dir, "largest_temp_range_station.txt"), "w") as f:
        for station, (r, hi, lo) in station_metrics.items():
            if math.isclose(r, max_range):
                f.write(f"Station {station}: Range {r:.1f}°C (Max: {hi:.1f}°C, Min: {lo:.1f}°C)\n")

    # --- Task 3: Temperature Stability ---
    def get_std_dev(data):
        if len(data) < 2: return 0.0
        mean = sum(data) / len(data)
        variance = sum((x - mean) ** 2 for x in data) / (len(data) - 1)
        return math.sqrt(variance)

    stability = {st: get_std_dev(t) for st, t in station_all_temps.items() if len(t) > 1}
    
    if stability:
        min_sd = min(stability.values())
        max_sd = max(stability.values())

        with open(os.path.join(script_dir, "temperature_stability_stations.txt"), "w") as f:
            for st, sd in stability.items():
                if math.isclose(sd, min_sd):
                    f.write(f"Most Stable: Station {st}: StdDev {sd:.1f}°C\n")
            for st, sd in stability.items():
                if math.isclose(sd, max_sd):
                    f.write(f"Most Variable: Station {st}: StdDev {sd:.1f}°C\n")

    print("Success! Processed the data. Check your text files.")

if __name__ == "__main__":
    analyze_weather_data()