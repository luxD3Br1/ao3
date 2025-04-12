# Streamlit Combination Count Dashboard

This Streamlit application is designed to visualize and explore data related to combinations of different categories and their associated counts. It allows users to filter data based on ratings, archive warnings, categories, and freeform names to discover the combinations with the highest counts.

## Key Features

*   **Interactive Filtering:**  Utilize sidebar filters to narrow down the data based on:
    *   **Rating:**  Filter by content rating (e.g., Not Rated, General Audiences, Mature).
    *   **Archive Warning:** Filter by archive warnings (e.g., Creator Chose Not To Use Archive Warnings, Graphic Depictions Of Violence).
    *   **Category:** Filter by relationship categories (e.g., F/F, F/M, Gen, M/M).
    *   **Freeform Names:** Filter by freeform tags (e.g., Complete, Work In Progress).
*   **Top Combinations Display:**  View a scrollable table displaying the top 15 combinations with the highest counts, based on selected filters.
*   **User-Friendly Labels:** Filters and table display human-readable labels for ratings, archive warnings, and categories instead of numerical IDs, making the data easier to understand.
*   **Data Loading from Text File:**  The application reads data from a text file (`ao3.txt` in the `data` folder), allowing for easy data updates.

## How to Use

1.  **Prerequisites:** Ensure you have Python and Streamlit installed. You can install them using pip:
    ```bash
    pip install streamlit pandas
    ```
2.  **Data File:** Place your data in a text file named `ao3.txt` inside a folder named `data` in the same directory as your Streamlit script (e.g., `app.py`). The data should be in the format of a Python dictionary string (or JSON-like structure as shown in the example).
3.  **Run the App:** Navigate to the directory containing `app.py` in your terminal and run:
    ```bash
    streamlit run app.py
    ```
4.  **Interact with the Dashboard:** The application will open in your web browser. Use the sidebar filters to select desired criteria. The main area will display the top combinations based on your selections.

## Data Source

The application reads data from the `ao3.txt` text file.  This file should contain data in a dictionary format where keys represent combination IDs and values include a `combination` list (with filter criteria) and a `count`.

## Libraries Used

*   **Streamlit:** For creating the interactive dashboard.
*   **Pandas:** For data manipulation and display in a DataFrame.
*   **ast (or json):** For safely loading data from the text file.

---

**Note:**  This README assumes your data is structured as discussed in the previous conversations and that you are using `ast.literal_eval` to load from `ao3.txt`.  If you are using JSON, update the "Libraries Used" and "Data File" sections accordingly to mention `json.loads`.

**How to use this README:**

1.  Create a file named `README.md` in the root directory of your Streamlit project (the same directory where `app.py` and the `data` folder are located).
2.  Copy and paste the markdown content above into your `README.md` file.
3.  You can further customize this README with more details, screenshots, or specific instructions as needed for your project.
