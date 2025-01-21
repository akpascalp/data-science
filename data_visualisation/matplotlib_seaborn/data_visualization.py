import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from io import StringIO

def fetch_data(url):
    """Fetch data from a given URL and return a DataFrame."""
    response = requests.get(url, verify=True)
    return pd.read_csv(StringIO(response.text))

def plot_automobile_sales(df):
    """Plot automobile sales during recession."""
    df_line = df.groupby(df['Year'])['Automobile_Sales'].mean()
    plt.figure(figsize=(10, 6))
    df_line.plot(kind='line')
    plt.xlabel('Year')
    plt.ylabel('Automobile Sales')
    plt.title('Automobile Sales during Recession')
    plt.xticks(list(range(1980, 2024)), rotation=75)
    plt.text(1982, 650, '1981-82 Recession')
    plt.text(1991, 600, '1991 Recession')
    plt.legend()
    plt.show()

def plot_vehicle_sales_trend(df):
    """Plot sales trend vehicle-wise during recession."""
    df_rec = df[df['Recession'] == 1]
    df_Mline = df_rec.groupby(['Year', 'Vehicle_Type'], as_index=False)['Automobile_Sales'].mean()
    df_Mline.set_index('Year', inplace=True)
    df_Mline = df_Mline.groupby(['Vehicle_Type'])['Automobile_Sales']
    df_Mline.plot(kind='line')
    plt.xlabel('Year')
    plt.ylabel('Automobile Sales')
    plt.title('Sales Trend Vehicle-wise during Recession')
    plt.legend()
    plt.show()

def plot_average_sales(df):
    """Plot average automobile sales during recession and non-recession."""
    new_df = df.groupby('Recession')['Automobile_Sales'].mean().reset_index()
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Recession', y='Automobile_Sales', hue='Recession', data=new_df)
    plt.xlabel('Recession')
    plt.ylabel('Automobile Sales')
    plt.title('Average Automobile Sales during Recession and Non-Recession')
    plt.xticks(ticks=[0, 1], labels=['Non-Recession', 'Recession'])
    plt.show()

def plot_gdp_variation(df):
    """Plot GDP variation during recession and non-recession periods."""
    rec_data = df[df['Recession'] == 1]
    non_rec_data = df[df['Recession'] == 0]
    fig = plt.figure(figsize=(12, 6))
    ax0 = fig.add_subplot(1, 2, 1)
    ax1 = fig.add_subplot(1, 2, 2)
    sns.lineplot(x='Year', y='GDP', data=rec_data, label='Recession', ax=ax0)
    ax0.set_xlabel('Year')
    ax0.set_ylabel('GDP')
    ax0.set_title('GDP Variation during Recession Period')
    sns.lineplot(x='Year', y='GDP', data=non_rec_data, label='Non-Recession', ax=ax1)
    ax1.set_xlabel('Year')
    ax1.set_ylabel('GDP')
    ax1.set_title('GDP Variation during Non-Recession Period')
    plt.tight_layout()
    plt.show()

def plot_seasonality_impact(df):
    """Plot seasonality impact on automobile sales."""
    non_rec_data = df[df['Recession'] == 0]
    size = non_rec_data['Seasonality_Weight']
    sns.scatterplot(data=non_rec_data, x='Month', y='Automobile_Sales', size=size)
    plt.xlabel('Month')
    plt.ylabel('Automobile Sales')
    plt.title('Seasonality impact on Automobile Sales')
    plt.show()

def plot_consumer_confidence(df):
    """Plot consumer confidence and automobile sales during recessions."""
    rec_data = df[df['Recession'] == 1]
    plt.scatter(rec_data['Consumer_Confidence'], rec_data['Automobile_Sales'])
    plt.xlabel('Consumer Confidence')
    plt.ylabel('Automobile Sales')
    plt.title('Consumer Confidence and Automobile Sales during Recessions')
    plt.show()
    plt.scatter(rec_data['Price'], rec_data['Automobile_Sales'])
    plt.xlabel('Average Vehicle Price')
    plt.ylabel('Automobile Sales')
    plt.title('Price and Automobile Sales during Recessions')
    plt.show()


if __name__ == "__main__":
    df = fetch_data("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv")
    plot_automobile_sales(df)
    plot_vehicle_sales_trend(df)
    plot_average_sales(df)
    plot_gdp_variation(df)
    plot_seasonality_impact(df)
    plot_consumer_confidence(df)