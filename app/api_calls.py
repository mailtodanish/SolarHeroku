import requests, os, datetime, pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle
from selenium import webdriver
from opencage.geocoder import OpenCageGeocode

# Web Scraping
import json
from time import sleep, strftime
from selenium.webdriver.common.keys import Keys

# chrome_options = webdriver.ChromeOptions()
# chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--no-sandbox")
CHROMEDRIVER_PATH = "/app/.chromedriver/bin/chromedriver"

chrome_options = webdriver.ChromeOptions()

chrome_options.binary_location = '.apt/usr/bin/google-chrome-stable'
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('headless')

driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
print('browser is ready')
# driver = webdriver.Chrome(executable_path= os.environ.get("CHROMEDRIVER_PATH"),chrome_options=chrome_options)

driver.get('https://www.google.com')


# Retrieve set environment variables
DarkSkyKey = "67ea5b58bde0e53adb5d1b0cf7c94395"
OpenCageKey = "227274f48bf449628de5ceeeacfbf6a7"
# DarkSkyKey = os.environ.get('DarkSky')
# OpenCageKey = os.environ.get('OpenCage')

# string formatting notes - user inputs hardcoded for debugging
location = '555 S Allison Pkwy, Lakewood, CO 80226'
time_span = 2



# Time Fx
def get_time(user_input = None):
    '''
    gets time in the right formats for our calls
    outputs are in strings
    user_input takes a user input in mm/dd/YYYY format
    
    '''
    if user_input:
        
        units = user_input.split('/')
        myorder = [2, 0, 1]
        units = [units[i] for i in myorder]
        units.append('06')
        units.append('00')
        units = [int(unit) for unit in units]

    else:
        current_time = datetime.datetime.now()
        units = [current_time.year, current_time.month, 
                 current_time.day-1, current_time.hour, 
                 current_time.minute]
    time_list = []
    for unit in units:
        if unit < 10:
            unit = '0' + str(unit)
        time_list.append(unit)
    return time_list

def convert_time(time_list):
    '''
    turns the time_list into the correct format for specific calls
    if sol, format for solortopo.  if not, format for darksky
    returns a string
    time_list should = [y, m, d, h, m, s]
    '''
    time = (f'{time_list[3]}:{time_list[4]}:00') 
    solartopo_date = (f'{time_list[2]}/{time_list[1]}/{time_list[0]}')    
    darksky_date = (f'{time_list[0]}-{time_list[1]}-{time_list[2]}')
    return solartopo_date, darksky_date, time
    
def get_next_day(date):
    '''
    time is relative, add a day.
    accepts YYYY-mm-dd format
    '''
    split = date.split('-')
    integers = [int(x) for x in split]
    integers[2] += 1
    string = '-'.join(str(num) for num in integers)
    return string

def convert_minutes(time, forward = False, seconds = True):
    '''
    function takes a military time clock reading eg 14:26 string 
    and converts it to minutes only and vice versa to the seconds 
    '''
    if (forward == True):
        converted = (int(time.split(':')[0]) * 60) + (int(time.split(':')[1]))
        
    elif (forward == False) & (seconds == True):
        minutes = time//60
        seconds = time%60
        hours = minutes//60
        minutes = hours%60
        if len(str(hours)) == 1:
            hours = '0' + str(hours)
        if len(str(minutes)) == 1:
            minutes = '0' + str(minutes)
        if len(str(seconds)) == 1:
            seconds = '0' + str(seconds)
        converted = str(hours) + ':' + str(minutes) + ":" +  str(seconds)
    else:
        hours = time//60
        minutes = time%60
        if len(str(hours)) == 1:
            hours = '0' + str(hours)
        if len(str(minutes)) == 1:
            minutes = '0' + str(minutes)
        converted = str(hours) + ':' + str(minutes)

    # missing conditional forward:True seconds:True currently returns the above condition
    return converted

def get_final_minutes(colon = False):
    '''
    creates a day minute index of 15 minute intervals with or without the colon
    '''
    minutes = []
    hours = []
    counter = 0
    h = 0
    for i in range(0,1440,15):
        minutes.append(counter)
        hours.append(h)
        counter += 15
        if counter > 45:
            h += 1
            counter = 0
    time = [] 
    for i in range(96):
        time.append(str(hours[i]) + ':' + str(minutes[i]))
    if colon:
        return time
    wonky_times = []
    for i, item in enumerate(time):
        h,m = item.split(':')
        h = int(h)
        m = int(m)
        if m == 0:
            h = h*10
        else:
            pass
        h = str(h)
        m = str(m)
        wonky_times.append(h + m)
    wonky_times = [int(i) for i in wonky_times]
    return wonky_times


# Clear
def clear_cache():
    '''
    optional function to be used to reset the stored data.
    '''
    results = pd.DataFrame(columns = ['Zenith Angle [degrees]', 'Azimuth Angle [degrees]', 'Latitude [deg]',
       'Longitude [deg]', 'Temp [deg C]', 'Minutes', 'Time Index'], index=range(96))
    return results


# # building Dataframe

def get_minutes(df):
    for i in range(96):
        df.loc[i]['Minutes'] = i*15
    return df

def get_coordinates(location, df):
    '''
    gets specific geometric location given a fuzzy address using OpenCage Geocoder.
    accepts a string address
    outputs latitude and longitude
    '''

    # print(location, df)
    postal_code = [int(s) for s in location.split() if s.isdigit()]
    # place_name = [str(s) for s in location.split() if not s.isdiget()]
    numbers = str(postal_code[-1])
    
    geocoder = OpenCageGeocode(OpenCageKey)

    locate = geocoder.geocode(location)

    geometry = locate[0]['geometry']
    lat_long = list(geometry.values())
    lat = lat_long[0]
    long = lat_long[1]
    # appends 1 reading for every hour in the day
    for i in range(96):
#             results['Latitude [deg]'].append(lat)
#             results['Longitude [deg]'].append(long)
            df['Latitude [deg]'] = lat
            df['Longitude [deg]'] = long
    lat = str(lat)
    long = str(long)
    return df, lat, long

def temp_converter(temp, f_to_c=True):
    '''
    helper function
    converts an integer or float to degrees Celsius
    or vice verse
    '''
    if f_to_c:
         new_temp = (temp - 32) * 5/9
    else:
         new_temp = (temp * 5/9) + 32
    return new_temp

def get_temp_log_daylight(df, lat, long, dark, time):

    darkSky = requests.get(f"https://api.darksky.net/forecast/{DarkSkyKey}/{lat},{long},{dark}T{time}?exclude=flags,alerts,currently")

    darkSky_call = darkSky.json()
   
    #     darkSky_call['hourly']['data'][0][] = 24 temp readings on the hour every hour and front fill
    for i in range(24):
        temp = (temp_converter(float(darkSky_call['hourly']['data'][i]['temperature'])))
        df['Temp [deg C]'].iloc[lambda x: x.index == i*4] = temp
    df['Temp [deg C]'].ffill(inplace = True)
    
    # using hourly temp data to fill every 15 minute interval
    datetime = darkSky_call['hourly']['data'][0]['time']
    df['Time Index'].iloc[0] = datetime
    for i in range(1,96):
        df['Time Index'].iloc[i] = df['Time Index'].iloc[i-1] + 900

    
    # sunrise and sunset times will be helpful in handling solar data
    
    sunrise = (darkSky_call['daily']['data'][0]['sunriseTime'] -  darkSky_call['hourly']['data'][0]['time'])
    sunrise = convert_minutes(sunrise, forward=False)
    sunset = (darkSky_call['daily']['data'][0]['sunsetTime'] -  darkSky_call['hourly']['data'][0]['time'])
    sunset = convert_minutes(sunset, forward=False)
    
    return sunrise, sunset, df

def get_solar_data(df, lat, long, date):
#     data will key off times in 00:00:00 format
        # init web browser
    os.environ.get('')
    chromedriver_path = os.path.join(os.getcwd(), 'app\static', 'chromedriver.exe')
    # print(chromedriver_path)
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
    
        #  SPA Calculator
    SPA_calc = 'https://midcdmz.nrel.gov/solpos/spa.html'

    start_date_picker = '//*[@id="syr"]' #value = 2005
    end_date_picker = '//*[@id="eyr"]'
    
    start_month_drop = '//*[@id="smo"]' #select / option value =" "
#     example_jan = '//*[@id="smo"]/option[1]' # equal to january
    end_month_drop = '//*[@id="emo"]'
    
    start_day_drop = '//*[@id="sdy"]'
    end_day_drop = '//*[@id="edy"]'
    
    interval = '//*[@id="int"]' #set to '15'
    
    lat_box = '//*[@id="lat"]'
    long_box = '//*[@id="lon"]'
    
    zenith_box = '//*[@id="o0"]' #make sure is True
    azimuth_box = '//*[@id="o1"]' #make sure is true
    
    submit = '//*[@id="content"]/div/div/center/form/table/tbody/tr[5]/td/table/tbody/tr/td[3]/input[1]'
    reset = '//*[@id="content"]/div/div/center/form/table/tbody/tr[5]/td/table/tbody/tr/td[3]/input[2]'
    
    # navigate to calculator
    go_to_calc = (f'{SPA_calc}')
    driver.get(go_to_calc)
    
    # fill form
    driver.find_element_by_xpath(f"{start_date_picker}").clear()
    driver.find_element_by_xpath(f"{start_date_picker}").send_keys(f'{str(date[2])}')
    driver.find_element_by_xpath(f"{end_date_picker}").clear()
    driver.find_element_by_xpath(f"{end_date_picker}").send_keys(f'{str(date[2])}')
    
    driver.find_element_by_xpath(f"{start_month_drop}/option[{int(date[1])}]").click()    
    driver.find_element_by_xpath(f"{end_month_drop}/option[{int(date[1])}]").click()

    driver.find_element_by_xpath(f"{start_day_drop}/option[{int(date[1])}]").click()
    driver.find_element_by_xpath(f"{end_day_drop}/option[{int(date[1])}]").click()
    
    driver.find_element_by_xpath(f"{lat_box}").clear()
    driver.find_element_by_xpath(f"{lat_box}").send_keys(f'{lat}')
    driver.find_element_by_xpath(f"{long_box}").clear()
    driver.find_element_by_xpath(f"{long_box}").send_keys(f'{long}')
    
    driver.find_element_by_xpath(f"{zenith_box}").click()
    driver.find_element_by_xpath(f"{azimuth_box}").click()
    
    driver.find_element_by_xpath(f'{submit}').click()
#     returns a blob of txt with comma seperation and break seperation between rows
    
    body = driver.find_element_by_xpath('/html/body/pre').text
    body2 = body.split('\n')
    body_string = ''
    for i in body2:
        body_string += str(i) + ','
    body3 = body_string.split(',')
    body_list = body3[4:] # remove header
    zenith = []
    azimuth = []
    count = 0
    while count < 96:
        for idx, info in enumerate(body_list):
            if idx == 2:
                zenith.append(float(info))
            elif idx == 3:
                azimuth.append(float(info))
            else:
                pass
        body_list = body_list[4:-1]
        count += 1
    df['Zenith Angle [degrees]'] = zenith
    df['Azimuth Angle [degrees]'] = azimuth
    print(df)
    return df


# # Post processing

def cleaning(df, sunrise, sunset):
    results = df.copy()
    sunrise_minutes = (convert_minutes(sunrise, forward=True, seconds=True) // 15) * 15
    sunset_minutes = (convert_minutes(sunset, forward=True, seconds=True) // 15) * 15
    results.loc[0:sunrise_minutes+15, ['Zenith Angle [degrees]', 'Azimuth Angle [degrees]', 'Latitude [deg]',
       'Longitude [deg]', 'Temp [deg C]']] = 0 # because we chose to back fill the solar data we have one na reading after sunsrise = 
    results.loc[sunset_minutes:1425, ['Zenith Angle [degrees]', 'Azimuth Angle [degrees]', 'Latitude [deg]',
       'Longitude [deg]', 'Temp [deg C]']] = 0
    return results

def reindexing(df, timezone=6):
    results = df.copy()
    results['Time Index'] = pd.to_datetime(results['Time Index'], unit='s')
    # time is six hours ahead because of timezone +6 GMT
    results['Time Index'] = results['Time Index'] - pd.Timedelta(hours = timezone) 
    results = results.set_index(pd.DatetimeIndex(results['Time Index']), append=False, drop=True)
#     results = results.reset_index(level=0)
    results['Feature Minutes'] = get_final_minutes()
#     results.drop(['index', 'Minutes'], axis = 1, inplace = True)

    return results


# # Looping wrapper Function

def loop_data_collect(time_span, location, target_date = None):
    '''
    initializes data collection and handles all args/kwargs for collections
    '''
  
    output = pd.DataFrame()

    
    for i in range(time_span):
        if target_date:
            time_list = get_time(target_date)
        else:
            time_list = get_time()

        sol, dark, time = convert_time(time_list)

        results = clear_cache()
        results = get_minutes(results)
        results, lat, long = get_coordinates(location, results)
        sunrise, sunset, results = get_temp_log_daylight(results, lat, long, dark, time)
        results = get_solar_data(results, lat, long, time_list)
        
#         clean data
        results['Day'] = i+1
        results.set_index('Minutes', inplace=True)
        cleaning_results = cleaning(results, sunrise, sunset)
        cleaned_results = reindexing(cleaning_results) #currently toggling for minutes/dt object index
#         reset for next iteration
        target_date = get_next_day(dark)
        output = output.append(cleaning_results, ignore_index=False)
        cleaning_results = None
        cleaned_results = None
        print('♥‿♥')
    return output, sunrise, sunset

#pass and send error in case of a future date
#if date flash a message to the /results template that warns the user of lowered accuracy for future dates

#  # Check Data vs Models stored in Static folder

def process(final_data, days, sunrise, sunset):
    '''
    runs the returned data on the trained model.
    each day returns a list of W/m^2 outputs which are then used to get some relavent information for the user:
    daily totals.
    '''
    cols = final_data.columns.to_list()
    feature_cols = cols[:5] + cols[-1:]
    BASE_PATH = os.path.dirname(__file__)
    model = os.path.join(BASE_PATH, 'static', 'day_model.pkl')
    scaler = os.path.join(BASE_PATH, 'static', 'day_scaler.pkl')
    print("DanishModel :", model)
#     model = os.path.join(os.getcwd(), 'static', 'day_model.pkl')
#     scaler = os.path.join(os.getcwd(), 'static', 'day_scaler.pkl')
    loaded_day_model = pickle.load(open(model, 'rb'))
    loaded_day_scaler = pickle.load(open(scaler, 'rb'))

    sunrise_minutes = (convert_minutes(sunrise, forward=True, seconds=True) // 15)
    sunset_minutes = (convert_minutes(sunset, forward=True, seconds=True) // 15)
       
    day_dict = {}
    for day in range(1,days+1):
        day_dict[day] = final_data[final_data.Day == day]
        feats = day_dict[day].loc[:,feature_cols]
        features = loaded_day_scaler.transform(feats)
        output = loaded_day_model.predict(features)
    #     because the government site the zenith angle was scraped from does not distingush between degrees above the horizon (+)
    #     and degrees below the horizon (-) there is a chance that some night time data will return a small positive number
    #     what follows is a few manipulations to make sure night time data is silenced
        output[:sunrise_minutes] = 0
        output[sunset_minutes:] = 0
        output = output.clip(min=0)
        day_dict[day]['Output'] = output
    
    return day_dict

# # Visualize Results

def plot(data_dict, days):
    
    '''
    takes a feature array and plots it against the time index and 
    time_span = days.unique
    converts minutes in integer form into into a clock reading for ease of translation
    splits data into an array of each features and days to be used in plot()
    '''
    images = {}
    y = [convert_minutes(time, forward=False, seconds=False) for time in dayz[1].index]
    for i in range(1,days+1):
        plt.figure(figsize=(20,10))
        plt.plot(y, final_data[i].Output, label='Photovoltaic Energy Produced', color='orange', fillstyle='bottom', animated=True)
        plt.xlabel('Time')
        plt.xticks(rotation=90)
        plt.ylabel('W/m^2')
        plt.legend(loc='upper left')
        plt.title(f'Day {i}')
        plt.show();
        images[i] = plt.savefig(f'plot{i}.png')
    return images



def daily_avg(results_series, sunrise, sunset):
    '''
    clips the model output array and gets a daily avg. caclulated in this way 
    because there could be zero results during mid day which should be counted
    '''
    'consistently found that the first 30 minutes after dawn do not produce light'
    sunrise_minutes = convert_minutes(sunrise, forward=True, seconds=True)
    sunset_minutes = convert_minutes(sunset, forward=True, seconds=True)

    results_array = np.array(results_series)
    pre_dawn = int(round(sunrise_minutes/15,0))
    after_dusk = int(round(sunset_minutes/15,0))
    for_avg = results_array[pre_dawn:after_dusk]
    avg = for_avg.mean()
    return avg
    





# # # # #

def run_sim(time_span, location, date):
    '''
    accepts user inputs and runs sim from data collection to processing data against model and finally plots data
    time_span = int, location = string address
    date = mm/dd/YYYY string
    '''
    output, sunrise, sunset = loop_data_collect(time_span, location, date)
    day_dict = process(output, time_span, sunrise, sunset)
    plot(day_dict, time_span, target_date)
    plot_features_day1(day_dict)
    mean_power = {}
    for day in range(time_span):
        mean_power[day] = daily_avg(day_dict[day+1].Output, sunrise, sunset)
        
    return mean_power
