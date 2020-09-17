#Thanakrit Apichayanuntakul 6030809021
"""An example of showing geographic data."""

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk



#set credit ,title and markdown
st.text("Credit : Thanakrit Apichayanuntakul 6030809021")

st.title("Uber Pickups in New York City")
st.markdown(
"""
This is a demo of a Streamlit app that shows the Uber pickups
geographical distribution in New York City. Use the slider
to pick a specific hour and look at how the charts change.
[See source code](https://github.com/streamlit/demo-uber-nyc-pickups/blob/master/app.py)
""")

#นำเข้าข้อมุลเป็น dataframe
##เนื่องจากข้อมูลที่ใช้มีหลายไฟล์จึงทำการนำเข้าทีละไฟล์ด้วยloops และรวมเป็นdataframe เดียว
DATE_TIME = "timestart"
@st.cache(persist=True)
def load_data(nb):
    data2 = []
    for i in range(nb):
        ll = pd.read_csv('https://github.com/bank750/geodatasciencee/raw/master/2019010%i.csv' %(i+1) ,parse_dates=['timestart','timestop'])
        data2.append(ll)
        data2[i] = data2[i].filter(regex='^(l|t)',axis=1)
    data = pd.concat(data2,keys = ['day1','day2','day3','day4','day5'])
    return data

data = load_data(5)

#latstartl	lonstartl	timestart
##streamlit.slider(label, min_value=None, max_value=None, value=None, step=None, format=None, key=None)

#จัดการเเสดงผลลัพธืในหน้าเว็บ
##ใช้steamlit จัดการหน้าเว็บ
hour = st.slider("Hour to look at", 0, 23,value=None, step=3)
#hour = st.slider("Hour to look at",0,23,[0,3])

data = data[data[DATE_TIME].dt.hour == hour ]
#df.query('1<=date<3')
#df[(data[DATE_TIME].dt.hour > hour)&(data[DATE_TIME].dt.hour <= hour+3)]

st.subheader("Geo data between %i:00 to %i:00" % (hour, (hour + 3) % 24))
midpoint = (np.average(data["latstartl"]), np.average(data["lonstartl"]))

##ใช้ pydeck แสดงผลข้อมูลรายชั่วโมง ในรูปเเผนที่สามมิติและกราฟเเท่ง3มิติ 
st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state={
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom": 11,
        "pitch": 50,
    },
    layers=[
        pdk.Layer(
            "HexagonLayer",
            data=data,
            get_position=["lonstartl", "latstartl"],
            radius=100,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
        ),
    ],
))

st.subheader("Breakdown by minute between %i:00 and %i:00" % (hour, (hour + 1) % 24))
filtered = data[
    (data[DATE_TIME].dt.hour >= hour) & (data[DATE_TIME].dt.hour < (hour + 1))
]
hist = np.histogram(filtered[DATE_TIME].dt.minute, bins=60, range=(0, 60))[0]
chart_data = pd.DataFrame({"minute": range(60), "pickups": hist})

##ใช้ altair เเสดงผลข้อมูลรายนาที
st.altair_chart(alt.Chart(chart_data)
    .mark_area(
        interpolate='step-after',
    ).encode(
        x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
        y=alt.Y("pickups:Q"),
        tooltip=['minute', 'pickups']
    ), use_container_width=True)

##ใช้streamlit สร้างcheckbox เพื่อเป็นทางเลือกในการขอดูdataframe
if st.checkbox("Show raw data", False):
    st.subheader("Raw data by minute between %i:00 and %i:00" % (hour, (hour + 1) % 24))
    st.write(data)
