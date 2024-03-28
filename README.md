


#GenAI Dashboard

GENAI Dashboard is a tool for Automatic Generation of Visualizations and Infographics with LLM.
## 🎯 Features
- Preprocessing applications data
- Data Summarization
- Generate Visualization using LLM
- Visualization Explanation
- Report Generation

## ☂️ Application Cover


## 📂 Directory Structure

```bash
├── config # all config files
├── data # data store in this folder
│   ├── graphs # all graphs 
│   ├── KPIs # all KPIs
│   ├── reports # all reports 
│   ├── user_data # templates
├── infra # infra related code
├── lida # proprt engg and execution
├── llmx
├── pages # HTML pages for each application
├── README.md
├── scr # source code for application
├── home
├── app
└── .gitignore

```  



-----
<!-- Env Variables -->
### 🔑 Environment Variables

To run this project, you will need to add the following environment variables to your .env file



-----

### ⚙️ Installation

Install from pypi.

#### create enviroment
```bash
conda create -n .venv python=3.9.18 or python -m venv .venv
```
#### Activate enviroment
```bash
conda activate .venv or cd .venv, cd Scripts, ./activate
```
#### Install requirements
```bash
pip install -r requirements.txt
```
-----
### 👀 Usage

```bash
streamlit run home.py
```
-----
### 📝 Summary
Summary default Json Structure.

```json
{
  "dataset_description":"",
  "field_names":[
    ""
  ],
  "fields":[
    {
      "column":"category",
      "properties":{
        "description":"",
        "dtype":"category",
        "num_unique_values":0,
        "samples":[
          "",
          "",
          ""
        ],
        "semantic_type":""
      }
    },
    {
      "column":"Date",
      "properties":{
        "description":"",
        "dtype":"date",
        "max":"",
        "min":"",
        "num_unique_values":0,
        "samples":[
          "",
          ""
        ],
        "semantic_type":""
      }
    },
    {
      "column":"Number",
      "properties":{
        "description":"",
        "dtype":"date",
        "max":1,
        "min":0,
        "num_unique_values":2,
        "samples":[
          1,
          0
        ],
        "semantic_type":""
      }
    }
  ],
  "file_name":"",
  "name":""
}
```

-----






