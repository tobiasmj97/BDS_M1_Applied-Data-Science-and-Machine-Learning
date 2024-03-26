import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
        page_title="Hackathon Group 7",
        page_icon="chart_with_upwards_trend",
        layout="wide",
)

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
    df['experience_level_des'] = df['experience_level'].map({
        'EN':'Entry-level',
        'MI':'Mid-level',
        'SE':'Senior-level',
        'EX':'Executive-level'
    })

    file_path2 = 'continents2.csv'
    
    # Load the CSV file into a pandas dataframe
    continents = pd.read_csv(file_path2)

    # Dropping all columns in the continents dataframe
    # except 'name', 'alpha-2' and 'region'
    continents = continents[['name', 'alpha-2', 'region']]
    
    # Renaming the column 'alpha-2' to 'company_location', so that we can merge the two dataframes
    continents = continents.rename(columns={'alpha-2':'company_location', 'name':'country'})
    
    # Merging the two dataframes
    df = df.merge(continents, how='left')

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
with st.expander("**Assignment Guide** 🗺️ "):
    st.markdown("""
    1. **Explore the dataset** - What questions could be interesting to explore? Consider using pygwalker if you're interested.

2. **EDA Notebook** - Select some questions from your exploration. - Build an EDA (Exploratory Data Analysis) notebook including visualizations.

3. **Remote Collaboration** - If you're working remotely, consider using Zoom with the AAU license.
	
4. **Learn Github with VSCode** - Get familiar with VSCode Github collaboration. Read the guide on VSCode's website. 
        Remember, using Github is frequently mentioned in job postings! Watch the official intro by VSCode.

5. **Dashboard Elements** - Select the elements that you want to be part of your dashboard.
		Think about filters and interactive elements. What should users be able to select or interact with?
6. **Build your App** - Use other apps as inspiration or reference. 
                
7. **Deployment Options** - Deploy on Streamlit cloud. """)
                             
# Data access Expander
with st.expander("**EDA Questions** 🙋❓"):
    st.markdown("""

        1. What's the distribution of jobs in the dataset?
        2. How does the mean salary change depending on the experience level?
        3. How does the salary change depending on the country and region?
        4. Which country has the highest mean salary in Europe?
        5. What are the top ten countries according to DS mean salary?
        6. In which countries are there the most DS job opportunities?
        """)
                             
# Tutorial Expander
with st.expander("**How to Use the Dashboard** 📚"):
    st.markdown("""
    1. **Filter Data** - Use the sidebar filters to narrow down specific data sets.
    2. **Visualize Data** - From the dropdown, select a visualization type to view patterns.
    3. **Insights & Recommendations** - Scroll down to see insights derived from the visualizations and actionable recommendations.
    """)

# Tutorial Expander
with st.expander("**Data explanation** 📈"):
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

# Show filtered data in a table



#------------------ Sidebar setup ------------------
# Filter by region
region_filter = ['Select All'] + list(df["region"].unique())
region_filter = st.sidebar.multiselect(
    "Select Region",
    region_filter,
    default=['Select All']
)

if 'Select All' in region_filter:
    region_filter = list(df["region"].unique())

if not region_filter:
    st.warning("Please select a region from the sidebar ⚠️")
    st.stop()

# Filter by experience level (multiselect)
experience_level_filter = st.sidebar.multiselect(
    "Select Experience Level",
    df["experience_level_des"].unique(),
    default=df["experience_level_des"].unique(),
    help="The experience level in the job during the year with the following possible values"

)
if not experience_level_filter:
    st.warning("Please select an experience level from the sidebar ⚠️")
    st.stop()

# Filter by job type description
job_type_filter = st.sidebar.multiselect(
    "Select Job type",
    df["job_type_des"].unique(),
    default=df["job_type_des"].unique(),
    help="The overall amount of work done remotely, possible values are as follows"
)
if not job_type_filter:
    st.warning("Please select a job type from the sidebar ⚠️")
    st.stop()

# Filter by job title
job_title_options = ['Select All'] + list(df["job_title"].unique())
job_title_filter = st.sidebar.multiselect(
    "Select Job Title",
    job_title_options,
    default=['Select All']
)

if 'Select All' in job_title_filter:
    job_title_filter = list(df["job_title"].unique())

if not job_title_filter:
    st.warning("Please select a job title from the sidebar ⚠️")
    st.stop()

# Filter by Employment type
employment_type_filter = st.sidebar.multiselect(
    "Select Job type",
    df["employment_type"].unique(),
    default=df["employment_type"].unique(),
    help="Choose the type of employment"
)
if not employment_type_filter:
    st.warning("Please select an employment type from the sidebar ⚠️")
    st.stop()

#---------- Apply filters ----------

# Apply filters to the DataFrame
filtered_df = df[df["experience_level_des"].isin(experience_level_filter) & (df["job_type_des"].isin(job_type_filter)) & (df["job_title"].isin(job_title_filter)) & (df["region"].isin(region_filter)) & (df["employment_type"].isin(employment_type_filter))]

#------------------ Dashboard ------------------


# Dropdown to select the type of visualization
visualization_option = st.selectbox(
    "Select Visualization 🎨", 
    ["Salary Distribution", 
     "Top and bottom 10 countries",
     "Continents",
     "Job distribution"
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
        order = ['EN','MI','SE','EX']
    )
    plt.title("Salary Distribution by Experience Level")
    plt.xlabel("Experience Level")
    plt.ylabel("Salary in USD")
    st.pyplot()



elif visualization_option == "Top and bottom 10 countries":

 

    st.header("Top and bottom 10 countries")

 

    st.markdown("""

        This diagrams shows the top 10 and bottom 10 countries according to DS mean salaries and top 10 countries having most DS job opportunities.

        """)

 

    # Top 10 company-locations according to mean salary

    top_cmp_locations = filtered_df.groupby('country')['salary_in_usd'].mean().sort_values(ascending=False)[:10]

 

    plt.figure(figsize=(8, 6))

    sns.barplot(

        data=filtered_df,

        y=top_cmp_locations.index,

        x=top_cmp_locations

    )

    plt.title("Top 10 countries according to DS mean salaries", fontdict={'fontsize': 16})

    plt.xlabel("Mean Salary in USD")

    plt.ylabel("Countries")

    st.pyplot()

 

 

 

 

    # Bottom 10 company-locations according to mean salary

    top_cmp_locations = filtered_df.groupby('country')['salary_in_usd'].mean().sort_values(ascending=True)[:10]

 

    plt.figure(figsize=(8, 6))

    sns.barplot(

        data=filtered_df,

        y=top_cmp_locations.index,

        x=top_cmp_locations

    )

    plt.title("Bottom 10 countries according to DS mean salaries", fontdict={'fontsize': 16})

    plt.xlabel("Mean Salary in USD")

    plt.ylabel("Countries")

    st.pyplot()

 

    # Top 10 company-locations having most job opportunities

    top_cl = filtered_df['country'].value_counts()[:10]

 

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

elif visualization_option == "Continents":

    st.header("Continents")

    st.markdown(""" 
        This diagrams shows the continents according to DS mean salaries.
        """)

   # Mean salary distributed by continent
    continents_mean_salaries = filtered_df.groupby('region')['salary_in_usd'].mean().sort_values(ascending=False)
    print(continents_mean_salaries)

    plt.figure(figsize=(8, 6))
    
    sns.barplot(
        data=filtered_df,
        y=continents_mean_salaries.index, 
        x=continents_mean_salaries
    )
    plt.title("Mean salary distributed by continents", fontdict={'fontsize': 16})
    plt.xlabel("Mean Salary in USD")
    plt.ylabel("Continents")
    st.pyplot()

elif visualization_option == "Job distribution":

    st.markdown("""

                This pie chart shows distribution of jobs in the dataset.""")

    job_counts = filtered_df['job_title'].value_counts()

    top_5 = job_counts.nlargest(5)

    others = pd.Series([job_counts.sum() - top_5.sum()], index=['Other'])

    final_counts = pd.concat([top_5, others])

 

    plt.figure(figsize=(10, 6))

    plt.pie(final_counts, labels=final_counts.index, autopct='%1.1f%%', startangle=90)

    plt.title('Distribution of Job Titles (Top 5 + Other)')

    plt.axis('equal')

    st.pyplot()

# Show filtered data in a table
st.write("Filtered Data:")
st.write(filtered_df)

# EDA Answers
with st.expander("**EDA Answer** 📚"):
    st.markdown("""
        1. **What's the distribution of jobs in the dataset?** \n
            The distribution of jobs in the dataset is:
            - 26.4 percent are other jobs
            - 24.5 percent are Data Engineers
            - 21.3 percent are Data Scientists
            - 15.3 percent are Data Analysts
            - 9.6 percent are Machine Learning Engineers
            - 2.9 percent are Analytics Engineers

        2. **How does the mean salary change depending on the experience level?** \n
            The job salary distribution are changing as we would excpect. The lowest paying are the entry-level jobs, thereafter the mid-level jobs, followed by the senior-level and the highest paying jobs are the executive-level jobs

        3. **How does the salary change depending on the region?** \n
            The highest paying region is the Americas, where the lowest paying is Africa

        4. **Which country has the highest mean salary in Europe?** \n
            Bosnia and Herzegovina has highest mean salary in Europe. But that's because there is only one job from Bosnia in the dataset. So Ireland would be more realistic option

        5. **What are the top ten countries according to DS mean salary?** \n
            The highest paying country is Qatar where the salary is 300.000 USD annualy,
            Then Israel, Puerto Rico, United States, Canada, Saudi Arabia, Australia, New Zealand, Bosnia and Herzegovina
            The 10th highest is Ireland with about 120.000 USD

        6. **In which countries are there the most DS job opportunities?** \n
            The United States has the most job oppertunities, and is almost 6000, where the second most is United Kingdom with below 500. But since the data is mainly from the US, the numbers are not very representative.
                
    """)