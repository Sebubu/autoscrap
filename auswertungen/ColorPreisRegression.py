from bokeh.plotting import figure, output_file, show
from bokeh.charts import Bar

from PdFrame import get_good_columns
import pandas as pd

selector = "Aussenfarbe_"

df, good_columns = get_good_columns()
columns = []
for col in df.columns.values:
    if selector in col:
        columns.append(col)



df['Inverkehrsetzung'] = pd.to_datetime(df['Inverkehrsetzung'])
df = df[(df.Inverkehrsetzung.dt.year > 1995) & (df.Inverkehrsetzung.dt.year < 2014)]
df = df.sample(frac=1).reset_index(drop=True)
df = df[(df['Leistung_in_PS'] < 200)]

x = []
y = []
for col in columns:
    rdf = df[[col,'Preis(chf)']].dropna().apply(pd.to_numeric)
    length = len(rdf[(rdf[col] == 1)])
    if length > 70:
        farbe = col.split("_")[1]
        x.append(farbe)
        y.append(rdf[(rdf[col] == 1)]['Preis(chf)'].mean())
        print(farbe + ": " + str(length))



dict = {'values':y, 'names':x}
df = pd.DataFrame(dict)
df = df.sort_values('values')
print(df)


output_file("lines.html")

# create a new plot with a title and axis labels
#p = figure(title=selector + "-Preis Diagramm", x_axis_label=selector, y_axis_label='Preis(chf)', width=1200)
from bokeh.charts.attributes import CatAttr
p = Bar(df, label=CatAttr(columns=['names'], sort=False), values='values', width=1200, height=700)

# add a line renderer with legend and line thickness

#p.line(x_test[column],p_list, legend="Regression", line_width=2, line_color="red")

# show the results
show(p)


