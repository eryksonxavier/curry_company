# Libraries
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
from PIL import Image
import folium
from streamlit_folium import folium_static
from datetime import datetime

st.set_page_config( page_title='Visão Entregadores', page_icon='🛒', layout='wide' )

# ------------------------------------
# Funções
# ------------------------------------

def top_delivers( df1, top_asc ):
	df2 = ( df1.loc[:,['Delivery_person_ID', 'City', 'Time_taken(min)']]
						   .groupby( ['City', 'Delivery_person_ID'] )
						   .mean()
						   .sort_values( ['City', 'Time_taken(min)'], ascending=top_asc )
						   .reset_index() )
				
	df_aux01 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
	df_aux02 = df2.loc[df2['City'] == 'Urban', :].head(10)
	df_aux03 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)			
					
	df3 = pd.concat( [df_aux01, df_aux02, df_aux03] ).reset_index( drop=True )
				
	return df3


def clean_code( df1 ):
	""" 
		Esta função tem a responsabilidade de limpar o DataFrame 
	
		Tipos de Limpeza:
		1. Remoção dos dados NaN
		2. Mudança do tipo da coluna de dados
		3. Remoção dos espaços das variáveis de texto
		4. Formatação da coluna de datas
		5. Limpeza da coluna de tempo (Remoção do texto da varável numérica)
		
		Input: DataFrame
		Output: DataFrame
		
	"""
	# 1. Removendo espaços em branco da coluna Age
	linhas_selecionadas = (df1['Delivery_person_Age'] != 'NaN ')
	df1 = df1.loc[linhas_selecionadas, :].copy()

	linhas_selecionadas = (df1['Road_traffic_density'] != 'NaN ')
	df1 = df1.loc[linhas_selecionadas, :].copy()

	# 1. Convertendo a coluna Age de texto para número
	df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype( int )

	# 2. Convertendo a coluna Ratings de texto para número decimal ( float )
	df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype( float )

	# 3. Convertendo a coluna order_date de texto para data
	df1['Order_Date'] = pd.to_datetime( df1['Order_Date'], format='%d-%m-%Y' )

	# 4. Removendo espaços em branco e Convertendo multiple_deliveries de texto para número inteiro ( int )
	linhas_selecionadas = (df1['multiple_deliveries'] != 'NaN ')
	df1 = df1.loc[linhas_selecionadas, :].copy()
	df1['multiple_deliveries'] = df1['multiple_deliveries'].astype( int )

	# 5. Removendo os espaços dentro de strings/texto/object com loop for
	# df1 = df1.reset_index( drop=True )
	# for i in range( len( df1 ) ):
	#   df1.loc[i, 'ID'] = df1.loc[i, 'ID'].strip()

	# 6. Removendo os espaços dentro de strings/texto/object das colunas abaixo
	df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
	df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
	df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
	df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
	df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
	df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()

	# 7. Limpando a coluna de time taken usando a função apply e escolhendo a função lambda dentro da apply
	df1['Time_taken(min)'] = df1['Time_taken(min)'].apply( lambda x: x.split( '(min) ')[1] )
	df1['Time_taken(min)'] = df1['Time_taken(min)'].astype( int )
	
	return df1

# Import Dataset
df = pd.read_csv( 'dataset/train.csv' )

# Cleaning Dataset
df1 = clean_code( df )

# =========================================
# Barra Lateral
# =========================================

st.header('Marketplace - Visão Entregadores')

#image_path = 'C:\\Users\\eryk-.000\\Documents\\repos\\ftc\\ex.png'
image = Image.open( 'ex.png' )
st.sidebar.image( image, width=120 )

st.sidebar.markdown( '### Cury Company' )
st.sidebar.markdown( '## Fastest Delivery in Town' )
st.sidebar.markdown( '''---''' )

st.sidebar.markdown( '## Selecione uma data limite' )

date_slider = st.sidebar.slider(
	'Até qual valor?',
	value=datetime( 2022, 2, 20),
	min_value=datetime(2022, 2, 11),
	max_value=datetime(2022, 4, 6),
	format='DD-MM-YYYY' )

st.sidebar.markdown( '''---''' )

traffic_options = st.sidebar.multiselect(
	'Quais as condições de trânsito',
	['Low', 'Medium', 'High', 'Jam'],
	default=['Low', 'Medium', 'High', 'Jam'] )

st.sidebar.markdown( '''---''' )
st.sidebar.markdown( '### Powered by Comunidade DS' )

# Filtro de data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

# Filtro de trânsito
linhas_selecionadas = df1['Road_traffic_density'].isin( traffic_options )
df1 = df1.loc[linhas_selecionadas, :]

# =========================================
# Layout no Streamlit
# =========================================	

tab1, tab2, tab3 = st.tabs( ['Visão Gerencial', '_', '_'] )

with tab1:
	with st.container():
		st.title( 'Overall Metrics' )
		
		col1, col2, col3, col4 = st.columns( 4, gap='large' )
		with col1:
			# A maior idade dos entregadores
			maior_idade = df1.loc[:, 'Delivery_person_Age'].max()
			col1.metric( 'Maior de idade', maior_idade )

		with col2:
			# A menor idade dos entregadores
			menor_idade = df1.loc[:, 'Delivery_person_Age'].min()
			col2.metric( 'Menor de idade', menor_idade )
			
		with col3:
			# A melhor condição dos veículos
			melhor_condicao = df1.loc[:, 'Vehicle_condition'].max()
			col3.metric( 'Melhor condição', melhor_condicao )
			
		with col4:
			# A pior condição dos veículos
			pior_condicao = df1.loc[:, 'Vehicle_condition'].min()
			col4.metric( 'Pior condição', pior_condicao )
	
	with st.container():
		st.markdown( '''---''' )
		st.title( 'Avaliações' )
		
		col1, col2 = st. columns( 2 )
		with col1:
			st.markdown( '##### Avaliações médias por Entregador' )
			df_aux = df1.loc[:, ['Delivery_person_ID', 'Delivery_person_Ratings'] ].groupby( 'Delivery_person_ID' ).mean().reset_index()
			st.dataframe( df_aux )
		
		with col2:
			st.markdown( '##### Avaliações médias por Trânsito' )
			
			df_avg_std_rating_by_traffic = ( df1.loc[:, ['Delivery_person_Ratings', 'Road_traffic_density'] ]
												.groupby( 'Road_traffic_density' )
												.agg( {'Delivery_person_Ratings' : ['mean', 'std']} ) )

			# Obs: Alteramos os nomes das colunas usando a função 'columns'
			df_avg_std_rating_by_traffic.columns = ['delivery_mean', 'delivery_std']

			# Obs2. Exibimos o dataframe com os nomes das colunas corretamente resetando o index.
			df_avg_std_rating_by_traffic = df_avg_std_rating_by_traffic.reset_index()
			
			st.dataframe( df_avg_std_rating_by_traffic )
			
			st.markdown( '##### Avaliações médias por Clima' )
			
			df_avg_std_rating_by_weatherconditions = ( df1.loc[:, ['Delivery_person_Ratings', 'Weatherconditions'] ]
														  .groupby( 'Weatherconditions' )
														  .agg( {'Delivery_person_Ratings' : ['mean', 'std']} ) )

			# Obs: Alteramos os nomes das colunas usando a função 'columns'
			df_avg_std_rating_by_weatherconditions.columns = ['delivery_mean', 'delivery_std']

			# Obs2. Exibimos o dataframe com os nomes das colunas corretamente resetando o index.
			df_avg_std_rating_by_weatherconditions.reset_index()
			
			st.dataframe( df_avg_std_rating_by_weatherconditions )
	
	with st.container():
		st.markdown( '''---''' )
		st.title( 'Velocidade de Entrega' )
		
		col1, col2 = st. columns( 2 )
		with col1:
			st.markdown( '##### Top Entregadores mais Rápidos' )
			df3 = top_delivers( df1, top_asc=True )
			st.dataframe( df3 )
		
		with col2:
			st.markdown( '##### Top Entregadores mais Lentos' )
			df3 = top_delivers( df1, top_asc=False )
			st.dataframe( df3 )
			