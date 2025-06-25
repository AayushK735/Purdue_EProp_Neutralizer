import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
import tkinter as tk
from tkinter import filedialog

def oscilloscope_graphs(file):
    '''Takes CSV file and plots the oscilloscope data'''
    # Read CSV file, skip first row, use second row as header
    df = pd.read_csv(file, sep=',', skiprows=1)
    print('First few rows of data:')
    print(df.head())

    # Check for expected columns
    if not all(col in df.columns for col in ['second', 'Ampere', 'Volt']):
        print('Error: CSV does not contain required columns.')
        return

    seconds = df['second']
    # Clean and convert Ampere and Volt columns to numeric
    Ampere = pd.to_numeric(df['Ampere'].astype(str).str.replace(',', ''), errors='coerce')
    Volt = pd.to_numeric(df['Volt'].astype(str).str.replace(',', ''), errors='coerce')
    # Remove rows with NaN values
    valid = ~(Ampere.isna() | Volt.isna() | pd.to_numeric(seconds, errors='coerce').isna())
    seconds = pd.to_numeric(df['second'], errors='coerce')[valid]
    Ampere = Ampere[valid]
    Volt = Volt[valid]
    
    plt.figure(figsize=(10, 6))
    plt.plot(seconds, Ampere, label='Ampere')
    plt.plot(seconds, Volt, label='Volt')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Value')
    plt.title('Oscilloscope Data: Ampere and Volt vs Time')
    plt.legend()
    # Set y-ticks for better readability
    y_min = min(Ampere.min(), Volt.min())
    y_max = max(Ampere.max(), Volt.max())
    plt.yticks(np.linspace(y_min, y_max, num=10))
    plt.tick_params(axis='y', labelsize=10)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    file = filedialog.askopenfilename(title="Select a CSV file")
    oscilloscope_graphs(file)