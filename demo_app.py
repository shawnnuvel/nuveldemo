# streamlit_with_patents.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Nuvel.ai Intelligence | Demo",
    page_icon="🎯",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .patent-highlight {
        background-color: #FEF3C7;
        padding: 1rem;
        border-radius: 8px;
        border-left: 6px solid #F59E0B;
        margin: 1rem 0;
    }
    .killer-feature {
        background-color: #ECFDF5;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 6px solid #10B981;
        margin: 1.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_enhanced_data():
    try:
        df = pd.read_csv('demo_with_patent_intelligence.csv')
        return df
    except FileNotFoundError:
        st.error("❌ Enhanced demo data not found. Run patent_integration.py first.")
        return None

def main():
    st.title("🎯 Nuvel.ai Intelligence Platform")
    st.markdown("*Investment-grade intelligence combining technical teams AND intellectual property*")
    
    # Killer feature highlight
    st.markdown("""
    <div class="killer-feature">
    <h3>🚀 Our Killer Feature: Patent + Talent Intelligence</h3>
    <p><strong>Unique in the market:</strong> We combine technical team analysis with patent portfolio intelligence. 
    See which companies have both strong engineering teams AND valuable IP portfolios.</p>
    </div>
    """, unsafe_allow_html=True)
    
    df = load_enhanced_data()
    if df is None:
        return
    
    # Enhanced metrics with patent data
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Demo Companies", len(df))
    with col2:
        st.metric("Total Engineers", f"{df['engineer_count'].sum():,}")
    with col3:
        st.metric("Total Patents", f"{df['patent_count'].sum():,}")
    with col4:
        st.metric("Avg Patents/Engineer", f"{df['patents_per_engineer'].mean():.2f}")
    with col5:
        st.metric("IP-Strong Companies", len(df[df['ip_strength_score'] >= 50]))
    
    # Patent data disclaimer
    st.markdown("""
    <div class="patent-highlight">
    <strong>📊 Patent Data:</strong> This demo simulates our patent intelligence methodology. 
    Our full platform analyzes <strong>658K+ patent-employment linkages</strong> across real companies.
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar filters (enhanced with patent filters)
    st.sidebar.title("🔍 Investment Filters")
    
    # Patent-specific filters
    st.sidebar.subheader("🏆 Patent Intelligence Filters")
    
    patent_min = st.sidebar.slider(
        "Minimum Patent Count",
        min_value=0,
        max_value=int(df['patent_count'].max()),
        value=0,
        help="Filter companies by patent portfolio size"
    )
    
    ip_score_min = st.sidebar.slider(
        "Minimum IP Strength Score",
        min_value=0,
        max_value=100,
        value=30,
        help="Filter by intellectual property strength"
    )
    
    # Original filters
    selected_sectors = st.sidebar.multiselect(
        "Technology Sectors",
        options=sorted(df['sector'].unique()),
        default=sorted(df['sector'].unique())
    )
    
    size_min, size_max = st.sidebar.slider(
        "Company Size",
        min_value=int(df['total_employees'].min()),
        max_value=int(df['total_employees'].max()),
        value=(10, 100)
    )
    
    # Apply filters
    filtered_df = df[
        (df['patent_count'] >= patent_min) &
        (df['ip_strength_score'] >= ip_score_min) &
        (df['sector'].isin(selected_sectors)) &
        (df['total_employees'] >= size_min) &
        (df['total_employees'] <= size_max)
    ]
    
    # Results section
    st.header(f"🎯 IP-Enhanced Investment Targets: {len(filtered_df)} Companies")
    
    if len(filtered_df) == 0:
        st.warning("No companies match your criteria. Try adjusting filters.")
        return
    
    # Enhanced summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Avg Investment Score", f"{filtered_df['investment_score'].mean():.1f}")
    with col2:
        st.metric("Avg Patents", f"{filtered_df['patent_count'].mean():.0f}")
    with col3:
        st.metric("Avg IP Strength", f"{filtered_df['ip_strength_score'].mean():.1f}")
    with col4:
        st.metric("Total IP Value", f"{filtered_df['patent_count'].sum():,} patents")
    
    # Patent vs Talent visualization
    st.subheader("📈 Patent Intelligence vs Technical Talent")
    
    fig = px.scatter(
        filtered_df,
        x='engineering_percentage',
        y='patent_count',
        size='investment_score',
        color='sector',
        hover_data=['company_name', 'ip_strength_score'],
        title="Engineering Team % vs Patent Count by Sector",
        labels={
            'engineering_percentage': 'Engineering Team %',
            'patent_count': 'Patent Count',
            'investment_score': 'Investment Score'
        }
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # IP Strength distribution
    st.subheader("🏆 IP Strength Distribution")
    
    fig2 = px.histogram(
        filtered_df,
        x='ip_strength_score',
        nbins=20,
        title="Distribution of IP Strength Scores",
        color='sector'
    )
    st.plotly_chart(fig2, use_container_width=True)
    
    # Enhanced company table
    st.subheader("🏢 Companies with Patent Intelligence")
    
    display_cols = ['company_name', 'sector', 'total_employees', 'engineer_count', 
                   'patent_count', 'patents_per_engineer', 'ip_strength_score', 'investment_score']
    
    results_df = filtered_df[display_cols].sort_values('investment_score', ascending=False)
    results_df.columns = ['Company', 'Sector', 'Employees', 'Engineers', 
                         'Patents', 'Patents/Eng', 'IP Score', 'Investment Score']
    
    st.dataframe(results_df, use_container_width=True)
    
    # Company deep-dive with patent analysis
    st.subheader("🔍 IP-Enhanced Company Analysis")
    
    selected_company = st.selectbox(
        "Select company for patent + talent analysis:",
        options=filtered_df['company_name'].tolist()
    )
    
    if selected_company:
        company = filtered_df[filtered_df['company_name'] == selected_company].iloc[0]
        
        st.markdown(f"### 📋 {selected_company} - Complete Intelligence Profile")
        
        # Enhanced metrics with patents
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Employees", int(company['total_employees']))
        with col2:
            st.metric("Engineers", int(company['engineer_count']))
        with col3:
            st.metric("Patents", int(company['patent_count']))
        with col4:
            st.metric("IP Strength", f"{company['ip_strength_score']:.0f}/100")
        with col5:
            st.metric("Investment Score", f"{company['investment_score']:.0f}/100")
        
        # Patent analysis
        st.markdown("#### 🏆 Patent Portfolio Analysis")
        
        if company['patent_count'] > 20:
            st.success(f"🔥 **Strong IP Portfolio**: {company['patent_count']} patents indicates significant R&D investment")
        elif company['patent_count'] > 5:
            st.info(f"⚡ **Growing IP Portfolio**: {company['patent_count']} patents shows innovation focus")
        else:
            st.warning(f"📊 **Limited IP Portfolio**: {company['patent_count']} patents may indicate early stage")
        
        if company['patents_per_engineer'] > 0.5:
            st.success(f"💎 **High Innovation Density**: {company['patents_per_engineer']:.2f} patents per engineer")
        
        st.info(f"**Primary Patent Focus**: {company['primary_patent_focus']}")
        
        # Investment recommendation
        st.markdown("#### 💰 Investment Recommendation")
        
        if company['investment_score'] >= 80:
            st.success("🚀 **STRONG BUY**: Excellent combination of technical talent and IP portfolio")
        elif company['investment_score'] >= 60:
            st.info("📈 **BUY**: Good balance of engineering team and patent assets")
        else:
            st.warning("📊 **HOLD**: Consider for strategic value or growth potential")
    
    # Call to action
    st.markdown("---")
    st.header("🚀 Ready for Full Patent + Talent Intelligence?")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Exclusive IP + Talent Intelligence Platform:
        
        ✅ **658K+ patent-employment linkages** analyzed  
        ✅ **300K+ companies** with verified technical teams AND patent portfolios  
        ✅ **Real patent data** including citations, classifications, and inventor networks  
        ✅ **Investment scoring** combining talent density with IP strength  
        ✅ **Competitive moats analysis** showing patent overlap between companies  
        ✅ **API access** for integration with your deal flow systems  
        
        **This combination is impossible for competitors to replicate.**
        """)
    
    with col2:
        st.markdown("""
        <div style='background-color: #F0FDF4; padding: 1.5rem; border-radius: 8px; text-align: center;'>
        <h4>🏆 Killer Feature Access</h4>
        <p>Email <a href='mailto:hello@nuvel.ai' style='color: #059669; font-weight: bold;'>hello@nuvel.ai</a> for exclusive patent + talent intelligence.</p>
        <p style='font-size: 0.9rem; color: #6B7280;'>See which companies have both strong engineering teams AND valuable IP portfolios.</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
