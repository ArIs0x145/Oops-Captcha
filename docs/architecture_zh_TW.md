# 架構

本項目遵循面向對象設計模式，包括工廠模式和抽象基類。

## 核心組件

1. **驗證碼生成器**：負責生成和保存驗證碼
2. **配置管理**：處理應用程序配置和參數
3. **工廠類**：創建和配置適當的驗證碼生成器
4. **資料集生成**：創建訓練、驗證和測試資料集
5. **ID 生成器**：生成唯一標識符和管理時間戳

## 目錄結構

```
Oops-Captcha/
├── configs/                  # 配置文件目錄
│   └── default.yaml          # 默認配置
├── data/                     # 數據存儲目錄
├── oopscaptcha/              # 主包目錄
│   ├── config/               # 配置處理模塊
│   │   └── settings.py       # 設置管理類
│   ├── generators/           # 驗證碼生成器模塊
│   │   ├── base.py           # 生成器抽象基類
│   │   ├── factory.py        # 生成器工廠類
│   │   ├── image.py          # 圖像驗證碼生成器
│   │   └── types.py          # 驗證碼類型定義
│   └── utils/                # 工具類
│       └── id_generator.py   # ID生成器
└── tests/                    # 測試目錄
    ├── test_*.py             # 各種測試模塊
    └── generate_dataset.py   # 資料集生成工具
```

## 目錄時間戳功能

為了組織生成的文件，系統使用時間戳目錄：
1. 單個驗證碼保存在 `output_dir/{timestamp}/samples` 和 `output_dir/{timestamp}/labels` 目錄中
2. 資料集保存在 `dataset_output_dir/{timestamp}/<split>` 目錄中，其中 `<split>` 為 `train`、`val` 或 `test` 