"""
イオン化率シミュレーター - メインアプリケーション
Saha方程式を用いたプラズマ中のイオン化率計算
"""

import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import pandas as pd

from modules.data_loader import IonizationDatabase
from modules.saha import calculate_ionization_fractions, calculate_average_ionization
from ui.sidebar import render_sidebar
from ui.monetization import display_footer_books
from ui.plotting import (
    plot_ionization_fractions_bar,
    plot_temperature_scan,
    plot_electron_density_scan
)


# ページ設定
st.set_page_config(
    page_title="Ionization Rate Simulator",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)


@st.cache_resource
def load_database():
    """データベースを読み込む（キャッシュ）"""
    return IonizationDatabase('data/ionizationenergy.csv')


def display_ad(ad_slot="sidebar", height=280):
    """
    Display advertisement
    
    Parameters
    ----------
    ad_slot : str
        Advertisement location ('sidebar', 'top', 'bottom')
    height : int
        Ad container height in pixels
    """
    # TODO: Replace with your actual Google AdSense code
    ad_html = f"""
    <div style="
        width: 100%;
        height: {height}px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-family: sans-serif;
        text-align: center;
        padding: 20px;
        box-sizing: border-box;
    ">
        <div>
            <h3 style="margin: 0 0 10px 0;">Advertisement Space</h3>
            <p style="margin: 0; font-size: 14px;">
                Replace this with your Google AdSense code
            </p>
            <p style="margin: 10px 0 0 0; font-size: 12px; opacity: 0.8;">
                Ad slot: {ad_slot}
            </p>
        </div>
    </div>
    
    <!-- 
    Replace above div with actual AdSense code like:
    
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXX"
         crossorigin="anonymous"></script>
    <ins class="adsbygoogle"
         style="display:block"
         data-ad-client="ca-pub-XXXXXXX"
         data-ad-slot="XXXXXXX"
         data-ad-format="auto"
         data-full-width-responsive="true"></ins>
    <script>
         (adsbygoogle = window.adsbygoogle || []).push({{}});
    </script>
    -->
    """
    
    components.html(ad_html, height=height)


def main():
    """メインアプリケーション"""
    
    # タイトル
    st.title("⚛️ Ionization Rate Simulator")
    st.markdown("**Equilibrium ionization calculation using Saha equation**")
    
    # License notice
    st.info("""
    📜 **License Notice**: This app is free for personal, educational, and non-commercial research use. 
    Commercial use requires a separate license. [Learn more](https://github.com/vikasci/ionization-simulator#-license)
    """)
    
    st.markdown("---")
    
    # データベース読み込み
    try:
        db = load_database()
        element_list = db.get_element_list()
    except Exception as e:
        st.error(f"❌ Database loading error: {e}")
        st.stop()
    
    # サイドバー（パラメータ入力）
    params = render_sidebar(element_list)
    
    # 選択された元素のデータを取得
    element_symbol = params['element']
    element_data = db.get_element_data(element_symbol)
    element_name = db.get_element_name(element_symbol)
    
    # メイン表示エリア
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(f"📊 {element_name} ({element_symbol})")
    
    with col2:
        st.metric("Max Ion Charge", f"+{db.get_max_ion_charge(element_symbol)}")
    
    st.markdown("---")
    
    # 計算実行
    T = params['temperature']
    n_e = params['electron_density']
    plot_type = params['plot_type']
    
    # プロット表示
    if plot_type == "Bar Chart":
        # 単一条件での計算
        with st.spinner("Calculating..."):
            fractions = calculate_ionization_fractions(element_data, T, n_e)
            z_avg = calculate_average_ionization(fractions)
        
        # 結果表示
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Temperature", f"{T:.0f} K")
        with col2:
            st.metric("Electron Density", f"{n_e:.2e} cm⁻³")
        with col3:
            st.metric("Average Ionization", f"{z_avg:.3f}")
        
        # 棒グラフ
        fig = plot_ionization_fractions_bar(fractions, element_symbol, T, n_e)
        st.plotly_chart(fig, use_container_width=True)
        
        # Data table
        with st.expander("📋 Show detailed data"):
            # Ionization fraction table
            table_data = []
            for charge, frac in sorted(fractions.items()):
                if charge == 0:
                    ion_name = f"{element_symbol} I"
                else:
                    roman = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
                    ion_name = f"{element_symbol} {roman[charge]}" if charge + 1 <= len(roman) else f"{element_symbol}+{charge}"
                
                table_data.append({
                    "Ion State": ion_name,
                    "Charge": f"+{charge}" if charge > 0 else "0",
                    "Fraction": f"{frac:.6f}",
                    "Percentage": f"{frac*100:.3f}%"
                })
            
            df_result = pd.DataFrame(table_data)
            st.dataframe(df_result, use_container_width=True, hide_index=True)
    
    elif plot_type == "Temperature Scan":
        # 温度スキャン
        scan_params = params['scan_params']
        T_min = scan_params['T_min']
        T_max = scan_params['T_max']
        T_points = scan_params['T_points']
        
        T_range = np.linspace(T_min, T_max, T_points)
        
        with st.spinner("Temperature scan in progress..."):
            fig = plot_temperature_scan(element_data, element_symbol, T_range, n_e)
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.info(f"📌 Fixed parameter: ne = {n_e:.2e} cm⁻³")
    
    elif plot_type == "Electron Density Scan":
        # 電子密度スキャン
        scan_params = params['scan_params']
        ne_min = 10 ** scan_params['ne_min']
        ne_max = 10 ** scan_params['ne_max']
        ne_points = scan_params['ne_points']
        
        ne_range = np.logspace(np.log10(ne_min), np.log10(ne_max), ne_points)
        
        with st.spinner("Electron density scan in progress..."):
            fig = plot_electron_density_scan(element_data, element_symbol, ne_range, T)
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.info(f"📌 Fixed parameter: T = {T:.0f} K")
    
    # Footer information
    st.markdown("---")
    
    # Amazon affiliate books section
    display_footer_books()
    
    st.markdown("---")
    
    with st.expander("ℹ️ About calculation method"):
        st.markdown("""
        ### Saha Equation
        
        The equilibrium distribution of ion states in plasma is described by the Saha equation:
        
        $$
        \\frac{n_{i+1}}{n_i} = \\frac{2Z_{i+1}}{n_e Z_i} \\left(\\frac{2\\pi m_e kT}{h^2}\\right)^{3/2} \\exp\\left(-\\frac{\\chi_i}{kT}\\right)
        $$
        
        Where:
        - $n_i$: Number density of ion state i
        - $Z_i$: Partition function (approximated by ground state degeneracy)
        - $\\chi_i$: Ionization energy
        - $T$: Temperature
        - $n_e$: Electron density
        - $k$: Boltzmann constant
        - $m_e$: Electron mass
        - $h$: Planck constant
        
        ### Data Source
        - **Ionization Energy**: NIST Atomic Spectra Database
        - **Partition Function**: Ground state degeneracy calculated from Ground Level notation
        
        ### Applicable Range
        - High accuracy for ICP-OES conditions (T = 6000-10000 K)
        - Ground state approximation may introduce errors at very high temperatures
        """)
    
    with st.expander("📚 How to use"):
        st.markdown("""
        1. **Select an element** from the sidebar
        2. **Choose plasma conditions** (preset or custom)
        3. **Select visualization type**:
           - **Bar Chart**: Ionization distribution at a single condition
           - **Temperature Scan**: Temperature dependence
           - **Electron Density Scan**: Electron density dependence
        """)
    
    # License information
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 12px; padding: 20px;">
        <p><strong>Ionization Rate Simulator</strong> | Free for non-commercial use</p>
        <p>Licensed under AGPL-3.0 | Commercial licenses available (see LICENSE file)</p>
        <p>⭐ <a href="https://github.com/vikasci/ionization-simulator" target="_blank">Star on GitHub</a> | 
        ☕ <a href="https://ko-fi.com/vikasci" target="_blank">Support Development</a></p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
