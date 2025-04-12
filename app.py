import streamlit as st
import pandas as pd
import ast

# --- HTML Label Mappings ---
rating_labels = {
    "9": "Not Rated",
    "10": "General Audiences",
    "11": "Teen And Up Audiences",
    "12": "Mature",
    "13": "Explicit"
}

archive_warning_labels = {
    "14": "Creator Chose Not To Use Archive Warnings",
    "17": "Graphic Depictions Of Violence",
    "18": "Major Character Death",
    "16": "No Archive Warnings Apply",
    "19": "Rape/Non-Con",
    "20": "Underage Sex"
}

category_labels = {
    "116": "F/F",
    "22": "F/M",
    "21": "Gen",
    "23": "M/M",
    "2246": "Multi",
    "24": "Other"
}

# Function to load data from text file (same as before)
def load_data_from_txt(filepath):
    try:
        with open(filepath, 'r') as f:
            data_str = f.read()
            data = ast.literal_eval(data_str)
            return data
    except FileNotFoundError:
        st.error(f"Error: File not found at path: {filepath}")
        return None
    except Exception as e:
        st.error(f"Error loading data from file: {e}")
        return None

# File path to your data
data_filepath = "data/ao3.txt"

# Load data from the text file
data = load_data_from_txt(data_filepath)

# Check if data was loaded successfully
if data is None:
    st.stop()

def transform_to_dataframe(data):
    df_rows = []
    for key, value in data.items():
        combination_list = value['combination']
        count = value['count']
        for combination_dict in combination_list:
            row = combination_dict.copy()
            row['count'] = count
            df_rows.append(row)
    df = pd.DataFrame(df_rows)
    return df

df = transform_to_dataframe(data)
st.set_page_config(layout="wide")
st.title("Combination Count Dashboard")

# Sidebar - Filter Card
st.sidebar.header("Filter Options")

unique_rating_ids = df['rating_ids'].explode().unique().tolist() if 'rating_ids' in df.columns else []
unique_archive_warning_ids = df['archive_warning_ids'].explode().unique().tolist() if 'archive_warning_ids' in df.columns else []
unique_category_ids = df['category_ids'].explode().unique().tolist() if 'category_ids' in df.columns else []
unique_freeform_names = df['freeform_names'].explode().unique().tolist() if 'freeform_names' in df.columns else []

# Use labels for filter display, but keep IDs for filtering logic
rating_id_options = [ (label, id_val) for id_val, label in rating_labels.items() if id_val in unique_rating_ids] # Ensure only available ids are shown
archive_warning_id_options = [(label, id_val) for id_val, label in archive_warning_labels.items() if id_val in unique_archive_warning_ids]
category_id_options = [(label, id_val) for id_val, label in category_labels.items() if id_val in unique_category_ids]

selected_rating_labels = st.sidebar.multiselect("Select Rating", options=rating_id_options, format_func=lambda option: option[0]) # Display label, return id
selected_archive_warning_labels = st.sidebar.multiselect("Select Archive Warning", options=archive_warning_id_options, format_func=lambda option: option[0])
selected_category_labels = st.sidebar.multiselect("Select Category", options=category_id_options, format_func=lambda option: option[0])
selected_freeform_names = st.sidebar.multiselect("Select Freeform Names", options=unique_freeform_names)

# Extract IDs from selected labels for filtering
selected_rating_ids_filter = [option[1] for option in selected_rating_labels]
selected_archive_warning_ids_filter = [option[1] for option in selected_archive_warning_labels]
selected_category_ids_filter = [option[1] for option in selected_category_labels]


# Filter DataFrame (use IDs for filtering logic)
filtered_df = df.copy()

if selected_rating_ids_filter:
    filtered_df = filtered_df[filtered_df['rating_ids'].apply(lambda x: any(item in selected_rating_ids_filter for item in x) if isinstance(x, list) else False)]
if selected_archive_warning_ids_filter:
    filtered_df = filtered_df[filtered_df['archive_warning_ids'].apply(lambda x: any(item in selected_archive_warning_ids_filter for item in x) if isinstance(x, list) else False)]
if selected_category_ids_filter:
    filtered_df = filtered_df[filtered_df['category_ids'].apply(lambda x: any(item in selected_category_ids_filter for item in x) if isinstance(x, list) else False)]
if selected_freeform_names:
    filtered_df = filtered_df[filtered_df['freeform_names'].apply(lambda x: any(item in selected_freeform_names for item in x) if isinstance(x, list) else False)]

# Display Highest Count
st.header("Top Combinations (Max 15)")

sorted_df = filtered_df.sort_values(by='count', ascending=False).head(15)

# Function to map IDs to labels for DataFrame display
def map_labels(id_list, label_dict):
    if isinstance(id_list, list):
        return [label_dict.get(str(item), str(item)) for item in id_list] # str conversion for keys
    return id_list # Return original if not a list (or no mapping needed)

# Apply label mapping to DataFrame for display
if 'rating_ids' in sorted_df.columns:
    sorted_df['rating_ids_labels'] = sorted_df['rating_ids'].apply(lambda x: map_labels(x, rating_labels))
    sorted_df = sorted_df.drop(columns=['rating_ids']).rename(columns={'rating_ids_labels': 'rating'}) # Replace IDs column with labels
if 'archive_warning_ids' in sorted_df.columns:
    sorted_df['archive_warning_ids_labels'] = sorted_df['archive_warning_ids'].apply(lambda x: map_labels(x, archive_warning_labels))
    sorted_df = sorted_df.drop(columns=['archive_warning_ids']).rename(columns={'archive_warning_ids_labels': 'archive_warning'})
if 'category_ids' in sorted_df.columns:
    sorted_df['category_ids_labels'] = sorted_df['category_ids'].apply(lambda x: map_labels(x, category_labels))
    sorted_df = sorted_df.drop(columns=['category_ids']).rename(columns={'category_ids_labels': 'category'})
if 'freeform_names' in sorted_df.columns:
    sorted_df = sorted_df.rename(columns={'freeform_names': 'freeform_names'}) # Just rename for clarity


st.dataframe(sorted_df, height=500)