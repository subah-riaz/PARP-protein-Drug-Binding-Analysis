# PARP-protein-Drug-Binding-Analysis
This project is a part of the computational drug discovery pipeline, focusing on the PARP (Poly (ADP- ribose) polymerase) protein and its interactions with key residues that could play a role in drug development, particularly for cancer therapies. By leveraging computational resources such as molecular docking and protein interaction analysis, this work reduces the need for extensive experimental resources, 
aligning with innovative drug discovery practices. The use of bioinformatics and computational tools to identify potential therapeutic targets is a crucial step in efficient drug development.

## Step 1: Determination of Interacting Residues within Multi-Domain Proteins and Cleaning the Data
In this initial step, the goal is to understand the complex interactions between different domains within a multi-domain protein using a computational framework. 
The process involves: 
1. Utilizing two primary input files: an Interacting Residues CSV file (Intercaat File) and MD Simulation Files for protein-DNA and protein-DNA-ZN-NAD complexes. 
2. Crafting a specialized data dictionary to delineate domain ranges, enabling precise identification of residues within distinct domains. 
3. Parsing and manipulating residues in MD simulation files to align with entries in the Intercaat File. 
4. Iterating through each interacting residue pair, validating interactions based on specified criteria. 
5. Filtering residues to isolate those participating in interactions between distinct domains. 
6. Transforming residues by removing atomic information denoted by '@'. 
7. Saving the filtered residues into a newly generated CSV file, cataloged by specific domains. 
8. This computational pipeline is essential for discerning atomic-level interactions within a multidomain protein.

## Step 2:  Fraction-Based Filtering of Interacting Residues in Protein Domain Interactions
Building on the previous step, this stage involves sorting residues based on interacting partners and further filtering based on a fraction metric. 
The process includes: 
✔ Sorting residues initially filtered in Step 1 based on interacting partners. 
✔ Applying a fraction metric, filtering residues with a fraction less than 0.2. 
✔ Retaining residues with a fraction equal to or greater than 0.2, signifying their significance in interactions between protein domains. 

## Step 3:  Aggregating Acceptor-Donor Residue Pairs for Molecular-Level Analysis 
Following the fraction-based filtration, the refined dataset is used to determine Acceptor-Donor Residue Pairs. 
The steps include: 
 Unifying rows to generate consolidated entries, combining acceptor and donor residue pairs. 
 Introducing 'Count' and 'Frames' columns to capture the number of unified rows and the total frames. 
 Calculating the 'Fraction' (Frac) to normalize the occurrence of the residue pair based on total simulation frames and count. 
 Generating a CSV output file containing Acceptor-Donor Residue Pairs alongside 'Frames,' 'Frac,' and 'Count' columns. 
 This step provides comprehensive insights into molecular interactions within specified protein domains. 

## Step 4:  Residual-Level Segregation of Interacting Residues in Protein Domains
Building upon the fraction-based filtration, this step focuses on the residue level. 
The process involves: 
 Revisiting the dataset for a refined analysis, focusing on residues and removing atomic information denoted by '@'. 
 Sorting residues based on specific domains' ranges using the established data dictionary. 
 Categorizing residues based on their numerical representation within defined domains. 
 Organizing and categorizing residues into separate CSV files, each containing columns for 'Domain,' 'Residue,' 'Frames,' 'Frac,' and 'Count.' 
 This systematic organization offers comprehensive insight into individual residue roles within protein domains.

## Step 5:  Investigating High-Fraction Interacting Residue Pairs across Multiple Molecular Dynamics Simulations
In this step, pairwise files generated previously undergo a comparative analysis based on the Fraction metric. 
The process includes: 
 Identifying Acceptor-Donor Residue Pairs within specific domains with elevated fractions. 
 Highlighting residue pairs with notable differences between pairwise files. 
 Presenting output CSV files with information on Fractions for each residue pair and a 'Frac source' column denoting the source file with the higher fraction. 
 This step enhances understanding of significant residue interactions at the protein domain interface across multiple simulations.

## Step 6:   Investigating Differential Residue Representation within PARP Protein Domains
Similar to Step 5, this phase involves a comparative analysis, this time between two singular files generated previously. 
The steps include: 
 Comparing files based on the Fraction metric to identify residues within specific domains with higher Fraction values. 
 Highlighting residues with notable discrepancies between the two files. 
 Presenting output files with Fraction values from both files and a 'frac source' column denoting the source file with the chosen fraction for each residue. 
 This comparative approach aids in discerning differential residue representation within distinct 
domains of the PARP protein. 




