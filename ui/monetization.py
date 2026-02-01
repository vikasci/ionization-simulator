"""
収益化コンポーネント
寄付ボタン、広告、アフィリエイトリンク
"""

import streamlit as st
import streamlit.components.v1 as components


def display_kofi_button():
    """
    Ko-fi寄付ボタンを表示
    
    TODO: 自分のKo-fiユーザーネームに置き換える
    """
    kofi_html = """
    <div style="text-align: center; padding: 10px;">
        <a href='https://ko-fi.com/YOUR_USERNAME' target='_blank'>
            <img height='36' style='border:0px;height:36px;' 
                 src='https://storage.ko-fi.com/cdn/kofi2.png?v=3' 
                 border='0' alt='Buy Me a Coffee at ko-fi.com' />
        </a>
    </div>
    
    <!-- 実際のKo-fiボタン（アカウント作成後に置き換え）
    <script src='https://storage.ko-fi.com/cdn/scripts/overlay-widget.js'></script>
    <script>
      kofiWidgetOverlay.draw('YOUR_USERNAME', {
        'type': 'floating-chat',
        'floating-chat.donateButton.text': 'Support Us',
        'floating-chat.donateButton.background-color': '#00b9fe',
        'floating-chat.donateButton.text-color': '#fff'
      });
    </script>
    -->
    """
    
    components.html(kofi_html, height=60)


def display_buymeacoffee_button():
    """
    Buy Me a Coffee寄付ボタンを表示（代替案）
    
    TODO: 自分のユーザーネームに置き換える
    """
    bmc_html = """
    <div style="text-align: center; padding: 10px;">
        <a href="https://www.buymeacoffee.com/YOUR_USERNAME" target="_blank">
            <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" 
                 alt="Buy Me A Coffee" 
                 style="height: 50px !important;width: 180px !important;">
        </a>
    </div>
    """
    
    components.html(bmc_html, height=80)


def display_ethicalads():
    """
    EthicalAds広告を表示
    
    TODO: EthicalAds承認後、実際のコードに置き換える
    """
    # プレースホルダー
    ethicalads_html = """
    <div style="
        width: 100%;
        min-height: 120px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-family: sans-serif;
        text-align: center;
        padding: 15px;
        box-sizing: border-box;
        margin: 10px 0;
    ">
        <div>
            <p style="margin: 0; font-size: 14px; font-weight: 600;">
                Advertisement Space
            </p>
            <p style="margin: 5px 0 0 0; font-size: 12px; opacity: 0.9;">
                EthicalAds will appear here after approval
            </p>
        </div>
    </div>
    
    <!-- 実際のEthicalAdsコード（承認後に置き換え）
    <div data-ea-publisher="your-publisher-id" 
         data-ea-type="image" 
         data-ea-style="stickybox"></div>
    <script async src="https://media.ethicalads.io/media/client/ethicalads.min.js"></script>
    -->
    """
    
    components.html(ethicalads_html, height=140)


def display_amazon_affiliate_books():
    """
    Amazon Associate 関連書籍リンク
    
    TODO: 実際のアフィリエイトリンクに置き換える
    """
    st.markdown("### 📚 Recommended Books")
    
    books = [
        {
            "title": "Inductively Coupled Plasma Spectrometry and its Applications",
            "author": "Steve J. Hill",
            "link": "https://www.amazon.com/dp/1841273783",  # TODO: アフィリエイトタグ追加
            "image": "https://via.placeholder.com/100x150.png?text=Book+1"
        },
        {
            "title": "Plasma Spectroscopy",
            "author": "Hans R. Griem",
            "link": "https://www.amazon.com/dp/0521455049",  # TODO: アフィリエイトタグ追加
            "image": "https://via.placeholder.com/100x150.png?text=Book+2"
        },
        {
            "title": "Introduction to Plasma Physics and Controlled Fusion",
            "author": "Francis F. Chen",
            "link": "https://www.amazon.com/dp/3319223089",  # TODO: アフィリエイトタグ追加
            "image": "https://via.placeholder.com/100x150.png?text=Book+3"
        }
    ]
    
    # カード形式で表示
    for book in books:
        book_html = f"""
        <div style="
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
            display: flex;
            align-items: center;
            background: white;
        ">
            <div style="flex-shrink: 0; margin-right: 15px;">
                <img src="{book['image']}" 
                     alt="{book['title']}" 
                     style="width: 80px; height: 120px; border-radius: 4px;">
            </div>
            <div style="flex-grow: 1;">
                <h4 style="margin: 0 0 5px 0; font-size: 16px;">
                    {book['title']}
                </h4>
                <p style="margin: 0 0 10px 0; font-size: 13px; color: #666;">
                    by {book['author']}
                </p>
                <a href="{book['link']}" 
                   target="_blank" 
                   style="
                       display: inline-block;
                       padding: 8px 16px;
                       background: #FF9900;
                       color: white;
                       text-decoration: none;
                       border-radius: 4px;
                       font-size: 13px;
                       font-weight: 600;
                   ">
                    View on Amazon
                </a>
            </div>
        </div>
        """
        
        components.html(book_html, height=160)


def display_support_section():
    """
    サポートセクション全体を表示
    サイドバー用
    """
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ☕ Support This Project")
    
    st.sidebar.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea22 0%, #764ba222 100%);
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    ">
        <p style="margin: 0; font-size: 13px; line-height: 1.6;">
            This app is <strong>free and open-source</strong>. 
            If you find it useful, consider supporting its development!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 寄付ボタン
    display_kofi_button()
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📢 Advertisement")
    
    # EthicalAds
    display_ethicalads()


def display_footer_books():
    """
    フッターに関連書籍を表示
    メインエリア用
    """
    with st.expander("📚 Recommended Reading"):
        st.markdown("""
        Learn more about plasma spectroscopy and ICP-OES with these comprehensive resources:
        """)
        
        display_amazon_affiliate_books()
        
        st.markdown("""
        <p style="font-size: 11px; color: #666; margin-top: 15px;">
        <em>As an Amazon Associate, we earn from qualifying purchases.</em>
        </p>
        """, unsafe_allow_html=True)
