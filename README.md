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
make install
```

### パッケージとしてのインストール

```bash
uv tool install git+https://github.com/chatflip/LrUtility.git
```

## 使用方法

### レーティング1の画像ファイル削除

```bash
lru delete-rate-1 /path/to/photos
lru delete-rate-1 /path/to/photos --dry-run  # 削除せずに確認
lru delete-rate-1 /path/to/photos --verbose  # 詳細ログ
```

### ファイル分割・ZIPアーカイブ化

```bash
lru zip-chunker /path/to/directory                          # デフォルト20GB
lru zip-chunker /path/to/directory --size-chunk 10737418240 # 10GBに指定
```

### ヘルプ

```bash
lru --help              # 全体のヘルプ
lru delete-rate-1 --help
lru zip-chunker --help
```

## ライセンス

このプロジェクトは[MITライセンス](LICENSE)の下で公開されています。

## 作者

[chatflip](https://github.com/chatflip)

## 注意事項

- **重要**: `lru delete-rate-1`コマンドは実際にファイルを削除します。必ず事前に`--dry-run`オプションで動作を確認してください。
- XMPファイルは写真編集ソフトウェア（Adobe Lightroom、Camera Raw等）で生成されるメタデータファイルです。
- このツールはAdobe Lightroomのワークフローを前提として設計されています。
