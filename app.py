import streamlit as st
import pandas as pd
import pickle


region_map = {
    "West":1,
    "South":2,
    "North":3,
    "East":4
}

Soil_map = {
    "Sandy":1,
    "Clay":2,
    "Loam":3,
    "Silt":4,
    "Peaty":5,
    "Chalky":6
}
Crop_map = {
    'Cotton':1,
    'Rice':2,
    'Barley':3,
    'Soybean':4,
    'Wheat':5,
    'Maize':6
}
Whether_map = {
    'Cloudy':1,
    'Rainy':2,
    'Sunny':3
}
with open("Model.pkl", 'rb') as f:
    Model = pickle.load(f)


st.title("Farmer's Helping Bot")

Region = st.selectbox("Select Your Region:", ['East', 'West', 'North','South'])
Soil_Type = st.selectbox("Select Your Soil Type:", ['Sandy', 'Clay', 'Loam', 'Silt', 'Peaty', 'Chalky'])
Crop = st.selectbox("Select Your Crop:", ['Cotton', 'Rice', 'Barley', 'Soybean', 'Wheat', 'Maize'])
Rain_Fall = st.number_input("Enter the rain fall(in mm) in your fields")
Temperature_Celsius = st.number_input("Enter your fields temperature(in celsius)")
Fertilizer_Used = st.selectbox("Select Whether You Used Fertilizer(1 for Yes 0 for No):", [1,0])
Irrigation_Used = st.selectbox("Select Whether You Used Irrigation(1 for Yes 0 for No):", [1,0])
Whether_Condition = st.selectbox("Select Your Whether Condition:", ['Cloudy', 'Rainy', 'Sunny'])
Days_To_Harvest = st.number_input("Enter the days remaining to harvest")

Region = region_map[Region]
Soil_Type = Soil_map[Soil_Type]
Crop = Crop_map[Crop]
Whether_Condition = Whether_map[Whether_Condition]

inputData = pd.DataFrame([[Region, Soil_Type, Crop, Rain_Fall, Temperature_Celsius, Fertilizer_Used, Irrigation_Used, Whether_Condition, Days_To_Harvest]])

Submit = st.button("Predict Yield")

if Submit:
    Predictd_Yield = Model.predict(inputData)
    st.write(f"Predicted Yield: {Predictd_Yield[0]:.2f} tons per hectare")
    import streamlit as st

    with open("metrics.pkl", "rb") as f:
        metrics = pickle.load(f)

    st.write(f"MSE: {metrics['MSE']:.2f}")
    st.write(f"MAE: {metrics['MAE']:.2f}")
    st.write(f"R2 Score: {metrics['R2']:.2f}")



# Recommendation Part
# Some natural factors like rain_fall, temp, whether etc can't be controlled by a farmer so, we recommend the following things
# to the farmer Fertilizer, Irrigation, Crop selection

recommendation = st.button("CHECK RECOMMENDATIONS")


if(recommendation):
    if Fertilizer_Used == 0:
        input_copy = pd.DataFrame([[Region, Soil_Type, Crop, Rain_Fall, Temperature_Celsius, 0, Irrigation_Used, Whether_Condition, Days_To_Harvest]])
        pred_without = Model.predict(input_copy)[0]
        
        input_copy[5] = 1  # Fertilizer_Used = 1
        pred_with = Model.predict(input_copy)[0]

        if pred_with > pred_without:
            st.write("Bhai Sahb tm Fertilizers use kro")

    if(Irrigation_Used == 0):
        Predictd_Yield1 = Model.predict(inputData)
        Irrigation_Used = 1
        inputData = pd.DataFrame([[Region, Soil_Type, Crop, Rain_Fall, Temperature_Celsius, Fertilizer_Used, Irrigation_Used, Whether_Condition, Days_To_Harvest]])
        Predictd_Yield2 = Model.predict(inputData)

        if(Predictd_Yield1 < Predictd_Yield2):
            st.write("Bhai Sahb tm Irrigation use kro")


    Crops = ['Cotton', 'Rice', 'Barley', 'Soybean', 'Wheat', 'Maize']

    Actual_Crop = Crop
    Yields = []
    for i in Crops:
        Crop_val = Crop_map[i]  # Convert to numeric for model
        inputData = pd.DataFrame([[Region, Soil_Type, Crop_val, Rain_Fall, Temperature_Celsius, Fertilizer_Used, Irrigation_Used, Whether_Condition, Days_To_Harvest]])
        pred = Model.predict(inputData)[0]  # scalar
        Yields.append((i, pred))


    max_tuple = max(Yields, key=lambda x: x[1])
    crop_max = max_tuple[0]
    max_yield = max_tuple[1]

    if(crop_max != Actual_Crop):
        st.write(f"Maximum possible yield with best crop: {max_yield:.2f} tons per hectare using {crop_max}")


