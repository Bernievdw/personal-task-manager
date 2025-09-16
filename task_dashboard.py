import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="📋 Personal Task Manager", layout="wide")
st.title("📋 Personal Task Manager")

tasks = pd.read_csv("tasks.csv")
tasks['deadline'] = pd.to_datetime(tasks['deadline'])
today = datetime.today()

def get_status_color(row):
    if row['status'] == "Complete":
        return "green"
    elif row['deadline'] < today:
        return "red"
    else:
        return "orange"

tasks['status_color'] = tasks.apply(get_status_color, axis=1)

st.sidebar.header("Filters")
status_filter = st.sidebar.multiselect("Status", options=["Complete", "Incomplete"], default=["Complete", "Incomplete"])
priority_filter = st.sidebar.multiselect("Priority", options=["High", "Medium", "Low"], default=["High", "Medium", "Low"])
category_filter = st.sidebar.multiselect("Category", options=tasks['category'].unique(), default=tasks['category'].unique())

filtered_tasks = tasks[
    (tasks['status'].isin(status_filter)) &
    (tasks['priority'].isin(priority_filter)) &
    (tasks['category'].isin(category_filter))
]

st.write("### Task List")
for idx, row in filtered_tasks.iterrows():
    st.markdown(f"- {row['task']} | **Deadline:** {row['deadline'].date()} | **Priority:** {row['priority']} | **Category:** {row['category']} | <span style='color:{row['status_color']}'>{row['status']}</span>", unsafe_allow_html=True)

completed_percentage = (tasks['status']=="Complete").mean()*100
st.write("### Completion Progress")
st.progress(int(completed_percentage))

st.write("### Analytics")
st.bar_chart(tasks.groupby('category')['task'].count())
st.bar_chart(tasks.groupby('priority')['task'].count())
