import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from helper import *

data = pd.read_csv("all_data.csv")

data.sort_values(by="order_approved_at", inplace=True)
data.reset_index(inplace=True)

data['order_approved_at'] = pd.to_datetime(data['order_approved_at'])

min_date = data["order_approved_at"].min()
max_date = data["order_approved_at"].max()


with st.sidebar:
    time_filter_option = st.selectbox(
        'Pilih Rentang Waktu:',
        options=['Pilih Rentang Waktu', 'All time']
    )

    if time_filter_option == 'Pilih Rentang Waktu':
        start_date, end_date = st.date_input(
            'Rentang Waktu',
            min_value=min_date,
            max_value=max_date,
            value=(min_date, max_date)
        )
    else:
        start_date, end_date = min_date, max_date

main_df = data[(data["order_approved_at"] >= str(start_date)) & 
                (data["order_approved_at"] <= str(end_date))]


st.header('Tiktopedia Ecommerce Dashboard :sparkles:')

daily_orders_df = create_daily_orders_df(main_df)
bystate_df = create_bystate_df(main_df)
sum_order_items_df = create_sum_order_items_df(main_df)


st.subheader("Customer Demographics")
 
col1, col2 = st.columns(2)
 
fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#90CAF9"]
sns.barplot(
    x="customer_count", 
    y="customer_state",
    data=bystate_df.sort_values(by="customer_count", ascending=False),
    palette=colors,
    ax=ax
)
ax.set_title("Number of Customer by States", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)


st.subheader('Total Orders')
 
col1, col2 = st.columns(2)
 
with col1:
    total_orders = daily_orders_df.order_count.sum()
    st.metric("Total orders", value=total_orders)
 
with col2:
    total_revenue = format_currency(daily_orders_df.revenue.sum(), "BRL", locale='es_CO') 
    st.metric("Total Revenue", value=total_revenue)
 
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_orders_df["order_approved_at"],
    daily_orders_df["order_count"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)


st.subheader("Best & Worst Performing Product")
 
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
 
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
sns.barplot(x="order_count", y="product_category", data=sum_order_items_df.sort_values(by="order_count", ascending=False).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales", fontsize=30)
ax[0].set_title("Best Performing Product", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)
 
sns.barplot(x="order_count", y="product_category", data=sum_order_items_df.sort_values(by="order_count", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Product", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)
 
st.pyplot(fig)
