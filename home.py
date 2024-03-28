import streamlit as st
import app


#@Shrina

def run():
    st.set_page_config(page_title="Dashboard", layout="wide", page_icon="📈")
    st.markdown("# Dashboard 📊")

    # Add a dropdown menu for selecting Home or CIDDS
    menu_options = ["Home", "CIDDS"]
    selected_option = st.sidebar.selectbox("Select an option", menu_options)

    if selected_option == "Home":
        Input = """Dashboard, powered by LLM (DeereAl), is a comprehensive tool designed for the automatic generation of visualizations and infographics. It seamlessly integrates with various software systems, including CIDDS, to provide detailed insights and analytics. PartsOps Dashboard provides users with a comprehensive view of their software testing and security processes. This empowers teams to make informed decisions, streamline workflows, and drive continuous improvement across their application development lifecycle.
        

        1. **CIDDS** 📉: 
CIDDS (Coburg Intrusion Detection Data Sets) is a concept to create evaluation data sets for anomaly-based network intrusion detection systems.CIDDS application provides a user-friendly interface for exploring and 
visualizing the CIDDS dataset, generating textual summaries, and creating custom visualizations,
 based on user-defined KPIs. This includes metrics such as Network Traffic Volume,
Daily Protocol Distribution,Network Traffic by IP Address and Traffic Composition by Class.
"""
        st.write(Input)

    elif selected_option == "CIDDS":
        app.run()

if __name__ == "__main__":
    run()