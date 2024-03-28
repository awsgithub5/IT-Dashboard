import streamlit as st
import logging
import uuid
import pprint
import pandas as pd
from urllib.error import URLError
from datetime import datetime
import src.st_utils as st_utils
import src.utils as utils
import src.preprocess_CIDDS as preprocess_CIDDS
import src.visuals as visualization
from src.visuals import generate_textual_summary
import src.reporting as reporting
import openai
import lida
from lida import Manager, TextGenerationConfig, llm
from dotenv import load_dotenv
import os

#@Shrina
is_diaplay_explability = True
# Load environment variables for API keys
load_dotenv()
openai.api_key = ''

datasets = [
    {"label": "CIDDS", "path": "data//user_data//CIDDS-001.csv"}
]

user_id = 2
logger = logging.getLogger()
pp = pprint.PrettyPrinter(indent=2)

# Initialize LIDA manager with text generation configuration
lida = Manager(text_gen=llm("openai"))
textgen_config = TextGenerationConfig(n=1, temperature=0.5, model="gpt-4", use_cache=True)

# Store LIDA manager in the session state
st.session_state['lida'] = lida
st.session_state['textgen_config'] = textgen_config

def run():
    # Initialize lida and textgen_config in the session state
    if "lida" not in st.session_state:
        st.session_state['lida'] = lida
    if "textgen_config" not in st.session_state:
        st.session_state['textgen_config'] = textgen_config
    
    # Create a sidebar form for data selection
    with st.sidebar.form(key="form"):
        st.write(" ## Get Data")
        tenant_name_selection = st.selectbox('Select Application', datasets, format_func=lambda x: x['label'], key="dataset")
        start_date = st.date_input('📅 Start Date', key="start_date")
        end_date = st.date_input("📅 End Date", key="end_date", max_value=datetime.today())
        submit_button = st.form_submit_button(label="Submit", on_click=st_utils.init_session)

    # Reset visualization paths when 'Submit' is pressed
    if submit_button:
        st.session_state['visualization_paths'] = []
        st.session_state['submit_pressed'] = True

    # Load data and generate summary when 'Submit' is pressed
    if st.session_state.get('submit_pressed') and tenant_name_selection.get('path'):
        if tenant_name_selection['path'].endswith('.csv'):
            input_file = tenant_name_selection['path']
            output_file = "F://John Deere//partsopsdashboard-main//data//preprocessed//preprocessed_data.csv"
            preprocess_CIDDS.preprocess_data(input_file, output_file)
            st.session_state['df'] = pd.read_csv(output_file)
        elif tenant_name_selection['path'].endswith('.json'):
            st.session_state['df'] = pd.read_json(tenant_name_selection['path'])
        
        # Display the loaded dataframe
        st.dataframe(st.session_state['df'].head(), hide_index=True)
        st.subheader("Summary")
        try:
            # Generate textual summary
            textual_summary = generate_textual_summary(st.session_state['df'])
            st.write(textual_summary)
        except Exception as e:
            st.error(f"An error occurred while generating the summary: {str(e)}")
        
        # Generate summary using LIDA
        st.session_state['summary'] = lida.summarize(st.session_state['df'], summary_method="default", textgen_config=textgen_config)
        st.session_state['processed_custom_kpi'] = False
        
        if 'processed_custom_kpis' not in st.session_state:
            st.subheader("KPIs")

            # Load custom KPIs from CSV file
            custom_kpis = pd.read_csv('data\KPIs\custom_kpis.csv')
            custom_kpis = custom_kpis['KPI_Text'].tolist()

            # Process KPI queries
            for kpi_text in custom_kpis:
                graph_title = "Graph Title"  # Provide the appropriate graph title
                textual_summary = st.session_state['summary']  # Use the textual summary from the session state
                st_utils.visuals(kpi_text, graph_title, textual_summary)

    if "df" in st.session_state:
        with st.container(border=True):
            st.write("##### KPIs")
            
            # Display KPI buttons and visualizations
            for i, kpi in enumerate(st.session_state["KPIs"][:4]):
                with st.container(border=True):
                    st.write(kpi["text"])
                    st.button("Generate", key=f"kpi_button_{i}",
                              on_click=st_utils.visual_edit, args=(f"kpi_{i}", st.session_state["summary"], kpi["KPI"], kpi["text"], ), disabled=kpi["disabled"])
                    
                    # Display KPI text area and visualization if available
                    if f"selected_kpi_text_{i}" in st.session_state:
                        st.text_area(f"KPI {i+1}", value=st.session_state[f"selected_kpi_text_{i}"], height=100,
                                     on_change=st_utils.visual_edit, args=(f"kpi_{i}", st.session_state["summary"], None, ))
                        st.image(st.session_state[f"selected_visualization_{i}"], use_column_width="auto")
                        if is_diaplay_explability:
                            with st.expander("See explanation"):
                                for description in st.session_state[f"selected_visualization_description_{i}"]:
                                    st.markdown(f"**{description['section']}**")
                                    st.write(description["explanation"])
                                    st.divider()
            
            # Custom KPI section
            with st.container(border=True):
                st.write(" ##### Custom KPI")
                id = str(uuid.uuid4())
                kpi_query = st.text_input("Enter your custom KPI",
                                          on_change=st_utils.visual_edit, args=(id, st.session_state["summary"],), key=id, placeholder="line chart for pass and failed")

    # Generate Report button
    if st.sidebar.button('Generate Report', type="primary"):
        with st.container(border=True):
            dataset = tenant_name_selection['label']
            start_date = st.session_state.start_date
            end_date = st.session_state.end_date

            visualization_details = st.session_state["visualizations"]
            if len(visualization_details):
                pdf_path = reporting.generate_report(dataset, [dataset], start_date, end_date, visualization_details)
                st_utils.displayPDF(pdf_path)
            else:
                st.write("Please create some KPIs before generating report")

if __name__ == "__main__":
    run()