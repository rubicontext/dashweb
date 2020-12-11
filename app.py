# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from pandas import DataFrame
import pandas.io.sql as sqlio
import plotly.graph_objs as go
import psycopg2
import os

#DATABASE_URL = os.environ['DATABASE_URL']
#conn = psycopg2.connect(DATABASE_URL, sslmode='require')
#conn = psycopg2.connect(host="localhost", dbname="rubiweb_dev", user="rubi", password="rubi_db")
#cur = conn.cursor()
#cur.execute("SELECT * FROM generic_search")
#gen_search_list = cur.fetchall()


#TODO in conf file
host="localhost"
dbname="rubiweb_dev"
user="rubi"
password="rubi_db"
port=5432

conn = psycopg2.connect("host='{}' port={} dbname='{}' user={} password={}".format(host, port, dbname, user, password))
sql = "SELECT * FROM generic_search;"
df_gen_search= sqlio.read_sql_query(sql, conn)
conn = None

#df = DataFrame(cur.fetchall())
#df.columns = resoverall.keys()

df = df_gen_search


#df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/c78bf172206ce24f77d6363a2d754b59/raw/c353e8ef842413cae56ae3920b8fd78468aa4cb2/usa-agricultural-exports-2011.csv')


def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H4(children='Gen search list from PostgreSQL'),
    generate_table(df)
])

if __name__ == '__main__':
    app.run_server(debug=True)