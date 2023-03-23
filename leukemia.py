import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import networkx as nx
from pyvis.network import Network
import pip
pip.main(["install", "openpyxl"])

# Read dataset 
df_interact = pd.read_excel('leukemia_ddi.xlsx')

# Set header title
st.title('Network Graph Visualization of Drug-Drug Interactions')

# Define list of selection options and sort alphabetically
drug_list = ['Mercaptopurine','Tioguanine','Prednisolone','Dexamethasone','Vincristine','Methotrexate','Daunorubicin','Cytarabine']
drug_list.sort()

# Implement multiselect dropdown menu for option selection (returns a list)
selected_drugs = st.multiselect('Select drug(s) to visualize', drug_list)

# Set info message on initial site load
if len(selected_drugs) == 0:
    st.text('Choose at least 1 drug to start')

# Create network graph when user selects >= 1 item
else:
    df_select = df_interact.loc[df_interact['drug1_name'].isin(selected_drugs) | \
                                df_interact['drug2_name'].isin(selected_drugs)]
    df_select = df_select.reset_index(drop=True)

    # Create networkx graph object from pandas dataframe
    G = nx.from_pandas_edgelist(df_select, 'drug1_name', 'drug2_name', 'weight')

    # Initiate PyVis network object
    drug_net = Network(
                       height='400px',
                       width='100%',
                       bgcolor='#222222',
                       font_color='white'
                      )

    # Take Networkx graph and translate it to a PyVis graph format
    drug_net.from_nx(G)

    # Generate network with specific layout settings
    drug_net.repulsion(
                        node_distance=420,
                        central_gravity=0.33,
                        spring_length=110,
                        spring_strength=0.10,
                        damping=0.95
                       )

    # Save and read graph as HTML file (on Streamlit Sharing)
    try:
        path = '/tmp'
        drug_net.save_graph(f'{path}/pyvis_graph.html')
        HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

    # Save and read graph as HTML file (locally)
    except:
        path = '/html_files'
        drug_net.save_graph(f'{path}/pyvis_graph.html')
        HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

    # Load HTML file in HTML component for display on Streamlit page
    components.html(HtmlFile.read(), height=435)
