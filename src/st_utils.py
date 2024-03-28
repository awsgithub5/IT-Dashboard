import logging
import uuid
import json
import copy
import pprint
import time
import httpx
import json
import src.utils as utils
import streamlit as st
from datetime import datetime
import src.visuals as visualization

from lida.datamodel import Goal
logger = logging.getLogger()


is_diaplay_explability = True


def visual_edit(id:str, textual_summary, kpi_query=None, graph_title=""):
    """
    Edits the visualization based on the provided KPI query or the selected KPI text.
    
    Args:
        id (str): The unique identifier of the visualization.
        textual_summary (str): The textual summary of the data.
        kpi_query (str, optional): The KPI query for generating the visualization. Defaults to None.
        graph_title (str, optional): The title of the graph. Defaults to an empty string.
    """
    logger.debug("****inside edits st_utils zone****")
    if kpi_query is not None:
        goal = Goal(question=graph_title, visualization=kpi_query, rationale="")
        edited_query = kpi_query
    else:
        edited_query = st.session_state[f"selected_kpi_text_{id.split('_')[-1]}"]
        goal = Goal(question=graph_title, visualization=edited_query, rationale="")
    
    visuals_dict = dict()
    visuals_dict["id"] = str(uuid.uuid4())
    visuals_dict["kpi_query"] = edited_query
    logger.info(edited_query)
    
    # Initialize the session state key if it doesn't exist
    if "visualizations" not in st.session_state:
        st.session_state["visualizations"] = []
    
    # Remove the previous visualization with the same ID
    for visual in st.session_state["visualizations"]:
        if visual["id"] == id:
            st.session_state["visualizations"].remove(visual)
            break
    
    try:
        # Generate visuals using the textual summary and goal
        images, visuals_paths, visuals = visualization.get_visuals(textual_summary, goal)
        if len(visuals) > 0:
            if is_diaplay_explability:
                time.sleep(2)
                # Get the explanation for the first visual
                visuals_description = visualization.get_explaination(visuals[0])
                visuals_dict["visualizations_description"] = visuals_description[0]
            
            # Update the visuals dictionary with metadata
            visuals_dict["Date_of_creation"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            visuals_dict["Date_of_updation"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            visuals_dict["last_executed"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            visuals_dict["is_active"] = True
            visuals_dict["code"] = visuals[0].code
            visuals_dict["visualizations"] = images[0]
            visuals_dict["visualizations_path"] = visuals_paths[0]
            st.session_state["visualizations"].append(visuals_dict)
            
            # Store the selected visualization, description, and KPI text in the session state based on the KPI index
            kpi_index = id.split("_")[-1]
            st.session_state[f"selected_visualization_{kpi_index}"] = images[0]
            st.session_state[f"selected_visualization_description_{kpi_index}"] = visuals_description[0]
            st.session_state[f"selected_kpi_text_{kpi_index}"] = edited_query
        else:
            visuals_dict = {}
            st.session_state["visualizations"].append(visuals_dict)
    except httpx.HTTPStatusError as exc:
        utils.get_status_message(exc.response.status_code)
        st.warning(f"I am unable to process the request due to: {exc.response.status_code} error", icon="😔")

def displayPDF(file):
    """
    Displays a PDF file in the Streamlit app.
    
    Args:
        file (str): The path or URL of the PDF file.
    """
    base64_pdf = utils.pdf_to_base_64(file)
    st.write("## Report")
    with st.container(border=True):
        pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="950" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)

def init_session():
    """
    Initializes the session state variables.
    """
    # Initialize session state variables
    st.session_state["df"] = None
    st.session_state["summary"] = None
    st.session_state["visualizations"] = []
    st.session_state["visualization_paths"] = []
    st.session_state["KPIs"] = utils.get_kpis()
    

def visuals(kpi_query, graph_title, textual_summary):
    """
    Generates visuals based on the provided KPI query and textual summary.
    
    Args:
        kpi_query (str): The KPI query for generating the visualization.
        graph_title (str): The title of the graph.
        textual_summary (str): The textual summary of the data.
    """
    with st.container(border=True):
        goal = Goal(question=graph_title, visualization=kpi_query, rationale="")
        visuals_dict = dict()
        visuals_dict["id"] = str(uuid.uuid4())
        visuals_dict["kpi_query"] = kpi_query
        st.text_input("KPI:", value=kpi_query, key=visuals_dict["id"],
                      on_change=visual_edit, args=(visuals_dict["id"], textual_summary))
        try:
            # Generate visuals using the textual summary and goal
            images, visuals_paths, visuals = visualization.get_visuals(textual_summary, goal)
            if len(visuals) > 0:
                # Display the first image
                st.image(images[0], use_column_width="auto")
                if is_diaplay_explability:
                    time.sleep(2)
                    # Get the explanation for the first visual
                    visuals_description = visualization.get_explaination(visuals[0])
                    with st.expander("See explanation"):
                        visuals_dict["visualizations_description"] = visuals_description[0]
                        for description in visuals_description[0]:
                            st.markdown(f"""**{description['section']}**""")
                            st.write(description["explanation"])
                            st.divider()
                
                # Update the visuals dictionary with metadata
                visuals_dict["Date_of_creation"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                visuals_dict["Date_of_updation"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                visuals_dict["last_executed"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                visuals_dict["is_active"] = True
                visuals_dict["code"] = visuals[0].code
                visuals_dict["visualizations"] = images[0]
                visuals_dict["visualizations_path"] = visuals_paths[0]
                st.session_state[f"visualizations"].append(visuals_dict)
            else:
                st.warning(f"No visualizations generated for KPI {kpi_query}.")
        except Exception as e:
            st.error(f"An error occurred while generating the visualization: {str(e)}")
            logger.error(f"Error generating visualization for KPI {kpi_query}: {str(e)}")



def load_template(path):
    """
    Loads a template from a JSON file and stores it in the session state.
    
    Args:
        path (str): The path to the JSON file containing the template.
    """
    with open(path, 'r') as myfile:
        template=json.load(myfile)
    st.session_state["visualizations"] = template["KPI_list"]

def Preload(except_ids=[]):
    """
    Preloads the visualizations from the session state.
    
    Args:
        except_ids (list, optional): A list of visualization IDs to exclude from preloading. Defaults to an empty list.
    """
    logger.info("Preloaded")
    if "df" in st.session_state:
        with st.container(border=True):
            st.dataframe(st.session_state["df"].head(7), hide_index=True)
            st.header("KPI")
            if "visualizations" in st.session_state:
                my_complex_dict = pprint.pformat(st.session_state["visualizations"])
                logger.debug(f"preloaded dictionary: \n{my_complex_dict}")
                for visuals in st.session_state["visualizations"]:
                    if visuals['id'] not in except_ids:
                        with st.container(border=True):
                            kpi_query = visuals["kpi_query"]
                            st.text_input("KPI:", value=visuals["kpi_query"], key=visuals["id"], on_change=visual_edit, args=(visuals["id"], st.session_state["summary"]))
                            if "visualizations_path" in visuals:
                                st.image(visuals["visualizations_path"], use_column_width="auto")
                                if is_diaplay_explability:
                                    with st.expander("See explanation"):
                                        for description in visuals["visualizations_description"]:
                                            st.markdown(f"**{description['section']}**")
                                            st.write(description["explanation"])
                                            st.divider()
                            else:
                                st.warning(f"I am unable to generate visualization for: {kpi_query}.")