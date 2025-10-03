import streamlit as st
import pandas as pd
from supabase import create_client, Client
import os
import dotenv
dotenv.load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

st.title("🏎️ F1 Driver Breakdown")

table_name = "f1_drivers"
response = supabase.table(table_name).select("*").order("points", desc=True).limit(8).execute()

df = pd.DataFrame(response.data)
st.subheader("Top 8 Drivers (Points Table)")
st.dataframe(df)

st.subheader("🏆 Points by Driver")
st.bar_chart(df.set_index("name")["points"])

st.subheader("📉 Average Finish per Driver")
st.line_chart(df.set_index("name")["avg_finish"])

st.subheader("🥇 Wins vs Podiums")
st.scatter_chart(df.set_index("name")[["wins", "podiums"]])