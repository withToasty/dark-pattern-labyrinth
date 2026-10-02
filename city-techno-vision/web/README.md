# city-techno-vision web (AWS Lambda)

`detect.py`と同じ検出パイプライン(`src/`)を、API Gateway + Lambdaコンテナ経由で
HTTP APIとして公開する。`static/index.html`は動作確認用の簡易アップロードUI。

音生成(BPM/MIDI/物体→音マッピング)はここには含まれない(スコープ外)。

## 構成

```
web/
  lambda_handler.py   Lambda本体。src/ の関数をそのまま呼び出す
  Dockerfile           Lambdaコンテナイメージ(ビルドコンテキストは city-techno-vision/)
  requirements.txt     Lambda用の依存関係(opencv-python-headless / torch cpu等)
  template.yaml         AWS SAMテンプレート(API Gateway + Lambda)
  static/index.html     動作確認用アップロードページ(別途S3等でホスト)
```

## 前提

- AWS CLI設定済み・SAM CLIインストール済み(`sam --version`)
- Docker起動済み(コンテナイメージビルドに使用)

## デプロイ

```
cd city-techno-vision/web
sam build
sam deploy --guided
```

初回`sam deploy --guided`ではスタック名・リージョンなどを聞かれる。
`samconfig.toml`が生成されるので、2回目以降は`sam deploy`だけでよい。

デプロイ完了時に出力される`ApiUrl`(例:
`https://xxxx.execute-api.ap-northeast-1.amazonaws.com/Prod/detect`)を
`static/index.html`のAPI endpoint欄、またはcurlで使う。

## 動作確認

```
curl -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -d "{\"image_base64\": \"$(base64 -w0 sample.jpg)\"}"
```

`static/index.html`をブラウザで直接開き(`file://`で可)、API endpoint欄に
`ApiUrl`を貼り付けて画像をアップロードしてもよい。ページを外部公開したい場合は
S3静的ウェブサイトホスティングやCloudFrontに置く(このスタックには含めていない)。

## モデルの扱い

`Dockerfile`はビルド時にYOLO重み(`yolov8n-oiv7.pt`)とfence用SegFormer
(`nvidia/segformer-b0-finetuned-cityscapes-1024-1024`)の両方をイメージに
焼き込む。これにより:

- 初回リクエスト(コールドスタート)でモデルダウンロードのネットワーク待ちが発生しない
- VPC内Lambda(NAT Gatewayなし)でも動く
- Hugging Faceへの接続がブロックされる環境でも実行時には影響しない

イメージサイズはtorch/transformers込みで数GBになる(Lambdaコンテナイメージの
上限は10GB)。`--extra-index-url`でCPU版torchを使っているため、GPU版より小さい。

## 設定を変える

`template.yaml`の`Globals.Function`で`MemorySize`/`Timeout`/`EphemeralStorage`を
調整できる。デフォルトはCPU推論(YOLO+SegFormer)が現実的な時間で終わる値として
`MemorySize: 3008`(Lambdaはメモリに比例してCPUも割り当てられる)、
`Timeout: 60`にしている。

## 既知の制約

- リクエスト/レスポンスをbase64のJSONでやり取りしているため、API Gatewayの
  ペイロード上限(現状10MB)より大きい画像は送れない。大きい画像を扱うなら
  S3経由(署名付きURLでアップロード→Lambdaをinvoke)に変更する必要がある
- コールドスタートは(モデルロードが軽くても)数秒かかる。低頻度アクセスの
  個人プロジェクト向け。頻繁に呼ばれるならProvisioned Concurrencyを検討
