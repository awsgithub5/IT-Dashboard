import json
import os
import base64
import pandas as pd

def get_kpis():
    """
    Retrieves a list of predefined KPIs.
    
    Returns:
        list: A list of dictionaries representing KPIs.
    """
    kpi_list = []
    
    kpi_dict = dict()
    kpi_dict["text"] = "📊 Network Traffic Volume"
    kpi_dict["KPI"] = "Generate a line chart with the x-axis representing time (Day or Month) and the y-axis representing the total bytes or packets"
    kpi_dict["disabled"] = False
    kpi_list.append(kpi_dict)
    
    kpi_dict = dict()
    kpi_dict["text"] = "📊 Daily Protocol Distribution"
    kpi_dict["KPI"] = "Generate a bar graph to show day trend of protocol"
    kpi_dict["disabled"] = False
    kpi_list.append(kpi_dict)
    
    kpi_dict = dict()
    kpi_dict["text"] = "📊 Network Traffic by IP Address"
    kpi_dict["KPI"] = "Create an interactive horizontal bar chart or treemap to display the top source or destination IP addresses contributing to the network traffic"
    kpi_dict["disabled"] = False
    kpi_list.append(kpi_dict)
    
    kpi_dict = dict()
    kpi_dict["text"] = "📊 Traffic Composition by Class"
    kpi_dict["KPI"] = "Create an interactive stacked bar chart to visualize the distribution of network traffic across different classes (e.g., normal, suspicious, unknown)"
    kpi_dict["disabled"] = False
    kpi_list.append(kpi_dict)
    
    kpi_dict = dict()
    kpi_dict["text"] = "📊 Weekly Test Volume"
    kpi_dict["KPI"] = "Create a line chart with x-axis as Week Number and y-axis as Number of Tests Performed to analyze weekly test execution volume. Label axes clearly and highlight peaks."
    kpi_dict["disabled"] = False
    kpi_list.append(kpi_dict)
    
    return kpi_list

def get_templates(user_id):
    """
    Retrieves a list of templates for a given user ID.
    
    Args:
        user_id (int): The ID of the user.
    
    Returns:
        list: A list of dictionaries representing templates.
    """
    template_list = []
    path = f"data/KPIs"
    obj = os.scandir(path)
    print(obj)
    
    for entry in obj:
        if entry.is_file():
            if str(user_id) == str(entry.name.split("_")[0]):
                temp = dict()
                temp["name"] = entry.name.split("_")[-1].split(".json")[0]
                temp["path"] = entry.path
                template_list.append(temp)
    
    return template_list

def pdf_to_base_64(file):
    """
    Converts a PDF file to base64 format.
    
    Args:
        file (str): The path to the PDF file.
    
    Returns:
        str: The base64-encoded content of the PDF file.
    """
    # Function to display the PDF of a given file
    # Opening file from file path. This is used to open the file from a website rather than local
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    return base64_pdf