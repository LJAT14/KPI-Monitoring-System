import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="KPI Monitoring System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        font-weight: 600;
        text-align: center;
        margin-bottom: 3rem;
        color: #1a1a1a;
        border-bottom: 2px solid #e0e0e0;
        padding-bottom: 1rem;
    }
    
    .kpi-card {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: transform 0.2s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    .alert-critical {
        border-left: 5px solid #dc3545;
        background: linear-gradient(135deg, #fff5f5 0%, #ffe6e6 100%);
        animation: pulse-alert 2s infinite;
    }
    
    .alert-warning {
        border-left: 5px solid #ffc107;
        background: linear-gradient(135deg, #fffbf0 0%, #fff3cd 100%);
    }
    
    .alert-normal {
        border-left: 5px solid #28a745;
        background: linear-gradient(135deg, #f8fff8 0%, #d4edda 100%);
    }
    
    @keyframes pulse-alert {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    .section-header {
        font-size: 1.6rem;
        font-weight: 500;
        color: #2c3e50;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #ecf0f1;
    }
    
    .metric-summary {
        background: #f8f9fa;
        border-radius: 6px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #007bff;
    }
    
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-critical { background-color: #dc3545; }
    .status-warning { background-color: #ffc107; }
    .status-normal { background-color: #28a745; }
</style>
""", unsafe_allow_html=True)

# Initialize session state for thresholds
if 'kpi_thresholds' not in st.session_state:
    st.session_state.kpi_thresholds = {
        'Revenue': {'target': 1000000.0, 'warning_low': 900000.0, 'critical_low': 800000.0},
        'Profit_Margin': {'target': 25.0, 'warning_low': 20.0, 'critical_low': 15.0},
        'Customer_Acquisition_Cost': {'target': 100.0, 'warning_high': 150.0, 'critical_high': 200.0},
        'Customer_Lifetime_Value': {'target': 2000.0, 'warning_low': 1600.0, 'critical_low': 1200.0},
        'Cash_Flow': {'target': 500000.0, 'warning_low': 300000.0, 'critical_low': 100000.0},
        'ROI': {'target': 20.0, 'warning_low': 15.0, 'critical_low': 10.0},
        'Market_Share': {'target': 15.0, 'warning_low': 12.0, 'critical_low': 10.0},
        'Customer_Satisfaction': {'target': 4.5, 'warning_low': 4.0, 'critical_low': 3.5}
    }

if 'alerts_log' not in st.session_state:
    st.session_state.alerts_log = []

# Generate comprehensive business KPI data
@st.cache_data
def generate_kpi_data():
    np.random.seed(42)
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    dates = pd.date_range(start_date, end_date, freq='D')
    
    data = []
    
    for i, date in enumerate(dates):
        day_of_year = date.timetuple().tm_yday
        seasonal_factor = 1 + 0.15 * np.sin(2 * np.pi * day_of_year / 365)
        growth_factor = 1 + (i / len(dates)) * 0.2
        weekend_factor = 0.7 if date.weekday() >= 5 else 1.0
        
        if date.month == 12 or date.month == 1:
            holiday_factor = 1.3
        elif date.month in [6, 7]:
            holiday_factor = 1.1
        else:
            holiday_factor = 1.0
        
        base_revenue = 850000
        revenue = base_revenue * seasonal_factor * growth_factor * weekend_factor * holiday_factor * np.random.normal(1, 0.1)
        revenue = max(500000, revenue)
        
        cost_ratio = np.random.uniform(0.6, 0.8)
        profit = revenue * (1 - cost_ratio)
        profit_margin = (profit / revenue) * 100
        
        customers_acquired = max(50, int(revenue / 15000 + np.random.normal(0, 20)))
        cac = revenue * 0.15 / customers_acquired if customers_acquired > 0 else 150
        clv = cac * np.random.uniform(12, 20)
        
        cash_flow = profit * np.random.uniform(0.6, 0.9)
        roi = (profit / (revenue * cost_ratio)) * 100
        market_share = np.random.uniform(12, 18)
        customer_satisfaction = np.random.uniform(3.8, 4.8)
        employee_productivity = np.random.uniform(85, 115)
        operational_efficiency = np.random.uniform(75, 95)
        
        data.append({
            'Date': date,
            'Revenue': round(revenue, 2),
            'Profit': round(profit, 2),
            'Profit_Margin': round(profit_margin, 2),
            'Customers_Acquired': customers_acquired,
            'Customer_Acquisition_Cost': round(cac, 2),
            'Customer_Lifetime_Value': round(clv, 2),
            'Cash_Flow': round(cash_flow, 2),
            'ROI': round(roi, 2),
            'Market_Share': round(market_share, 2),
            'Customer_Satisfaction': round(customer_satisfaction, 2),
            'Employee_Productivity': round(employee_productivity, 2),
            'Operational_Efficiency': round(operational_efficiency, 2),
            'Year': date.year,
            'Month': date.month,
            'Quarter': date.quarter,
            'Week': date.isocalendar()[1]
        })
    
    return pd.DataFrame(data)

# KPI status evaluation
def evaluate_kpi_status(value, kpi_name):
    thresholds = st.session_state.kpi_thresholds.get(kpi_name, {})
    
    if not thresholds:
        return 'normal', 'No thresholds defined'
    
    if 'critical_high' in thresholds:
        if value >= thresholds['critical_high']:
            return 'critical', f'Above critical threshold ({thresholds["critical_high"]})'
        elif value >= thresholds['warning_high']:
            return 'warning', f'Above warning threshold ({thresholds["warning_high"]})'
        else:
            return 'normal', f'Within target range'
    else:
        if value <= thresholds['critical_low']:
            return 'critical', f'Below critical threshold ({thresholds["critical_low"]})'
        elif value <= thresholds['warning_low']:
            return 'warning', f'Below warning threshold ({thresholds["warning_low"]})'
        else:
            return 'normal', f'Meeting or exceeding target'

# Load data
df = generate_kpi_data()

# Header
st.markdown('<h1 class="main-header">Business Intelligence KPI Monitoring System</h1>', unsafe_allow_html=True)

st.markdown("""
<div class="metric-summary">
    <p><strong>Executive Dashboard</strong> - Real-time monitoring of key performance indicators with automated alerting and threshold management. This system provides comprehensive business intelligence for strategic decision-making and operational excellence.</p>
    <p><em>Tracking 8 critical business metrics with historical trend analysis and predictive insights.</em></p>
</div>
""", unsafe_allow_html=True)

# Sidebar configuration
st.sidebar.header("Dashboard Configuration")

time_period = st.sidebar.selectbox(
    "Analysis Period",
    ["Last 7 Days", "Last 30 Days", "Last 90 Days", "Last 6 Months", "Last Year"]
)

today = df['Date'].max()
if time_period == "Last 7 Days":
    start_date = today - timedelta(days=7)
elif time_period == "Last 30 Days":
    start_date = today - timedelta(days=30)
elif time_period == "Last 90 Days":
    start_date = today - timedelta(days=90)
elif time_period == "Last 6 Months":
    start_date = today - timedelta(days=180)
else:
    start_date = today - timedelta(days=365)

df_filtered = df[df['Date'] >= start_date].copy()

auto_refresh = st.sidebar.checkbox("Auto Refresh (30s)", value=False)
if auto_refresh:
    time.sleep(1)
    st.rerun()

# Get latest data
latest_data = df_filtered.iloc[-1] if len(df_filtered) > 0 else df.iloc[-1]

# Check for active alerts
active_alerts = []
for kpi in ['Revenue', 'Profit_Margin', 'Customer_Acquisition_Cost', 'Customer_Lifetime_Value', 
            'Cash_Flow', 'ROI', 'Market_Share', 'Customer_Satisfaction']:
    if kpi in latest_data:
        status, message = evaluate_kpi_status(latest_data[kpi], kpi)
        if status != 'normal':
            active_alerts.append({
                'KPI': kpi,
                'Status': status,
                'Current_Value': latest_data[kpi],
                'Message': message
            })

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs(["Live Dashboard", "Alert Management", "Trend Analysis", "Performance Reports"])

with tab1:
    st.markdown('<div class="section-header">Real-time KPI Monitoring</div>', unsafe_allow_html=True)
    
    # Financial Metrics - Row 1
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        status, message = evaluate_kpi_status(latest_data['Revenue'], 'Revenue')
        status_class = f"alert-{status}" if status != 'normal' else "alert-normal"
        
        st.markdown(f"""
        <div class="kpi-card {status_class}">
            <h4><span class="status-indicator status-{status}"></span>Revenue</h4>
            <h2>${latest_data['Revenue']:,.0f}</h2>
            <p><strong>Target:</strong> ${st.session_state.kpi_thresholds['Revenue']['target']:,}</p>
            <small>{message}</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        status, message = evaluate_kpi_status(latest_data['Profit_Margin'], 'Profit_Margin')
        status_class = f"alert-{status}" if status != 'normal' else "alert-normal"
        
        st.markdown(f"""
        <div class="kpi-card {status_class}">
            <h4><span class="status-indicator status-{status}"></span>Profit Margin</h4>
            <h2>{latest_data['Profit_Margin']:.1f}%</h2>
            <p><strong>Target:</strong> {st.session_state.kpi_thresholds['Profit_Margin']['target']}%</p>
            <small>{message}</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        status, message = evaluate_kpi_status(latest_data['Customer_Acquisition_Cost'], 'Customer_Acquisition_Cost')
        status_class = f"alert-{status}" if status != 'normal' else "alert-normal"
        
        st.markdown(f"""
        <div class="kpi-card {status_class}">
            <h4><span class="status-indicator status-{status}"></span>Customer Acquisition Cost</h4>
            <h2>${latest_data['Customer_Acquisition_Cost']:.0f}</h2>
            <p><strong>Target:</strong> ${st.session_state.kpi_thresholds['Customer_Acquisition_Cost']['target']}</p>
            <small>{message}</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        status, message = evaluate_kpi_status(latest_data['Customer_Lifetime_Value'], 'Customer_Lifetime_Value')
        status_class = f"alert-{status}" if status != 'normal' else "alert-normal"
        
        st.markdown(f"""
        <div class="kpi-card {status_class}">
            <h4><span class="status-indicator status-{status}"></span>Customer Lifetime Value</h4>
            <h2>${latest_data['Customer_Lifetime_Value']:,.0f}</h2>
            <p><strong>Target:</strong> ${st.session_state.kpi_thresholds['Customer_Lifetime_Value']['target']:,}</p>
            <small>{message}</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Operational Metrics - Row 2
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        status, message = evaluate_kpi_status(latest_data['Cash_Flow'], 'Cash_Flow')
        status_class = f"alert-{status}" if status != 'normal' else "alert-normal"
        
        st.markdown(f"""
        <div class="kpi-card {status_class}">
            <h4><span class="status-indicator status-{status}"></span>Cash Flow</h4>
            <h2>${latest_data['Cash_Flow']:,.0f}</h2>
            <p><strong>Target:</strong> ${st.session_state.kpi_thresholds['Cash_Flow']['target']:,}</p>
            <small>{message}</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        status, message = evaluate_kpi_status(latest_data['ROI'], 'ROI')
        status_class = f"alert-{status}" if status != 'normal' else "alert-normal"
        
        st.markdown(f"""
        <div class="kpi-card {status_class}">
            <h4><span class="status-indicator status-{status}"></span>Return on Investment</h4>
            <h2>{latest_data['ROI']:.1f}%</h2>
            <p><strong>Target:</strong> {st.session_state.kpi_thresholds['ROI']['target']}%</p>
            <small>{message}</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        status, message = evaluate_kpi_status(latest_data['Market_Share'], 'Market_Share')
        status_class = f"alert-{status}" if status != 'normal' else "alert-normal"
        
        st.markdown(f"""
        <div class="kpi-card {status_class}">
            <h4><span class="status-indicator status-{status}"></span>Market Share</h4>
            <h2>{latest_data['Market_Share']:.1f}%</h2>
            <p><strong>Target:</strong> {st.session_state.kpi_thresholds['Market_Share']['target']}%</p>
            <small>{message}</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        status, message = evaluate_kpi_status(latest_data['Customer_Satisfaction'], 'Customer_Satisfaction')
        status_class = f"alert-{status}" if status != 'normal' else "alert-normal"
        
        st.markdown(f"""
        <div class="kpi-card {status_class}">
            <h4><span class="status-indicator status-{status}"></span>Customer Satisfaction</h4>
            <h2>{latest_data['Customer_Satisfaction']:.2f}/5.0</h2>
            <p><strong>Target:</strong> {st.session_state.kpi_thresholds['Customer_Satisfaction']['target']}/5.0</p>
            <small>{message}</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Trend Charts
    st.markdown('<div class="section-header">Trend Analysis</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_revenue = px.line(
            df_filtered.tail(30),
            x='Date',
            y='Revenue',
            title="Revenue Trend (Last 30 Days)",
            template="plotly_white"
        )
        
        fig_revenue.add_hline(
            y=st.session_state.kpi_thresholds['Revenue']['target'],
            line_dash="solid",
            line_color="green",
            annotation_text="Target"
        )
        fig_revenue.add_hline(
            y=st.session_state.kpi_thresholds['Revenue']['warning_low'],
            line_dash="dash",
            line_color="orange",
            annotation_text="Warning"
        )
        fig_revenue.add_hline(
            y=st.session_state.kpi_thresholds['Revenue']['critical_low'],
            line_dash="dash",
            line_color="red",
            annotation_text="Critical"
        )
        
        fig_revenue.update_traces(line_color='#2E8B57', line_width=3)
        fig_revenue.update_layout(height=400)
        st.plotly_chart(fig_revenue, use_container_width=True)
    
    with col2:
        fig_margin = px.line(
            df_filtered.tail(30),
            x='Date',
            y='Profit_Margin',
            title="Profit Margin Trend (Last 30 Days)",
            template="plotly_white"
        )
        
        fig_margin.add_hline(
            y=st.session_state.kpi_thresholds['Profit_Margin']['target'],
            line_dash="solid",
            line_color="green",
            annotation_text="Target"
        )
        fig_margin.add_hline(
            y=st.session_state.kpi_thresholds['Profit_Margin']['warning_low'],
            line_dash="dash",
            line_color="orange",
            annotation_text="Warning"
        )
        
        fig_margin.update_traces(line_color='#1f77b4', line_width=3)
        fig_margin.update_layout(height=400)
        st.plotly_chart(fig_margin, use_container_width=True)

with tab2:
    st.markdown('<div class="section-header">Alert Management & Threshold Configuration</div>', unsafe_allow_html=True)
    
    if active_alerts:
        st.markdown(f"""
        <div class="alert-critical" style="padding: 1rem; border-radius: 6px; margin: 1rem 0;">
            <h4>Active Alerts: {len(active_alerts)}</h4>
        </div>
        """, unsafe_allow_html=True)
        
        alerts_df = pd.DataFrame(active_alerts)
        st.dataframe(alerts_df, use_container_width=True, hide_index=True)
    else:
        st.markdown("""
        <div class="alert-normal" style="padding: 1rem; border-radius: 6px; margin: 1rem 0;">
            <h4>All KPIs Operating Within Normal Parameters</h4>
            <p>No active alerts at this time.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">Threshold Configuration</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Financial Metrics")
        
        st.markdown("**Revenue Thresholds**")
        rev_target = st.number_input("Target", value=float(st.session_state.kpi_thresholds['Revenue']['target']), step=10000.0, key="rev_target")
        rev_warning = st.number_input("Warning Low", value=float(st.session_state.kpi_thresholds['Revenue']['warning_low']), step=10000.0, key="rev_warning")
        rev_critical = st.number_input("Critical Low", value=float(st.session_state.kpi_thresholds['Revenue']['critical_low']), step=10000.0, key="rev_critical")
        
        st.markdown("**Profit Margin Thresholds (%)**")
        pm_target = st.number_input("Target", value=float(st.session_state.kpi_thresholds['Profit_Margin']['target']), step=1.0, key="pm_target")
        pm_warning = st.number_input("Warning Low", value=float(st.session_state.kpi_thresholds['Profit_Margin']['warning_low']), step=1.0, key="pm_warning")
        pm_critical = st.number_input("Critical Low", value=float(st.session_state.kpi_thresholds['Profit_Margin']['critical_low']), step=1.0, key="pm_critical")
    
    with col2:
        st.subheader("Customer Metrics")
        
        st.markdown("**Customer Acquisition Cost**")
        cac_target = st.number_input("Target", value=float(st.session_state.kpi_thresholds['Customer_Acquisition_Cost']['target']), step=10.0, key="cac_target")
        cac_warning = st.number_input("Warning High", value=float(st.session_state.kpi_thresholds['Customer_Acquisition_Cost']['warning_high']), step=10.0, key="cac_warning")
        cac_critical = st.number_input("Critical High", value=float(st.session_state.kpi_thresholds['Customer_Acquisition_Cost']['critical_high']), step=10.0, key="cac_critical")
        
        st.markdown("**Customer Satisfaction**")
        cs_target = st.number_input("Target", value=float(st.session_state.kpi_thresholds['Customer_Satisfaction']['target']), step=0.1, key="cs_target")
        cs_warning = st.number_input("Warning Low", value=float(st.session_state.kpi_thresholds['Customer_Satisfaction']['warning_low']), step=0.1, key="cs_warning")
        cs_critical = st.number_input("Critical Low", value=float(st.session_state.kpi_thresholds['Customer_Satisfaction']['critical_low']), step=0.1, key="cs_critical")
    
    if st.button("Update Thresholds", type="primary"):
        st.session_state.kpi_thresholds.update({
            'Revenue': {'target': float(rev_target), 'warning_low': float(rev_warning), 'critical_low': float(rev_critical)},
            'Profit_Margin': {'target': float(pm_target), 'warning_low': float(pm_warning), 'critical_low': float(pm_critical)},
            'Customer_Acquisition_Cost': {'target': float(cac_target), 'warning_high': float(cac_warning), 'critical_high': float(cac_critical)},
            'Customer_Satisfaction': {'target': float(cs_target), 'warning_low': float(cs_warning), 'critical_low': float(cs_critical)}
        })
        st.success("Thresholds updated successfully!")
        st.rerun()

with tab3:
    st.markdown('<div class="section-header">Advanced Trend Analysis</div>', unsafe_allow_html=True)
    
    selected_kpi = st.selectbox(
        "Select KPI for Analysis",
        ['Revenue', 'Profit_Margin', 'Customer_Acquisition_Cost', 'Customer_Lifetime_Value', 
         'Cash_Flow', 'ROI', 'Market_Share', 'Customer_Satisfaction']
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_trend = px.line(
            df_filtered,
            x='Date',
            y=selected_kpi,
            title=f"{selected_kpi} Historical Trend",
            template="plotly_white"
        )
        
        if selected_kpi in st.session_state.kpi_thresholds:
            thresholds = st.session_state.kpi_thresholds[selected_kpi]
            if 'target' in thresholds:
                fig_trend.add_hline(y=thresholds['target'], line_dash="solid", line_color="green", annotation_text="Target")
            if 'warning_low' in thresholds:
                fig_trend.add_hline(y=thresholds['warning_low'], line_dash="dash", line_color="orange", annotation_text="Warning")
            if 'critical_low' in thresholds:
                fig_trend.add_hline(y=thresholds['critical_low'], line_dash="dash", line_color="red", annotation_text="Critical")
        
        fig_trend.update_traces(line_width=3)
        fig_trend.update_layout(height=400)
        st.plotly_chart(fig_trend, use_container_width=True)
    
    with col2:
        fig_dist = px.histogram(
            df_filtered,
            x=selected_kpi,
            title=f"{selected_kpi} Distribution",
            template="plotly_white",
            nbins=30
        )
        fig_dist.update_layout(height=400)
        st.plotly_chart(fig_dist, use_container_width=True)
    
    # Statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-summary">
            <h4>Current Performance</h4>
            <p><strong>Current:</strong> {latest_data[selected_kpi]:.2f}</p>
            <p><strong>Average:</strong> {df_filtered[selected_kpi].mean():.2f}</p>
            <p><strong>Change:</strong> {((latest_data[selected_kpi] - df_filtered[selected_kpi].iloc[0]) / df_filtered[selected_kpi].iloc[0] * 100):.1f}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-summary">
            <h4>Statistics</h4>
            <p><strong>Mean:</strong> {df_filtered[selected_kpi].mean():.2f}</p>
            <p><strong>Median:</strong> {df_filtered[selected_kpi].median():.2f}</p>
            <p><strong>Std Dev:</strong> {df_filtered[selected_kpi].std():.2f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-summary">
            <h4>Range</h4>
            <p><strong>Min:</strong> {df_filtered[selected_kpi].min():.2f}</p>
            <p><strong>Max:</strong> {df_filtered[selected_kpi].max():.2f}</p>
            <p><strong>Range:</strong> {df_filtered[selected_kpi].max() - df_filtered[selected_kpi].min():.2f}</p>
        </div>
        """, unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="section-header">Performance Reports & Export</div>', unsafe_allow_html=True)
    
    if st.button("Generate Executive Summary", type="primary"):
        st.markdown("## Executive Summary Report")
        st.markdown(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        st.markdown(f"**Period:** {time_period}")
        
        st.markdown("### Key Performance Indicators")
        summary_metrics = {
            'Revenue': latest_data['Revenue'],
            'Profit Margin': latest_data['Profit_Margin'],
            'Cash Flow': latest_data['Cash_Flow'],
            'ROI': latest_data['ROI'],
            'Customer Satisfaction': latest_data['Customer_Satisfaction']
        }
        
        for metric, value in summary_metrics.items():
            if metric in ['Revenue', 'Cash Flow']:
                st.write(f"- **{metric}:** ${value:,.0f}")
            else:
                st.write(f"- **{metric}:** {value:.1f}{'%' if metric in ['Profit Margin', 'ROI'] else ''}")
        
        if active_alerts:
            st.markdown("### Active Alerts")
            for alert in active_alerts:
                st.write(f"- **{alert['KPI']}:** {alert['Message']}")
        else:
            st.markdown("### Status: All Systems Normal")
    
    st.markdown("### Data Export")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        csv_data = df_filtered.to_csv(index=False)
        st.download_button(
            label="Download KPI Data",
            data=csv_data,
            file_name=f"kpi_data_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )
    
    with col2:
        thresholds_df = pd.DataFrame.from_dict(st.session_state.kpi_thresholds, orient='index')
        thresholds_csv = thresholds_df.to_csv()
        st.download_button(
            label="Download Thresholds",
            data=thresholds_csv,
            file_name=f"kpi_thresholds_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )
    
    with col3:
        summary_stats = df_filtered.describe()
        summary_csv = summary_stats.to_csv()
        st.download_button(
            label="Download Summary Stats",
            data=summary_csv,
            file_name=f"kpi_summary_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )

# Sidebar status
st.sidebar.markdown("---")
st.sidebar.markdown("### System Status")

alert_count = len(active_alerts)
if alert_count > 0:
    st.sidebar.error(f"Active Alerts: {alert_count}")
else:
    st.sidebar.success("All Systems Normal")

st.sidebar.markdown(f"""
**Dashboard Metrics:**
- Data Points: {len(df_filtered):,}
- Analysis Period: {time_period}
- Last Update: {datetime.now().strftime('%H:%M:%S')}
- KPIs Monitored: 8
""")

st.sidebar.markdown("---")
st.sidebar.markdown("""
### Technical Specifications

**Business Intelligence Features:**
- Real-time KPI monitoring
- Automated threshold alerting
- Historical trend analysis
- Executive reporting
- Data export capabilities

**Technology Stack:**
- Python & Streamlit
- Plotly visualizations
- Pandas analytics
- Real-time processing

**Developer:** Larismar Tati  
**Portfolio:** Virtual Code Analytics
""")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; margin-top: 2rem; padding: 2rem; background-color: #f8f9fa; border-radius: 8px;'>
    <h4 style='margin-bottom: 1rem; color: #2c3e50;'>Business Intelligence KPI Monitoring System</h4>
    <p style='margin-bottom: 0.5rem;'>Real-time Performance Monitoring and Executive Reporting</p>
    <p style='margin-bottom: 0.5rem;'><strong>Technology Stack:</strong> Python • Streamlit • Plotly • Pandas</p>
    <p style='margin-bottom: 1rem;'><strong>Developer:</strong> Larismar Tati | <strong>Portfolio:</strong> Virtual Code</p>
    <p style='font-size: 0.9rem; color: #7f8c8d;'><em>Demonstrating business intelligence, dashboard development, and real-time monitoring capabilities</em></p>
</div>
""", unsafe_allow_html=True)
