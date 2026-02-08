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
        # Default presets (宇宙工学向け)
        return {
            "Interstellar Medium": {
                "temperature": 15000,
                "electron_density": 1e6,
                "description": "Typical interstellar plasma conditions"
            },
            "Solar Corona": {
                "temperature": 2000000,
                "electron_density": 1e9,
                "description": "Solar corona plasma"
            },
            "Planetary Nebula": {
                "temperature": 10000,
                "electron_density": 1e3,
                "description": "Planetary nebula conditions"
            },
            "Custom": {
                "temperature": 15000,
                "electron_density": 1e6,
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
    
    # Temperature (宇宙工学用に制限)
    # ICP-OES範囲（6000-10000K）はPro版のみ
    temperature = st.sidebar.number_input(
        "Temperature (K)",
        min_value=10000,  # ICP-OES以上
        max_value=10000000,  # 超高温プラズマまで
        value=default_temp if default_temp >= 10000 else 15000,
        step=5000,
        help="Plasma temperature [K] - Free version: Space plasmas only (T ≥ 10,000 K)"
    )
    
    st.sidebar.info("🔒 ICP-OES range (6,000-10,000 K) available in Pro version")
    
    # Electron density (宇宙工学用に制限、対数スケール)
    # ICP-OES範囲（10^14-10^16）はPro版のみ
    ne_log = st.sidebar.slider(
        "log₁₀(Electron Density [cm⁻³])",
        min_value=0.0,   # 希薄プラズマ
        max_value=12.0,  # ICP-OES未満
        value=8.0,
        step=0.5,
        help="Log of electron density - Free version: Space plasmas only (ne < 10^12)"
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
        ✨ <strong>ICP-OES Range</strong><br>
        &nbsp;&nbsp;&nbsp;• Temperature: 6,000-10,000 K<br>
        &nbsp;&nbsp;&nbsp;• Density: 10¹⁴-10¹⁶ cm⁻³<br>
        ✨ Temperature Scan<br>
        ✨ Electron Density Scan<br>
        ✨ 2D Heat Map<br>
        ✨ Data Export (CSV/Excel)<br>
        ✨ All Elements (6 → 118)
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
