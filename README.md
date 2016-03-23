# Gracenote検索用バッチ
##動作環境
Python2.7＋django1.4以降
要GracenoteAPIキー　※Sign up して取得してください。

##事前設定
* Gracenote/Gracenote/settings.py  
API_CLIENT_IDにGracenoteにサインアップして取得したAPIキーを設定してください。

* Gracenote/Gracenote/grace.d/data/inputMZ.txtを配置  
inputMZ.txtには検索したいトラック名アーティスト名を1行ごとにTSV形式で記載してください。  

>例：inputMZ.txt　\tはタブ区切り  
>A-La Coltrane\tJazz Co/Op  
>All Of Me\tJoan Monne Trio  
>All The Things You Are\tElfa's Voices & Jazz Band  
>Amalgam\tDudley Moore Trio  
>Apache\tIncredible Bongo Band  
>Aura\t3io  
>Autmn Leave's\tBill Evans   

##Usage
python manage.py search

結果は標準出力に出力されます。



