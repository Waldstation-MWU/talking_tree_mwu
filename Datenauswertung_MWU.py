import pandas as pd
import glob
import matplotlib.pyplot as plt
import re
import openpyxl


dateipfade = glob.glob("Datensicherung*.csv")


if dateipfade:
    df = pd.read_csv(dateipfade[0])
    monat = re.search(r'_(.*?)\.', dateipfade[0]).group(1)
    print(df.head())
else:
    print("Keine Dateien gefunden, die mit 'Datensicherung' beginnen.")


df['Zeit'] = pd.to_datetime(df['Zeit'])

def plot_sensors_and_measurements(df, sensors_to_plot, measurements_to_plot,save_path=None):
    """
    Plottet die Zeit-Wert-Daten für eine Liste von Sensoren und Messungen.
    
    Parameters:
    df (DataFrame): Der DataFrame mit den Daten.
    sensors_to_plot (list): Liste der Sensoren, die geplottet werden sollen.
    measurements_to_plot (list): Liste der Messungen, die geplottet werden sollen (z.B. °C).
    """
    # Filter für die gewünschten Sensoren und Messungen
    filtered_df = df[df['Sensor'].isin(sensors_to_plot) & df['Messung'].isin(measurements_to_plot)]
    
    # Plot-Erstellung
    plt.figure(figsize=(20, 10))
    
    # Plot für jeden Sensor und jede Messung separat
    for sensor, group in filtered_df.groupby('Sensor'):
        for measurement, sub_group in group.groupby('Messung'):
            plt.plot(sub_group['Zeit'], sub_group['Wert'], label=f"{sensor} ({measurement})")
    
    # Diagrammeinstellungen
    plt.xlabel("Zeit")
    plt.ylabel("Wert")
    plt.title(f"Zeit-Wert-Diagramm für Sensoren: {', '.join(sensors_to_plot)} und Messungen: {', '.join(measurements_to_plot)}")
    plt.legend(title="Sensoren und Messungen")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
        print(f"Plot gespeichert unter: {save_path}")
    else:
        plt.show()


# Beispiel: Liste der Sensoren und Messungen, die du plotten möchtest
sensors_to_plot = ['B1_SHT31/1', 'B1_SHT31/2','B1_SHT31/3','B1_SHT31/4']  # Diese Liste kannst du anpassen
measurements_to_plot = ['°C']  # Diese Liste kannst du anpassen

# Plot erstellen
plot_sensors_and_measurements(df, sensors_to_plot, measurements_to_plot,f"B1_SHT_Sensoren_Temperatur_{monat}.pdf")

sensors_to_plot = ['B1_SHT31/1', 'B1_SHT31/2','B1_SHT31/3','B1_SHT31/4']  # Diese Liste kannst du anpassen
measurements_to_plot = ['%rF']  # Diese Liste kannst du anpassen

# Plot erstellen
plot_sensors_and_measurements(df, sensors_to_plot, measurements_to_plot,f"B1_SHT_Sensoren_Luftfeuchtigkeit_{monat}.pdf")

sensors_to_plot = ['B1_DC4/1']  # Diese Liste kannst du anpassen
measurements_to_plot = ['device_frmpayload_data_DC4_1_circumference']  # Diese Liste kannst du anpassen

# Plot erstellen
plot_sensors_and_measurements(df, sensors_to_plot, measurements_to_plot,f"B1_Umfang_{monat}.pdf")


sensors_to_plot = ['B1_SMT100/1','B1_SMT100/2','B1_SMT100/3']  # Diese Liste kannst du anpassen
measurements_to_plot = ['°C']  # Diese Liste kannst du anpassen

# Plot erstellen
plot_sensors_and_measurements(df, sensors_to_plot, measurements_to_plot,f"Boden_Temperatur_{monat}.pdf")

sensors_to_plot = ['B1_SMT100/1','B1_SMT100/2','B1_SMT100/3']  # Diese Liste kannst du anpassen
measurements_to_plot = ['Vol.-%']  # Diese Liste kannst du anpassen

# Plot erstellen
plot_sensors_and_measurements(df, sensors_to_plot, measurements_to_plot,f"Boden_Feuchtigkeit_{monat}.pdf")

# Sicherstellen, dass 'Zeit' der Index ist
df_resample = df.set_index('Zeit')

# Leerer DataFrame für alle Sensoren & Messungen
resampled_all = pd.DataFrame()

# Für jede Kombination aus Sensor und Messung interpolieren wir separat
for (sensor, messung), group in df_resample.groupby(['Sensor', 'Messung']):
    # Sortieren nach Zeit
    group_sorted = group.sort_index()
    
    # Nur die Spalte 'Wert' resamplen und interpolieren
    wert_resampled = group_sorted[['Wert']].resample('30min').mean()
    wert_resampled['Wert'] = wert_resampled['Wert'].interpolate(method='time')
    wert_resampled['Wert'] = wert_resampled['Wert'].round(2)
    
    # Sensor und Messung wieder hinzufügen
    wert_resampled['Sensor'] = sensor
    wert_resampled['Messung'] = messung
    
    # Zusammenführen
    resampled_all = pd.concat([resampled_all, wert_resampled])

# Index zurück in Spalte 'Zeit' umwandeln
resampled_all = resampled_all.reset_index()
resampled_all['Zeit'] = resampled_all['Zeit'].dt.tz_localize(None)

# Datum und Uhrzeit trennen
resampled_all['Datum'] = resampled_all['Zeit'].dt.date
resampled_all['Uhrzeit'] = resampled_all['Zeit'].dt.time
resampled_all = resampled_all.drop(columns=['Zeit'])

# Spalten in gewünschter Reihenfolge anordnen
resampled_all = resampled_all[['Datum', 'Uhrzeit', 'Sensor', 'Messung', 'Wert']]


# In Excel schreiben mit Spaltenbreitenanpassung
resampled_excel_path = f"Resampled_Daten_{monat}.xlsx"
with pd.ExcelWriter(resampled_excel_path, engine='openpyxl', datetime_format='DD.MM.YYYY HH:MM') as writer:
    resampled_all.to_excel(writer, index=False, sheet_name='Resampled')
    
    workbook = writer.book
    worksheet = writer.sheets['Resampled']
    
    from openpyxl.utils import get_column_letter
    for i, col in enumerate(resampled_all.columns, 1):
        max_length = max(resampled_all[col].astype(str).map(len).max(), len(str(col)))
        worksheet.column_dimensions[get_column_letter(i)].width = min(max_length + 2, 50)

print(f"Resampled Excel-Datei gespeichert unter: {resampled_excel_path}")