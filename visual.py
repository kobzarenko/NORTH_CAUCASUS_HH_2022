import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split


'''data = []

with open('dataset_klust.csv', 'r') as f:
	reader = csv.reader(f, delimiter=',')
	for i, line in enumerate(reader):
		data.append(line)
print(len(data))'''

df = pd.read_csv('dataset_klust.csv', sep=',')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True


def clusters_show_2d(data, x_col, y_col, clusters_count=5, scale=0.01):

	markers = ['ro', 'go', 'bo', 'yo', 'co', 'mo', 'ko']
	dfs = []

	for i in range(clusters_count):    

		x = np.array(df[(df['k_means_clust'] == i)][x_col])
		y = np.array(df[(df['k_means_clust'] == i)][y_col])

		_, x, _, y = train_test_split(x, y, test_size=scale, random_state=1)

		dfs.append(pd.DataFrame({'colors': markers[i], 'x': x, 'y': y}))

	_df = pd.concat(dfs)
	fig = px.scatter(_df, x=x, y=y, color_discrete_sequence=["yellow", "blue", "pink", "skyblue", "red"])

	return fig

SIDESTYLE = {
	'position': 'fixed',
	'top': 0,
	'left': 0,
	'bottom': 0,
	'width': '16rem',
	'padding': '2rem 1rem',
	'background-color': '#222222',
}


CONTSTYLE = {
	'margin-left': '18rem',
	'margin-right': '2rem',
	'padding': '2rem 1rem',
}


app.layout = html.Div([
	dcc.Location(id='url'),
	html.Div(
		[
			html.H2('Map', className='display-3', style={'color': 'white'}),
			html.Hr(style={'color': 'white'}),
			dbc.Nav(
				[
					dbc.NavLink('Сравнительный анализ кластеров', href='/page1', active='exact'),
					dbc.NavLink('Характеристика кластеров', href='/page2', active='exact'),
					dbc.NavLink('Визуализация кластеров по параметрам', href='/page3', active='exact'),
				],
				vertical=True,pills=True),
		],
		style=SIDESTYLE,
	),
	html.Div(id='page-content', children=[], style=CONTSTYLE)
])


@app.callback(
	Output('page-content', 'children'),
	[Input('url', 'pathname')])


def pagecontent(pathname):
	if pathname == '/page1':
		return [

			html.Div(
				children=[
					html.H1(children='Визуализация данных', className='header-title'),

					html.P(children='Сравнительный анализ кластеров по исходным данным', className='header-description')
				], className='header'),

			html.Div([
				dcc.Dropdown(
					id='page1_drop',
					options=[
						{'label': 'Регионы', 'value': 'region'},
						{'label': 'Время жизни', 'value': 'lifetime'},
						{'label': '', 'value': 'мгы'}
					],
					value='region', className='dropdown', style= {'margit-bottom':'32px'}
				), dcc.Graph(id='output_graph')], className='card')
				]

	elif pathname == '/page2':
		return [
			html.Div(
				children=[
				html.H1('Заголовок',className='header-title',
						style={'textAlign':'center'})
					], className='header'),
				dcc.Graph(id='graph1',
						 figure=px.scatter(df1, x='',
						 y= 'price'),className='card'),

				dcc.Graph(id='graph2',
						 figure=px.scatter(df1,x='carat',
						 y= 'price',facet_col= 'color'),className='card')
				]
	elif pathname == '/page3':
		return [
			html.Div(
				children=[
					html.H1(children='Визуализация данных', className='header-title'),

					html.P(children='Сравнительный анализ кластеров по исходным данным', className='header-description')
				], className='header'),

			html.Div([
				dcc.Dropdown(
					id='page2_drop',
					options=[
						{'label': 'Регионы', 'value': 'region'},
						{'label': 'Время жизни', 'value': 'lifetime'},
						{'label': 'ОКВЭД', 'value': 'okved'},
						{'label': 'Средняя ЗП', 'value': 'average salary'},
						{'label': 'Оборот розничной торговли', 'value': 'oborot'}
					],
					multi=True, value=['region', 'lifetime'], className='dropdown', style= {'margit-bottom':'32px'}
				), dcc.Graph(id='output2_graph')], className='card')

				]

@app.callback(
	Output(component_id='output_graph', component_property='figure'),
	[Input(component_id='page1_drop', component_property='value')]
)

def update_output(value):
	if value == 'region':
		figure={
				'data': [
					{'x': ['г. Москва', 'г. Санкт-Петербург', 'Ростов-на-Дону', 'Приморский край'], 'y': [len(df[(df['k_means_clust'] == 0) & (df['region'] == 77)].value_counts()), len(df[(df['k_means_clust'] == 0) & (df['region'] == 78)].value_counts()), len(df[(df['k_means_clust'] == 0) & (df['region'] == 61)].value_counts()), len(df[(df['k_means_clust'] == 0) & (df['region'] == 25)].value_counts())], 'type': 'bar', 'name': 'Кластер №1'},
					{'x': ['г. Москва', 'г. Санкт-Петербург', 'Ростов-на-Дону', 'Приморский край'], 'y': [len(df[(df['k_means_clust'] == 1) & (df['region'] == 77)].value_counts()), len(df[(df['k_means_clust'] == 1) & (df['region'] == 78)].value_counts()), len(df[(df['k_means_clust'] == 1) & (df['region'] == 61)].value_counts()), len(df[(df['k_means_clust'] == 1) & (df['region'] == 25)].value_counts())], 'type': 'bar', 'name': 'Кластер №2'},
					{'x': ['г. Москва', 'г. Санкт-Петербург', 'Ростов-на-Дону', 'Приморский край'], 'y': [len(df[(df['k_means_clust'] == 2) & (df['region'] == 77)].value_counts()), len(df[(df['k_means_clust'] == 2) & (df['region'] == 78)].value_counts()), len(df[(df['k_means_clust'] == 2) & (df['region'] == 61)].value_counts()), len(df[(df['k_means_clust'] == 2) & (df['region'] == 25)].value_counts())], 'type': 'bar', 'name': 'Кластер №3'},
					{'x': ['г. Москва', 'г. Санкт-Петербург', 'Ростов-на-Дону', 'Приморский край'], 'y': [len(df[(df['k_means_clust'] == 3) & (df['region'] == 77)].value_counts()), len(df[(df['k_means_clust'] == 3) & (df['region'] == 78)].value_counts()), len(df[(df['k_means_clust'] == 3) & (df['region'] == 61)].value_counts()), len(df[(df['k_means_clust'] == 3) & (df['region'] == 25)].value_counts())], 'type': 'bar', 'name': 'Кластер №4'},
					{'x': ['г. Москва', 'г. Санкт-Петербург', 'Ростов-на-Дону', 'Приморский край'], 'y': [len(df[(df['k_means_clust'] == 4) & (df['region'] == 77)].value_counts()), len(df[(df['k_means_clust'] == 4) & (df['region'] == 78)].value_counts()), len(df[(df['k_means_clust'] == 4) & (df['region'] == 61)].value_counts()), len(df[(df['k_means_clust'] == 4) & (df['region'] == 25)].value_counts())], 'type': 'bar', 'name': 'Кластер №5'}
				],
				'layout': {
					'title': 'Сравнительный анализ кластеров по регионам'
				}
			}
	elif value == 'lifetime':
		y = []
		for i in range(5):
			y.append(int(df[(df['k_means_clust'] == i)]['lifetime'].mean()))

		figure={'data': [
					{'x': ['Кластер ' + str(i) for i in range(1, 6)], 'y': y, 'type': 'bar'},
				]
				,
				'layout': {
					'title': 'Сравнительный анализ кластеров по времени жизни'
				}
			}
	elif value == '3':
		figure={
				'data': [
					{'x': ['г. Москва', 'г. Санкт-Петербург', 'Ростов-на-Дону', 'Приморский край'], 'y': [len(df[(df['k_means_clust'] == 0) & (df['region'] == 77)].value_counts()), len(df[(df['k_means_clust'] == 0) & (df['region'] == 78)].value_counts()), len(df[(df['k_means_clust'] == 0) & (df['region'] == 61)].value_counts()), len(df[(df['k_means_clust'] == 0) & (df['region'] == 25)].value_counts())], 'type': 'bar', 'name': 'Кластер №1'},
					{'x': ['г. Москва', 'г. Санкт-Петербург', 'Ростов-на-Дону', 'Приморский край'], 'y': [len(df[(df['k_means_clust'] == 1) & (df['region'] == 77)].value_counts()), len(df[(df['k_means_clust'] == 1) & (df['region'] == 78)].value_counts()), len(df[(df['k_means_clust'] == 1) & (df['region'] == 61)].value_counts()), len(df[(df['k_means_clust'] == 1) & (df['region'] == 25)].value_counts())], 'type': 'bar', 'name': 'Кластер №2'},
					{'x': ['г. Москва', 'г. Санкт-Петербург', 'Ростов-на-Дону', 'Приморский край'], 'y': [len(df[(df['k_means_clust'] == 2) & (df['region'] == 77)].value_counts()), len(df[(df['k_means_clust'] == 2) & (df['region'] == 78)].value_counts()), len(df[(df['k_means_clust'] == 2) & (df['region'] == 61)].value_counts()), len(df[(df['k_means_clust'] == 2) & (df['region'] == 25)].value_counts())], 'type': 'bar', 'name': 'Кластер №3'},
					{'x': ['г. Москва', 'г. Санкт-Петербург', 'Ростов-на-Дону', 'Приморский край'], 'y': [len(df[(df['k_means_clust'] == 3) & (df['region'] == 77)].value_counts()), len(df[(df['k_means_clust'] == 3) & (df['region'] == 78)].value_counts()), len(df[(df['k_means_clust'] == 3) & (df['region'] == 61)].value_counts()), len(df[(df['k_means_clust'] == 3) & (df['region'] == 25)].value_counts())], 'type': 'bar', 'name': 'Кластер №4'},
					{'x': ['г. Москва', 'г. Санкт-Петербург', 'Ростов-на-Дону', 'Приморский край'], 'y': [len(df[(df['k_means_clust'] == 4) & (df['region'] == 77)].value_counts()), len(df[(df['k_means_clust'] == 4) & (df['region'] == 78)].value_counts()), len(df[(df['k_means_clust'] == 4) & (df['region'] == 61)].value_counts()), len(df[(df['k_means_clust'] == 4) & (df['region'] == 25)].value_counts())], 'type': 'bar', 'name': 'Кластер №5'}
				],
				'layout': {
					'title': 'Сравнительный анализ кластеров по регионам'
				}
			}
	return figure


@app.callback(
	Output(component_id='output2_graph', component_property='figure'),
	[Input(component_id='page2_drop', component_property='value')]
)

def update_output(value):

	return clusters_show_2d(df, value[0], value[1])


app.run_server(debug=True, port=3000)