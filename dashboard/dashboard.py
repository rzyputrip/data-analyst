import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv("all_data.csv")


date_columns = ["order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date"]
for column in date_columns:
    df[column] = pd.to_datetime(df[column])


df["delivery_time"] = (df["order_delivered_customer_date"] - df["order_purchase_timestamp"]).dt.days


df["is_late"] = df["delivery_time"] > (df["order_estimated_delivery_date"] - df["order_purchase_timestamp"]).dt.days


st.sidebar.title("Filter Waktu")
min_date = df["order_purchase_timestamp"].min().to_pydatetime().date()
max_date = df["order_purchase_timestamp"].max().to_pydatetime().date()
start_date, end_date = st.sidebar.date_input("Rentang Waktu", min_value=min_date, max_value=max_date, value=(min_date, max_date))


start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)


df_filtered = df[(df["order_purchase_timestamp"] >= start_date) & (df["order_purchase_timestamp"] <= end_date)]


average_delivery_time = df_filtered.groupby("order_status")["delivery_time"].mean().reset_index()


late_orders_by_seller = df_filtered[df_filtered["is_late"]].groupby("seller_id")["order_id"].count().reset_index()


st.title("Analisis Pengiriman")


st.subheader("Waktu Pengiriman Rata-Rata Berdasarkan Status Pesanan")
fig, ax = plt.subplots()
sns.barplot(data=average_delivery_time, x="order_status", y="delivery_time", ax=ax)
ax.set_xlabel("Status Pesanan")
ax.set_ylabel("Waktu Pengiriman Rata-Rata (hari)")
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
st.pyplot(fig)

