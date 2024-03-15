def create_daily_orders_df(df):

    daily_orders_df = df.resample(rule='D', on='order_approved_at').agg({
        "order_id": "nunique",
        "payment_value": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "order_id": "order_count",
        "payment_value": "revenue"
    }, inplace=True)
    
    return daily_orders_df

def create_sum_order_items_df(df):
    sum_order_items_df = df['product_category_name_english'].value_counts().reset_index()
    sum_order_items_df.columns = ['product_category', 'order_count']
    return sum_order_items_df

def create_bystate_df(df):
    bycity_df = df.groupby(by="customer_state").customer_id.nunique().reset_index()
    bycity_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)
    
    return bycity_df