import streamlit as st
import pandas as pd
from supabase import create_client, Client
import os

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

st.title("🏎️ F1 Driver Breakdown")

table_name = "f1_drivers"
response = supabase.table(table_name).select("*").order("P", desc=True).limit(8).execute()

df = pd.DataFrame(response.data)
st.subheader("Top 8 Drivers (Points Table)")
st.dataframe(df)

st.subheader("🏆 Points by Driver")
st.bar_chart(df.set_index("Driver")["P"])

st.subheader("📉 Average Finish per Driver")
st.line_chart(df.set_index("Driver")["AF"])

st.subheader("🥇 Wins vs Podiums")
st.scatter_chart(df.set_index("Driver")[["W", "PD"]])