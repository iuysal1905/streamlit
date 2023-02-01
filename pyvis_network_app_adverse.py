
# Import dependencies
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import networkx as nx
from pyvis.network import Network
import pip
pip.main(["install", "openpyxl"])

# Read dataset
df_interact = pd.read_excel('ddi_adverse.xlsx')

# Set header title
st.title('Network Graph Visualization of Drug-Drug Interactions')

# Define list of selection options and sort alphabetically
drug_list = ['Ticlopidine','Clotrimazole','Rucaparib','Fluvoxamine','Acetyl sulfisoxazole','Delavirdine','Clemastine','Diltiazem','Bortezomib',
             'Phenobarbital','Sulfisoxazole','Primidone','Carbamazepine','Nevirapine','Atomoxetine','Curcumin','Verapamil','Rifapentine','Fluconazole','Rifampicin']
drug_list.sort()
vs=['Repulsion', 'Barnes Hut']

def generate_network_viz(df, source_col, target_col, weights, 
                         layout='barnes_hut',
                         central_gravity=0.15,
                         node_distance=420,
                         spring_length=100,
                         spring_strength=0.15,
                         damping=0.96
                         ):
    
    # Generate a networkx graph
    G = nx.from_pandas_edgelist(df, source_col, target_col, weights)
    
    if layout == 'repulsion':
        bgcolor, font_color = '#222222', 'white'
    else:
        bgcolor, font_color = 'white', 'black'
    
    # Initiate PyVis network object
    drug_net = Network(
                       height='700px', 
                       width='100%',
                       bgcolor=bgcolor, 
                       font_color=font_color, 
                       notebook=True
                      )
    
    # Take Networkx graph and translate it to a PyVis graph format
    drug_net.from_nx(G)
    
    # Create different network layout (repulsion or Barnes Hut)
    if layout == 'repulsion':
        drug_net.repulsion(
                            node_distance=node_distance, 
                            central_gravity=central_gravity, 
                            spring_length=spring_length, 
                            spring_strength=spring_strength, 
                            damping=damping
                           )
        
    # Run default Barnes Hut visualization
    else:
        drug_net.barnes_hut(
                          overlap=0
                          )      
return drug_net


# Implement multiselect dropdown menu for option selection (returns a list)
selected_drugs = st.multiselect('Select drug(s) to visualize', drug_list)
selected_vs=st.multiselect('Select one for visualization', vs)
if selected_vs=='Repulsion'
  generate_network_viz(data_sm, 'drug1_name', 'drug2_name', 'weight', layout='Repulsion')
else:
  generate_network_viz(data_sm, 'drug1_name', 'drug2_name', 'weight', layout='Barnes Hut')
  
# Set info message on initial site load
if len(selected_drugs) == 0:
    st.text('Choose at least 1 drug to get started')

# Create network graph when user selects >= 1 item
else:
    df_select = df_interact.loc[df_interact['drug1_name'].isin(selected_drugs) | \
                                df_interact['drug2_name'].isin(selected_drugs)]
    df_select = df_select.reset_index(drop=True)
    
 
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
