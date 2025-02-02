import streamlit as st

# Title of the app
st.title("Automated Geospatial Analysis for Sub-National Tailoring of Malaria Interventions")

# Display the image using the GitHub raw URL
st.image("https://github.com/mohamedsillahkanu/si/raw/b0706926bf09ba23d8e90c394fdbb17e864121d8/Sierra%20Leone%20Map.png", 
         caption="Sierra Leone Administrative Map",
         use_container_width=True)

# Overview Section
st.header("Overview")
st.write("""
Sub-National Tailoring (SNT) of malaria interventions requires complex analysis of multiple data sources including disease burden, intervention coverage, and environmental factors at district and sub-district levels. Traditional manual analysis using tools like QGIS can take weeks, potentially delaying critical intervention decisions. Our automated system transforms this process, enabling rapid analysis and visualization of key SNT indicators within minutes.

This automation is particularly crucial for National Malaria Control Programs (NMCPs) implementing SNT strategies, as it allows for quick assessment of geographical variations in malaria burden, intervention coverage gaps, and resource allocation needs. The system integrates multiple data sources including routine surveillance data, household surveys, entomological data, and environmental factors to support evidence-based stratification of interventions.
""")

# Objectives Section
st.header("Objectives")
st.write("""
The key objectives of this automated system for SNT analysis are:
1. **Accelerate Stratification**: Automate the process of stratifying geographic areas based on multiple indicators (prevalence, incidence, intervention coverage, resistance patterns) to identify optimal intervention packages.
2. **Enhance Data Integration**: Seamlessly combine various data sources (DHIS2, surveys, environmental data) to create comprehensive district-level profiles for decision-making.
3. **Standardize Analysis**: Ensure consistent application of WHO-recommended SNT approaches across all districts through standardized analytical workflows.
4. **Enable Real-time Updates**: Allow for rapid updates to stratification and intervention recommendations as new data becomes available.
""")

# Features Section
st.header("Key Features")
st.write("""
Our automated system includes:
- Automated integration with DHIS2 and other routine data sources
- Pre-programmed analysis workflows following WHO SNT guidelines
- Interactive maps showing key indicators and recommended intervention packages
- Automated generation of district-specific intervention recommendation reports
- Built-in quality checks for data consistency and completeness
- Export capabilities for various reporting formats needed by NMCPs
""")

# Technical Details
st.header("Technical Implementation")
st.write("""
The system is built entirely in Python, leveraging key libraries:
- **GeoPandas**: For spatial data processing and analysis
- **Numpy & Pandas**: For efficient data manipulation and statistical analysis
- **Scikit-learn**: For classification and clustering in stratification
- **Plotly & Folium**: For interactive visualization and mapping
- **DHIS2 API**: For automated data extraction from DHIS2

All code has undergone rigorous testing and validation against manual analyses to ensure accuracy and reliability. The system follows WHO guidelines for SNT and incorporates best practices for malaria data analysis.
""")

# Benefits Section
st.header("Benefits for SNT")
st.write("""
This automated system specifically supports SNT by:
- Reducing stratification analysis time from weeks to hours
- Ensuring consistent application of stratification criteria across all areas
- Enabling rapid scenario analysis for different intervention packages
- Facilitating regular updates to intervention recommendations as new data becomes available
- Supporting evidence-based resource allocation decisions
- Enabling quick identification of areas requiring specific intervention adjustments
""")

# Implementation Guide
st.header("Implementation Process")
st.write("""
The system can be implemented in phases:
1. **Data Integration**: Setup automated connections to existing data sources
2. **Validation**: Compare automated analysis results with existing manual processes
3. **Customization**: Adjust stratification criteria and thresholds to country context
4. **Training**: Build capacity of NMCP staff in using the automated system
5. **Monitoring**: Regular assessment of system performance and user feedback
""")

# Conclusion Section
st.header("Conclusion")
st.write("""
This automated system represents a significant advancement in supporting data-driven SNT for malaria interventions. By dramatically reducing the time and effort required for analysis while ensuring consistency and accuracy, it enables NMCPs to respond more quickly to changing epidemiological situations and optimize their intervention strategies. The system's foundation in Python ensures reliability and maintainability, while its alignment with WHO guidelines ensures that all analyses meet international standards for SNT implementation.
""")
