"""
Saha方程式による平衡イオン化率の計算
"""

import numpy as np
from .constants import k_eV, h, m_e, pi, eV_to_J
from .partition import partition_function


def saha_equation(chi, Z_i, Z_ip1, T, n_e):
    """
    Saha方程式による平衡定数の計算
    
    n_{i+1} / n_i = K_saha
    
    Parameters
    ----------
    chi : float
        イオン化エネルギー [eV]
    Z_i : float
        イオン状態 i の分配関数
    Z_ip1 : float
        イオン状態 i+1 の分配関数
    T : float
        温度 [K]
    n_e : float
        電子密度 [cm^-3]
    
    Returns
    -------
    K_saha : float
        Saha平衡定数 n_{i+1}/n_i
    """
    # 温度をeV単位に変換
    kT = k_eV * T
    
    # 電子密度を m^-3 に変換
    n_e_SI = n_e * 1e6  # cm^-3 -> m^-3
    
    # Saha式の前因子
    # (2πm_e kT / h^2)^(3/2)
    T_SI = T  # K
    prefactor = (2 * pi * m_e * k_eV * eV_to_J * T_SI / h**2)**(3/2)
    
    # Saha方程式
    # K = (2 * Z_{i+1} / (n_e * Z_i)) * prefactor * exp(-chi / kT)
    K_saha = (2 * Z_ip1 / (n_e_SI * Z_i)) * prefactor * np.exp(-chi / kT)
    
    return K_saha


def calculate_ionization_fractions(element_data, T, n_e):
    """
    特定元素の各イオン状態の存在比を計算
    
    Parameters
    ----------
    element_data : pd.DataFrame
        元素のイオン化エネルギーとGround Levelデータ
        必要カラム: 'Ion Charge', 'Ionization Energy (b) (eV)', 'Ground Level'
    T : float
        温度 [K]
    n_e : float
        電子密度 [cm^-3]
    
    Returns
    -------
    fractions : dict
        各イオン電荷の存在比
        {0: f0, 1: f1, 2: f2, ...}
    """
    # イオン電荷でソート
    data = element_data.sort_values('Ion Charge').reset_index(drop=True)
    
    max_charge = int(data['Ion Charge'].max())
    
    # 各イオン状態の相対存在比（n_0 = 1として）
    n_relative = np.zeros(max_charge + 1)
    n_relative[0] = 1.0  # 中性原子を基準
    
    # 逐次的にSaha方程式を適用
    for i in range(max_charge):
        # i番目のイオン化
        chi = data.loc[data['Ion Charge'] == i, 'Ionization Energy (b) (eV)'].values[0]
        
        # 分配関数
        ground_level_i = data.loc[data['Ion Charge'] == i, 'Ground Level'].values[0]
        ground_level_ip1 = data.loc[data['Ion Charge'] == i + 1, 'Ground Level'].values[0]
        
        Z_i = partition_function(ground_level_i, T)
        Z_ip1 = partition_function(ground_level_ip1, T)
        
        # Saha平衡定数
        K = saha_equation(chi, Z_i, Z_ip1, T, n_e)
        
        # n_{i+1} = K * n_i
        n_relative[i + 1] = K * n_relative[i]
    
    # 規格化（合計が1になるように）
    total = np.sum(n_relative)
    fractions = {i: n_relative[i] / total for i in range(max_charge + 1)}
    
    return fractions


def calculate_average_ionization(fractions):
    """
    平均イオン価数を計算
    
    Parameters
    ----------
    fractions : dict
        各イオン電荷の存在比
    
    Returns
    -------
    z_avg : float
        平均イオン価数
    """
    z_avg = sum(charge * frac for charge, frac in fractions.items())
    return z_avg


def calculate_electron_density_self_consistent(element_data, T, n_total, max_iter=50, tol=1e-6):
    """
    電子密度を自己無撞着に計算
    
    Parameters
    ----------
    element_data : pd.DataFrame
        元素データ
    T : float
        温度 [K]
    n_total : float
        全粒子密度（原子+イオン） [cm^-3]
    max_iter : int
        最大反復回数
    tol : float
        収束判定の閾値
    
    Returns
    -------
    n_e : float
        自己無撞着な電子密度 [cm^-3]
    fractions : dict
        収束後の各イオン状態の存在比
    """
    # 初期推定値（完全電離と仮定）
    max_charge = element_data['Ion Charge'].max()
    n_e = n_total * max_charge / 2  # 半分電離と仮定
    
    for iteration in range(max_iter):
        # 現在の n_e でイオン化率を計算
        fractions = calculate_ionization_fractions(element_data, T, n_e)
        
        # 平均イオン価数から新しい n_e を計算
        z_avg = calculate_average_ionization(fractions)
        n_e_new = n_total * z_avg
        
        # 収束判定
        if abs(n_e_new - n_e) / n_e < tol:
            return n_e_new, fractions
        
        n_e = n_e_new
    
    print(f"Warning: 収束しませんでした（{max_iter}回反復後）")
    return n_e, fractions


# テスト用
if __name__ == "__main__":
    from data_loader import IonizationDatabase
    
    # データベース読み込み
    db = IonizationDatabase('data/ionizationenergy.csv')
    
    # 水素のテスト
    print("=== Hydrogen Ionization Test ===")
    h_data = db.get_element_data('H')
    
    T = 10000  # K
    n_e = 1e15  # cm^-3
    
    fractions = calculate_ionization_fractions(h_data, T, n_e)
    
    print(f"Temperature: {T} K")
    print(f"Electron density: {n_e:.2e} cm^-3")
    print(f"\nIonization fractions:")
    for charge, frac in fractions.items():
        print(f"  Charge +{charge}: {frac:.4f} ({frac*100:.2f}%)")
    
    z_avg = calculate_average_ionization(fractions)
    print(f"\nAverage ionization: {z_avg:.3f}")
    
    # 鉄のテスト
    print("\n=== Iron Ionization Test ===")
    fe_data = db.get_element_data('Fe')
    
    fractions_fe = calculate_ionization_fractions(fe_data, T, n_e)
    
    print(f"Temperature: {T} K")
    print(f"Electron density: {n_e:.2e} cm^-3")
    print(f"\nIonization fractions (top 5):")
    sorted_fractions = sorted(fractions_fe.items(), key=lambda x: x[1], reverse=True)[:5]
    for charge, frac in sorted_fractions:
        print(f"  Fe{'+' if charge > 0 else ''}{charge if charge > 0 else ''}: {frac:.4f} ({frac*100:.2f}%)")
    
    z_avg_fe = calculate_average_ionization(fractions_fe)
    print(f"\nAverage ionization: {z_avg_fe:.3f}")