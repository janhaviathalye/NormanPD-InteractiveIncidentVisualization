from flask import Flask, request, render_template, redirect, url_for, session
import os
import pandas as pd
from fetchincidents import fetchincidents
from extractincidents import extractincidents
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from bokeh.transform import cumsum

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.palettes import Category10, Category20c
from bokeh.layouts import column
from datetime import datetime
from urllib.error import HTTPError, URLError

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Use a randomly generated secret key for security

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url_input = request.form.get('urls', '').strip()
        uploaded_files = request.files.getlist('files')

        incident_list = []
        encountered_errors = []

        # Handle URLs input
        if url_input:
            for single_url in url_input.split():
                try:
                    raw_data = fetchincidents(single_url)
                    extracted_incidents = extractincidents(raw_data)
                    incident_list.extend(extracted_incidents)
                except HTTPError as http_err:
                    msg = f"HTTP Error {http_err.code} for URL: {single_url}"
                    print(msg)
                    encountered_errors.append(msg)
                except URLError as url_err:
                    msg = f"URL Error for URL: {single_url} - {url_err.reason}"
                    print(msg)
                    encountered_errors.append(msg)
                except Exception as ex:
                    msg = f"Failed to fetch from URL: {single_url} - {str(ex)}"
                    print(msg)
                    encountered_errors.append(msg)

        # Handle file uploads
        for file in uploaded_files:
            if file and file.filename.lower().endswith('.pdf'):
                try:
                    pdf_content = file.read()
                    incidents_from_pdf = extractincidents(pdf_content)
                    incident_list.extend(incidents_from_pdf)
                except Exception as ex:
                    msg = f"Failed to process file: {file.filename} - {str(ex)}"
                    print(msg)
                    encountered_errors.append(msg)

        if not incident_list:
            error_msg = "No incidents were found or the input provided is invalid."
            if encountered_errors:
                error_msg += " Errors: " + "; ".join(encountered_errors)
            return render_template('index.html', error=error_msg)

        # Save incidents data in session for later use
        session['incident_data'] = incident_list
        return redirect(url_for('display_results'))

    return render_template('index.html')


@app.route('/results', methods=['GET', 'POST'])
def display_results():
    # Retrieve incidents data from session
    incidents = session.get('incident_data', [])
    if not incidents:
        return redirect(url_for('home'))

    df_incidents = pd.DataFrame(incidents)

    # Convert 'Date Time' to datetime objects
    df_incidents['Date Time'] = pd.to_datetime(df_incidents['Date Time'], format='%m/%d/%Y %H:%M', errors='coerce')

    # Remove entries with invalid dates
    df_incidents.dropna(subset=['Date Time'], inplace=True)

    if df_incidents.empty:
        return render_template('results.html', error="No valid incident data available for display.")

    try:
        # Text vectorization and clustering
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(df_incidents['Nature'])
        kmeans_model = KMeans(n_clusters=4, random_state=42)
        cluster_labels = kmeans_model.fit_predict(tfidf_matrix)

        # Dimensionality reduction for visualization
        pca_transformer = PCA(n_components=2)
        pca_coordinates = pca_transformer.fit_transform(tfidf_matrix.toarray())
        df_incidents['Cluster'] = cluster_labels
        df_incidents['X'] = pca_coordinates[:, 0]
        df_incidents['Y'] = pca_coordinates[:, 1]

        # Assign colors based on cluster
        color_palette = Category10[10]
        df_incidents['Color'] = df_incidents['Cluster'].apply(lambda x: color_palette[x])

        # Clustering Scatter Plot
        source_cluster = ColumnDataSource(df_incidents)
        cluster_figure = figure(
            title="Incident Clusters Based on Nature",
            sizing_mode='stretch_width',
            height=600,
            tools="pan,wheel_zoom,box_zoom,reset,hover,save",
            margin=(50, 50, 50, 50)
        )
        cluster_figure.scatter(
            'X',
            'Y',
            source=source_cluster,
            color='Color',
            legend_field='Cluster',
            size=8
        )
        hover_cluster = HoverTool(tooltips=[("Nature", "@Nature"), ("Cluster", "@Cluster")])
        cluster_figure.add_tools(hover_cluster)
        cluster_figure.legend.title = 'Cluster'
        cluster_figure.legend.location = "top_left"

        # Top 10 Incident Types Bar Chart
        top_nature = 10
        top_natures = df_incidents['Nature'].value_counts().nlargest(top_nature).reset_index()
        top_natures.columns = ['Nature', 'Count']
        source_nature = ColumnDataSource(top_natures)
        bar_chart = figure(
            x_range=top_natures['Nature'],
            title="Top 10 Incident Types",
            sizing_mode='stretch_width',
            height=600,
            tools="pan,wheel_zoom,box_zoom,reset,hover,save",
            margin=(50, 50, 50, 50)
        )
        bar_chart.vbar(
            x='Nature',
            top='Count',
            width=0.9,
            source=source_nature,
            legend_field="Nature",
            line_color='white',
            fill_color='navy'
        )
        bar_chart.xaxis.major_label_orientation = 1.2
        bar_chart.y_range.start = 0
        hover_bar = HoverTool(tooltips=[("Nature", "@Nature"), ("Count", "@Count")])
        bar_chart.add_tools(hover_bar)
        bar_chart.legend.visible = False

        # Pie Chart: Distribution of Incidents Across Clusters
        cluster_distribution = df_incidents['Cluster'].value_counts().reset_index()
        cluster_distribution.columns = ['Cluster', 'Count']
        cluster_distribution['Angle'] = cluster_distribution['Count'] / cluster_distribution['Count'].sum() * 2 * 3.141592653589793
        cluster_distribution['Color'] = Category20c[len(cluster_distribution)] if len(cluster_distribution) <= 20 else Category10[10]
        
        source_pie = ColumnDataSource(cluster_distribution)
        pie_chart = figure(
            title="Distribution of Incidents Across Clusters",
            sizing_mode='stretch_width',
            height=600,
            tools="hover,save",
            toolbar_location=None,
            tooltips="@Cluster: @Count",
            x_range=(-0.5, 1.0)
        )
        pie_chart.wedge(
            x=0, y=1, radius=0.4,
            start_angle=cumsum('Angle', include_zero=True),
            end_angle=cumsum('Angle'),
            line_color="white",
            fill_color='Color',
            legend_field='Cluster',
            source=source_pie
        )
        pie_chart.axis.axis_label = None
        pie_chart.axis.visible = False
        pie_chart.grid.grid_line_color = None

        # Combine all plots into a single layout
        combined_layout = column(cluster_figure, bar_chart, pie_chart, sizing_mode='stretch_width')

        script_components, div_components = components(combined_layout)

    except Exception as viz_error:
        print(f"Visualization Error: {viz_error}")
        return render_template('results.html', error="Failed to generate visualizations.")

    if request.method == 'POST':
        user_feedback = request.form.get('feedback')
        if user_feedback:
            print("Feedback Received:", user_feedback)
            feedback_status = True
            return render_template('results.html', script=script_components, div=div_components, feedback_submitted=feedback_status)

    return render_template('results.html', script=script_components, div=div_components, feedback_submitted=False)


if __name__ == '__main__':
    app.run(debug=True)
