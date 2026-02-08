"""
データ読み込みモジュール
NIST Atomic Spectra Database (イオン化エネルギー) の読み込み
"""

import pandas as pd
import numpy as np
from pathlib import Path


class IonizationDatabase:
    """
    イオン化エネルギーデータベース
    """
    
    def __init__(self, csv_path='data/ionizationenergy.csv'):
        """
        Parameters
        ----------
        csv_path : str
            CSVファイルのパス
        """
        self.csv_path = csv_path
        self.df = None
        self.load_data()
    
    def load_data(self):
        """CSVファイルを読み込む"""
        try:
            self.df = pd.read_csv(self.csv_path, delimiter='\t')
            # カラム名のクリーニング（空白除去）
            self.df.columns = self.df.columns.str.strip()
            print(f"✓ データ読み込み成功: {len(self.df)} レコード")
        except FileNotFoundError:
            raise FileNotFoundError(f"ファイルが見つかりません: {self.csv_path}")
        except Exception as e:
            raise Exception(f"データ読み込みエラー: {e}")
    
    def get_element_list(self):
        """
        利用可能な元素のリストを取得
        
        Returns
        -------
        elements : list
            元素記号のリスト（無料版は6元素のみ）
        """
        all_elements = self.df['Element'].unique()
        all_elements = sorted(all_elements)
        
        # 無料版：6元素のみ
        # Pro版では全118元素が利用可能
        FREE_ELEMENTS = ['H', 'He', 'Ne', 'Cr', 'Fe', 'Cu']
        
        return [e for e in all_elements if e in FREE_ELEMENTS]
    
    def get_element_data(self, element_symbol):
        """
        特定元素の全イオン状態のデータを取得
        
        Parameters
        ----------
        element_symbol : str
            元素記号（例: 'H', 'He', 'Fe'）
        
        Returns
        -------
        data : pd.DataFrame
            該当元素のデータ（Ion Charge順にソート）
        """
        element_data = self.df[self.df['Element'] == element_symbol].copy()
        element_data = element_data.sort_values('Ion Charge')
        return element_data
    
    def get_ionization_energy(self, element_symbol, ion_charge):
        """
        特定のイオン化エネルギーを取得
        
        Parameters
        ----------
        element_symbol : str
            元素記号
        ion_charge : int
            イオン電荷（0=中性原子, 1=1価イオン, ...）
        
        Returns
        -------
        ionization_energy : float
            イオン化エネルギー [eV]
        """
        data = self.df[
            (self.df['Element'] == element_symbol) & 
            (self.df['Ion Charge'] == ion_charge)
        ]
        
        if len(data) == 0:
            return None
        
        return data.iloc[0]['Ionization Energy (b) (eV)']
    
    def get_ground_level(self, element_symbol, ion_charge):
        """
        基底準位の表記を取得
        
        Parameters
        ----------
        element_symbol : str
            元素記号
        ion_charge : int
            イオン電荷
        
        Returns
        -------
        ground_level : str
            Ground Levelの表記
        """
        data = self.df[
            (self.df['Element'] == element_symbol) & 
            (self.df['Ion Charge'] == ion_charge)
        ]
        
        if len(data) == 0:
            return None
        
        return data.iloc[0]['Ground Level']
    
    def get_element_name(self, element_symbol):
        """
        元素名を取得
        
        Parameters
        ----------
        element_symbol : str
            元素記号
        
        Returns
        -------
        element_name : str
            元素名（英語）
        """
        data = self.df[self.df['Element'] == element_symbol]
        
        if len(data) == 0:
            return None
        
        return data.iloc[0]['El. Name']
    
    def get_max_ion_charge(self, element_symbol):
        """
        該当元素の最大イオン電荷を取得
        
        Parameters
        ----------
        element_symbol : str
            元素記号
        
        Returns
        -------
        max_charge : int
            最大イオン電荷
        """
        element_data = self.get_element_data(element_symbol)
        return element_data['Ion Charge'].max()


# テスト用
if __name__ == "__main__":
    # データベース読み込みテスト
    db = IonizationDatabase()
    
    print("\n=== Element List ===")
    elements = db.get_element_list()
    print(f"Total elements: {len(elements)}")
    print(f"First 10: {elements[:10]}")
    
    print("\n=== Hydrogen Data ===")
    h_data = db.get_element_data('H')
    print(h_data[['Element', 'Ion Charge', 'Ground Level', 'Ionization Energy (b) (eV)']])
    
    print("\n=== Iron Data (first 5 ion states) ===")
    fe_data = db.get_element_data('Fe')
    print(fe_data[['Element', 'Ion Charge', 'Ground Level', 'Ionization Energy (b) (eV)']].head())
    
    print(f"\n=== Individual Data Access ===")
    print(f"H I ionization energy: {db.get_ionization_energy('H', 0)} eV")
    print(f"H I ground level: {db.get_ground_level('H', 0)}")
    print(f"Fe max ion charge: {db.get_max_ion_charge('Fe')}")
