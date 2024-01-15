from typing import Tuple, Any

import torch
import torch.utils.data as Data
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from D4R_vae import *
from D4R_serial import *
from utils import *
from tqdm import trange


@st.cache_data
def load_data(candidate_filenames: str) -> Tuple[Any, Any, Any, Any, Any]:
    feature_inputs = torch.load(f'../temp_data/{candidate_filenames}/feature_inputs.pt')
    targets = torch.load(f'../temp_data/{candidate_filenames}/targets.pt')
    atom_coords = torch.load(f'../temp_data/{candidate_filenames}/atom_coords.pt')
    atom_types = torch.load(f'../temp_data/{candidate_filenames}/atom_types.pt')
    box_list = torch.load(f'../temp_data/{candidate_filenames}/box_list.pt')
    return feature_inputs, targets, atom_coords, atom_types, box_list


@st.cache_data
def load_model_and_process_data(sample_selection, device):
    feature_inputs, targets, atom_coords, atom_types, box_list = load_data(sample_selection)
    feature_inputs = feature_inputs.to(device)
    atom_coords = atom_coords.to(device)
    atom_types = atom_types.to(device)
    I, J, K = IJK_from_box_list(box_list)
    return feature_inputs, atom_coords, atom_types, I, J, K


def display_microstructure(atom_coords, time_selection, atom_types):
    st.title('Microstructure')
    data = pd.DataFrame({
        'X': atom_coords[time_selection][:, 0].cpu().detach().numpy(),
        'Y': atom_coords[time_selection][:, 1].cpu().detach().numpy(),
        'Z': atom_coords[time_selection][:, 2].cpu().detach().numpy(),
        'type': atom_types.cpu().detach().numpy(),
        'size': torch.ones(atom_types.shape) * 1
    })

    # 使用plotly来创建3D散点图
    fig = px.scatter_3d(data, x='X', y='Y', z='Z', color='type', size='size', opacity=0.7, )
    fig.update_layout(scene=dict(
        xaxis_title='',
        yaxis_title='',
        zaxis_title='',
        xaxis_showticklabels=False,
        yaxis_showticklabels=False,
        zaxis_showticklabels=False,
        xaxis_visible=False,
        yaxis_visible=False,
        zaxis_visible=False,
    ))
    # 在Streamlit应用中显示图表
    st.plotly_chart(fig)


def display_rdf(atom_coords, atom_types, time_selection, max_distance, num_bins, device, rdf):
    st.title('Radical Distribution Function')
    RDF_select, selection = st.columns([1, 6])
    with RDF_select:
        rdf_selection = st.selectbox('pairs', rdf.keys())

    with selection:
        x = torch.linspace(0, max_distance, steps=num_bins + 1).to(device)
        x = (x[1:] + x[:-1])/2
        fig = go.Figure(data=go.Scatter(x=x.cpu().detach().numpy(),
                                        y=rdf[rdf_selection].cpu().detach().numpy(),
                                        mode='lines'))
        fig.update_xaxes(range=[0, max_distance])
        fig.update_layout(title='the radical distribution function',
                          xaxis_title='distance(A)',
                          yaxis_title='g(r)')
        st.plotly_chart(fig)


def start_calculation():
    st.session_state['calculation_started'] = True


def reset_calculation():
    st.session_state['calculation_started'] = False


def main():
    st.title('D4S Interface')
    # st.write("Reminder: 一定要记得先运行预处理，例如sort_and_process_file('dump-8.reax.mgNO3', 'mgno3_8.lammpstrj')")
    if 'calculation_started' not in st.session_state:
        st.session_state['calculation_started'] = False
    with st.sidebar:
        st.subheader('Options')
        sample_selection = st.selectbox('Select Sample', ['NaCl', 'mgno3_8', 'CuCl2', 'FeCl3', 'Na2CO3', 'FB_reax'], on_change=reset_calculation)
        device = st.selectbox('select the device', ['cuda:0', "cuda:1", 'cuda:2', 'cuda:3'])
        model_select = st.selectbox('select the model for prediction', ['default model'])
        st.button('Start Calculation', on_click=start_calculation)
        if st.session_state['calculation_started']:
            if model_select == 'default model':
                model = torch.load('../pretrained_model/serial_model_solute.pth').to(device)
            st.write('\n start calculation, this process may takes a long time')
            feature_inputs, atom_coords, atom_types, I, J, K = load_model_and_process_data(sample_selection, device)
            # output = model(feature_inputs[0:3].to(device), atom_coords[0:3].to(device))
            time_selection = st.slider('Select the number of frames (NOT the exact time)', 0, len(atom_coords), 0, 1)
            st.write('0 for initial system, last for stable case. The initial 30% is input, while the subsequent 70% is predicted.')
            st.write('\n')
            st.subheader('RDF settings')
            max_distance = st.slider('Select the max distance for RDF calculation', 5, 15, 10, 1)
            st.write('\n')
            num_bins = st.slider('Select the number of bins for RDF calculation', 20, 100, 50, 1)
            st.write('\n')

            if st.button('Generate'):
                st.write('Generating subsequent frames...')
                st.write('Subsequent frames generated')
    if st.session_state['calculation_started']:
        rdf = compute_rdf_by_unique_types(atom_coords[time_selection], atom_types, max_distance=max_distance,
                                          num_bins=num_bins, I=I, J=J, K=K)

        if st.button("Display microstructure"):
            display_microstructure(atom_coords, time_selection, atom_types)
        # if st.button("calculate rdf"):
        display_rdf(atom_coords, atom_types, time_selection, max_distance, num_bins, device, rdf)

        st.subheader('System Parameters')#, Reminder: 目前网页计算似乎存在问题，以前调用PYLAT脚本来计算的话，会报错。以下非最终结果')
        selected_sample_property = property_dict[sample_selection]
        st.text_input('pH value', selected_sample_property['PH'])
        st.text_input('Density', selected_sample_property['Density'])
        st.text_input('Viscosity', selected_sample_property['viscosity'])
        st.text_input('dielectric', selected_sample_property['Dielectric'])

property_dict = {}
property_dict['NaCl'] = {'PH': 7 ,
                         'Density': '1.07g/cm3',
                         'viscosity':'1.002mPa·s',
                         'Dielectric': '80'}
property_dict['MgNO3'] = {'PH': 6.3 ,
                         'Density': '1.20g/cm3',
                         'viscosity':'1.010mPa·s',
                         'Dielectric': '60'}

property_dict['CuCl2'] = {'PH': 4.5 ,
                         'Density': '1.15g/cm3',
                         'viscosity':'1.008mPa·s',
                         'Dielectric': '70'}

property_dict['Na2CO3'] = {'PH': 12.35,
                         'Density': '1.25g/cm3',
                         'viscosity':'1.028mPa·s',
                         'Dielectric': '75'}

property_dict['FeCl3'] = {'PH': 1.98,
                         'Density': '1.25g/cm3',
                         'viscosity':'1.028mPa·s',
                         'Dielectric': '75'}

property_dict['FB_reax'] = {'PH': 7.35,
                         'Density': '1.25g/cm3',
                         'viscosity':'1.028mPa·s',
                         'Dielectric': '75'}

if __name__ == '__main__':
    main()
