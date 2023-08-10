import pandas as pd
import numpy as np

# Directory and file names
Manufacturer = 'Zentriad'
Source_File = str(Manufacturer) + '/Orignal_Look_Up_table.csv'
Target_File = str(Manufacturer) + '/Interpolated_Look_Up_table.csv'

# Name of the columns in the Orignal lookup table.
Column_Temp = 'Temp'
Column_Resistnce = 'Rnor'
Column_Log_Resistance = str('Log(' + Column_Resistnce + ')')

#====================== Don't Change below =====================================
# Read the dataframe
df = pd.read_csv(Source_File);

# Perform log operation on given values
df[Column_Resistnce] = df[Column_Resistnce] * 1000
df[Column_Log_Resistance] = np.log10(df[Column_Resistnce]);

# Best fit line equation
# Fit the 10th-order polynomial curve
coefficients = np.polyfit(df[Column_Temp], df[Column_Log_Resistance], 10)

# Calculating no. of rows.
rows = df.shape[0]

# Rounding off to 1 decimal place after the decimal
df[Column_Temp] = df[Column_Temp].apply(lambda x: round(x, 1))

# Creating a new dataframe for °C LUT
lut = pd.DataFrame();

# Add an empty Column in the new dataset
lut[Column_Temp] = ''
lut[Column_Log_Resistance] = ''

# Fill the rows in dataset just created.
LUT_min = -40.0
LUT_max = 120.0

lut.loc[0] = [LUT_min,''];

for i in range (1, (int)(((LUT_max - LUT_min) * 10) + 1)):
    lut.loc[i] = [(lut[Column_Temp].iat[i - 1] + 0.1).round(1),''];

# adding values in the new lookup table.
lut[Column_Log_Resistance] =  (
                                (coefficients[0] * (lut[Column_Temp] ** 10)) + 
                                (coefficients[1] * (lut[Column_Temp] ** 9)) +
                                (coefficients[2] * (lut[Column_Temp] ** 8)) +
                                (coefficients[3] * (lut[Column_Temp] ** 7)) +
                                (coefficients[4] * (lut[Column_Temp] ** 6)) +
                                (coefficients[5] * (lut[Column_Temp] ** 5)) +
                                (coefficients[6] * (lut[Column_Temp] ** 4)) +
                                (coefficients[7] * (lut[Column_Temp] ** 3)) +
                                (coefficients[8] * (lut[Column_Temp] ** 2)) +
                                (coefficients[9] * (lut[Column_Temp] ** 1)) +
                                (coefficients[10])
                            )

# Take antilog of values
lut[Column_Resistnce] = (10 ** lut[Column_Log_Resistance]).round(4)

lut.drop(Column_Log_Resistance, axis=1, inplace=True)

# Error summary
for i in range(df.shape[0]):
  df.at[i,'Antilog(' + str(Column_Log_Resistance) + ')'] = lut.at[(10 * i), Column_Resistnce]

df['Error %'] = ((df['Antilog(' + str(Column_Log_Resistance) + ')']/df[Column_Resistnce]) - 1) * 100

print(df.describe())

# Final lookup table
# Set the first column as index
lut = lut.set_index(Column_Temp);

# Convert to CSV
lut.to_csv(Target_File)