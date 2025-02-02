import streamlit as st
import pandas as pd
import numpy as np
from jellyfish import jaro_winkler_similarity
from io import BytesIO

def show_columns_comparison(df1, df2):
    """Display columns from both datasets side by side"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Master Facility List Columns:")
        for col in df1.columns:
            st.write(f"- {col}")
            
    with col2:
        st.write("DHIS2 Facility List Columns:")
        for col in df2.columns:
            st.write(f"- {col}")

def calculate_match(column1, column2, threshold):
    """Calculate matching scores between two columns using Jaro-Winkler similarity."""
    results = []
    
    for value1 in column1:
        if value1 in column2.values:
            results.append({
                'Col1': value1,
                'Col2': value1,
                'Match_Score': 100,
                'Match_Status': 'Match'
            })
        else:
            best_score = 0
            best_match = None
            for value2 in column2:
                similarity = jaro_winkler_similarity(str(value1), str(value2)) * 100
                if similarity > best_score:
                    best_score = similarity
                    best_match = value2
            results.append({
                'Col1': value1,
                'Col2': best_match,
                'Match_Score': round(best_score, 2),
                'Match_Status': 'Unmatch' if best_score < threshold else 'Match'
            })
    
    for value2 in column2:
        if value2 not in [r['Col2'] for r in results]:
            results.append({
                'Col1': None,
                'Col2': value2,
                'Match_Score': 0,
                'Match_Status': 'Unmatch'
            })
    
    return pd.DataFrame(results)

def main():
    st.title("Health Facility Name Matching Tool")
    
    # Introduction
    st.write("""
    ### Why Health Facility Name Matching?
    
    Accurate health facility name matching is crucial for:
    
    1. **Data Quality**: Ensuring consistency between the Master Facility List (MFL) and DHIS2 facility names 
    is essential for accurate health data reporting and analysis. This helps maintain data integrity across 
    different health information systems.
    
    2. **Resource Allocation**: Proper facility matching helps in tracking resource distribution and avoiding 
    duplication in supply chain management. This ensures efficient distribution of medical supplies and 
    equipment.
    
    3. **Monitoring & Evaluation**: Accurate facility matching enables better tracking of health interventions 
    and their impacts across different health information systems. This is crucial for program evaluation 
    and impact assessment.
    
    4. **Decision Making**: Having standardized facility names across systems supports evidence-based 
    decision making and improves data use for public health actions. This leads to better health service 
    delivery and planning.
    
    This tool uses advanced string matching algorithms to:
    - Compare facility names between MFL and DHIS2
    - Identify potential matches and discrepancies
    - Suggest standardized naming conventions
    - Generate reports for review and updates
    """)

    # Initialize session state
    if 'step' not in st.session_state:
        st.session_state.step = 1
    if 'master_hf_list' not in st.session_state:
        st.session_state.master_hf_list = None
    if 'health_facilities_dhis2_list' not in st.session_state:
        st.session_state.health_facilities_dhis2_list = None

    # Step 1: File Upload
    if st.session_state.step == 1:
        st.header("Step 1: Upload Files")
        mfl_file = st.file_uploader("Upload Master HF List (CSV, Excel):", type=['csv', 'xlsx', 'xls'])
        dhis2_file = st.file_uploader("Upload DHIS2 HF List (CSV, Excel):", type=['csv', 'xlsx', 'xls'])

        if mfl_file and dhis2_file:
            try:
                # Read files
                if mfl_file.name.endswith('.csv'):
                    st.session_state.master_hf_list = pd.read_csv(mfl_file)
                else:
                    st.session_state.master_hf_list = pd.read_excel(mfl_file)

                if dhis2_file.name.endswith('.csv'):
                    st.session_state.health_facilities_dhis2_list = pd.read_csv(dhis2_file)
                else:
                    st.session_state.health_facilities_dhis2_list = pd.read_excel(dhis2_file)

                st.success("Files uploaded successfully!")
                
                # Display columns comparison
                st.subheader("Available Columns in Both Datasets")
                show_columns_comparison(st.session_state.master_hf_list, 
                                     st.session_state.health_facilities_dhis2_list)
                
                # Display previews
                st.subheader("Preview of Master HF List")
                st.dataframe(st.session_state.master_hf_list.head())
                st.write(f"Total records in Master HF List: {len(st.session_state.master_hf_list)}")
                
                st.subheader("Preview of DHIS2 HF List")
                st.dataframe(st.session_state.health_facilities_dhis2_list.head())
                st.write(f"Total records in DHIS2 HF List: {len(st.session_state.health_facilities_dhis2_list)}")

                if st.button("Proceed to Column Renaming"):
                    st.session_state.step = 2
                    st.experimental_rerun()

            except Exception as e:
                st.error(f"Error reading files: {e}")

    # Step 2: Column Renaming
    elif st.session_state.step == 2:
        st.header("Step 2: Rename Columns (Optional)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Master HF List Columns")
            mfl_renamed_columns = {}
            for col in st.session_state.master_hf_list.columns:
                new_col = st.text_input(f"Rename '{col}' to:", key=f"mfl_{col}", value=col)
                mfl_renamed_columns[col] = new_col

        with col2:
            st.subheader("DHIS2 HF List Columns")
            dhis2_renamed_columns = {}
            for col in st.session_state.health_facilities_dhis2_list.columns:
                new_col = st.text_input(f"Rename '{col}' to:", key=f"dhis2_{col}", value=col)
                dhis2_renamed_columns[col] = new_col

        if st.button("Apply Changes and Continue"):
            st.session_state.master_hf_list = st.session_state.master_hf_list.rename(columns=mfl_renamed_columns)
            st.session_state.health_facilities_dhis2_list = st.session_state.health_facilities_dhis2_list.rename(
                columns=dhis2_renamed_columns)
            st.session_state.step = 3
            st.experimental_rerun()

        if st.button("Skip Renaming"):
            st.session_state.step = 3
            st.experimental_rerun()

    # Step 3: Column Selection and Matching
    elif st.session_state.step == 3:
        st.header("Step 3: Select Columns for Matching")
        
        mfl_col = st.selectbox("Select HF Name column in Master HF List:", 
                              st.session_state.master_hf_list.columns)
        dhis2_col = st.selectbox("Select HF Name column in DHIS2 HF List:", 
                                st.session_state.health_facilities_dhis2_list.columns)
        
        threshold = st.slider("Set Match Threshold (0-100):", 
                            min_value=0, max_value=100, value=70)

        if st.button("Perform Matching"):
            # Process data
            master_hf_list_clean = st.session_state.master_hf_list.copy()
            dhis2_list_clean = st.session_state.health_facilities_dhis2_list.copy()
            
            master_hf_list_clean[mfl_col] = master_hf_list_clean[mfl_col].astype(str)
            master_hf_list_clean = master_hf_list_clean.drop_duplicates(subset=[mfl_col])
            dhis2_list_clean[dhis2_col] = dhis2_list_clean[dhis2_col].astype(str)

            st.write("### Counts of Health Facilities")
            st.write(f"Count of HFs in DHIS2 list: {len(dhis2_list_clean)}")
            st.write(f"Count of HFs in MFL list: {len(master_hf_list_clean)}")

            # Perform matching
            with st.spinner("Performing matching..."):
                hf_name_match_results = calculate_match(
                    master_hf_list_clean[mfl_col],
                    dhis2_list_clean[dhis2_col],
                    threshold
                )

                # Rename columns and add new column for replacements
                hf_name_match_results = hf_name_match_results.rename(
                    columns={'Col1': 'HF_Name_in_MFL', 'Col2': 'HF_Name_in_DHIS2'}
                )
                hf_name_match_results['New_HF_Name_in_MFL'] = np.where(
                    hf_name_match_results['Match_Score'] >= threshold,
                    hf_name_match_results['HF_Name_in_DHIS2'],
                    hf_name_match_results['HF_Name_in_MFL']
                )

                # Display results
                st.write("### Matching Results")
                st.dataframe(hf_name_match_results)

                # Display matching statistics
                total_matches = len(hf_name_match_results[hf_name_match_results['Match_Status'] == 'Match'])
                total_unmatches = len(hf_name_match_results[hf_name_match_results['Match_Status'] == 'Unmatch'])
                
                st.write("### Matching Statistics")
                st.write(f"Total Matches: {total_matches}")
                st.write(f"Total Unmatches: {total_unmatches}")
                st.write(f"Match Rate: {(total_matches/len(hf_name_match_results)*100):.2f}%")

                # Download results
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    hf_name_match_results.to_excel(writer, index=False)
                output.seek(0)

                st.download_button(
                    label="Download Matching Results as Excel",
                    data=output,
                    file_name="hf_name_matching_results.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

        if st.button("Start Over"):
            st.session_state.step = 1
            st.session_state.master_hf_list = None
            st.session_state.health_facilities_dhis2_list = None
            st.experimental_rerun()

if __name__ == "__main__":
    main()
