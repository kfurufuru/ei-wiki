# インタラクティブ計算ツール追加

ei-wikiにHTML/JSベースの計算ツールを追加する手順。

## 引数

- `$ARGUMENTS`: ツール名と用途（例: "cable-sizing ケーブル選定計算"）

## 手順

1. `docs/reference/` 配下にMarkdownファイルを作成
   - 学習コンテンツ（理論解説）を上部に配置
   - 計算ツール（HTML/JS/CSS）を下部に埋め込み

2. HTML/JS計算ツールの構成:
   ```html
   <div class="calculator-container">
     <h3>計算ツール名</h3>
     <div class="input-group">
       <label>入力項目</label>
       <input type="number" id="input1" placeholder="値を入力">
     </div>
     <button onclick="calculate()">計算</button>
     <div id="result"></div>
   </div>

   <style>
   /* レスポンシブ対応のCSS */
   </style>

   <script>
   function calculate() {
     // 入力バリデーション必須
     // 計算ロジック
     // 結果表示
   }
   </script>
   ```

3. `mkdocs.yml` の nav に追加

4. レスポンシブデザインとバリデーションの動作確認

## 設計原則

- 単一ファイル内にHTML/JS/CSSをすべて含める
- 入力値のバリデーションは必須
- モバイル対応のレイアウト
- 計算根拠（公式・規格）を学習コンテンツとして併記
