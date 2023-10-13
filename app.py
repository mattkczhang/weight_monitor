import numpy as np
import pandas as pd
from datetime import date
import streamlit as st

# load data

records = pd.read_csv('weight_record.csv')
# records.drop(records.index, inplace=True)
# records.to_csv('weight_record.csv', index=False)

# preparation

def findDayofWeek(date):
    dow = date.today().weekday()
    if dow == 0:
        return 'Monday'
    elif dow == 1:
        return 'Tuesday'
    elif dow == 2:
        return 'Wednesday'
    elif dow == 3:
        return 'Thursday'
    elif dow == 4:
        return 'Friday'
    elif dow == 5:
        return 'Saturday'
    elif dow == 6:
        return 'Sunday'
    
def disable():
    st.session_state.button_disable = True

todayDate = date.today()
todayDoW = findDayofWeek(todayDate)

if 'button_disable' not in st.session_state:
    st.session_state.button_disable = False

# app

st.title('Weight Monitor')

st.balloons()

col1, col2 = st.columns(2)

# with st.form("daily_weight"):
st.header("Happy "+todayDoW)
enteredDate = str(st.date_input("Today's Date", date.today()))
enteredName = st.selectbox(
    'username',
    ('Matt', 'Winnie'))
enteredWeight = st.number_input("Today's weight in kg")
if records.date.str.contains(enteredDate).any() and records[records.date==enteredDate].name.str.contains(enteredName).any():
    st.session_state.button_disable=True
else:
    st.session_state.button_disable=False

submit = st.button(
        "Submit!", on_click=disable, disabled=st.session_state.button_disable
)

if submit:
    records = pd.concat([records, pd.DataFrame([[enteredDate,enteredName,enteredWeight]], columns=records.columns)], ignore_index=True)
    records.to_csv('weight_record.csv', index=False)
    st.experimental_rerun()

    
tab1, tab2 = st.tabs(["📈 Trend", "🗃 Data"])

tab1.line_chart(data=records, x='date', y='weight', color='name')

tab2.write(records)
    
