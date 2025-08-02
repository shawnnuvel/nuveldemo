# streamlit_synthetic_demo.py
import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Technical Talent Intelligence | Demo",
    page_icon="🎯",
    layout="wide"
)

@st.cache_data
def load_synthetic_data():
    """Load the synthetic demo dataset"""
    try:
        df = pd.read_csv('synthetic_demo_data.csv')
        return df
    except FileNotFoundError:
        st.error("❌ Demo data file not found. Please run synthetic_demo_creator.py first.")
        return None

def main():
    st.title("🎯 Technical Talent Intelligence Platform")
    st.markdown("*Investment-grade technical team intelligence demonstrated on synthetic companies*")
    
    # Load data
    df = load_synthetic_data()
    if df is None:
        return
    
    # Demo notice
    st.info("🔍 **Synthetic Demo Data**: This demonstration uses synthetic companies with realistic technical team patterns. Our full platform analyzes 1,000+ real companies with verified metrics.")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Demo Companies", len(df))
    with col2:
        st.metric("Total Engineers", f"{df['engineer_count'].sum():,}")
    with col3:
        st.metric("Avg Engineering %", f"{df['engineering_percentage'].mean():.1f}%")
    with col4:
        st.metric("Sectors", df['sector'].nunique())
    
    # Sidebar filters
    st.sidebar.title("🔍 Investment Filters")
    
    # Company size filter
    size_min, size_max = st.sidebar.slider(
        "Company Size",
        min_value=int(df['total_employees'].min()),
        max_value=int(df['total_employees'].max()),
        value=(10, 100)
    )
    
    # Engineering percentage filter
    eng_min, eng_max = st.sidebar.slider(
        "Engineering Team %",
        min_value=int(df['engineering_percentage'].min()),
        max_value=int(df['engineering_percentage'].max()),
        value=(40, 80)
    )
    
    # Sector filter
    selected_sectors = st.sidebar.multiselect(
        "Sectors",
        options=sorted(df['sector'].unique()),
        default=sorted(df['sector'].unique())
    )
    
    # Funding stage filter
    selected_stages = st.sidebar.multiselect(
        "Funding Stages",
        options=df['funding_stage'].unique(),
        default=df['funding_stage'].unique()
    )
    
    # Apply filters
    filtered_df = df[
        (df['total_employees'] >= size_min) &
        (df['total_employees'] <= size_max) &
        (df['engineering_percentage'] >= eng_min) &
        (df['engineering_percentage'] <= eng_max) &
        (df['sector'].isin(selected_sectors)) &
        (df['funding_stage'].isin(selected_stages))
    ]
    
    # Results
    st.header(f"🎯 Investment Targets: {len(filtered_df)} Companies")
    
    if len(filtered_df) > 0:
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Avg Engineering %", f"{filtered_df['engineering_percentage'].mean():.1f}%")
        with col2:
            st.metric("Avg Company Size", f"{filtered_df['total_employees'].mean():.0f}")
        with col3:
            st.metric("Total Engineers", f"{filtered_df['engineer_count'].sum():,}")
        
        # Visualization
        fig = px.scatter(
            filtered_df,
            x='total_employees',
            y='engineering_percentage',
            size='tech_strength_score',
            color='sector',
            hover_data=['company_name'],
            title="Technical Team Analysis - Synthetic Companies",
            labels={'total_employees': 'Total Employees', 'engineering_percentage': 'Engineering %'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Company table
        display_cols = ['company_name', 'sector', 'total_employees', 'engineer_count', 
                       'engineering_percentage', 'funding_stage', 'tech_strength_score']
        results_df = filtered_df[display_cols].sort_values('tech_strength_score', ascending=False)
        
        st.dataframe(results_df, use_container_width=True)
        
        # Company analysis
        st.subheader("🔍 Company Deep-Dive")
        
        selected_company = st.selectbox(
            "Select company for analysis:",
            options=filtered_df['company_name'].tolist()
        )
        
        if selected_company:
            company = filtered_df[filtered_df['company_name'] == selected_company].iloc[0]
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Employees", int(company['total_employees']))
            with col2:
                st.metric("Engineers", int(company['engineer_count']))
            with col3:
                st.metric("Engineering %", f"{company['engineering_percentage']:.1f}%")
            with col4:
                st.metric("Tech Score", f"{company['tech_strength_score']:.0f}/100")
            
            # Investment insights
            if company['total_employees'] <= 50:
                st.success("✅ **VC Profile**: Ideal for Series A/B investment")
            else:
                st.info("ℹ️ **Growth Stage**: Suitable for later-stage investment")
    
    # Call to action
    st.markdown("---")
    st.header("🚀 Ready for Real Data?")
    st.markdown("""
    This synthetic demonstration shows our analytical methodology. 
    Our full platform includes:
    
    ✅ **1,000+ real companies** with verified employee counts  
    ✅ **Household tech names** you actually want to track  
    ✅ **Historical hiring trends** and growth patterns  
    ✅ **API access** for integration with deal flow systems  
    ✅ **Custom sector analysis** for your investment thesis  
    """)
    
    if st.button("📅 Request Full Platform Demo", type="primary", use_container_width=True):
        st.success("🎉 Demo request submitted! We'll show you real company intelligence within 24 hours.")

if __name__ == "__main__":
    main()

