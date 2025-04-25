from utils import load_data, filter_data, calculate_oee

df = load_data()
filtered = filter_data(df, device_id='PKG-010', location='Mumbai', month='March 2025')
result = calculate_oee(filtered)

print(result)
