import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

df_glance = pd.read_csv('/Users/andreybobua/PycharmProjects/cost-of-living_v2.csv')

st.set_page_config(page_title="My Webpage", page_icon=":tada")

st.title("Living cost comparsion")
st.subheader("This dashboard will present the information about different living costs all over the world.")
st.write("Let's display my dataset:")
st.dataframe(df_glance)
st.write("Seems like we have some extra data and unreadable names of columns,"
         " that's why we are to shorten our range of data, basing on our hypothesis, which gonna be stated later and rename our columns:")
df = pd.read_csv('/Users/andreybobua/PycharmProjects/cost-of-living_v2.csv')
df = df[["city", "country", "x1", "x3", "x4", "x5", "x7", "x9", "x10", "x12", "x16", "x20", "x23", "x25", "x26","x27", "x38", "x44", "x46", "x49", "x54"]]
df.rename(columns = {"x1": "cheap_rest", "x3": "mcdonalds", "x4": "domestic_beer_rest", "x5": "imported_beer_rest",
                     "x25": "domestic_beer_market", "x26": "imported_beer_market", "x7": "coke",
                    "x9": "milk", "x10": "bread", "x12": "eggs", "x16": "apple", "x20": "potato", "x23": "water", "x27": "cigarettes",
                     "x38": "internet", "x44": "jeans", "x46": "nike_shoes", "x49": "apartment", "x54": "wage"},inplace=True)
st.dataframe(df)
st.write("____________________________________________________________________________________")
st.subheader("Features of the dataset:")
st.write("city - Name of the city")
st.write("country - Name of the country")
st.write("cheap_rest - Meal, Inexpensive Restaurant (USD)")
st.write("mcdonalds - McMeal at McDonalds (or Equivalent Combo Meal) (USD)")
st.write("domestic_beer_rest - Domestic Beer (0.5 liter draught, in restaurants) (USD)")
st.write("imported_beer_rest - Imported Beer (0.33 liter bottle, in restaurants) (USD)")
st.write("coke - Coke/Pepsi (0.33 liter bottle, in restaurants) (USD)")
st.write("milk - Milk (regular), (1 liter) (USD)")
st.write("bread - Loaf of Fresh White Bread (500g) (USD)")
st.write("eggs - Eggs (regular) (12) (USD)")
st.write("apple - Apples (1kg) (USD)")
st.write("potato - Potato (1kg) (USD)")
st.write("water - Water (1.5 liter bottle, at the market) (USD)")
st.write("domestic_beer_market - Domestic Beer (0.5 liter bottle, at the market) (USD)")
st.write("imported_beer_market - Imported Beer (0.33 liter bottle, at the market) (USD)")
st.write("cigarettes - Cigarettes 20 Pack (Marlboro) (USD)")
st.write("internet - Internet (60 Mbps or More, Unlimited Data, Cable/ADSL) (USD)")
st.write("jeans - 1 Pair of Jeans (Levis 501 Or Similar) (USD)")
st.write("nike_shoes - 1 Pair of Nike Running Shoes (Mid-Range) (USD)")
st.write("apartment - Apartment (1 bedroom) Outside of Centre (USD)")
st.write("wage - Average Monthly Net Salary (After Tax) (USD)")
st.write("____________________________________________________________________________________")
st.subheader("Now let's check if there are any NaN values in this dataset:")
st.metric(label="NaN", value=str(df.isnull().sum().sum()))
st.write("Too much NaN values make dataset impossible to work with, then let's clean it")
df = df.dropna(subset = ["wage", "apartment", "domestic_beer_market", "imported_beer_market"])
st.metric(label="NaN", value=str(df.isnull().sum().sum()))
st.write("That looks better (considering the fact that the dataset is now almost 5000 rows x 20 columns)")
st.write("____________________________________________________________________________________")
st.subheader("Analysis")
st.subheader("Firstly I compared prices on some basics such as milk, water, eggs and something like that.")
st.subheader("Here's the example of histogram I built for analysis:")
df_temp = df[["country", "water"]]
df_temp = df_temp.dropna(subset = ["water"])
fig1 = px.histogram(df_temp.groupby(["country"]).mean().reset_index(), range_y = [0, df['water'].max() + 1], x = "country", y="water",
                   title="Average water prices in the world", color_discrete_sequence=["aqua"])
fig1.add_scatter(x = ["Afghanistan", "Yemen"], y=[df['water'].median(), df['water'].median()], mode='lines', name='Median Line')
fig1.update_layout(template="plotly_dark", width=1000, height=600)
st.plotly_chart(fig1)
st.write('''<p>I came to conclusion that<strong>the highest prices</strong> on the main basic products like milk, eggs and others <br>
            are mainly met in Oceania and the countries in area of North America:</p>''', unsafe_allow_html=True)
st.markdown('''<ul>
                <li>Nauru</li>
                <li>Cook islands</li>
                <li>Antigua and Barbuda</li>
                <li>Saint Vincent and The Grenadines,</li>
                <li>Bermuda,</li>
                <li>Bahamas, etc.</li>
            </ul>''', unsafe_allow_html=True)
st.write('''<p>I came to conclusion that<strong>the highest prices</strong> on the main basic products like milk, eggs and others <br>
            are mainly met in Oceania and the countries in area of North America:</p>''', unsafe_allow_html=True)
st.write("And it's also worth-mentioning from analysis that regions with the highest prices are mostly remote areas like islands, "
         "and shipping products may be more expensive, than transportation in other countries is.")
st.write("____________________________________________________________________________________")
st.subheader("Then I had a hypothesis that in the United States McDonald's prices are much lower then in the rest of the world, but I denied it using choropleth graph")
df_temp2 = df[["country", "mcdonalds"]]
fig2 = px.choropleth(df_temp2.groupby(["country"]).mean().reset_index(), locations="country", color="mcdonalds", hover_name="country",
                     projection="natural earth", locationmode="country names", color_continuous_scale=px.colors.sequential.Plasma)
fig2.update_layout(template="plotly_dark", width=1000, height=600)
st.plotly_chart(fig2)
st.write("____________________________________________________________________________________")
st.subheader("After that I wanted to compare prices of beer from different places: a market and a restaurant. I made this ccomparsion using two-lined histogram. Now I'll provide one example:")
df_temp3 = df[["country", "domestic_beer_market", "domestic_beer_rest"]]
df_temp3 = df_temp3.dropna(subset = ["domestic_beer_market", "domestic_beer_rest"])
df_temp3 = df_temp3[(df_temp3['country'] >= 'Libya')]

fig3 = px.bar(df_temp3.groupby(["country"]).mean().reset_index(),
             x='country',
             y=['domestic_beer_market', 'domestic_beer_rest'],
             labels={'value': 'Values'},
             title='Average domestic beer prices in the world (part 2)',
             color_discrete_map={'domestic_beer_market': '#fbb117', 'domestic_beer_rest': '#fce6cc'},
             barmode='group')
fig3.update_layout(template="plotly_dark", width=1100, height=600)
fig3.add_scatter(x = ["Libya", "Zimbabwe"], y=[df_temp3['domestic_beer_market'].median(), df_temp3['domestic_beer_market'].median()], mode='lines', name='Median price of domestic beer from markets')
fig3.add_scatter(x = ["Libya", "Zimbabwe"], y=[df_temp3['domestic_beer_rest'].median(), df_temp3['domestic_beer_rest'].median()], mode='lines', name='Median price of domestic beer from restaurants')
st.plotly_chart(fig3)
st.write("____________________________________________________________________________________")
st.subheader("And by the end of my analysis I compared prices on different things in 6 countries from different parts of the world using 'make_subplots' and 'go.Pie'")
df_temp4 = df[["country", "cheap_rest", "apartment", "internet", "cigarettes", "jeans", "nike_shoes"]]
df_temp4 = df_temp4[df_temp4['country'].isin(['Russia', "United States", "Italy", "Australia", "Japan", "Chile"])]
df_temp4 = df_temp4.dropna(subset = ["country", "cheap_rest", "apartment", "internet", "cigarettes", "jeans", "nike_shoes"])
df_temp4 = df_temp4.groupby(["country"]).mean()
fig4 = make_subplots(
    rows=3, cols=2,
    specs=[[{"type": "pie"}, {"type": "pie"}], [{"type": "pie"}, {"type": "pie"}], [{"type": "pie"}, {"type": "pie"}]],
    subplot_titles=("Australia", "Chile", "Italy", "Japan", "Russia", "United States"))
names = ["Cheap restaurant", "Apartments", "Internet", "Cigarettes", "Jeans", "Shoes"]
fig4.add_trace(go.Pie(values=[15, 942, 52, 24, 68, 96], labels = names, textinfo='label+value'), row=1, col=1)
fig4.add_trace(go.Pie(values=[7, 338, 26, 5, 43, 51], labels = names, textinfo='label+value'), row=1, col=2)
fig4.add_trace(go.Pie(values=[15, 461, 29, 6, 77, 88], labels = names, textinfo='label+value'), row=2, col=1)
fig4.add_trace(go.Pie(values=[6, 439, 34, 4, 43, 60], labels = names, textinfo='label+value'), row=2, col=2)
fig4.add_trace(go.Pie(values=[10, 267, 9, 3, 84, 100], labels = names, textinfo='label+value'), row=3, col=1)
fig4.add_trace(go.Pie(values=[17, 1233, 69, 8, 45, 78], labels = names, textinfo='label+value'), row=3, col=2)

fig4.update_layout(template="plotly_dark", width=1100, height=1000)
st.plotly_chart(fig4)