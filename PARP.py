import pandas as pd 
import re 
def clean_and_process_csv(input_files, combined_output_files, 
summary_output_files): 
for input_file, combined_output_file, summary_output_file in zip(input_files, 
combined_output_files, summary_output_files): 
# Read the CSV file into a DataFrame 
df = pd.read_csv(input_file) 
# List of columns to clean 
columns_to_clean = ['Acceptor', 'Donor', 'Donor_h'] 
 
# Loop through each specified column and clean residues 
for column in columns_to_clean: 
# Extract only the residue part by removing the atom number after '@' 
df[column] = df[column].str.replace(r'@.*$', '', regex=True) 
interacting_residues = ['TYR_33', 'LYS_35', 'GLU_46', 'ASP_51', 'SER_95', 
'GLU_96', 'LEU_97', 'ARG_98', 'TRP_99', 'GLN_60', 
'PRO_62', 'MET_63', 'PHE_64', 'ASP_65', 
'ALA_337','LYS_340', 'ASP_334','TRP_338','LYS_340', 'MET_342', 
'ASP_334','LYS_35' 
'SER_36', 'ARG_38','ALA_39', 'SER_40', 'LYS_42', 'ARG_54', 
'PHE_64', 'VAL_68', 'PRO_69', 'TRP_71', 'THR_278', 'ASN_279', 
'SER_294', 'GLY_295', 'GLU_296', 'TYR_590', 'ARG_607', 
'TRP_609', 'LYS_620', 'GLU_640', 'LYS_641', 
'LYS_682', 'SER_683', 'LEU_685', 'PRO_686', 'PRO_688', 
'VAL_689', 'GLN_690', 'ASP_691', 'LEU_692', 
'ILE_693', 'LYS_694', 'MET_695', 'ILE_696', 'PHE_697', 
'SER_701', 'MET_702', 'LYS_704', 'ALA_705', 
'TYR_709', 'GLN_727', 'TYR_730', 'SER_731', 'LEU_733', 
'SER_734', 'GLN_737', 'VAL_778', 'GLN_779', 
'THR_576', 'GLY_578', 'VAL_580', 'ASP_581', 'ILE_582', 
'VAL_583', 'LYS_584', 'GLY_585', 'ASN_587', 
'TYR_589', 'ARG_611', 'VAL_612', 'GLY_613', 'THR_614', 
'ILE_616', 'LYS_653'] 
pattern = r"\b(" + "|".join(interacting_residues) + r")\b" 
filtered_df = df[df.apply(lambda row: any(re.search(pattern, str(row[col]), 
flags=re.IGNORECASE) for col in df.columns), axis=1)] 
filtered_df = filtered_df[filtered_df['Frac'] >= 0.2] 
def categorize_domain(residue_number): 
if 1 <= residue_number <= 20: 
return 'DNA' 
elif 29 <= residue_number <= 113: 
return 'ZN1' 
elif 133 <= residue_number <= 223: 
return 'ZN2' 
elif 245 <= residue_number <= 379: 
return 'ZN3' 
elif 405 <= residue_number <= 496: 
return 'BRCT' 
elif 562 <= residue_number <= 658: 
return 'WGR' 
elif 682 <= residue_number <= 799: 
return 'HD' 
elif 808 <= residue_number <= 1034: 
return 'ART' 
else: 
return 'other' 
filtered_df['Acceptor_Domain'] = filtered_df['Acceptor'].apply(lambda residue: 
categorize_domain(int(re.search(r'\d+', residue).group()))) 
filtered_df['Donor_Domain'] = filtered_df['Donor'].apply(lambda residue: 
categorize_domain(int(re.search(r'\d+', residue).group()))) 
# Remove rows where Acceptor Domain is equal to Donor Domain 
filtered_df = filtered_df[filtered_df['Acceptor_Domain'] != 
filtered_df['Donor_Domain']] 
 
# Sort the DataFrame based on the 'Acceptor_Domain' and 'Donor_Domain' 
columns 
filtered_df = filtered_df.sort_values(by=['Acceptor_Domain', 'Donor_Domain']) 
# Drop unnecessary columns 
filtered_df_combined = filtered_df[['Acceptor', 'Donor', 'Acceptor_Domain', 
'Donor_Domain', 'Frac', 'Frames']] 
# Save the combined and processed DataFrame to a new CSV file 
filtered_df_combined.to_csv(combined_output_file, index=False) 
# Create a DataFrame to store individual frames for each residue 
individual_frames = pd.DataFrame({ 
'Residue': pd.concat([filtered_df['Acceptor'], filtered_df['Donor']]), 
'Domain': pd.concat([filtered_df['Acceptor_Domain'], 
filtered_df['Donor_Domain']]), 
'Frames': pd.concat([filtered_df['Frames'], filtered_df['Frames']]) 
}) 
 
# Group by residue and domain, count occurrences, and sum the frames 
residue_counts = individual_frames.groupby(['Residue', 
'Domain']).agg({'Frames': ['sum', 'count']}).reset_index() 
residue_counts.columns = ['Residue', 'Domain', 'TotalFrames', 'Count'] 
# Calculate the fraction based on the count of occurrences 
residue_counts['Fraction'] = residue_counts.apply(lambda row: 
row['TotalFrames'] / (5000 * row['Count']) if row['Count'] > 0 else 0, axis=1) 
# Sort the DataFrame based on domain and residue 
residue_counts.sort_values(['Domain', 'Residue'], inplace=True) 
# Save the output DataFrame to a new CSV file 
residue_counts.to_csv(summary_output_file, index=False) 
def generate_output(input_files, output_files): 
for input_file, output_file in zip(input_files, output_files): 
# Read the CSV file into a DataFrame 
df = pd.read_csv(input_file) 
 
# Group by 'Acceptor' and 'Donor' columns and sum the frames 
grouped_frames = df.groupby(['Acceptor', 'Donor', 'Acceptor_Domain', 
'Donor_Domain'])['Frames'].agg(['sum', 'count']).reset_index() 
# Calculate the total number of frames 
total_frames = grouped_frames['sum'].sum() 
 
# Calculate the fraction based on the count of repetitions 
grouped_frames['Fraction'] = grouped_frames.apply(lambda row: row['sum'] / 
(5000 * row['count']) if row['count'] == 1 else 
(row['sum'] / 10000) if row['count'] == 2 else 
(row['sum'] / 15000) if row['count'] == 3 else 
(row['sum'] / 20000) if row['count'] == 4 else 0, 
axis=1) 
# Rename the 'sum' column to 'Frame' 
grouped_frames = grouped_frames.rename(columns={'sum': 'Frame'}) 
 
# Sort the DataFrame by 'Acceptor_Domain' and 'Donor_Domain' 
grouped_frames = grouped_frames.sort_values(by=['Acceptor_Domain', 
'Donor_Domain']) 
# Save the output DataFrame to a new CSV file 
grouped_frames.to_csv(output_file, index=False) 
def merge_and_calculate_max_fraction(file1, file2, output_file): 
# Read CSV Files 
df1 = pd.read_csv(file1) 
df2 = pd.read_csv(file2) 
 
# Merge DataFrames on 'Acceptor' and 'Donor' 
merged_df = pd.merge(df1, df2, how='inner', on=['Residue','Domain'], 
suffixes=('_file1', '_file2')) 
# Create a new column 'Max_Fraction' comparing fractions of both files 
merged_df['Max_Fraction'] = merged_df[['Fraction_file1', 
'Fraction_file2']].max(axis=1) 
# Save Output 
merged_df.to_csv(output_file, index=False) 
def new_module(input_files, output_file): 
# Read CSV Files 
df1 = pd.read_csv(input_files[0]) 
df2 = pd.read_csv(input_files[1]) 
# Merge DataFrames on 'Residue' and 'Domain' 
merged_df = pd.merge(df1, df2, how='inner', on=['Acceptor', 
'Donor','Acceptor_Domain','Donor_Domain'], suffixes=('_file1', '_file2')) 
 
# Create a new column 'Max_Fraction' comparing fractions of both files 
merged_df['Max_Fraction'] = merged_df[['Fraction_file1', 
'Fraction_file2']].max(axis=1) 
# Save Output 
merged_df.to_csv(output_file, index=False) 
if _name_ == "_main_": 
input_file_paths = ['parp_dna_wildtype.csv', 'parp_dna_zn_nad.csv'] 
combined_output_file_paths = ['1_parp_dna_filtered.csv', 
'2_parp_dna_zn_nad_filtered.csv'] 
summary_output_file_paths = ['3_parp_dna_singular.csv', 
'4_parp_dna_zn_nad_singular.csv'] 
individual_output_file_paths = ['5_parp_dna_pairwise_3.csv', 
'6_parp_dna_zn_nad_pairwise_3.csv'] 
merged_output_file_paths = ['7_parp_dna_singular_comparison_4.csv'] 
comparison_output_file_paths = ['8_parp_dna_pairwise_comparison_5.csv'] 
# Clean and Process CSV, and Generate Outputs 
clean_and_process_csv(input_file_paths, combined_output_file_paths, 
summary_output_file_paths) 
generate_output(combined_output_file_paths, individual_output_file_paths) 
# Merge and Calculate Max Fraction 
merge_and_calculate_max_fraction(summary_output_file_paths[0], 
summary_output_file_paths[1], merged_output_file_paths[0]) 
# New Module: Compare Individual Outputs 
new_module(individual_output_file_paths, comparison_output_file_paths[0])