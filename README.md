# Ionization Rate Simulator

Saha方程式を用いたプラズマ中のイオン化率計算シミュレーター

## 機能
- 全元素のイオン化率計算
- 温度・電子密度依存性の可視化
- プリセット条件（ICP, アーク放電など）

## インストール
```bash
pip install -r requirements.txt
```

## 使い方
```bash
streamlit run app.py
```

## データソース
- NIST Atomic Spectra Database (イオン化エネルギー)
```

### 3. `.gitignore`
```
__pycache__/
*.py[cod]
*$py.class
.venv/
venv/
env/
.env
.DS_Store
*.csv~
.streamlit/