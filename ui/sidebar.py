"""
サイドバーUI - パラメータ入力
"""

import streamlit as st
import streamlit.components.v1 as components
import json
from ui.monetization import display_support_section


def load_presets():
    """Load preset conditions"""
    try:
        with open('data/plasma_presets.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data['presets']
    except:
        # Default presets
        return {
            "ICP Standard": {
                "temperature": 7000,
                "electron_density": 1e15,
                "description": "Typical ICP-OES conditions"
            },
            "Custom": {
                "temperature": 7000,
                "electron_density": 1e15,
                "description": "Custom settings"
            }
        }


def render_sidebar(element_list):
    """
    Render sidebar
    
    Parameters
    ----------
    element_list : list
        List of available elements
    
    Returns
    -------
    params : dict
        User-selected parameters
    """
    st.sidebar.title("⚛️ Ionization Simulator")
    st.sidebar.markdown("---")
    
    # Element selection
    st.sidebar.subheader("Element Selection")
    selected_element = st.sidebar.selectbox(
        "Element",
        element_list,
        index=element_list.index('Fe') if 'Fe' in element_list else 0
    )
    
    st.sidebar.markdown("---")
    
    # Preset selection
    st.sidebar.subheader("Plasma Conditions")
    presets = load_presets()
    preset_names = list(presets.keys())
    
    selected_preset = st.sidebar.selectbox(
        "Preset",
        preset_names,
        index=preset_names.index("ICP Standard") if "ICP Standard" in preset_names else 0
    )
    
    # Preset description
    if selected_preset in presets:
        st.sidebar.info(presets[selected_preset]["description"])
    
    # Parameter input
    st.sidebar.markdown("### Parameters")
    
    # プリセットから初期値を取得
    default_temp = presets[selected_preset]["temperature"]
    default_ne = presets[selected_preset]["electron_density"]
    
    # Temperature
    temperature = st.sidebar.number_input(
        "Temperature (K)",
        min_value=1000,
        max_value=50000,
        value=default_temp,
        step=500,
        help="Plasma temperature [K]"
    )
    
    # Electron density (logarithmic scale)
    ne_log = st.sidebar.slider(
        "log₁₀(Electron Density [cm⁻³])",
        min_value=10.0,
        max_value=18.0,
        value=float(f"{default_ne:.1e}".split('e+')[1]) if default_ne >= 1 else 15.0,
        step=0.5,
        help="Log of electron density"
    )
    electron_density = 10 ** ne_log
    
    st.sidebar.markdown(f"**ne = {electron_density:.2e} cm⁻³**")
    
    st.sidebar.markdown("---")
    
    # Visualization options
    st.sidebar.subheader("Visualization Options")
    
    plot_type = st.sidebar.radio(
        "Plot Type",
        ["Bar Chart"],
        index=0,
        help="Free version: Bar Chart only. Upgrade to Pro for all visualization types."
    )
    
    # Pro版の機能を表示（ロック状態）
    st.sidebar.markdown("### 🔒 Pro Features")
    st.sidebar.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea22 0%, #764ba222 100%);
        border-radius: 8px;
        padding: 12px;
        margin: 10px 0;
    ">
        <p style="margin: 0; font-size: 13px; color: #666;">
        ✨ Temperature Scan<br>
        ✨ Electron Density Scan<br>
        ✨ 2D Heat Map<br>
        ✨ Data Export (CSV/Excel)<br>
        ✨ All Elements (20 → 118)
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Upgrade button
    if st.sidebar.button("🚀 Upgrade to Pro - $7/month", use_container_width=True):
        st.sidebar.info("👉 [Become a GitHub Sponsor](https://github.com/sponsors/vikasci) to get Pro access!")
    
    # Scan parameters
    scan_params = {}
    
    # Return parameters as a dictionary
    params = {
        'element': selected_element,
        'temperature': temperature,
        'electron_density': electron_density,
        'plot_type': plot_type,
        'scan_params': scan_params
    }
    
    # Support and monetization section
    display_support_section()
    
    return params
