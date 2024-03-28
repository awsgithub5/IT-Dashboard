from PIL import Image
from io import BytesIO
import base64
import streamlit as st
import openai
import logging
from datetime import datetime

logger = logging.getLogger()

def generate_textual_summary(df):
    """
    Generates a textual summary of the given dataset using OpenAI's GPT-3.5 Turbo model.
    
    Args:
        df (pandas.DataFrame): The dataset to summarize.
        
    Returns:
        str: The generated textual summary.
    """
    summary_data = df.head().to_csv(index=False)
    messages = [
        {"role": "system", "content": "Please summarize the following dataset."},
        {"role": "user", "content": summary_data}
    ]
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.5,
        max_tokens=500
    )
    return response.choices[0].message.content

def _base64_to_image(base64_string, image_path):
    """
    Converts a base64-encoded string to an image object and saves it to the specified path.
    
    Args:
        base64_string (str): The base64-encoded string representing the image.
        image_path (str): The path where the image will be saved.
        
    Returns:
        PIL.Image: The image object.
    """
    byte_data = base64.b64decode(base64_string)
    with open(image_path, 'wb') as file:
        file.write(byte_data)
    img = Image.open(BytesIO(byte_data))
    return img

def get_explaination(visualization, library="matplotlib"):
    """
    Generates an explanation for the given visualization using LIDA.
    
    Args:
        visualization (Visualization): The visualization object.
        library (str, optional): The library used for the visualization. Defaults to "matplotlib".
        
    Returns:
        dict: The explanation for the visualization.
    """
    lida, textgen_config = st.session_state["lida"], st.session_state["textgen_config"]
    visuals_explain = lida.explain(code=visualization.code, textgen_config=textgen_config, library=library)
    return visuals_explain

def vis_edit(visualization, summary, instructions, library="matplotlib"):
    """
    Edits the given visualization based on natural language instructions using LIDA.
    
    Args:
        visualization (Visualization): The visualization object to edit.
        summary (str): The textual summary of the dataset.
        instructions (str): The natural language instructions for editing the visualization.
        library (str, optional): The library used for the visualization. Defaults to "matplotlib".
        
    Returns:
        tuple: A tuple containing the edited images, image paths, and visualization objects.
    """
    lida, textgen_config = st.session_state["lida"], st.session_state["textgen_config"]
    edited_charts = lida.edit(code=visualization.code, summary=summary, instructions=instructions, library=library, textgen_config=textgen_config)
    image_path = f'data/graphs/visualization_{datetime.now():%Y-%m-%d_%H-%M-%S}.png'
    imgs = []
    imgs_paths = []
    visuals = []
    if edited_charts:
        visualization = edited_charts[0]
        image_base64 = visualization.raster
        logger.info(f"Error {visualization.error}")
        logger.info(f"library {visualization.library}")
        logger.info("spec {visualization.spec}")
        logger.info("status {visualization.status}")
        logger.info("Code")
        print("'''"*20)
        logger.debug(visualization.code)
        print("'''"*20)
        img = _base64_to_image(image_base64, image_path)
        imgs.append(img)
        imgs_paths.append(image_path)
        visuals.append(visualization)
        return imgs, imgs_paths, visuals
    else:
        return None

def get_goals(summary, no_of_goal=2):
    """
    Generates goals based on the given summary using LIDA.
    
    Args:
        summary (str): The textual summary of the dataset.
        no_of_goal (int, optional): The number of goals to generate. Defaults to 2.
        
    Returns:
        list: A list of generated goals.
    """
    lida, textgen_config = st.session_state["lida"], st.session_state["textgen_config"]
    goals = lida.goals(summary, n=no_of_goal, textgen_config=textgen_config)
    return goals

def get_visuals(summary, kpi_query, library="matplotlib"):
    """
    Generates visualizations based on the given summary and KPI query using LIDA.
    
    Args:
        summary (str): The textual summary of the dataset.
        kpi_query (str): The KPI query for generating visualizations.
        library (str, optional): The library used for the visualization. Defaults to "matplotlib".
        
    Returns:
        tuple: A tuple containing the generated images, image paths, and visualization objects.
    """
    lida, textgen_config = st.session_state["lida"], st.session_state["textgen_config"]
    visualizations = lida.visualize(
        summary=summary,
        goal=kpi_query,
        textgen_config=textgen_config,
        library=library,
    )
    imgs = []
    imgs_paths = []
    visuals = []
    for visualization in visualizations:
        image_path = f'data/graphs/visualization_{datetime.now():%Y-%m-%d_%H-%M-%S}.png'
        image_base64 = visualization.raster
        logger.info(f"Error: {visualization.error}")
        logger.info(f"library: {visualization.library}")
        logger.info(f"spec: {visualization.spec}")
        logger.info(f"status: {visualization.status}")
        logger.info("Code:")
        logger.debug(f"Code: \n{visualization.code}")
        img = _base64_to_image(image_base64, image_path)
        imgs.append(img)
        imgs_paths.append(image_path)
        visuals.append(visualization)
    return imgs, imgs_paths, visuals