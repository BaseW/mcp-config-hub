# バイナリ化手順（PyInstaller）

このプロジェクトをスタンドアロンバイナリとしてビルドするには、以下の手順を実行してください。

## 1. 依存パッケージのインストール

```sh
uv pip install -e .[dev]
```

## 2. バイナリのビルド

```sh
bash scripts/build_binary.sh
```

- `dist/mcp-config-hub` にバイナリが生成されます。
- macOSでビルドした場合、他OS向けバイナリは別途そのOS上でビルドしてください。

## 3. 注意事項
- 依存パッケージの更新があった場合は再ビルドしてください。
- ビルドに失敗する場合は `pyinstaller` のバージョンや依存パッケージの競合を確認してください。
- `uv` を利用している場合、`uv pip install` で依存を管理してください。

## 4. 今後の課題
- Windows/Linux向けバイナリのビルド手順追加
- CI/CDによる自動ビルド対応
- Nuitka, cx_Freeze等の他ツール検証
