import streamlit as st
import pandas as pd
import plotly.express as px
import locale
from impatometro.df import fetch_data_from_view

# Configurar locale para português do Brasil
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')
    except:
        pass

# Função auxiliar para formatar moeda no padrão brasileiro
def format_brl(value):
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

host = "10.0.122.94"
port = 3306
user = "usr_impactometro"
password = "DqFgVGkdZ"  # Substitua pela sua senha
database = "sgg"
view_name = "vw_impactometro"

df = fetch_data_from_view(host, port, user, password, database, view_name)

print(df)

import pymysql
import pandas as pd

st.set_page_config(
    page_title='IMPACTÔMETRO',
    layout='wide',
    initial_sidebar_state="auto",
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;700&display=swap');
    
    /* Base styles */
    * {
        font-family: 'Montserrat', sans-serif !important;
    }
    
    /* Container styles */
    .page-container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 0 2rem;
    }
    
    /* Header styles */
    .header-wrapper {
        background-color: white;
        border-bottom: 2px solid #034ea2;
        margin-bottom: 2rem;
    }
    
    .header-container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 2rem;
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: center;
        gap: 2rem;
    }
    
    .header-content {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: center;
        gap: 3rem;
        width: 100%;
        max-width: 1000px;
    }
    
    .header-container img {
        width: 200px;
        height: auto;
    }
    
    .header-container h1 {
        margin: 0;
        color: #034ea2;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: left;
        flex: 1;
    }
    
    /* Main content area */
    .main-content {
        padding: 2rem;
        background-color: white;
    }
    
    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important;
        color: #034ea2 !important;
    }
    
    /* Form elements */
    .stSelectbox [data-baseweb="select"] > div,
    .stMultiSelect [data-baseweb="select"] > div {
        border-color: #fdb913;
        background-color: white;
        border-radius: 4px;
    }
    
    /* Pills style */
    div[data-baseweb="tag"] {
        background-color: #fdb913 !important;
        color: #034ea2 !important;
        border-radius: 4px;
        padding: 0.25rem 0.5rem;
    }
    
    /* Radio buttons */
    .stRadio > div[role="radiogroup"] label {
        color: #034ea2 !important;
    }
    
    /* Number inputs */
    .stNumberInput input {
        border: 1px solid #fdb913;
        border-radius: 4px;
        padding: 0.5rem;
    }
    
    /* Results container */
    .results-container {
        background-color: white;
        border: 2px solid #034ea2;
        border-radius: 8px;
        padding: 2rem;
        margin: 2rem 0;
    }
    
    .metric-card {
        background-color: #f5f5f5;
        border: 1px solid #e5e5e5;
        border-radius: 4px;
        padding: 1rem;
        text-align: center;
    }
    
    .metric-label {
        color: #666;
        font-size: 0.875rem;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        color: #034ea2;
        font-size: 1.25rem;
        font-weight: 700;
    }
    
    /* Table/DataFrame styling */
    .dataframe {
        border: 1px solid #e5e5e5;
        border-radius: 4px;
    }
    
    .dataframe th {
        background-color: #034ea2;
        color: white !important;
        padding: 0.75rem;
    }
    
    .dataframe td {
        padding: 0.75rem;
        border-bottom: 1px solid #e5e5e5;
    }
    
    /* Button styling */
    .stButton button {
        background-color: #fdb913 !important;
        color: #034ea2 !important;
        font-weight: 500;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        border: none;
        cursor: pointer;
        transition: background-color 0.2s;
    }
    
    .stButton button:hover {
        background-color: #e5a711 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="header-wrapper">
        <div class="header-container">
            <div class="header-content">
                <img src="https://www.sead.pi.gov.br/wp-content/uploads/2024/01/logo.svg" alt="Logo SEAD">
                <h1>IMPACTÔMETRO</h1>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Load data function

# Form container
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# First set of filters (GRUPO EIXO, EIXO, and PLANO)
col1, col2, col3 = st.columns(3)

# GRUPO EIXO filter
with col1:
    grupo_eixo_counts = df['GRUPO_EIXO'].value_counts()
    grupo_eixo_list = sorted(df['GRUPO_EIXO'].dropna().unique().tolist())
    grupo_eixo_options = []
    for grupo_eixo in grupo_eixo_list:
        count = grupo_eixo_counts.get(grupo_eixo, 0)
        grupo_eixo_options.append(f"{grupo_eixo} ({count:,} servidores)")
    grupo_eixo_mapping = {option: grupo_eixo for grupo_eixo, option in zip(grupo_eixo_list, grupo_eixo_options)}
    
    selected_grupo_eixo_options = st.multiselect(
        'Grupos de Eixo',
        grupo_eixo_options,
        default=[],
        key='grupo_eixo_select',
        placeholder='Selecione os grupos de eixo'
    )
    
    selected_grupos_eixo = [grupo_eixo_mapping[option] for option in selected_grupo_eixo_options]

# Initial filtering based on GRUPO EIXO
if selected_grupos_eixo:
    filtered_df = df[df['GRUPO_EIXO'].isin(selected_grupos_eixo)]
else:
    filtered_df = df.copy()

# EIXO filter
with col2:
    eixo_counts = filtered_df['EIXO'].value_counts()
    eixo_list = sorted(filtered_df['EIXO'].dropna().unique().tolist())
    eixo_options = []
    for eixo in eixo_list:
        count = eixo_counts.get(eixo, 0)
        eixo_options.append(f"{eixo} ({count:,} servidores)")
    eixo_mapping = {option: eixo for eixo, option in zip(eixo_list, eixo_options)}
    
    selected_eixo_options = st.multiselect(
        'Eixos',
        eixo_options,
        default=[],
        key='eixo_select',
        placeholder='Selecione os eixos'
    )
    
    selected_eixos = [eixo_mapping[option] for option in selected_eixo_options]

# Update filtered_df based on EIXO selection
if selected_eixos:
    filtered_df = filtered_df[filtered_df['EIXO'].isin(selected_eixos)]

# PLANO filter (moved up)
with col3:
    planos_list = sorted(filtered_df['PLANO'].unique().tolist())
    plano_counts = filtered_df['PLANO'].value_counts()
    plano_options = [f"{plano} ({plano_counts[plano]:,} servidores)" for plano in planos_list]
    plano_mapping = {f"{plano} ({plano_counts[plano]:,} servidores)": plano for plano in planos_list}
    
    selected_plano_options = st.multiselect(
        'Planos de Carreira',
        plano_options,
        default=[],
        key='plano_select',
        placeholder='Selecione os planos'
    )
    
    selected_planos = [plano_mapping[option] for option in selected_plano_options]

# Update filtered_df based on PLANO selection
if selected_planos:
    filtered_df = filtered_df[filtered_df['PLANO'].isin(selected_planos)]

# Second set of filters (CARGO, CLASSE, and NIVEL)
col4, col5, col6 = st.columns(3)

# CARGO filter (moved down)
with col4:
    cargo_counts = filtered_df['CARGO'].value_counts()
    all_CARGOs = sorted(filtered_df['CARGO'].astype(str).unique().tolist())
    cargo_options = [f"{cargo} ({cargo_counts[cargo]:,} servidores)" for cargo in all_CARGOs]
    cargo_mapping = {f"{cargo} ({cargo_counts[cargo]:,} servidores)": cargo for cargo in all_CARGOs}
    
    selected_options = st.multiselect(
        'Cargos',
        cargo_options,
        default=[],
        key='CARGO_select',
        placeholder='Selecione os cargos'
    )
    
    selected_CARGOs = [cargo_mapping[option] for option in selected_options]

# Update filtered_df based on CARGO selection
if selected_CARGOs:
    filtered_df = filtered_df[filtered_df['CARGO'].isin(selected_CARGOs)]

# CLASSE filter
with col5:
    classe_counts = filtered_df['CLASSE'].value_counts()
    classe_list = sorted(filtered_df['CLASSE'].dropna().unique().tolist())
    classe_options = []
    for classe in classe_list:
        count = classe_counts.get(classe, 0)
        classe_options.append(f"{classe} ({count:,} servidores)")
    classe_mapping = {option: classe for classe, option in zip(classe_list, classe_options)}
    
    selected_classe_options = st.multiselect(
        'Classes',
        classe_options,
        default=[],
        key='classe_select',
        placeholder='Selecione as classes'
    )
    
    selected_classes = [classe_mapping[option] for option in selected_classe_options]

# Update filtered_df based on CLASSE selection
if selected_classes:
    filtered_df = filtered_df[filtered_df['CLASSE'].isin(selected_classes)]

# NIVEL filter
with col6:
    nivel_counts = filtered_df['NIVEL'].value_counts()
    nivel_list = sorted(filtered_df['NIVEL'].dropna().unique().tolist())
    nivel_options = []
    for nivel in nivel_list:
        count = nivel_counts.get(nivel, 0)
        nivel_options.append(f"{nivel} ({count:,} servidores)")
    nivel_mapping = {option: nivel for nivel, option in zip(nivel_list, nivel_options)}
    
    selected_nivel_options = st.multiselect(
        'Níveis',
        nivel_options,
        default=[],
        key='nivel_select',
        placeholder='Selecione os níveis'
    )
    
    selected_niveis = [nivel_mapping[option] for option in selected_nivel_options]

# Final filter for NIVEL
if selected_niveis:
    filtered_df = filtered_df[filtered_df['NIVEL'].isin(selected_niveis)]


# [Rest of your code remains unchanged]
st.markdown('### Tipo de Aumento')
increase_type = st.radio(
    "",
    ["Percentual (%)", "Novo Salário (R$)"],
    key='increase_type',
    horizontal=True
)

# Add Geral control
if selected_CARGOs:
    st.markdown('##### Ajuste Geral')
    if increase_type == "Percentual (%)":
        Geral_increase = st.number_input(
            "Aplicar percentual para todos os cargos (%)",
            min_value=-100.0,
            max_value=100.0,
            value=0.0,
            step=0.5,
            key='Geral_increase'
        )
    else:
        Geral_salary = st.number_input(
            "Aplicar novo salário para todos os cargos (R$)",
            min_value=0.0,
            value=float(filtered_df['VALOR'].mean()),
            step=100.0,
            key='Geral_salary'
        )

# Dictionary to store new salaries
new_salaries = {}
increases = {}
cols = st.columns(4)
for idx, CARGO in enumerate(selected_CARGOs):
    cargo_df = filtered_df[filtered_df['CARGO'] == CARGO]
    cargo_count = len(cargo_df)
    current_avg_salary = cargo_df['VALOR'].mean()
    col_idx = idx % 4
    
    if col_idx == 0 and idx > 0:
        cols = st.columns(4)
    
    with cols[col_idx]:
        st.markdown(f"""
            <div style="
                background-color: #f0f2f6;
                padding: 0.5rem;
                border-radius: 4px;
                margin-bottom: 0.5rem;
                ">
                <span style="color: #034ea2; font-weight: 500;">{CARGO}</span><br>
                <span style="font-size: 0.9em; color: #666;">
                    {cargo_count:,} servidor{'es' if cargo_count != 1 else ''}<br>
                    Média atual: {format_brl(current_avg_salary)}
                </span>
            </div>
        """, unsafe_allow_html=True)
        
        if increase_type == "Percentual (%)":
            increases[CARGO] = st.number_input(
                "Aumento (%)",
                min_value=-100.0,
                max_value=100.0,
                value=Geral_increase if 'Geral_increase' in st.session_state else 0.0,
                step=0.5,
                key=f'increase_{CARGO}'
            )
        else:
            new_salaries[CARGO] = st.number_input(
                "Novo Salário (R$)",
                min_value=0.0,
                value=Geral_salary if 'Geral_salary' in st.session_state else float(current_avg_salary),
                step=100.0,
                key=f'increase_{CARGO}'
            )

# Calculate button and results
if st.button('Calcular Impacto', use_container_width=True):
    if not selected_CARGOs:
        st.warning('Por favor, selecione pelo menos um cargo para calcular o impacto.')
    else:
        results_df = filtered_df.copy()
        
        # Calculate new values
        for CARGO in selected_CARGOs:
            mask = results_df['CARGO'] == CARGO
            if increase_type == "Percentual (%)":
                results_df.loc[mask, 'VALOR COM IMPACTO'] = results_df.loc[mask, 'VALOR'] * (1 + increases[CARGO]/100)
            else:
                # Apply the new salary for each cargo separately
                results_df.loc[mask, 'VALOR COM IMPACTO'] = new_salaries[CARGO]
        
        results_df['IMPACTO'] = results_df['VALOR COM IMPACTO'] - results_df['VALOR']
        results_df['VALOR COM ENCARGO'] = results_df['VALOR COM IMPACTO'] * 1.4144
        
        # Calculate totals
        total_current = results_df['VALOR'].sum()
        total_new = results_df['VALOR COM IMPACTO'].sum()
        total_increase = results_df['IMPACTO'].sum()
        total_multiplicado = results_df['VALOR COM ENCARGO'].sum()
        total_servidores = len(results_df)
        
        # Display results cards with employee count
        st.markdown("""
            <div class="results-container">
                <h2 style="text-align: center; margin-bottom: 2rem;">Resultados do Impacto Salarial</h2>
                <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 1rem;">
                    <div class="metric-card">
                        <div class="metric-label">Total de Servidores</div>
                        <div class="metric-value">{}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Salário Total Atual</div>
                        <div class="metric-value">{}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Novo Salário Total</div>
                        <div class="metric-value">{}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Alteração Total</div>
                        <div class="metric-value">{}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Total com Encargos</div>
                        <div class="metric-value">{}</div>
                    </div>
                </div>
            </div>
        """.format(
            f"{total_servidores:,}".replace(",", "."),
            format_brl(total_current),
            format_brl(total_new),
            format_brl(total_increase),
            format_brl(total_multiplicado)
        ), unsafe_allow_html=True)
        
        # Primeiro exibir o resumo por cargo
        st.markdown('### Resumo por Cargo')
        summary_by_cargo = results_df.groupby('CARGO').agg({
            'MATRICULA': 'count',
            'VALOR': ['sum', 'mean'],
            'VALOR COM IMPACTO': ['sum', 'mean'],
            'IMPACTO': 'mean',  # Changed from 'sum' to 'mean'
            'VALOR COM ENCARGO': 'sum'
        }).round(2)
        
        # Calculate percentage impact for each position
        percentage_impact = (
            (summary_by_cargo[('VALOR COM IMPACTO', 'sum')] - summary_by_cargo[('VALOR', 'sum')]) / 
            summary_by_cargo[('VALOR', 'sum')] * 100
        ).round(2)
        
        # Add percentage impact to the summary
        summary_by_cargo['Impacto Percentual'] = percentage_impact
        
        # Rename columns for better readability
        summary_by_cargo.columns = [
            'Quantidade de Servidores',
            'Salário Total Atual',
            'Salário Médio Atual',
            'Novo Salário Total',
            'Novo Salário Médio',
            'Alteração Média',  # Changed from 'Alteração Total'
            'Total com Encar',
            'Impacto Percentual'
        ]
        
        # Função de formatação personalizada para o DataFrame
        formatters = {
            'Quantidade de Servidores': lambda x: f"{x:,.0f}".replace(",", "."),
            'Salário Total Atual': format_brl,
            'Salário Médio Atual': format_brl,
            'Novo Salário Total': format_brl,
            'Novo Salário Médio': format_brl,
            'Alteração Média': format_brl,  # Updated formatter name
            'Total com Encar': format_brl,
            'Impacto Percentual': lambda x: f"{x:,.2f}%".replace(",", ".")
        }

        st.dataframe(
            summary_by_cargo.style.format(formatters),
            use_container_width=True
        )
        
        # Create salary comparison chart in its own container
        st.markdown('### Comparação de Salários Médios por Cargo')
        chart_data = results_df.groupby('CARGO').agg({
            'VALOR': 'mean',
            'VALOR COM IMPACTO': 'mean'
        }).round(0).reset_index()  # Arredondando para número inteiro
        
        # Convertendo as colunas numéricas para inteiro
        chart_data['VALOR'] = chart_data['VALOR'].astype(int)
        chart_data['VALOR COM IMPACTO'] = chart_data['VALOR COM IMPACTO'].astype(int)
        
        chart_data_melted = pd.melt(
            chart_data,
            id_vars=['CARGO'],
            value_vars=['VALOR', 'VALOR COM IMPACTO'],
            var_name='Tipo',
            value_name='Valor'
        )
        
        # Mapeamento para   s mais amigáveis na legenda
        chart_data_melted['Tipo'] = chart_data_melted['Tipo'].map({
            'VALOR': 'VALOR ATUAL',
            'VALOR COM IMPACTO': 'VALOR COM IMPACTO'
        })
        
        fig_salary = px.bar(
            chart_data_melted,
            x='CARGO',
            y='Valor',
            color='Tipo',
            barmode='group',
            title=' ',
            labels={
                'CARGO': 'Cargo',
                'Valor': 'Salário Médio (R$)',
                'Tipo': ''
            },
            color_discrete_map={
                'VALOR ATUAL': '#034ea2',
                'VALOR COM IMPACTO': '#fdb913'
            }
        )
        
        fig_salary.update_layout(
            height=400,
            title_x=0.5,
            title_font=dict(size=20, color='#034ea2'),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(size=12)
            ),
            xaxis_tickangle=-45,
            margin=dict(t=50, l=50, r=50, b=100),
            plot_bgcolor='white',
            xaxis=dict(
                showgrid=True,
                gridcolor='#E5E5E5'
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='#E5E5E5',
                tickformat='',  # Removido formato decimal
                title='Salário Médio (R$)'
            )
        )
        
        # Formatação do hover com valores inteiros
        fig_salary.update_traces(
            hovertemplate="<b>%{data.name}</b><br>" +
                         "Cargo: %{x}<br>" +
                         "Valor: R$ %{y:,.0f}".replace(",", ".") +
                         "<extra></extra>"
        )
        
        st.plotly_chart(fig_salary, use_container_width=True)
        
        # Display detailed results table in a collapsible section
        with st.expander("### Detalhamento por Servidor", expanded=False):
            formatted_results = results_df[[ 'TIPO DE VINCULO',
                'MATRICULA', 'CARGO', 'PLANO', 
                'VALOR', 'VALOR COM IMPACTO', 'IMPACTO', 'VALOR COM ENCARGO'
            ]].copy()

            st.dataframe(
                formatted_results.style.format({
                    'VALOR': format_brl,
                    'VALOR COM IMPACTO': format_brl,
                    'IMPACTO': format_brl,
                    'VALOR COM ENCARGO': format_brl,
                }),
                use_container_width=True
            )

st.markdown('</div>', unsafe_allow_html=True)