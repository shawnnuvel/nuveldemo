"""
Nuvel.ai Demo Platform - Technical & IP Diligence
Save as: app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import time
import random

# Page config
st.set_page_config(
    page_title="Nuvel.ai - Technical Intelligence Platform",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for premium look
st.markdown("""
<style>
    /* Premium color scheme */
    :root {
        --primary-color: #0A1628;
        --secondary-color: #00D9FF;
        --success-color: #10B981;
        --warning-color: #F59E0B;
        --danger-color: #F43F5E;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom styling */
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .big-font {
        font-size: 48px !important;
        font-weight: bold;
        color: #0A1628;
    }
    
    .highlight {
        background: linear-gradient(120deg, #00D9FF 0%, #0A1628 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        height: 100%;
    }
    
    .stealth-badge {
        background: #F43F5E;
        color: white;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 12px;
    }
</style>
""", unsafe_allow_html=True)

# Load synthetic data (would come from your data generator script)
@st.cache_data
def load_demo_data():
    # This would load from your generated JSON/CSV files
    try:
        return {
            'companies': pd.read_csv('synthetic_companies.csv'),
            'stealth': pd.read_csv('synthetic_stealth.csv'),
            'patents': pd.read_csv('synthetic_patents.csv'),
            'patterns': pd.read_csv('synthetic_patterns.csv')
        }
    except:
        # Return empty dataframes if files don't exist
        return {
            'companies': pd.DataFrame(),
            'stealth': pd.DataFrame(),
            'patents': pd.DataFrame(),
            'patterns': pd.DataFrame()
        }

# Initialize session state
if 'selected_company' not in st.session_state:
    st.session_state.selected_company = None
if 'analysis_run' not in st.session_state:
    st.session_state.analysis_run = False

# Header
st.markdown("""
<h1 style='text-align: center; color: #0A1628;'>
    🧬 Nuvel.ai Technical Intelligence Platform
</h1>
<p style='text-align: center; color: #666; font-size: 18px;'>
    Analyze technical DNA and patent intelligence across 319,000 companies
</p>
""", unsafe_allow_html=True)

# Stats bar
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Companies Analyzed", "319,247", "+12,384 this quarter")
with col2:
    st.metric("Patent Holders Tracked", "1.8M", "+47K new patents")
with col3:
    st.metric("Stealth Startups", "3,147", "+148 verified")
with col4:
    st.metric("Success Pattern Accuracy", "84.3%", "+2.1%")

st.divider()

# Main search interface
st.markdown("### 🔍 Analyze Any Company")
col1, col2 = st.columns([3, 1])

with col1:
    # Company search with autocomplete simulation
    company_search = st.text_input(
        "Enter company name or domain",
        placeholder="e.g., Stripe, Airbnb, or any Series A+ company",
        label_visibility="collapsed"
    )

with col2:
    analyze_button = st.button("🚀 Analyze", type="primary", use_container_width=True)

# Demo company quick select
st.markdown("**Quick Demo:** Select a company to see sample analysis")
demo_companies = ["Stripe", "Airbnb", "Plaid", "Coinbase", "TechStartup AI"]
selected_demo = st.radio(
    "demo_select",
    demo_companies,
    horizontal=True,
    label_visibility="collapsed"
)

if analyze_button or selected_demo:
    st.session_state.selected_company = company_search if analyze_button else selected_demo
    st.session_state.analysis_run = True

# Analysis Results Section
if st.session_state.analysis_run and st.session_state.selected_company:
    
    # Loading animation
    with st.spinner(f"Analyzing {st.session_state.selected_company} across 372M profiles..."):
        time.sleep(2)  # Simulate processing
    
    st.success(f"✅ Analysis complete for **{st.session_state.selected_company}**")
    
    # Company header info
    st.markdown(f"""
    <div style='background: white; padding: 20px; border-radius: 10px; margin: 20px 0;'>
        <h2>{st.session_state.selected_company}</h2>
        <p>Series B • B2B SaaS • San Francisco • 127 employees</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different analyses
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Technical Density", 
        "🧬 Pattern Matching", 
        "🔬 Patent Intelligence",
        "🕵️ Stealth Tracker",
        "📈 Investment Score"
    ])
    
    with tab1:
        st.markdown("### Technical Density Analysis")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Technical Density Score - Big visual
            score = random.randint(65, 92)
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = score,
                title = {'text': "Technical Density Score"},
                delta = {'reference': 41, 'relative': True},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "#00D9FF"},
                    'steps': [
                        {'range': [0, 40], 'color': "#F43F5E"},
                        {'range': [40, 70], 'color': "#F59E0B"},
                        {'range': [70, 100], 'color': "#10B981"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
            
            # Key metrics
            st.metric("Engineers", f"{score}%", f"+{score-41}% vs industry")
            st.metric("Eng:Sales Ratio", "4.2:1", "Optimal range")
            st.metric("Technical Leadership", "8/10", "Strong")
        
        with col2:
            # Talent DNA Breakdown
            st.markdown("#### Talent DNA Composition")
            
            dna_data = pd.DataFrame({
                'Source': ['FAANG', 'Other Unicorns', 'Failed Startups', 'Academia', 'Traditional'],
                'Percentage': [34, 23, 18, 15, 10]
            })
            
            fig = px.pie(dna_data, values='Percentage', names='Source', 
                        color_discrete_sequence=['#00D9FF', '#0A1628', '#10B981', '#F59E0B', '#F43F5E'])
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
            
            # Historical hiring chart
            st.markdown("#### Engineering Hiring Velocity")
            
            dates = pd.date_range(start='2022-01-01', end='2024-01-01', freq='Q')
            eng_growth = pd.DataFrame({
                'Date': dates,
                'Engineers': [20, 25, 32, 41, 52, 67, 78, 89, 102]
            })
            
            fig = px.line(eng_growth, x='Date', y='Engineers', 
                         line_shape='spline', markers=True)
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### Pattern Matching Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Best Pattern Match")
            st.info(f"""
            **🎯 "Early Stripe DNA" Pattern** (87% match)
            
            **Why this pattern:**
            - ✅ High technical density (73% vs 41% average)
            - ✅ API-first engineering indicators
            - ✅ Talent from fintech/payments companies
            - ✅ Patent holders in core technology
            
            **Historical Success Rate:** 73% reach $1B+ valuation
            """)
            
            # Similar successful companies
            st.markdown("#### Similar Successful Companies")
            similar_companies = pd.DataFrame({
                'Company': ['Stripe', 'Plaid', 'Square', 'Adyen', 'Braintree'],
                'Match %': [87, 82, 78, 75, 71],
                'Exit Value': ['$95B', '$13.4B', '$85B', '$46B', '$4.3B']
            })
            st.dataframe(similar_companies, hide_index=True, use_container_width=True)
        
        with col2:
            st.markdown("#### Pattern Distribution")
            
            patterns = pd.DataFrame({
                'Pattern': ['Early Stripe DNA', 'Uber Ops-Heavy', 'Airbnb Balanced', 
                           'Facebook Social', 'Enterprise B2B', 'Deep Tech R&D'],
                'Success Rate': [73, 67, 71, 58, 64, 81],
                'Companies': [234, 567, 412, 891, 1243, 187]
            })
            
            fig = px.scatter(patterns, x='Companies', y='Success Rate', 
                           size='Companies', text='Pattern',
                           color='Success Rate',
                           color_continuous_scale='viridis')
            fig.update_traces(textposition='top center')
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("### 🔬 Patent Intelligence")
        
        # Check if premium
        if st.checkbox("🔓 Unlock Premium Patent Intelligence"):
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Patent Holders", "7", "+3 this year")
                st.metric("Patents Filed", "12", "2 pending")
                st.metric("Patent Density", "0.094", "3x industry avg")
            
            with col2:
                st.markdown("#### Patent Domains")
                patent_domains = pd.DataFrame({
                    'Domain': ['Machine Learning', 'Distributed Systems', 
                              'Security', 'Data Processing'],
                    'Count': [5, 3, 2, 2]
                })
                fig = px.bar(patent_domains, x='Count', y='Domain', 
                           orientation='h', color='Count')
                st.plotly_chart(fig, use_container_width=True)
            
            with col3:
                st.markdown("#### Key Patent Holders")
                st.success("""
                **Dr. Sarah Chen** - Senior ML Engineer
                - 3 ML patents (2 cited by Google)
                - Ex-DeepMind
                
                **John Park** - Principal Engineer  
                - 2 distributed systems patents
                - Ex-Amazon AWS
                
                **Maria Rodriguez** - Staff Engineer
                - 2 security patents
                - Ex-Apple Security
                """)
            
            # Acqui-hire value
            st.warning(f"""
            **💰 IP-Based Acquisition Value Indicator**
            
            Based on patent portfolio and holder market rates:
            - Patent portfolio value: $2.4M - $3.8M
            - Key person risk: 2 patent holders with <1 year tenure
            - Acquisition attractiveness: HIGH (multiple citations from FAANG)
            """)
        else:
            st.info("🔒 Patent Intelligence is available in Professional and Enterprise plans")
    
    with tab4:
        st.markdown("### 🕵️ Stealth Startup Tracker")
        
        if st.checkbox("🔓 Access Stealth Intelligence (Enterprise Only)"):
            
            st.warning("🔥 **Exclusive Intelligence**: 3,147 FAANG engineers currently in stealth")
            
            # Stealth metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Stealth", "3,147", "+148 this quarter")
            with col2:
                st.metric("From Google", "1,247", "39.6%")
            with col3:
                st.metric("Senior+", "1,893", "60.1%")
            with col4:
                st.metric("Since Launched", "743", "23.6%")
            
            # Sample stealth profiles
            st.markdown("#### Recent Stealth Transitions (Sample)")
            
            stealth_data = pd.DataFrame({
                'Profile': ['Ex-Google ML Principal', 'Ex-Meta Staff Eng', 
                           'Ex-Apple Senior iOS', 'Ex-Amazon Principal', 'Ex-Netflix Senior BE'],
                'Previous Role': ['Principal @ Google Brain', 'Staff @ Meta Reality Labs',
                                'Senior @ Apple Maps', 'Principal @ AWS', 'Senior @ Netflix Core'],
                'Transition': ['Nov 2024', 'Oct 2024', 'Sep 2024', 'Sep 2024', 'Aug 2024'],
                'Location': ['SF Bay Area', 'Seattle', 'SF Bay Area', 'NYC', 'LA'],
                'Status': ['Stealth', 'Stealth', 'Launched', 'Stealth', 'Raised Seed']
            })
            
            # Add LinkedIn tracking buttons
            for idx, row in stealth_data.iterrows():
                col1, col2, col3, col4, col5 = st.columns([2, 2, 1, 1, 1])
                with col1:
                    st.text(row['Profile'])
                with col2:
                    st.text(row['Previous Role'])
                with col3:
                    st.text(row['Transition'])
                with col4:
                    if row['Status'] == 'Stealth':
                        st.markdown(f"<span class='stealth-badge'>{row['Status']}</span>", 
                                  unsafe_allow_html=True)
                    else:
                        st.success(row['Status'])
                with col5:
                    st.button("Track", key=f"track_{idx}")
            
            # Geographic distribution
            st.markdown("#### Geographic Distribution of Stealth Activity")
            
            geo_data = pd.DataFrame({
                'Location': ['SF Bay Area', 'Seattle', 'NYC', 'Austin', 'Boston', 'LA'],
                'Count': [1284, 567, 432, 287, 234, 343]
            })
            
            fig = px.bar(geo_data, x='Location', y='Count', 
                        color='Count', color_continuous_scale='blues')
            st.plotly_chart(fig, use_container_width=True)
        
        else:
            st.info("🔒 Stealth Tracker available in Enterprise plan only - 3,147 profiles tracked")
    
    with tab5:
        st.markdown("### 📈 Investment Intelligence Summary")
        
        # Investment score calculation (not actual investment advice)
        tech_score = random.randint(65, 92)
        pattern_score = random.randint(70, 95)
        patent_score = random.randint(60, 85)
        overall = int((tech_score + pattern_score + patent_score) / 3)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Overall intelligence score
            st.markdown("#### Intelligence Metrics")
            st.metric("Technical Density", f"{tech_score}/100", "Strong")
            st.metric("Pattern Match", f"{pattern_score}/100", "Very Strong")
            st.metric("Innovation Capability", f"{patent_score}/100", "Above Average")
            st.metric("Overall Intelligence", f"{overall}/100", "HIGH POTENTIAL")
            
            if overall > 80:
                st.success("✅ Strong technical indicators across all metrics")
            elif overall > 60:
                st.warning("⚠️ Mixed signals - deeper diligence recommended")
            else:
                st.error("❌ Below typical success thresholds")
        
        with col2:
            st.markdown("#### Key Insights & Risks")
            
            st.success("""
            **✅ Positive Signals**
            - Technical density in top 5% of B2B SaaS
            - Hiring velocity increasing quarter-over-quarter
            - Strong patent portfolio for company stage
            - Pattern matches 3 successful exits
            """)
            
            st.warning("""
            **⚠️ Risk Factors**
            - No technical co-founder identified
            - Recent departure of 2 senior engineers
            - Lower than average senior:junior ratio
            """)
            
            st.info("""
            **📊 Comparable Exits**
            - Similar companies acquired for 8-12x revenue
            - Average time to exit: 5.3 years
            - Most common acquirers: Microsoft, Salesforce, Google
            """)
        
        # Download report button
        st.divider()
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.button("📥 Download Full Report (PDF)", type="primary", use_container_width=True)

# Footer with credibility
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>This is a demo of Nuvel.ai's Technical Intelligence Platform</p>
    <p><strong>Real platform includes:</strong> 319K+ companies • 372M profiles • 1.8M patents • 3K+ stealth startups</p>
    <p>📧 Contact: hello@nuvel.ai</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for additional controls (hidden by default)
with st.sidebar:
    st.markdown("### Demo Controls")
    st.info("This is a demo environment with synthetic data")
    if st.button("Reset Demo"):
        st.session_state.clear()
        st.rerun()
