# LrUtility

Adobe Lightroomで使用されるXMPファイルを解析し、画像ファイル管理を効率化するPythonユーティリティです。

## 特徴

- **XMPファイル解析**: Adobe LightroomのXMPメタデータファイルから詳細な情報を抽出
- **レーティング管理**: 指定されたレーティング（評価）の画像ファイルを一括削除
- **ファイル分割**: 大容量ディレクトリ内のファイルをサイズ指定でZIPアーカイブに分割

## 動作環境

- Python >= 3.11
- uv >= 0.8

## インストール

### 開発環境のセットアップ

```bash
uv sync
pre-commit install
```

### パッケージとしてのインストール

```bash
uv tool install git+https://github.com/chatflip/LrUtility.git
```

## 使用方法

### 1. レーティング1の画像ファイル削除

Adobe Lightroomでレーティング1を付けた画像ファイルとXMPファイルを一括削除します。

- `directory`: 検索対象のディレクトリパス
- `-d, --dry_run`: ドライランモード（実際に削除せずに対象ファイルを表示）
- `-v, --verbose`: 詳細ログの有効化（DEBUGレベル）

```bash
# 基本的な使用方法
delete_rate_1 /path/to/photos

# ドライランモード（実際に削除せずに対象ファイルを表示）
delete_rate_1 /path/to/photos --dry_run

# 詳細ログを有効にして実行
delete_rate_1 /path/to/photos --verbose
```

### 2. ファイル分割・ZIPアーカイブ化

ディレクトリ内のファイルを指定サイズごとにZIPアーカイブに分割します。

- `directory`: 検索対象のディレクトリパス
- `-v, --verbose`: 詳細ログの有効化（DEBUGレベル）

```bash
# 基本的な使用方法（デフォルト20GB）
zip_chunker /path/to/directory

# チャンクサイズを指定（10GBに設定）
zip_chunker /path/to/directory --size_chunk 10737418240

# 詳細ログを有効にして実行
zip_chunker /path/to/directory --verbose
```

### オプション

- `directory`: 対象ディレクトリパス
- `-s, --size_chunk`: チャンクサイズ（バイト単位、デフォルト: 20GB）
- `-v, --verbose`: 詳細ログの有効化（DEBUGレベル）

## ライセンス

このプロジェクトは[MITライセンス](LICENSE)の下で公開されています。

## 作者

[chatflip](https://github.com/chatflip)

## 注意事項

- **重要**: `delete_rate_1`コマンドは実際にファイルを削除します。必ず事前に`--dry_run`オプションで動作を確認してください。
- XMPファイルは写真編集ソフトウェア（Adobe Lightroom、Camera Raw等）で生成されるメタデータファイルです。
- このツールはAdobe Lightroomのワークフローを前提として設計されています。
