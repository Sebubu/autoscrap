from bokeh.plotting import figure, output_file, show
from PdFrame import get_main_df, get_good_columns
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score
import pandas as pd


column = 'Leergewicht(kg)'


df, good_columns = get_good_columns()
#df[column] = df[column].astype(int)


df['Inverkehrsetzung'] = pd.to_datetime(df['Inverkehrsetzung'])
df = df[(df.Inverkehrsetzung.dt.year > 1995) & (df.Inverkehrsetzung.dt.year < 2016)]
df = df.sample(frac=1).reset_index(drop=True)

rdf = df[[column, 'Preis(chf)', 'vehid']].dropna().apply(pd.to_numeric)
rdf = rdf[(rdf[column] != 0)]

test_count = 1000
train = rdf[:-test_count]
test = rdf[-test_count:]
test = test.sort_values(column)

x_columns = [column]
y_columns = ['Preis(chf)']


x_train = train[x_columns]
y_train = train[y_columns]
x_test = test[x_columns]
y_test = test[y_columns]

best_fit = 1
best_r2 = -100000
best_regr = None
for i in range(1,15):
    regr = make_pipeline(PolynomialFeatures(i), Ridge())
    regr.fit(x_train, y_train)
    prediction = regr.predict(x_test)
    score = r2_score(y_test,prediction)
    if score > best_r2:
        best_fit = i
        best_r2 = score
        best_regr = regr
        print(str(i) + ": " + str(best_r2))

regr = make_pipeline(PolynomialFeatures(best_fit), Ridge())
regr.fit(x_train, y_train)
prediction = regr.predict(x_test)
p_list = []

for p in prediction:
    p_list.append(p[0])




output_file("lines.html")

# create a new plot with a title and axis labels
p = figure(title=column + "-Preis Diagramm", x_axis_label=column, y_axis_label='Preis(chf)', width=1200)

# add a line renderer with legend and line thickness

p.circle(df[column], df['Preis(chf)'], legend="Temp.", size=1)
p.line(x_test[column],p_list, legend="Regression", line_width=2, line_color="red")

# show the results
show(p)

exit()
colors = ['Aussenfarbe_grau mét.', 'Aussenfarbe_grün mét.', 'Aussenfarbe_rot', 'Aussenfarbe_schwarz', 'Aussenfarbe_schwarz mét.', 'Aussenfarbe_silber mét.', 'Aussenfarbe_weiss']
for color in colors:

    df1 = df[[color, 'Preis(chf)']].dropna()
    print(color + ": " + str(df1[(df1[color] == 1)]['Preis(chf)'].mean()))
exit()

