<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/images/icon-rounded-dark.svg" width="140">
    <source media="(prefers-color-scheme: light)" srcset="docs/images/icon-rounded-light.svg" width="140">
    <img alt="oMLX" src="docs/images/icon-rounded-light.svg" width="140">
  </picture>
</p>

<h1 align="center">oMLX</h1>
<p align="center"><b>Mac向けに最適化されたLLM推論サーバー</b><br>連続バッチングと階層型KVキャッシュを、メニューバーから直接管理します。</p>

<p align="center">
  <img src="https://img.shields.io/badge/license-Apache%202.0-blue" alt="License">
  <img src="https://img.shields.io/badge/python-3.10+-green" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/platform-Apple%20Silicon-black?logo=apple" alt="Apple Silicon">
  <a href="https://buymeacoffee.com/jundot"><img src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?logo=buy-me-a-coffee&logoColor=black" alt="Buy Me a Coffee"></a>
</p>

<p align="center">
  <a href="mailto:junkim.dot@gmail.com">junkim.dot@gmail.com</a> · <a href="https://omlx.ai/me">https://omlx.ai/me</a>
</p>

<p align="center">
  <a href="#インストール">インストール</a> ·
  <a href="#クイックスタート">クイックスタート</a> ·
  <a href="#機能">機能</a> ·
  <a href="#モデル">モデル</a> ·
  <a href="#cli-設定">CLI 設定</a> ·
  <a href="https://omlx.ai/benchmarks">ベンチマーク</a> ·
  <a href="https://omlx.ai">oMLX.ai</a>
</p>

<p align="center">
  <a href="README.md">English</a> ·
  <a href="README.zh.md">中文</a> ·
  <a href="README.ko.md">한국어</a> ·
  <b>日本語</b>
</p>

---

<p align="center">
  <img src="docs/images/omlx_dashboard.png" alt="oMLX 管理画面" width="800">
</p>

> *これまで試したLLMサーバーは、利便性とコントロールのどちらかを選ばせるものでした。よく使うモデルをメモリにピン留めし、重いモデルは必要に応じて自動スワップし、コンテキスト制限を設定して、すべてをメニューバーから管理したかったのです。*
>
> *oMLXはKVキャッシュをホットなメモリ層とコールドなSSD層の2階層で永続化します。会話中にコンテキストが変わっても、すべての過去のコンテキストはキャッシュされ、リクエスト間で再利用可能です。これによりClaude Codeのようなツールでの実際のコーディング作業において、ローカルLLMが実用的になります。だから作りました。*

## インストール

### macOSアプリ

[Releases](https://github.com/jundot/omlx/releases)から`.dmg`をダウンロードし、Applicationsにドラッグするだけです。アプリ内自動アップデートに対応しているので、以降のアップグレードはワンクリックで完了します。macOSアプリには`omlx` CLIコマンドは含まれていません。ターミナルで使用するにはHomebrewまたはソースからインストールしてください。

### Homebrew

```bash
brew tap jundot/omlx https://github.com/jundot/omlx
brew install omlx

# 最新バージョンへアップグレード
brew update && brew upgrade omlx

# バックグラウンドサービスとして実行（クラッシュ時に自動再起動）
brew services start omlx

# オプション: MCP（Model Context Protocol）サポート
/opt/homebrew/opt/omlx/libexec/bin/pip install mcp
```

### ソースからインストール

```bash
git clone https://github.com/jundot/omlx.git
cd omlx
pip install -e .          # コアのみ
pip install -e ".[mcp]"   # MCP（Model Context Protocol）サポート付き
```

Python 3.10+とApple Silicon（M1/M2/M3/M4）が必要です。

> **メモ:** M1 Maxで動作確認済み。uvを使った仮想環境（`uv venv && uv pip install -e .`）でインストールするとpipより大幅に速いのでおすすめです。
>
> **個人メモ:** M2 Proでも問題なく動作することを確認しました。uvでのインストールは特におすすめです。また、ソースからインストールする場合はPython 3.11を使うと依存関係の解決が安定していました（3.12ではmlxのビルドで稀にエラーが出ることがあります）。
>
> **追記:** `uv venv --python 3.11` で明示的にバージョンを指定してからインストールするのが一番トラブルが少なかったです。`uv venv --python 3.11 && source .venv/bin/activate && uv pip install -e .` の順で実行するとスムーズです。
