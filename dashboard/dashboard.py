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


rfm_df = df.groupby('customer_id').agg({
    'order_purchase_timestamp': lambda x: (pd.Timestamp.now() - x.max()).days,  
    'order_id': 'count', 
    'price': 'sum'  
}).rename(columns={
    'order_purchase_timestamp': 'Recency',
    'order_id': 'Frequency',
    'price': 'Monetary'
})


st.sidebar.title("Filter Waktu")
min_date = df["order_purchase_timestamp"].min().date()
max_date = df["order_purchase_timestamp"].max().date()
start_date, end_date = st.sidebar.date_input("Rentang Waktu", min_value=min_date, max_value=max_date, value=(min_date, max_date))
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)


df_filtered = df[(df["order_purchase_timestamp"] >= start_date) & (df["order_purchase_timestamp"] <= end_date)]


st.header("Dashboard Analisis Pengiriman")


st.subheader("Waktu Pengiriman Rata-Rata Berdasarkan Status Pesanan")


average_delivery_time = df_filtered.groupby("order_status")["delivery_time"].mean().reset_index()
fig, ax = plt.subplots()
sns.barplot(data=average_delivery_time, x="order_status", y="delivery_time", ax=ax)
ax.set_xlabel("Status Pesanan")
ax.set_ylabel("Waktu Pengiriman Rata-Rata (hari)")
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
st.pyplot(fig)


st.header("Analisis Pola Waktu Pesanan")


fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(df_filtered['order_purchase_timestamp'], bins=30, color='pink', edgecolor='black')
ax.set_title('Distribusi Waktu Pembelian Pesanan')
ax.set_xlabel('Waktu')
ax.set_ylabel('Frekuensi')
st.pyplot(fig)


st.subheader("Analisis RFM")


fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(20, 10))
sns.barplot(y=rfm_df.sort_values(by="Recency").head(5).index, x="Recency", data=rfm_df.sort_values(by="Recency").head(5))
plt.title("Top 5 Customers by Recency", fontsize=50)
plt.ylabel("Customer ID", fontsize=50)
st.pyplot(fig)


fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(20, 10))
sns.barplot(y=rfm_df.sort_values(by="Frequency", ascending=False).head(5).index, x="Frequency", data=rfm_df.sort_values(by="Frequency", ascending=False).head(5))
plt.title("Top 5 Customers by Frequency", fontsize=50)
plt.ylabel("Customer ID", fontsize=50)
st.pyplot(fig)


fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(20, 10))
sns.barplot(y=rfm_df.sort_values(by="Monetary", ascending=False).head(5).index, x="Monetary", data=rfm_df.sort_values(by="Monetary", ascending=False).head(5))
plt.title("Top 5 Customers by Monetary", fontsize=50)
plt.ylabel("Customer ID", fontsize=50)
st.pyplot(fig)
