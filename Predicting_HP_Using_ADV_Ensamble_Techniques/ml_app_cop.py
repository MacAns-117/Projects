from pickle import load
import pandas as pd
import numpy as np
import streamlit as st
from pycaret.regression import predict_model,load_model
 
model = load_model('blended_model')
 
def run():

    html_temp = """ 
    <div style ="background-color:tomato;padding:13px"> 
    <h1 style ="color:black;text-align:center;"> Streamlit Indian House Price Predictor ML App</h1> 
    </div> 
    """
     # display the front end aspect
    st.markdown(html_temp, unsafe_allow_html = True) 

    st.write('---')
    from PIL import Image
    image_house = Image.open('house_sale.jpg')
    st.image(image_house)

    st.write("""This app predicts the house prices all over **India**!""")
    st.write('---')

    posted_by = st.selectbox('Select Property posted by:', ('Owner', 'Dealer', 'Builder'))
    rera = st.selectbox('Select Rera approved:', ('Yes','No'))
    bhk_no = st.selectbox('Select BHK number:', ('1', '2', '3', '4', '5'))

    pp_sqft = st.selectbox('Enter price per square feet:',(900,1000,1200,1500,2000))
    under_construction = st.selectbox('Select Ready to Move:', ('Yes', 'No'))
    resale = st.selectbox('Select Resale:', ('Yes', 'No'))
    city = st.selectbox('Select City:', ('Agra', 'Ahmednagar', 'Ajmer', 'Aligarh','Bahadurgarh', 'Bangalore', 'Belgaum', 'Chandigarh', 'Chandrapur', 'Chennai', 'Coimbatore', 'Dehradun', 'Dharuhera'
     'Gandhinagar', 'Ghaziabad', 'Gurgaon', 'Gwalior', 'Hyderabad' , 'Indore', 'Jaipur', 'Kota','Lucknow',
    'Ludhiana', 'Mumbai', 'Mysore', 'Noida',
    'Pune','Visakhapatnam', 'Vizianagaram'))
    
    output = ""

    # Pre-processing user input    
    if posted_by == "Builder":
        posted_by = 0
    elif posted_by == "Dealer":
        posted_by = 1
    else:
        posted_by = 2

    if rera == "yes":
        rera = 1
    else:
        rera = 0


    if under_construction == "yes":
        under_construction = 1
    else:
        under_construction = 0

    if resale == "yes":
        resale = 1
    else:
        resale = 0

    if city == "Agra":
        city = 0
    elif city == "Ahmednagar":
        city = 1  
    elif city == "Ajmer":
        city = 2
    elif city == "Aligarh":
        city = 3
    elif city == "Allahabad":
        city = 4  
    elif city == "Alwar":
        city = 5
    elif city == "Amravati":
        city = 6 
    elif city == "Anand":
        city = 7   
    elif city == "Aurangabad":
        city = 8
    elif city == "Bahadurgarh":
        city = 9   
    elif city == "Bangalore":
        city = 10  
    elif city == "Belgaum":
        city = 11
    elif city == "Bharuch":
        city = 12 
    elif city == "Bhavnagar":
        city = 13 
    elif city == "Bhilai":
        city = 14 
    elif city == "Bhiwadi":
        city = 15 
    elif city == "Bhopal":
        city = 16 
    elif city == "Bilaspur":
        city = 17 
    elif city == "Chandigarh":
        city = 18 
    elif city == "Chandrapur":
        city = 19 
    elif city == "Chennai":
        city = 20 
    elif city == "Coimbatore":
        city = 21 
    elif city == "Dehradun":
        city = 22 
    elif city == "Dharuhera":
        city = 23 
    elif city == "Ernakulam":
        city = 24 
    elif city == "Faridabad":
        city = 25 
    elif city == "Gandhinagar":
        city = 26 
    elif city == "Ghaziabad":
        city = 27 
    elif city == "Goa":
        city = 28 
    elif city == "Guntur":
        city = 29 
    elif city == "Gurgaon":
        city = 30 
    elif city == "Gwalior":
        city = 31 
    elif city == "Haridwar":
        city = 32 
    elif city == "Hubli":
        city = 33 
    elif city == "Indore":
        city = 34 
    elif city == "Jabalpur":
        city = 35 
    elif city == "Jaipur":
        city = 36 
    elif city == "Jalandhar":
        city = 37 
    elif city == "Jalgaon":
        city = 38 
    elif city == "Jamnagar":
        city = 39 
    elif city == "Jodhpur":
        city = 40 
    elif city == "Junagadh":
        city = 41 
    elif city == "Kakinada":
        city = 42 
    elif city == "Kanchipuram":
        city = 43 
    elif city == "Kannur":
        city = 44 
    elif city == "Kanpur":
        city = 45 
    elif city == "Karad":
        city = 46 
    elif city == "Karjat":
        city = 47 
    elif city == "Kochi":
        city = 48 
    elif city == "Kolhapur":
        city = 49 
    elif city == "Kota":
        city = 50 
    elif city == "Kottayam":
        city = 51 
    elif city == "Lalitpur":
        city = 52 
    elif city == "Lucknow":
        city = 53
    elif city == "Ludhiana":
        city = 54
    elif city == "Madurai":
        city = 55
    elif city == "Maharashtra":
        city = 56
    elif city == "Mangalore":
        city = 57
    elif city == "Margao":
        city = 58
    elif city == "Mathura":
        city = 59
    elif city == "Meerut":
        city = 60
    elif city == "Mohali":
        city = 61
    elif city == "Mumbai":
        city = 62
    elif city == "Mysore":
        city = 63
    elif city == "Nagpur":
        city = 64
    elif city == "Navsari":
        city = 65
    elif city == "Neemrana":
        city = 66
    elif city == "Nellore":
        city = 67
    elif city == "Noida":
        city = 68
    elif city == "Other":
        city = 69
    elif city == "Palakkad":
        city = 70
    elif city == "Palghar":
        city = 71
    elif city == "Panaji":
        city = 72
    elif city == "Panchkula":
        city = 73
    elif city == "Pondicherry":
        city = 74
    elif city == "Pune":
        city = 75
    elif city == "Raigad":
        city = 76
    elif city == "Raipur":
        city = 77
    elif city == "Rajkot":
        city = 78
    elif city == "Ratnagiri":
        city = 79
    elif city == "Rudrapur":
        city = 80
    elif city == "Secunderabad":
        city = 81
    elif city == "Shimla":
        city = 82
    elif city == "Siliguri":
        city = 83
    elif city == "Sindhudurg":
        city = 84
    elif city == "Solan":
        city = 85
    elif city == "Solapur":
        city = 86
    elif city == "Sonipat":
        city = 87
    elif city == "Surat":
        city = 88
    elif city == "Thrissur":
        city = 89
    elif city == "Tirupati":
        city = 90
    elif city == "Udaipur":
        city = 91
    elif city == "Udupi":
        city = 92
    elif city == "Vadodara":
        city = 93
    elif city == "Valsad":
        city = 94
    elif city == "Vapi":
        city = 95
    elif city == "Varanasi":
        city = 96
    elif city == "Vijayawada":
        city = 97
    elif city == "Visakhapatnam":
        city = 98
    elif city == "Vizianagaram":
        city = 99
    elif city == "Wardha":
        city = 100
    else:
        city = 69

    # Input Dict
    input_dict = {'posted_by': posted_by, 'rera': rera, 'bhk_no': bhk_no, 'pp_sqft': pp_sqft, 'under_construction': under_construction,'resale':resale,'city':city}
    input_df = pd.DataFrame([input_dict])

    # Predict
    if st.button('Predict'):
        output = predict_model(model, data = input_df)
        output = str(np.round(np.exp(output['Label'][0])*1e5,2)) 

    # Display
    st.success('The house price is \u20B9 {}'.format(output))

if __name__ == '__main__':
    run()