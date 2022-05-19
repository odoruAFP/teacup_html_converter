# teacup_html_converter

【このプログラムについて】<br>
2022年8月1日に閉鎖するteacup掲示板をバックアップ後に再利用できるようにするhtml変換ユーティリティです。<br>

【要件定義】<br>
バックアップツール「Free Download Manager」を使ってバックアップした画像とサムネイルとhtmlファイルを他のサーバーへ引っ越すために
teacup掲示板固有のディレクトリやAタグ、パンくずリストの表記を変換します。<br>
<br>
取得したhtmlファイルは、もっとも書き込みが古いものから3桁のゼロインデックスでファイル名をつける前提で作ってあります。<br>
例)<br>
最も古いhtmlファイル名：odoruAFP_(000).html<br>
最も新しいhtmlファイル名:odoruAFP_(999).html<br>
<br>
ディフォルトでパンくずリストは9リンク（新しいもの4リンクと古いもの5リンク）+前後1ページ分を生成します。<br>
<br>
htmlファイルと画像ファイル、サムネイルのディフォルトのディレクトリは下記のとおりです。<br>
┌──html<br>
├──image_library<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└thmubnails<br>

各関数の説明は下記のとおりです。<br>
conv_breadcrumbs関数<br>
　URLパラメータによって記述されているリンク先をダウンロードしたhtmlファイル名による直リンクに変換します。<br>
<br> 
conv_thumbnail_directory関数<br>
　teacup掲示板ではサムネイルと画像ファイルが同一ディレクトリに入っているため、ファイル名でしか判別できず管理しにくいため別フォルダへ振り分けるためにAタグを変換します。<br>
<br> 
conv_image_directory関数<br>
 teacup掲示板依存の画像ファイル保存ディレクトリを任意のディレクトリ名に変換します。<br>
<br>
decode_url_link関数<br>
　teacup掲示板では、フィッシングサイトへの誘導を回避するために書き込み内に記述されたURLに直接リンクさせないための記述が追加されています。また、2バイト文字はURLエンコードされています。それらを適切に変換して直接リンクされるように変換します。<br>
<br> 
conv_thread_directory<br>
　掲示板内でスレッドを作成した場合に適切にリンクできるように変換します。<br>
<br>
conv_return_bbs_directory<br>
　スレッドから掲示板へ戻ることができるようにhtmlを変換します。<br>
<br> 
conv_html_title<br>
　掲示板のタイトルを変換します。<br>
<br>
<br>
【重要なお知らせ】teacup. byGMOのサービス終了につきまして※追記あり（2022/3/25）(3月01日 14時00分)<br>
https://www.teacup.com/information/view?id=243<br>
<br>
掲示版の記事を他のサイトに移行したい<br>
https://support.teacup.com/hc/ja/articles/4544682345497-%E6%8E%B2%E7%A4%BA%E7%89%88%E3%81%AE%E8%A8%98%E4%BA%8B%E3%82%92%E4%BB%96%E3%81%AE%E3%82%B5%E3%82%A4%E3%83%88%E3%81%AB%E7%A7%BB%E8%A1%8C%E3%81%97%E3%81%9F%E3%81%84
