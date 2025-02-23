# NormanPD-InteractiveIncidentVisualization

Name: Janhavi Athalye

# Project Description

This project builds on [NormanPD-PDFParser](https://github.com/janhaviathalye/NormanPD-PDFParser), where data from the Norman, Oklahoma Police Department’s incident reports was processed and stored. The goal is to create an interactive web interface that serves as the final stage of the data pipeline, enabling users to visualize and interact with the data while also providing feedback. The interface accepts incident reports via file upload or URLs, extracts fields such as date/time, incident number, location, and nature of the incident using the pypdf library and regular expressions.

The interface offers three distinct visualizations implemented with Bokeh: a clustering scatter plot that groups incidents based on their nature, a bar graph comparing the frequency of various incident types, and a pie chart displaying the proportional distribution of incidents across clusters. These interactive visualizations allow users to explore patterns, compare data, and gain meaningful insights. Additionally, a feedback mechanism is integrated into the interface, enabling users to provide suggestions or comments, which are collected for further application refinement.

Built with Flask, this project demonstrates the integration of tools such as pypdf, scikit-learn,and Bokeh to create a complete end-to-end solution. This project not only enhances data usability by presenting it in an intuitive and actionable format but also highlights the importance of end-user interaction in the data pipeline.

# How to install
Ensure you have pipenv installed otherwise install it using the following command.

```
pip install pipenv
```
The following command can also be used.

```
pipenv install -e
```

# How to run

To run the project, ensure you have all dependencies installed and activate your pipenv environment. Then execute the following command to start the web interface:

```
pipenv run python app.py
```
Once the server is running, open a web browser and navigate to:

http://127.0.0.1:5000/

Here, you can upload one or more NormanPD-style incident PDFs via file upload or URL. The application will process the files, visualize the data through interactive charts, and allow you to provide feedback. The visualizations include clustering of incidents, a bar graph comparing incident types, and a pie chart showing the proportional distribution of incidents.

To run the test cases, execute the following command:

```
pipenv run python -m pytest
```

# Project Demo Video

https://drive.google.com/file/d/1nf5-W6epGMuU6F3t-LRjyqIovHbAVeRX/view?usp=sharing


# Functions

## app.py

The main entry point for the project. This file sets up the Flask web application, routes, and integrates the functions necessary for PDF processing, data storage, and visualization. It provides endpoints for uploading PDFs or providing URLs, displaying visualizations, and collecting user feedback.

## fetchincidents(url)

This function takes the URL of a NormanPD-style incident PDF, downloads it, and returns the binary data. It includes error handling for HTTP and URL-related issues, ensuring robustness when downloading files.

## extractincidents(incident_data)

This function processes the binary PDF data using the pypdf library and extracts the following fields using regular expressions:

- Date/Time
- Incident Number
- Location
- Nature of the Incident
- ORI

The extracted data is returned as a list of dictionaries, where each dictionary corresponds to a single incident.

## display_results()

A Flask route (/results) that handles data visualization and feedback submission. It retrieves processed data from the session, performs clustering using KMeans and PCA, and generates three visualizations:

- A scatter plot for incident clustering.
- A bar graph comparing the frequency of different incident types.
- A pie chart showing the proportional distribution of incidents across clusters.

The visualizations are created using Bokeh and embedded into the web interface.

## home()

A Flask route (/) that serves as the home page for the application. It provides a form for users to:

- Upload PDF files.
- Enter URLs pointing to NormanPD incident PDFs.

This route handles input validation, calls fetchincidents() and extractincidents() as needed, and stores the extracted data in the session for further processing.

## Visualization Functions

These are integrated into display_results() and handle the creation of interactive plots using Bokeh:

- Clustering Plot: Uses KMeans and PCA to display incident clusters based on their nature.

- Bar Graph: Displays the frequency of various incident types, sorted by occurrence.

- Pie Chart: Visualizes the proportional distribution of incidents across clusters. Uses cumsum to calculate angles for each slice.

## Feedback Handling

Within the /results route, feedback submitted by users is captured and logged for further analysis. This feature ensures that user insights can be incorporated into future refinements of the application.

# Visualizations and Graphs

The web application provides three distinct visualizations to help users explore and understand the incident data effectively. Each visualization is dynamically generated using the data extracted from the uploaded PDFs, ensuring that the results are tailored to the specific input. Below are the details of the three visualizations:

### 1. Clustering Scatter Plot

- Purpose: This scatter plot groups incidents based on their nature, allowing users to identify patterns and relationships between different types of incidents.

- How It Works: Clustering is performed using the KMeans algorithm to group similar incidents into clusters.
PCA (Principal Component Analysis) reduces the data to two dimensions, making it easier to visualize the clusters.
Each cluster is represented by a different color, with points in the scatter plot corresponding to individual incidents.

- Interactivity: Users can hover over the points to see detailed information about specific incidents, such as the incident number, date/time, and location. Zoom and pan tools allow users to explore the visualization in detail.

- Insights: This plot is particularly useful for identifying common types of incidents and understanding how they relate to one another.

### 2. Comparison Bar Graph

- Purpose: This bar graph compares the frequency of different incident types, providing a clear view of the most and least common incidents.

- How It Works: The application calculates the frequency of each type of incident from the extracted data. The incidents are displayed as bars, sorted by frequency. The height of each bar corresponds to the number of occurrences for that incident type.

- Interactivity: Hovering over a bar reveals the exact count of incidents for that type. Users can quickly identify patterns, such as which types of incidents occur most frequently.

- Insights: This graph helps users understand the overall distribution of incidents and prioritize resources or focus areas based on incident frequency.

### 3. Pie Chart – Incident Distribution

- Purpose: This pie chart visualizes the proportional distribution of incidents across different clusters, offering a high-level overview of the data.

- How It Works: The incidents are grouped into clusters (using the same clusters as in the scatter plot), and the proportions of each cluster are calculated. Each slice of the pie chart represents a cluster, with the size of the slice corresponding to the percentage of incidents in that cluster. Colors are assigned to slices to differentiate clusters visually.

- Interactivity: Hovering over a slice displays the cluster number and the exact number of incidents in that cluster. The chart allows users to focus on specific segments by hovering or zooming in.

- Insights: This chart is useful for identifying which clusters dominate the dataset and understanding the overall distribution of incidents.


# Test Cases

This project includes several test cases designed to verify the correctness and functionality of key components, including PDF downloading, data extraction and visualizations. The tests ensure that each function works as expected and can handle edge cases, such as missing data, incorrect formatting, and multiple-line fields.

The tests are located in the tests/ directory. Each function is tested individually, and test coverage includes normal inputs as well as edge cases. You can run all the tests using pytest to verify the correctness of the application.

## test_fetchincidents.py

#### Purpose: 
Tests the fetchincidents() function to ensure it can successfully download a PDF file from the provided URL.

#### Test Case:

The test mocks the URL and simulates downloading the data. The response is a mock object that mimics a real PDF download.
It verifies that the function correctly handles HTTP requests and retrieves data.


## test_extractincidents.py

#### Purpose: 

Tests the extractincidents() function to ensure accurate extraction of incident data from a downloaded PDF.

#### Test Case:

The test provides sample incident PDF data, including both typical and edge-case scenarios (e.g., missing fields or malformed data).
It verifies that the function correctly extracts key fields (date/time, incident number, location, nature of the incident, ORI) and handles edge cases such as missing or incomplete information.


# External Resources

#### Flask Documentation:
Official Flask documentation was used to understand routing, creating endpoints, handling file uploads, and serving static files.

Link: https://flask.palletsprojects.com/

#### Bokeh Documentation:
The Bokeh documentation was crucial for creating interactive visualizations like scatter plots, bar graphs, and pie charts.

Link: https://docs.bokeh.org/

#### Stack Overflow:
Multiple solutions and discussions on Stack Overflow helped troubleshoot issues, such as file upload handling, regular expression queries, and Flask configuration challenges.

Link: https://stackoverflow.com/

# Bugs and Assumptions

## Bugs

#### PDF Parsing Inconsistencies:
The pypdf library may sometimes struggle with non-standard or poorly formatted PDFs, leading to incomplete or inaccurate data extraction. This is especially true for PDFs with complex layouts or embedded images, which can affect text parsing.

#### Data Overlap in Incident Fields:
In some cases, the extraction of multiple fields (e.g., date, location, incident number) from the same line or section in the PDF may result in data misalignment or duplication. This can occasionally lead to incorrect or missing data for certain incidents.

#### Visualization Rendering Delays:
When a large number of incidents are processed, the interactive visualizations (e.g., scatter plot, pie chart) may experience rendering delays or performance issues, particularly when displaying large datasets. This could affect user experience in cases of significant data volume.

## Assumptions

#### Standardized PDF Format:
The project assumes that the incident PDF files are formatted consistently according to the structure used by the Norman Police Department. Any deviation from this format (e.g., changes in layout or field names) may cause issues with data extraction.

#### Valid Incident Data:
It is assumed that the incident data in the PDF files is complete and follows a standard structure. Missing or malformed data (such as incomplete incident numbers or invalid dates) may not be handled perfectly by the current implementation.

#### User Interaction:
The web interface assumes users will upload PDFs or provide valid URLs. If a user uploads unsupported file types (e.g., non-PDF documents) or invalid URLs, the application may not handle these errors gracefully, and additional error handling may be required.

#### Data Integrity:
The system assumes that the extracted incident data is free from significant errors or corruption, as it relies on the integrity of the source PDF for accurate data extraction. Issues with the source files (such as corrupted or encrypted PDFs) may result in incomplete data extraction or errors in the final database.

#### Basic Browser Compatibility:
The web application assumes basic compatibility with modern browsers (Chrome, Firefox, etc.). Users with outdated browsers or certain privacy settings may encounter issues with rendering visualizations or uploading files.


