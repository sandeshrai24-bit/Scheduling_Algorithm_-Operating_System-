import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set sleek page configuration
st.set_page_config(
    page_title="Core CPU Kernel Dispatcher",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# High-Tech Dark Mode Dashboard UI Theme & Styling
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    code, pre, .mono-text {
        font-family: 'JetBrains Mono', monospace;
    }

    /* Minimalist Technical HUD Banner */
    .hud-console {
        background: #0d1117;
        border-left: 5px solid #10b981;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: inset 0 0 20px rgba(16, 185, 129, 0.05);
    }
    .hud-title {
        color: #ffffff;
        margin: 0;
        font-weight: 700;
        font-size: 2.2rem;
        letter-spacing: -0.03em;
    }
    .hud-subtitle {
        color: #8b949e;
        margin-top: 0.3rem;
        font-size: 0.95rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    /* Grid Analytics Cards */
    .grid-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    .grid-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 1rem;
        text-align: left;
    }
    .grid-label {
        font-size: 0.75rem;
        font-weight: 700;
        color: #8b949e;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .grid-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #58a6ff;
        margin-top: 0.2rem;
    }
    .grid-winner {
        font-size: 0.8rem;
        color: #56d364;
        margin-top: 0.4rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Title Engine Block
st.markdown("""
<div class="hud-console">
    <div class="hud-title">⚡ Kernel Dispatch Analytics Engine</div>
    <div class="hud-subtitle">Comparative Execution Sandbox: FCFS vs. SJF vs. Priority (Non-Preemptive)</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Algorithmic Scheduling Logic Units
# ---------------------------------------------------------

def fcfs_schedule(processes):
    sorted_p = sorted(processes, key=lambda x: x['arrival'])
    timeline, current_time = [], 0
    metrics = {}
    
    for p in sorted_p:
        if current_time < p['arrival']:
            timeline.append({'Process': 'Idle', 'Start': current_time, 'End': p['arrival']})
            current_time = p['arrival']
        
        start = current_time
        current_time += p['burst']
        timeline.append({'Process': p['id'], 'Start': start, 'End': current_time})
        
        metrics[p['id']] = {
            'CT': current_time,
            'TAT': current_time - p['arrival'],
            'WT': (current_time - p['arrival']) - p['burst']
        }
    return metrics, timeline


def sjf_schedule(processes):
    ready_pool = list(processes)
    timeline, current_time = [], 0
    metrics = {}
    
    while ready_pool:
        available = [p for p in ready_pool if p['arrival'] <= current_time]
        if not available:
            next_arrival = min(p['arrival'] for p in ready_pool)
            timeline.append({'Process': 'Idle', 'Start': current_time, 'End': next_arrival})
            current_time = next_arrival
            continue
        
        # Pick job with shortest burst time
        next_job = min(available, key=lambda x: x['burst'])
        ready_pool.remove(next_job)
        
        start = current_time
        current_time += next_job['burst']
        timeline.append({'Process': next_job['id'], 'Start': start, 'End': current_time})
        
        metrics[next_job['id']] = {
            'CT': current_time,
            'TAT': current_time - next_job['arrival'],
            'WT': (current_time - next_job['arrival']) - next_job['burst']
        }
    return metrics, timeline


def priority_schedule(processes):
    ready_pool = list(processes)
    timeline, current_time = [], 0
    metrics = {}
    
    while ready_pool:
        available = [p for p in ready_pool if p['arrival'] <= current_time]
        if not available:
            next_arrival = min(p['arrival'] for p in ready_pool)
            timeline.append({'Process': 'Idle', 'Start': current_time, 'End': next_arrival})
            current_time = next_arrival
            continue
        
        # Lower integer value = Higher processing priority
        next_job = min(available, key=lambda x: x['priority'])
        ready_pool.remove(next_job)
        
        start = current_time
        current_time += next_job['burst']
        timeline.append({'Process': next_job['id'], 'Start': start, 'End': current_time})
        
        metrics[next_job['id']] = {
            'CT': current_time,
            'TAT': current_time - next_job['arrival'],
            'WT': (current_time - next_job['arrival']) - next_job['burst']
        }
    return metrics, timeline

# ---------------------------------------------------------
# Dynamic Presets Configuration Block
# ---------------------------------------------------------
PRESETS = {
    "Standard Mix": pd.DataFrame([
        {"Process ID": "P1", "Arrival Time": 0, "Burst Time": 6, "Priority": 3},
        {"Process ID": "P2", "Arrival Time": 1, "Burst Time": 2, "Priority": 1},
        {"Process ID": "P3", "Arrival Time": 2, "Burst Time": 8, "Priority": 4},
        {"Process ID": "P4", "Arrival Time": 3, "Burst Time": 4, "Priority": 2},
    ]),
    "SJF Showdown (Long Job First Out)": pd.DataFrame([
        {"Process ID": "P1", "Arrival Time": 0, "Burst Time": 10, "Priority": 2},
        {"Process ID": "P2", "Arrival Time": 1, "Burst Time": 2, "Priority": 3},
        {"Process ID": "P3", "Arrival Time": 2, "Burst Time": 1, "Priority": 1},
    ]),
    "Priority Conflicts (High Burst vs High Priority)": pd.DataFrame([
        {"Process ID": "P1", "Arrival Time": 0, "Burst Time": 8, "Priority": 4},
        {"Process ID": "P2", "Arrival Time": 0, "Burst Time": 2, "Priority": 1},
        {"Process ID": "P3", "Arrival Time": 0, "Burst Time": 4, "Priority": 2},
    ])
}

st.sidebar.subheader("🎛️ Matrix Presets")
selected_preset = st.sidebar.selectbox("Load Thread Vector", list(PRESETS.keys()))

if "current_df" not in st.session_state or st.sidebar.button("Force Re-index Preset"):
    st.session_state.current_df = PRESETS[selected_preset].copy()

# ---------------------------------------------------------
# Redesigned Dynamic Split-Pane Dashboard
# ---------------------------------------------------------
left_panel, right_panel = st.columns([1, 1.3])

with left_panel:
    st.markdown("### 📥 Dynamic Pipeline Matrix")
    st.write("Modify properties directly inline. Lower numbers indicate higher execution urgency for priority metrics.")
    
    edited_df = st.data_editor(
        st.session_state.current_df,
        num_rows="fixed",
        use_container_width=True,
        column_config={
            "Process ID": st.column_config.TextColumn("Process Name"),
            "Arrival Time": st.column_config.NumberColumn("Arrival ($T_a$)", min_value=0, step=1),
            "Burst Time": st.column_config.NumberColumn("Execution ($T_b$)", min_value=1, step=1),
            "Priority": st.column_config.NumberColumn("Priority (Rank)", min_value=1, step=1)
        },
        key="hud_matrix_editor"
    )
    st.session_state.current_df = edited_df

    # Inline dynamic pipeline nodes modification buttons
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("➕ Inject Process Row", use_container_width=True):
            next_num = len(st.session_state.current_df) + 1
            new_row = pd.DataFrame([{"Process ID": f"P{next_num}", "Arrival Time": 0, "Burst Time": 2, "Priority": 3}])
            st.session_state.current_df = pd.concat([st.session_state.current_df, new_row], ignore_index=True)
            st.rerun()
    with btn_col2:
        if st.button("🗑️ Prune Last Row", use_container_width=True):
            if len(st.session_state.current_df) > 1:
                st.session_state.current_df = st.session_state.current_df.iloc[:-1]
                st.rerun()

# Compile inputs to localized arrays
parsed_processes = []
for idx, r in edited_df.iterrows():
    parsed_processes.append({
        "id": str(r["Process ID"]).strip() if pd.notna(r["Process ID"]) else f"P{idx+1}",
        "arrival": int(r["Arrival Time"]) if pd.notna(r["Arrival Time"]) else 0,
        "burst": int(r["Burst Time"]) if pd.notna(r["Burst Time"]) else 1,
        "priority": int(r["Priority"]) if pd.notna(r["Priority"]) else 1
    })

# Compute metrics
fcfs_m, fcfs_t = fcfs_schedule(parsed_processes)
sjf_m, sjf_t = sjf_schedule(parsed_processes)
prio_m, prio_t = priority_schedule(parsed_processes)

# Calculate system engine averages
def get_averages(metrics_dict):
    wts = [m['WT'] for m in metrics_dict.values()]
    tats = [m['TAT'] for m in metrics_dict.values()]
    return sum(wts)/len(wts), sum(tats)/len(tats)

f_awt, f_atat = get_averages(fcfs_m)
s_awt, s_atat = get_averages(sjf_m)
p_awt, p_atat = get_averages(prio_m)

# Find absolute architecture winners
awt_winner = "FCFS" if f_awt <= s_awt and f_awt <= p_awt else ("SJF" if s_awt <= f_awt and s_awt <= p_awt else "Priority")
atat_winner = "FCFS" if f_atat <= s_atat and f_atat <= p_atat else ("SJF" if s_atat <= f_atat and s_atat <= p_atat else "Priority")

with right_panel:
    st.markdown("### 🏁 Consolidated Analytical HUD")
    
    st.markdown(f"""
    <div class="grid-container">
        <div class="grid-card">
            <div class="grid-label">FCFS Framework Averages</div>
            <div class="grid-value">{f_awt:.2f} <span style='font-size:0.9rem; color:#8b949e;'>WT</span></div>
            <div style='color:#8b949e; font-size:0.8rem; margin-top:0.2rem;'>Turnaround: {f_atat:.2f}</div>
        </div>
        <div class="grid-card">
            <div class="grid-label">SJF Framework Averages</div>
            <div class="grid-value">{s_awt:.2f} <span style='font-size:0.9rem; color:#8b949e;'>WT</span></div>
            <div style='color:#8b949e; font-size:0.8rem; margin-top:0.2rem;'>Turnaround: {s_atat:.2f}</div>
        </div>
        <div class="grid-card">
            <div class="grid-label">Priority Engine Averages</div>
            <div class="grid-value">{p_awt:.2f} <span style='font-size:0.9rem; color:#8b949e;'>WT</span></div>
            <div style='color:#8b949e; font-size:0.8rem; margin-top:0.2rem;'>Turnaround: {p_atat:.2f}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.info(f"⚡ **Architectural Engine Insight:** **{awt_winner}** optimal for Waiting Time reduction; **{atat_winner}** holds optimal Turnaround sequence profile.")

st.markdown("---")

# ---------------------------------------------------------
# Timeline Render Block (Replacing Linear Layouts)
# ---------------------------------------------------------
st.markdown("### 🎚️ Stacked Execution Timelines")

palette = ["#ff5555", "#50fa7b", "#8be9fd", "#ffb86c", "#bd93f9", "#ff79c6", "#f1fa8c"]
p_ids = list(set([p['id'] for p in parsed_processes]))
color_map = {pid: palette[i % len(palette)] for i, pid in enumerate(p_ids)}
color_map['Idle'] = '#44475a'

def build_timeline_trace(timeline, title):
    df = pd.DataFrame(timeline)
    df['Duration'] = df['End'] - df['Start']
    df['Task'] = ""
    
    fig = px.bar(
        df, x="Duration", y="Task", base="Start", orientation="h",
        color="Process", text="Process", color_discrete_map=color_map,
        custom_data=["Process", "Start", "End"]
    )
    fig.update_traces(
        textposition="inside", insidetextanchor="middle",
        hovertemplate="<b>Node: %{customdata[0]}</b><br>Active Vector: %{customdata[1]} ➔ %{customdata[2]}<extra></extra>"
    )
    fig.update_layout(
        title=dict(text=title, font=dict(size=14, color="#ffffff")),
        xaxis=dict(title="System Clock Ticks", gridcolor="#30363d", zeroline=False),
        yaxis=dict(visible=False),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        height=130, margin=dict(l=10, r=10, t=40, b=30), showlegend=False
    )
    return fig

st.plotly_chart(build_timeline_trace(fcfs_t, "📁 First-Come First-Served Sequence Execution Trace"), use_container_width=True)
st.plotly_chart(build_timeline_trace(sjf_t, "🔬 Shortest Job First Execution Sequence Trace"), use_container_width=True)
st.plotly_chart(build_timeline_trace(prio_t, "👑 Arbitrary Numeric Priority Execution Sequence Trace"), use_container_width=True)

st.markdown("---")

# ---------------------------------------------------------
# Detailed Tabulated Consolidated Block
# ---------------------------------------------------------
st.markdown("### 📋 Deep Architecture Telemetry Matrix")

master_compiled_rows = []
for p in parsed_processes:
    pid = p['id']
    master_compiled_rows.append({
        "ID": pid,
        "FCFS CT": fcfs_m[pid]['CT'], "FCFS WT": fcfs_m[pid]['WT'], "FCFS TAT": fcfs_m[pid]['TAT'],
        "SJF CT": sjf_m[pid]['CT'], "SJF WT": sjf_m[pid]['WT'], "SJF TAT": sjf_m[pid]['TAT'],
        "PRIO CT": prio_m[pid]['CT'], "PRIO WT": prio_m[pid]['WT'], "PRIO TAT": prio_m[pid]['TAT']
    })

master_df = pd.DataFrame(master_compiled_rows)
st.dataframe(
    master_df.style.background_gradient(subset=["FCFS WT", "SJF WT", "PRIO WT"], cmap="YlOrRd"),
    use_container_width=True,
    hide_index=True
)
st.caption("Heatmap highlights process starvation hotspots (higher waiting times inside the microkernel).")