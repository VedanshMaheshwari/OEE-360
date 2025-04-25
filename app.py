import streamlit as st
import os
import plotly.express as px
from utils import load_data, filter_data, calculate_oee, parse_query_with_gemini

# ------------ STREAMLIT CONFIG -------------
st.set_page_config(page_title="OEE-360 – OEE Chat Assistant", layout="wide")

# ------------ SIDEBAR -------------
with st.sidebar:
    st.title("📁 Data & Filters")
    uploaded_file = st.file_uploader("Upload IoT Excel Data", type=["xlsx"])

    st.markdown("---")
    st.markdown("💡 **Try These:**")
    st.markdown("- *OEE for PKG-005 in Mumbai in January 2025*")
    st.markdown("- *How did PKG-015 perform in Hyderabad last July?*")

# ------------ DATA LOADING -------------
data = None
if uploaded_file:
    data = load_data(uploaded_file)
    st.sidebar.success("✅ Data loaded!")
else:
    default_path = "data/oee_data.xlsx"
    if os.path.exists(default_path):
        data = load_data(default_path)
        st.sidebar.info("Using default synthetic data.")
    else:
        st.warning("⚠️ Upload data to begin.")
        st.stop()

# ------------ TITLE & DESCRIPTION -------------
st.markdown("""
    <style>
    .chat-bubble {
        background-color: #f0f2f6;
        border-radius: 1rem;
        padding: 1rem;
        margin: 1rem 0;
        font-size: 1rem;
    }
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #eee;
        padding: 1rem;
        border-radius: 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

st.title("💬 Welcome to OEE-360: Your OEE Chat Assistant")
st.markdown("Chat with your IoT data to explore packaging device efficiency (OEE).")

# ------------ CHAT SECTION -------------
query = st.chat_input("Ask something like: OEE for PKG-010 in Delhi for March 2025")

if query:
    st.markdown(f"<div class='chat-bubble'><strong>You:</strong> {query}</div>", unsafe_allow_html=True)

    # 1. Parse the query using our utility function
    parsed = parse_query_with_gemini(query)

    # 2. Show debugging information in a collapsible section
    with st.expander("🛠️ Debug Information", expanded=False):
        st.write("Parsing result:", parsed)
        if data is not None:
            st.write("Original columns:", data.columns.tolist())
            st.write("Data sample:", data.head(2))

    # Show the final parsed filters
    st.markdown(f"<div class='chat-bubble'><strong>Bot:</strong> Here's what I found:<br>"
                f"🔧 Device: <b>{parsed.get('device_id', 'Any')}</b><br>"
                f"📍 Location: <b>{parsed.get('location', 'Any')}</b><br>"
                f"📅 Month: <b>{parsed.get('month', 'All Time')}</b></div>", unsafe_allow_html=True)

    try:
        if data is None:
            st.error("No data available for analysis.")
        else:
            # Display sample of the data for debugging
            with st.expander("📊 Data Preview", expanded=False):
                st.write(data.head())
            
            # Filter the data
            filtered_data = filter_data(data, parsed.get("device_id"), parsed.get("location"), parsed.get("month"))
            
            if filtered_data.empty:
                st.warning("No data matches your query filters.")
            else:
                # Calculate OEE
                result = calculate_oee(filtered_data)
                
                if result:
                    st.markdown("<div class='chat-bubble'><strong>Bot:</strong> Here's your OEE breakdown 👇</div>", unsafe_allow_html=True)
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("📈 OEE (%)", result['OEE'])
                    with col2:
                        st.metric("⏱️ Availability", result['Availability'])
                    with col3:
                        st.metric("⚙️ Performance", result['Performance'])
                    with col4:
                        st.metric("🧪 Quality", result['Quality'])

                    # Add a bar chart
                    st.markdown("### 📊 KPI Breakdown")
                    chart_df = {
                        "Metric": ["OEE", "Availability", "Performance", "Quality"],
                        "Value": [result['OEE'], result['Availability'], result['Performance'], result['Quality']]
                    }
                    fig = px.bar(chart_df, x="Metric", y="Value", color="Metric", text="Value", range_y=[0, 100])
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Unable to calculate OEE with the available data.")
    except Exception as e:
        st.error(f"Error processing your query: {str(e)}")
        import traceback
        st.expander("Error Details", expanded=False).code(traceback.format_exc())