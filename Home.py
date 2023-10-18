import streamlit as st
from PIL import Image

st.set_page_config(
	page_title="Home",
	page_icon="🏠"
)

#image_path = '/Users/eryk-.000/Documents/repos/ftc/'
image = Image.open( 'ex.png' )
st.sidebar.image( image, width=120 )

st.sidebar.markdown( '### Cury Company' )
st.sidebar.markdown( '## Fastest Delivery in Town' )
st.sidebar.markdown( '''---''' )

st.write( "# Curry Company Growth Dashboard" )

st.markdown(
	"""
	Growth Dashboard foi construído para acompanhar as métricas de crescimento dos Entregadores e Restaurantes.
	### Como utilizar esse Growth Dashboard?
	- Visão Empresa:
		- Visão Gerencial: Métricas gerais de comportamento.
		- Visão Tática: Indicadores samanais de crescimento.
		- Visão Geográfica: Insigths de geolocalização.
	- Visão Entregador:
		- Acompanhamento dos indicadores semanais de crescimento
	- Visão Restaurante:
		- Indicadores semanais de crescimento dos restaurantes.
	### Ask for Help
	- Time de Data Science no Discord
		- @eryksonxavier
	""")