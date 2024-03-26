import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to load the dataset
@st.cache_data  # Cache the function to enhance performance
def load_data():
    # Define the file path
    file_path = 'salaries.csv'
    
    # Load the CSV file into a pandas dataframe
    df = pd.read_csv(file_path)

    df['job_type_des'] = df['remote_ratio'].map({
        100: 'Remote',
        0: 'Onsite',
        50: 'Hybrid',
    })

    return df

# Load the data using the defined function
df = load_data()


#------------------ Streamlit UI and Introduction ------------------

# Title and Sidebar Title
st.title("EDA Streamlit App with the Salaries dataset💵👨‍💻👩‍💻")
st.sidebar.title("Filters 📊")

# Introduction
st.markdown("""
        Welcome to the dashboard made by Group 7 in the Hackathon competition. 
        """)

#--------- Expander ---------

# Guidance Expander
with st.expander("**Guidance from Teams** 📊 "):
    st.markdown("""
        After the kick-off on the 12th, you have the exciting task of creating and hosting an engaging and user-friendly dashboard using Streamlit and the datasets we have provided.
        """)
                             
# Data access Expander
with st.expander("**Data access** 📚"):
    st.markdown("""
        The datasets will be released in good time in the general channel in Teams as a zip file. You just have to choose one of them, and perform EDA on it.
        """)
                             
# Tutorial Expander
with st.expander("**How to Use the Dashboard** 📚"):
    st.markdown("""
    1. **Filter Data** - Use the sidebar filters to narrow down specific data sets.
    2. **Visualize Data** - From the dropdown, select a visualization type to view patterns.
    3. **Insights & Recommendations** - Scroll down to see insights derived from the visualizations and actionable recommendations.
    """)

# Tutorial Expander
with st.expander("**Data explanation** 📚"):
    st.markdown("""
    The download basically contains a single table with all salary information structured as follows:

        work_year: The year the salary was paid.

        experience_level: The experience level in the job during the year with the following possible values:
            - EN: Entry-level / Junior
            - MI: Mid-level / Intermediate
            - SE: Senior-level / Expert
            - EX: Executive-level / Director
                    
        employment_type - The type of employement for the role:
            - PT: Part-time
            - FT: Full-time
            - CT: Contract
            - FL: Freelance

        job_title: The role worked in during the year.

        salary: The total gross salary amount paid.

        salary_currency: The currency of the salary paid as an ISO 4217 currency code.

        salary_in_usd: The salary in USD (FX rate divided by avg. USD rate of respective year) via statistical data from the BIS and central banks.

        employee_residence: Employee's primary country of residence in during the work year as an ISO 3166 country code.

        remote_ratio: The overall amount of work done remotely, possible values are as follows:
            - 0: No remote work (less than 20%)
            - 50: Partially remote/hybird
            - 100: Fully remote (more than 80%)

        company_location: The country of the employer's main office or contracting branch as an ISO 3166 country code.

        company_size: The average number of people that worked for the company during the year:
            - S: less than 50 employees (small)
            - M: 50 to 250 employees (medium)
            - L: more than 250 employees (large)

    """)


#------------------ Sidebar setup ------------------

# Filter by experience level (multiselect)
experience_level_filter = st.sidebar.multiselect(
    "Select Experience Level",
    df["experience_level"].unique(),
    default=df["experience_level"].unique(),
    help="The experience level in the job during the year with the following possible values"
    
)

# Filter by job type description
job_type_filter = st.sidebar.multiselect(
    "Select Job type",
    df["job_type_des"].unique(),
    default=['Onsite'],
    help="The overall amount of work done remotely, possible values are as follows"
)

# Filter by job title
job_title_filter = st.sidebar.multiselect(
    "Select Job Title",
    df["job_title"].unique(),
    default=['Data Analyst']
)

#---------- Apply filters ----------

# Apply filters to the DataFrame
filtered_df = df[df["experience_level"].isin(experience_level_filter) & (df["job_type_des"].isin(job_type_filter)) & (df["job_title"].isin(job_title_filter)) ]

#------------------ Dashboard ------------------

# Show filtered data in a table
st.write("Filtered Data:")
st.write(filtered_df)

# Dropdown to select the type of visualization
visualization_option = st.selectbox(
    "Select Visualization 🎨", 
    ["Salary Distribution", 
     "Top 10 countries"
     ]
)

if visualization_option == "Salary Distribution":
    # Plot salary distribution for the filtered data

    st.header("Salary Distribution")

    st.markdown(""" 
        This is a boxplot which shows the Salary Distribution between each Experience Level.
        Remember to use the filter panel in the side to change the view of the boxplot.
    """)

    st.set_option('deprecation.showPyplotGlobalUse', False)
    plt.figure(figsize=(8, 6))
    sns.boxplot(
        data=filtered_df,
        x="experience_level",
        y="salary_in_usd",
        width=0.7,
    )
    plt.title("Salary Distribution by Experience Level")
    plt.xlabel("Experience Level")
    plt.ylabel("Salary in USD")
    st.pyplot()


elif visualization_option == "Top 10 countries":

    st.header("Top 10 countries")

    st.markdown(""" 
        This two diagrams shows the top 10 countries according to DS mean salaries and top 10 countries having most DS job opportunities.
        """)

    # Top 10 company-locations according to mean salary
    top_cmp_locations = filtered_df.groupby('company_location')['salary_in_usd'].mean().sort_values(ascending=False)[:10]

    plt.figure(figsize=(8, 6))
    sns.barplot(
        data=filtered_df,
        y=top_cmp_locations.index, 
        x=top_cmp_locations
    )
    plt.title("Top 10 countries according to DS mean salaries", fontdict={'fontsize': 16})
    plt.xlabel("Mean Salary")
    plt.ylabel("Countries")
    st.pyplot()

    # Top 10 company-locations having most job opportunities
    top_cl = filtered_df['company_location'].value_counts()[:10]

    plt.figure(figsize=(8, 6))
    sns.barplot(
        data=filtered_df,
        x=top_cl, 
        y=top_cl.index
    )
    plt.title("Top 10 countries having most DS job opportunities", fontdict={'fontsize': 16})
    plt.xlabel("Number of Job Opportunities")
    plt.ylabel("Countries")
    st.pyplot()
