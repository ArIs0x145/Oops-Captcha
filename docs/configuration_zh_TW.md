# 配置

默認配置位於 `configs/default.yaml`：

```yaml
captcha:
  image:
    width: 160              # 驗證碼寬度
    height: 60              # 驗證碼高度
    length: 4               # 字符數量
    fonts: []               # 自定義字體
    characters: "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    output_dir: "data/image" # 單個驗證碼輸出目錄
    
    # 資料集生成參數
    train_ratio: 0.8        # 訓練集比例
    val_ratio: 0.1          # 驗證集比例
    test_ratio: 0.1         # 測試集比例
    parallel: false         # 啟用並行生成
    max_workers: null       # 最大工作線程數
    seed: null              # 隨機種子
    dataset_output_dir: "data/image_dataset" # 資料集輸出目錄
```

你可以通過程式碼或命令行參數覆蓋這些參數。 