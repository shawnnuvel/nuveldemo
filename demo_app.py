# streamlit_credible_demo_updated.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Technical Talent Intelligence | Credible Demo",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E40AF;
        text-align: center;
        margin-bottom: 1rem;
    }
    .value-prop {
        font-size: 1.2rem;
        color: #374151;
        text-align: center;
        margin-bottom: 2rem;
    }
    .data-scale {
        background-color: #EBF8FF;
        padding: 1rem;
        border-radius: 8px;
        border-left: 6px solid #3B82F6;
        margin-bottom: 1.5rem;
        font-weight: 500;
    }
    .disclaimer {
        background-color: #FEF3C7;
        padding: 1rem;
        border-radius: 8px;
        border-left: 6px solid #F59E0B;
        margin-bottom: 1.5rem;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('credible_demo.csv')
        return df
    except FileNotFoundError:
        st.error("❌ Credible demo data file not found. Please run the data preparation script.")
        return None

def main():
    st.markdown('<h1 class="main-header">🎯 Technical Talent Intelligence Platform</h1>', unsafe_allow_html=True)
    st.markdown('<p class="value-prop">Investment-grade technical talent intelligence demonstrated on anonymous companies</p>', unsafe_allow_html=True)

    # Updated messaging highlighting true data scale
    st.markdown("""
    <div class="data-scale">
    <strong>📊 Platform Scale:</strong> Our platform analyzes <strong>over 300,000 companies</strong> from <strong>1.3+ million employment records</strong> 
    with 41M+ total data points. This demo shows a small anonymized sample demonstrating our analytical methodology.
    </div>
    """, unsafe_allow_html=True)

    # Disclaimer about estimated funding stages
    st.markdown("""
    <div class="disclaimer">
    <strong>⚠️ Demo Disclaimer:</strong> Funding stages shown are <em>estimated based on company size</em> for demonstration purposes only. 
    Company names are anonymized to maintain data confidentiality. The full platform includes verified metrics for household-name companies.
    </div>
    """, unsafe_allow_html=True)

    df = load_data()
    if df is None:
        return

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Demo Companies", 
            f"{len(df):,}",
            help="Sample from 300,000+ company database"
        )
    
    with col2:
        st.metric(
            "Technical Roles Mapped",
            f"{df['engineer_count'].sum():,}",
            help="Engineering roles classified using our algorithms"
        )
        
    with col3:
        st.metric(
            "Avg Engineering Density", 
            f"{df['engineering_percentage'].mean():.1f}%",
            help="Average technical team concentration"
        )
        
    with col4:
        st.metric(
            "Sectors Covered",
            f"{df['sector'].nunique()}",
            help="Technology sectors in demo dataset"
        )

    # Sidebar filters
    st.sidebar.title("🔍 Investment Filters")
    
    # Sector filter
    sectors = sorted(df['sector'].unique())
    selected_sectors = st.sidebar.multiselect(
        "Technology Sectors",
        options=sectors,
        default=sectors,
        help="Filter companies by technology sector"
    )
    
    # Company size filter
    size_min, size_max = st.sidebar.slider(
        "Company Size (Employees)",
        min_value=int(df['total_employees'].min()),
        max_value=int(df['total_employees'].max()),
        value=(10, 100),
        help="Filter by company size for investment stage targeting"
    )
    
    # Engineering percentage filter
    eng_min, eng_max = st.sidebar.slider(
        "Engineering Team Density (%)",
        min_value=int(df['engineering_percentage'].min()),
        max_value=int(df['engineering_percentage'].max()),
        value=(40, 85),
        help="Filter by technical team concentration"
    )
    
    # Funding stage filter with clear disclaimer
    if 'funding_stage' in df.columns:
        funding_stages = sorted(df['funding_stage'].unique())
        selected_stages = st.sidebar.multiselect(
            "Funding Stage (Estimated)",
            options=funding_stages,
            default=funding_stages,
            help="⚠️ Estimated from company size - not verified data"
        )
    else:
        selected_stages = []

    # Apply filters
    filtered_df = df[
        (df['sector'].isin(selected_sectors)) &
        (df['total_employees'] >= size_min) &
        (df['total_employees'] <= size_max) &
        (df['engineering_percentage'] >= eng_min) &
        (df['engineering_percentage'] <= eng_max)
    ]
    
    if selected_stages and 'funding_stage' in df.columns:
        filtered_df = filtered_df[filtered_df['funding_stage'].isin(selected_stages)]

    # Results section
    st.header(f"🎯 Investment Targets: {len(filtered_df)} Companies")
    
    if len(filtered_df) == 0:
        st.warning("No companies match your search criteria. Try adjusting the filters.")
        return

    # Summary metrics for filtered results
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Avg Engineering %", f"{filtered_df['engineering_percentage'].mean():.1f}%")
    with col2:
        st.metric("Avg Company Size", f"{filtered_df['total_employees'].mean():.0f}")
    with col3:
        st.metric("Total Engineers", f"{filtered_df['engineer_count'].sum():,}")

    # Visualization
    st.subheader("📈 Technical Talent Distribution")
    
    fig = px.scatter(
        filtered_df,
        x='total_employees',
        y='engineering_percentage',
        size='tech_strength_score',
        color='sector',
        hover_data=['company_name', 'engineer_count'],
        title="Company Size vs Engineering Density by Sector",
        labels={
            'total_employees': 'Total Employees',
            'engineering_percentage': 'Engineering Team %',
            'sector': 'Sector'
        },
        height=500
    )
    
    fig.update_layout(
        xaxis_title="Total Employees",
        yaxis_title="Engineering Team %",
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)

    # Company results table
    st.subheader("🏢 Company Results")
    
    # Prepare display columns
    display_columns = ['company_name', 'sector', 'total_employees', 'engineer_count', 'engineering_percentage', 'tech_strength_score']
    if 'funding_stage' in filtered_df.columns:
        display_columns.append('funding_stage')
    if 'region' in filtered_df.columns:
        display_columns.append('region')
    
    # Rename columns for display
    display_df = filtered_df[display_columns].copy()
    column_names = ['Company', 'Sector', 'Employees', 'Engineers', 'Eng %', 'Tech Score']
    if 'funding_stage' in filtered_df.columns:
        column_names.append('Funding Stage*')
    if 'region' in filtered_df.columns:
        column_names.append('Region')
    
    display_df.columns = column_names
    
    # Sort by tech strength score
    display_df = display_df.sort_values('Tech Score', ascending=False)
    
    st.dataframe(display_df, use_container_width=True, height=400)
    
    if 'Funding Stage*' in display_df.columns:
        st.caption("*Funding stages are estimated based on company size")

    # Company deep-dive section
    st.subheader("🔍 Company Intelligence Deep-Dive")
    
    selected_company = st.selectbox(
        "Select company for detailed analysis:",
        options=filtered_df['company_name'].tolist(),
        help="Choose a company to see detailed technical intelligence"
    )
    
    if selected_company:
        company_data = filtered_df[filtered_df['company_name'] == selected_company].iloc[0]
        
        st.markdown("---")
        
        # Company profile
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"### 📋 {selected_company}")
            
            # Metrics row
            metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
            
            with metric_col1:
                st.metric("Total Employees", f"{int(company_data['total_employees'])}")
            with metric_col2:
                st.metric("Engineers", f"{int(company_data['engineer_count'])}")
            with metric_col3:
                st.metric("Engineering %", f"{company_data['engineering_percentage']:.1f}%")
            with metric_col4:
                st.metric("Tech Score", f"{company_data['tech_strength_score']:.0f}/100")
        
        with col2:
            # Company details
            st.info(f"**Sector:** {company_data['sector']}")
            if 'funding_stage' in company_data:
                st.info(f"**Funding Stage:** {company_data['funding_stage']} (estimated)")
            if 'region' in company_data:
                st.info(f"**Region:** {company_data['region']}")
        
        # Investment suitability analysis
        st.markdown("#### 💰 Investment Analysis")
        
        if company_data['total_employees'] <= 50:
            st.success("✅ **VC Investment Profile**: Suitable for Series A/B investment")
        elif company_data['total_employees'] <= 150:
            st.info("ℹ️ **PE Acquisition Profile**: Suitable for growth capital or buyout")
        else:
            st.warning("⚠️ **Large Company**: May require partnership approach")
        
        # Technical team insights
        if company_data['engineering_percentage'] >= 60:
            st.success(f"🔥 **High Technical Density**: {company_data['engineering_percentage']:.1f}% engineering team indicates strong execution capability")
        elif company_data['engineering_percentage'] >= 40:
            st.info(f"⚡ **Balanced Technical Team**: {company_data['engineering_percentage']:.1f}% engineering concentration suggests solid technical foundation")

    # Call to action
    st.markdown("---")
    st.header("🚀 Ready for Full Platform Access?")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### What you get with the full platform:
        
        ✅ **300,000+ companies** with verified employment data  
        ✅ **1.3M+ employment records** with comprehensive analysis  
        ✅ **Real company names** including household tech brands  
        ✅ **Advanced search** with 20+ filters and custom criteria  
        ✅ **API access** for integration with your deal flow systems  
        ✅ **Custom reports** for specific sectors and investment theses  
        
        **This demo represents <5% of our total analytical capability.**
        """)
    
    with col2:
        st.markdown("### 📧 Contact for Demo")
        
        st.markdown("""
        <div style='background-color: #F0F9FF; padding: 1.5rem; border-radius: 8px; text-align: center;'>
        <h4>Ready to see the full platform?</h4>
        <p>Email us at <a href='mailto:hello@nuvel.ai' style='color: #2563EB; font-weight: bold;'>hello@nuvel.ai</a> to schedule your personalized demo.</p>
        <p style='font-size: 0.9rem; color: #6B7280;'>See verified data for 300,000+ companies with real-time technical intelligence.</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
