#!/usr/bin/env python3
"""
簡易Web検索スクリプト
使い方: python web_search.py "バリューブックス 中村大樹"
"""

import sys
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup

def search_google(query):
    """Googleで検索して結果のタイトルとURLを取得"""
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.google.com/search?q={encoded_query}&hl=ja"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    try:
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request, timeout=10) as response:
            html = response.read().decode('utf-8')
        
        soup = BeautifulSoup(html, 'html.parser')
        
        print(f"\n🔍 検索結果: {query}\n")
        print("=" * 60)
        
        # 検索結果を取得
        results = soup.find_all('div', class_='g')
        
        for i, result in enumerate(results[:10], 1):
            title_elem = result.find('h3')
            link_elem = result.find('a')
            
            if title_elem and link_elem:
                title = title_elem.get_text()
                link = link_elem.get('href')
                
                if link and link.startswith('http'):
                    print(f"\n{i}. {title}")
                    print(f"   {link}")
        
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        print("\n💡 ヒント: BeautifulSoup4が必要です:")
        print("   pip install beautifulsoup4")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使い方: python web_search.py '検索キーワード'")
        sys.exit(1)
    
    query = " ".join(sys.argv[1:])
    search_google(query)


