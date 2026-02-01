"""
分配関数の計算
Ground Levelの表記から基底状態の縮退度を計算
"""

import re
import numpy as np


def parse_ground_level(ground_level):
    """
    Ground Level表記からJ値と縮退度を計算
    
    Parameters
    ----------
    ground_level : str
        Ground Levelの表記（例: '2S<1/2>', '3P0', '1S0'）
    
    Returns
    -------
    J : float or None
        全角運動量量子数
    g : int or None
        縮退度 (2J + 1)
    
    Examples
    --------
    >>> parse_ground_level('2S<1/2>')
    (0.5, 2)
    >>> parse_ground_level('3P0')
    (0, 1)
    >>> parse_ground_level('3P2')
    (2, 5)
    """
    if not isinstance(ground_level, str):
        return None, None
    
    # <J> 形式（分数表記）
    match = re.search(r'<(\d+)/(\d+)>', ground_level)
    if match:
        numerator = int(match.group(1))
        denominator = int(match.group(2))
        J = numerator / denominator
        g = int(2 * J + 1)
        return J, g
    
    # 末尾の数字（整数J）
    match = re.search(r'(\d+)$', ground_level)
    if match:
        J = int(match.group(1))
        g = 2 * J + 1
        return J, g
    
    # パースできない場合
    return None, None


def get_ground_state_degeneracy(ground_level):
    """
    Ground Levelから基底状態の縮退度のみを取得
    
    Parameters
    ----------
    ground_level : str
        Ground Levelの表記
    
    Returns
    -------
    g : int
        縮退度（パース失敗時は1を返す）
    """
    _, g = parse_ground_level(ground_level)
    return g if g is not None else 1


def partition_function(ground_level, T=None):
    """
    分配関数の計算（基底状態近似）
    
    ICP-OES程度の温度範囲（6000-10000K）では、
    基底状態の縮退度のみで十分な精度
    
    Parameters
    ----------
    ground_level : str
        Ground Levelの表記
    T : float, optional
        温度 [K]（現在は未使用、将来の拡張用）
    
    Returns
    -------
    Z : float
        分配関数
    """
    g0 = get_ground_state_degeneracy(ground_level)
    
    # 現時点では基底状態の縮退度のみ
    # 将来的には温度依存の補正を追加可能
    return float(g0)


# テスト用
if __name__ == "__main__":
    # テストケース
    test_cases = [
        '2S<1/2>',
        '3P0',
        '3P1', 
        '3P2',
        '1S0',
        '2P*<1/2>',
        '2P*<3/2>',
        '4S<3/2>',
    ]
    
    print("Ground Level Parsing Test")
    print("-" * 50)
    print(f"{'Ground Level':<15} {'J':<8} {'g (2J+1)':<10}")
    print("-" * 50)
    
    for level in test_cases:
        J, g = parse_ground_level(level)
        print(f"{level:<15} {J:<8} {g:<10}")