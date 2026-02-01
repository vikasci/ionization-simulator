"""
グラフ描画モジュール
"""

import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from modules.saha import calculate_ionization_fractions, calculate_average_ionization


def plot_ionization_fractions_bar(fractions, element_symbol, T, n_e):
    """
    イオン化率の棒グラフ
    
    Parameters
    ----------
    fractions : dict
        各イオン電荷の存在比
    element_symbol : str
        元素記号
    T : float
        温度 [K]
    n_e : float
        電子密度 [cm^-3]
    
    Returns
    -------
    fig : plotly.graph_objects.Figure
    """
    # データ整形
    charges = list(fractions.keys())
    values = [fractions[c] * 100 for c in charges]  # パーセント表示
    
    # イオン名を作成
    ion_names = []
    for c in charges:
        if c == 0:
            ion_names.append(f"{element_symbol} I")
        else:
            # ローマ数字変換（簡易版）
            roman = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
                    "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX"]
            if c + 1 <= len(roman):
                ion_names.append(f"{element_symbol} {roman[c]}")
            else:
                ion_names.append(f"{element_symbol}+{c}")
    
    # カラースケール
    colors = px.colors.sequential.Viridis
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=ion_names,
        y=values,
        marker=dict(
            color=charges,
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Ion Charge")
        ),
        text=[f"{v:.2f}%" for v in values],
        textposition='outside',
    ))
    
    fig.update_layout(
        title=f"{element_symbol} Ionization Fractions<br>T = {T:.0f} K, ne = {n_e:.2e} cm⁻³",
        xaxis_title="Ion State",
        yaxis_title="Fraction (%)",
        yaxis=dict(range=[0, max(values) * 1.15]),
        template="plotly_white",
        height=500,
        showlegend=False
    )
    
    return fig


def plot_temperature_scan(element_data, element_symbol, T_range, n_e):
    """
    温度スキャン（各イオン状態の温度依存性）
    
    Parameters
    ----------
    element_data : pd.DataFrame
        元素データ
    element_symbol : str
        元素記号
    T_range : array-like
        温度範囲 [K]
    n_e : float
        電子密度 [cm^-3]
    
    Returns
    -------
    fig : plotly.graph_objects.Figure
    """
    # 各温度でイオン化率を計算
    max_charge = int(element_data['Ion Charge'].max())
    fractions_vs_T = {i: [] for i in range(max_charge + 1)}
    
    for T in T_range:
        fracs = calculate_ionization_fractions(element_data, T, n_e)
        for charge in range(max_charge + 1):
            fractions_vs_T[charge].append(fracs.get(charge, 0) * 100)
    
    # プロット
    fig = go.Figure()
    
    # 主要なイオン状態のみプロット（存在比が1%以上になるもの）
    for charge in range(max_charge + 1):
        max_frac = max(fractions_vs_T[charge])
        if max_frac > 1.0:  # 1%以上
            if charge == 0:
                name = f"{element_symbol} I"
            else:
                roman = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
                name = f"{element_symbol} {roman[charge]}" if charge + 1 <= len(roman) else f"{element_symbol}+{charge}"
            
            fig.add_trace(go.Scatter(
                x=T_range,
                y=fractions_vs_T[charge],
                mode='lines',
                name=name,
                line=dict(width=2),
            ))
    
    fig.update_layout(
        title=f"{element_symbol} Ionization vs Temperature<br>ne = {n_e:.2e} cm⁻³",
        xaxis_title="Temperature (K)",
        yaxis_title="Fraction (%)",
        template="plotly_white",
        height=500,
        hovermode='x unified'
    )
    
    return fig


def plot_electron_density_scan(element_data, element_symbol, ne_range, T):
    """
    電子密度スキャン
    
    Parameters
    ----------
    element_data : pd.DataFrame
        元素データ
    element_symbol : str
        元素記号
    ne_range : array-like
        電子密度範囲 [cm^-3]
    T : float
        温度 [K]
    
    Returns
    -------
    fig : plotly.graph_objects.Figure
    """
    # 各電子密度でイオン化率を計算
    max_charge = int(element_data['Ion Charge'].max())
    fractions_vs_ne = {i: [] for i in range(max_charge + 1)}
    
    for ne in ne_range:
        fracs = calculate_ionization_fractions(element_data, T, ne)
        for charge in range(max_charge + 1):
            fractions_vs_ne[charge].append(fracs.get(charge, 0) * 100)
    
    # プロット
    fig = go.Figure()
    
    # 主要なイオン状態のみプロット
    for charge in range(max_charge + 1):
        max_frac = max(fractions_vs_ne[charge])
        if max_frac > 1.0:
            if charge == 0:
                name = f"{element_symbol} I"
            else:
                roman = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
                name = f"{element_symbol} {roman[charge]}" if charge + 1 <= len(roman) else f"{element_symbol}+{charge}"
            
            fig.add_trace(go.Scatter(
                x=ne_range,
                y=fractions_vs_ne[charge],
                mode='lines',
                name=name,
                line=dict(width=2),
            ))
    
    fig.update_layout(
        title=f"{element_symbol} Ionization vs Electron Density<br>T = {T:.0f} K",
        xaxis_title="Electron Density (cm⁻³)",
        xaxis_type="log",
        yaxis_title="Fraction (%)",
        template="plotly_white",
        height=500,
        hovermode='x unified'
    )
    
    return fig


def plot_average_ionization_2d(element_data, element_symbol, T_range, ne_range):
    """
    平均イオン価数の2Dマップ（温度vs電子密度）
    
    Parameters
    ----------
    element_data : pd.DataFrame
        元素データ
    element_symbol : str
        元素記号
    T_range : array-like
        温度範囲 [K]
    ne_range : array-like
        電子密度範囲 [cm^-3]
    
    Returns
    -------
    fig : plotly.graph_objects.Figure
    """
    Z_avg = np.zeros((len(ne_range), len(T_range)))
    
    for i, ne in enumerate(ne_range):
        for j, T in enumerate(T_range):
            fracs = calculate_ionization_fractions(element_data, T, ne)
            Z_avg[i, j] = calculate_average_ionization(fracs)
    
    fig = go.Figure(data=go.Heatmap(
        z=Z_avg,
        x=T_range,
        y=ne_range,
        colorscale='Viridis',
        colorbar=dict(title="Average<br>Ionization")
    ))
    
    fig.update_layout(
        title=f"{element_symbol} Average Ionization State",
        xaxis_title="Temperature (K)",
        yaxis_title="Electron Density (cm⁻³)",
        yaxis_type="log",
        template="plotly_white",
        height=500
    )
    
    return fig