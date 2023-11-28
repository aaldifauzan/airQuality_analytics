import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')
all_data = pd.read_csv('all_data.csv')

def main():
    districts = all_data['station'].unique()
    selected_district = st.sidebar.selectbox('Select a district', districts)
    
    start_date = pd.Timestamp(st.sidebar.date_input("Start Date"))
    end_date = pd.Timestamp(st.sidebar.date_input("End Date"))
    
    filtered_data = all_data[all_data['station'] == selected_district]
    filtered_data = filtered_data[(pd.to_datetime(filtered_data['datetime']) >= start_date) & (pd.to_datetime(filtered_data['datetime']) <= end_date)]

    avg_temp = filtered_data['TEMP'].mean()
    avg_pres = filtered_data['PRES'].mean()
    avg_dewp = filtered_data['DEWP'].mean()
    avg_rain = filtered_data['RAIN'].mean()

    st.write(f'### Average Climate Data for {selected_district}')
    avg_climate_dict = {'TEMP': avg_temp, 'PRES': avg_pres, 'DEWP': avg_dewp, 'RAIN': avg_rain}
    avg_climate_df = pd.DataFrame.from_dict(avg_climate_dict, orient='index', columns=['Average'])
    st.table(avg_climate_df)

    avg_pm25 = filtered_data['PM2.5'].mean()
    avg_pm10 = filtered_data['PM10'].mean()
    st.write(f'### Average PM2.5 and PM10 for {selected_district}')
    avg_pm_dict = {'PM2.5': avg_pm25, 'PM10': avg_pm10}
    avg_df = pd.DataFrame.from_dict(avg_pm_dict, orient='index', columns=['Average'])
    st.bar_chart(avg_df)

    trend_data = filtered_data[['datetime', 'SO2', 'NO2', 'O3', 'CO']]
    trend_data['datetime'] = pd.to_datetime(trend_data['datetime'])
    trend_data.set_index('datetime', inplace=True)
    monthly_trend = trend_data.resample('M').mean() 
    st.write(f'### Monthly Trend for SO2, NO2, O3, and CO in {selected_district}')

    plt.figure(figsize=(10, 6))
    plt.plot(monthly_trend.index, monthly_trend['SO2'], label='SO2')
    plt.plot(monthly_trend.index, monthly_trend['NO2'], label='NO2')
    plt.plot(monthly_trend.index, monthly_trend['O3'], label='O3')
    plt.xlabel('Date')
    plt.ylabel('Pollutant Level')
    plt.title('Monthly Trend for SO2, NO2, and O3')
    plt.legend()
    st.pyplot(plt)

    plt.figure(figsize=(10, 6))
    plt.plot(monthly_trend.index, monthly_trend['CO'], label='CO', color='green')
    plt.xlabel('Date')
    plt.ylabel('CO Level')
    plt.title('Monthly Trend for CO')
    plt.legend()
    st.pyplot(plt)

if __name__ == '__main__':
    st.title('Air Quality Dashboard')
    st.write('Visualize Average Climate Data, Average PM2.5 and PM10, and Monthly Trend for SO2, NO2, O3, and CO')
    main()
