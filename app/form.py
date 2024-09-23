import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import statsmodels.api as sm
from streamlit_extras.colored_header import colored_header


#st.set_option('deprecation.showPyplotGlobalUse', False)


def handle_transformation(df, column, transformation, curr_type):
    """
    Handles different data transformations based on the type and the selected transformation.
    
    Args:
        df (pd.DataFrame): The dataframe to apply transformations on.
        column (str): The column to apply the transformation to.
        transformation (str): The type of transformation to apply.
        curr_type (type): The type of the column (e.g., float, object).
    """
    if transformation == 'Find and Replace':
        if curr_type == float or curr_type == int:
            with st.form(key='float_fr'):
                user_input1 = st.number_input(label="Type a number you want to find", format="%f")
                user_input2 = st.number_input(label="Enter a number you want to replace with", format="%f")
                submit_button = st.form_submit_button(label='Submit')
            if submit_button:
                df[column] = df[column].replace(user_input1, user_input2)
                st.dataframe(df)
        
        elif curr_type == object:
            with st.form(key='obj_fr'):
                user_input1 = st.text_input(label='Enter the information to find')
                user_input2 = st.text_input(label="Enter the information to replace with")
                submit_button = st.form_submit_button(label='Submit')
            if submit_button:
                df[column] = df[column].replace(user_input1, user_input2)
                st.dataframe(df)
    
    elif transformation == 'Update Your Data':
        with st.form(key='update'):
            edited_df = st.data_editor(df)
            submit_button = st.form_submit_button(label='Submit')
        if submit_button:
            st.dataframe(edited_df)
    
    elif transformation == 'Filter Data':
        if curr_type == float or curr_type == int:
            with st.form(key='float_fltr'):
                user_input1 = st.number_input(label="Type a number to filter", format="%f")
                submit_button = st.form_submit_button(label='Submit')
            if submit_button:
                filtered_df = df[df[column] == user_input1]
                st.dataframe(filtered_df)
        
        elif curr_type == object:
            with st.form(key='obj_fltr'):
                user_input1 = st.text_input(label="Enter the information to filter")
                submit_button = st.form_submit_button(label='Submit')
            if submit_button:
                filtered_df = df[df[column] == user_input1]
                st.dataframe(filtered_df)

def na_values(df):
    nan_mask = df.isna()
    where_nan = nan_mask.any()
    col_nan = where_nan[where_nan].index.tolist()
    return col_nan

def interact_na(df, lst, cont_none, nan_menu, curr_nacol):
    if cont_none == lst[0]:
        if curr_nacol == float or curr_nacol == int:
            num_inp = st.number_input(label="Enter a number you want to replace with", format="%f")
            df[nan_menu] = df[nan_menu].fillna(num_inp)
        else:
            text_inp = st.text_input(label ="Enter the information to replace with")
            df[nan_menu] = df[nan_menu].fillna(text_inp)
        #st.success("Successfully changed the data")
    elif cont_none == lst[1]:
        df = df.dropna(subset=[nan_menu])
        st.dataframe(df)
        #st.success("Successfully dropped the None values")
    elif cont_none == lst[2]:
        # Calculate the number of NaN values per column
        nan_counts = df.isna().sum()

        # Calculate the total number of rows
        total_rows = len(df)

        # Calculate the percentage of NaN values per column
        nan_percentages = (nan_counts / total_rows) * 100

        # Create a new DataFrame with columns, NaN counts, and NaN percentages
        nan_summary_df = pd.DataFrame({
            'Column': nan_counts.index,
            'NaN Count': nan_counts.values,
            'NaN Percentage': nan_percentages.values
        })

        st.dataframe(nan_summary_df)
    else:
        df = df.dropna()
        #st.success("Successfully deleted all rows containing NaN")
    return df

def plot_graphs(df):
    """
    Provides options to plot different types of graphs: Line, Bar, Scatter with y-axis showing value counts.
    
    Args:
        df (pd.DataFrame): The dataframe to plot.
    """
    
    colored_header(
        label="Graph Options",
        description="Note: This is currently in the beta stage. You may come across exceptions!",
        color_name="violet-70",
    )

    graph_type = st.selectbox("Choose the type of graph", ["Line", "Bar", "Scatter", "Correlation"], key='graph_type')
    
    if graph_type == "Line":
        x_cols = st.multiselect("Select Columns for X-axis", df.columns, key='x_columns')
        y_col = st.selectbox("Select Y-axis Column", df.columns, key='y_axis')
        
        if x_cols and y_col:
            st.write(f"**Line Plot of {y_col} for selected X-axis columns**")
            plt.figure(figsize=(12, 6))
            for x_col in x_cols:
                if x_col in df.columns:
                    # Ensure that the x_col is numeric for line plotting
                    df[x_col] = pd.to_numeric(df[x_col], errors='coerce')
                    sns.lineplot(data=df, x=x_col, y=y_col, label=x_col, marker='o')
            plt.xlabel('X-axis')
            plt.ylabel(y_col)
            plt.title(f'Line Plot of {y_col} for Selected X-axis Columns')
            plt.legend()
            st.pyplot()

    elif graph_type == "Bar":
        x_col = st.selectbox("Select X-axis", df.columns, key='bar_x_axis')
        
        # Compute value counts for the x-axis column
        value_counts = df[x_col].value_counts().reset_index()
        value_counts.columns = [x_col, 'Count']
        
        # Calculate percentages for the bar plot
        total_count = value_counts['Count'].sum()
        value_counts['Percentage'] = (value_counts['Count'] / total_count) * 100
        
        st.write(f"**Bar Chart of Percentages for {x_col}**")
        plt.figure(figsize=(10, 5))
        
        # Convert x_col to categorical
        value_counts[x_col] = value_counts[x_col].astype(str)
        
        bars = plt.bar(value_counts[x_col], value_counts['Count'], color='skyblue')
        plt.ylabel('Count')
        plt.title(f'Bar Chart of Percentages for {x_col}')
        
        # Annotate bars with percentage values
        for bar, pct in zip(bars, value_counts['Percentage']):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, height + height * 0.01,
                     f'{pct:.2f}%', ha='center', va='bottom', weight='bold')
        
        st.pyplot()
    
    elif graph_type == "Scatter":
        x_col = st.selectbox("Select X-axis", df.columns, key='scatter_x_axis')
        y_col = st.selectbox("Select Y-axis", df.columns, key='scatter_y_axis')
        
        if x_col and y_col:
            st.write(f"**Scatter Plot of {y_col} vs {x_col}**")
            
            # Create Scatter Plot
            plt.figure(figsize=(12, 6))
            sns.scatterplot(data=df, x=x_col, y=y_col, color='blue', label='Data Points')
            
            # Add option for Line of Best Fit
            show_best_fit = st.checkbox("Show Line of Best Fit", key='show_best_fit')
            if show_best_fit:
                best_fit_color = st.color_picker("Choose Line of Best Fit Color", "#FF0000", key='line_color')
                sns.regplot(data=df, x=x_col, y=y_col, scatter=False, color=best_fit_color, line_kws={"label": "Best Fit"})
                plt.legend()
            
            plt.xlabel(x_col)
            plt.ylabel(y_col)
            plt.title(f'Scatter Plot of {y_col} vs {x_col}')
            st.pyplot()
    elif graph_type == "Correlation":
        # Calculate the correlation matrix
        target_col = st.selectbox("Select Target Column", df.columns, key='target_column')
        
        if target_col in df.columns:
            # Convert target column to numeric if it is not already
            if df[target_col].dtype == 'object':
                df[target_col] = pd.to_numeric(df[target_col], errors='coerce')
            
            # Filter numeric columns
            numeric_columns = df.select_dtypes(include=[float, int]).columns
            
            # Ensure target column is excluded from the numeric columns for correlation calculation
            numeric_columns = numeric_columns.difference([target_col])
            
            # Calculate correlation with the target column
            correlations = df[numeric_columns].corrwith(df[target_col])
            
            # Plot the correlation bar plot
            st.write(f"**Correlation with {target_col}**")
            plt.figure(figsize=(20, 8))
            correlations.plot(kind='bar', grid=True)
            plt.title(f"Correlation with {target_col} Column")
            plt.xlabel('Columns')
            plt.ylabel('Correlation')
            st.pyplot()
            
            # Display correlation values
            st.write("**Correlation Coefficients:**")
            st.write(correlations)

def display_dashboard():
    """
    Main function to display the dashboard with file upload, data transformation, and graph plotting.
    """
    st.title("Data Playground")
    st.write("'Play' with your data!")
    colored_header(
                label="Upload Your Data",
                description = "Be sure to only upload CSV files!",
                color_name="violet-70",
            )
    uploaded_file = st.file_uploader("Choose a File")

    if uploaded_file is not None:
        # Read CSV
        uploading = st.container()
        with uploading:
            df1 = pd.read_csv(uploaded_file)
        if df1.isna().any().any():
            curr_file, nan_values = st.columns(2)
        else:
            curr_file = st.container()
        
        with curr_file:
            colored_header(
                label="Your Uploaded Data",
                description = "This is a preview of your data",
                color_name="violet-70",
            )
            st.dataframe(df1)


        # Get column names
        col = df1.columns

        #deal with None values
        if df1.isna().any().any():
            
            with nan_values:
                colored_header(
                    label="Dealing with NaN Values",
                    description = "Your data contains None types! Choose what to do next",
                    color_name="violet-70",
                )
                options_list = ['Replace with another value', 'Drop None values in Specific Column', 'Info Table on None Values', 'Drop All']
                cont_none = st.selectbox("Choose how to deal with None values", options_list)
                nan_menu = st.selectbox("Choose column to interact with", na_values(df1))
                curr_nacol = df1[nan_menu].dtype

                
                df1 = interact_na(df1, options_list, cont_none, nan_menu, curr_nacol)
                if st.button("Change"):
                    st.success("Successfully changed the data")

            

        data_change, graph = st.columns(2)
        with data_change:
            colored_header(
                    label="Transform Your Data",
                    description = "This is optional! You may want to query, update your data manually, or find and replace values in a specifc column",
                    color_name="violet-70",
                )
            # Select column and transformation type
            menu = st.selectbox('Columns', col, key='menu_column')
            transform = st.selectbox("Choose", ['Filter Data', 'Update Your Data', 'Find and Replace'], key='transformation')
            curr_type = df1[menu].dtype

            # Handle transformations using the function
            handle_transformation(df1, menu, transform, curr_type)
        with graph:
            # Plot graphs
            plot_graphs(df1)

    else:
        st.warning("You need to upload a CSV file to proceed.")

# If this script is run directly, it will execute the display_dashboard function
if __name__ == "__main__":
    st.set_page_config(
        layout = "wide",
        initial_sidebar_state= "expanded"
    )
    display_dashboard()


