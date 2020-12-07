def find_top_total_cases(n = 20):

    import pandas as pd
    corona_df=pd.read_csv("covid-dataset.csv")
    corona_df.replace('USA', "United States of America", inplace = True)
    corona_df.replace('Tanzania', "United Republic of Tanzania", inplace = True)
    corona_df.replace('Democratic Republic of Congo', "Democratic Republic of the Congo", inplace = True)
    corona_df.replace('Congo', "Republic of the Congo", inplace = True)
    corona_df.replace('Lao', "Laos", inplace = True)
    corona_df.replace('Syrian Arab Republic', "Syria", inplace = True)
    corona_df.replace('Serbia', "Republic of Serbia", inplace = True)
    corona_df.replace('Czechia', "Czech Republic", inplace = True)
    corona_df.replace('UAE', "United Arab Emirates", inplace = True)
    by_country = corona_df.groupby('Country').sum()[['total_cases', 'total_deaths', 'icu_patients', 'total_tests']]
    cdf = by_country.nlargest(n, 'total_cases')[['total_cases']]
    return cdf

cdf=find_top_total_cases()
pairs=[(country,total_cases) for country,total_cases in zip(cdf.index,cdf['total_cases'])]


import folium
import pandas as pd
corona_df = pd.read_csv("covid-dataset.csv")
corona_df=corona_df[['latitude','longitude','total_cases','Country','total_deaths']]
corona_df=corona_df.dropna()

m=folium.Map(location=[34.223334,-82.461707],
            tiles='cartodbpositron',
            zoom_start=2)

def circle_maker(x):
    tooltip= 'Click Me!'
    folium.Circle(location=[x[0],x[1]],
                 radius=float(x[2])/5,
                 color="red",
                 popup='Country:{} Cases:{} Deaths:{}'.format(x[3],x[2],x[4]),
                 tooltip=tooltip
    ).add_to(m)

url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
country_shapes = f'{url}/world-countries.json'
folium.Choropleth(
    geo_data=country_shapes,
    name='choropleth COVID-19',
    data=corona_df,
    columns=['Country','total_deaths'],
    key_on='feature.properties.name',
    fill_color='PuRd',
    nan_fill_color='white',
    legend_name='Total Deaths'
).add_to(m)

corona_df.apply(lambda x:circle_maker(x),axis=1)
folium.LayerControl().add_to(m)




html_map=m._repr_html_()
from flask import Flask,render_template

app=Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html",table=cdf, cmap=html_map,pairs=pairs)

if __name__=="__main__":
    app.run(debug=True)
