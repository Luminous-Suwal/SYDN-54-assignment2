import os
import pandas as pd

def process_temperature_data():
    # Folder containing all CSV files
    folder = "temperatures"
    if not os.path.exists(folder):
        print(f"Folder '{folder}' does not exist.")
        return

    all_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".csv")]
    if not all_files:
        print(f"No CSV files found in '{folder}' folder.")
        return

    all_data_frames = []
    for file in all_files:
        try:
            df = pd.read_csv(file)
            all_data_frames.append(df)
        except Exception as e:
            print(f"Error reading {file}: {e}")

    if not all_data_frames:
        print("No valid data could be processed.")
        return

    data = pd.concat(all_data_frames, ignore_index=True)

    months = ["January","February","March","April","May","June",
              "July","August","September","October","November","December"]

    # -----------------------------
    # 1. Seasonal Average
    # -----------------------------
    season_months = {
        "Summer": ["December","January","February"],
        "Autumn": ["March","April","May"],
        "Winter": ["June","July","August"],
        "Spring": ["September","October","November"]
    }

    season_avg = {}
    for season, m in season_months.items():
        values = data[m].values.flatten()
        values = [v for v in values if pd.notna(v)]
        season_avg[season] = sum(values) / len(values)

    # Save and print seasonal averages
    with open("average_temp.txt", "w") as f:
        print("Seasonal Averages:")
        for season in ["Summer","Autumn","Winter","Spring"]:
            line = f"{season}: {season_avg[season]:.1f}°C"
            print(line)
            f.write(line + "\n")

    # -----------------------------
    # 2. Temperature Range per Station
    # -----------------------------
    data["MaxTemp"] = data[months].max(axis=1)
    data["MinTemp"] = data[months].min(axis=1)
    data["Range"] = data["MaxTemp"] - data["MinTemp"]

    max_range = data["Range"].max()
    largest_range_stations = data[data["Range"] == max_range]

    with open("largest_temp_range_station.txt", "w") as f:
        print("\nLargest Temperature Range Station(s):")
        for _, row in largest_range_stations.iterrows():
            line = (f"Station {row['STATION_NAME']}: Range {row['Range']:.1f}°C "
                    f"(Max: {row['MaxTemp']:.1f}°C, Min: {row['MinTemp']:.1f}°C)")
            print(line)
            f.write(line + "\n")

    # -----------------------------
    # 3. Temperature Stability
    # -----------------------------
    data["StdDev"] = data[months].std(axis=1)

    min_std = data["StdDev"].min()
    max_std = data["StdDev"].max()

    most_stable = data[data["StdDev"] == min_std]
    most_variable = data[data["StdDev"] == max_std]

    with open("temperature_stability_stations.txt", "w") as f:
        print("\nTemperature Stability:")
        for _, row in most_stable.iterrows():
            line = f"Most Stable: Station {row['STATION_NAME']}: StdDev {row['StdDev']:.1f}°C"
            print(line)
            f.write(line + "\n")
        for _, row in most_variable.iterrows():
            line = f"Most Variable: Station {row['STATION_NAME']}: StdDev {row['StdDev']:.1f}°C"
            print(line)
            f.write(line + "\n")

    print("\nTemperature analysis completed successfully.")

if __name__ == "__main__":
    process_temperature_data()