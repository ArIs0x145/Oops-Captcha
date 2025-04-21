# Oops-Captcha

[![版本](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/ArIs0x145/Oops-Captcha)
[![授權](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)

一個靈活且可擴展的 Python 驗證碼（CAPTCHA）生成庫，可用於生成驗證碼圖像和資料集。

## 安裝

### 方法1: 通過GitHub安裝

```bash
pip install git+https://github.com/ArIs0x145/Oops-Captcha.git
```

### 方法2: 本地安裝

```bash
# 克隆儲存庫
git clone https://github.com/ArIs0x145/Oops-Captcha.git
cd Oops-Captcha

# 安裝
pip install .
```

## 快速開始

生成單個驗證碼圖像：

```python
from oopscaptcha.generators.factory import CaptchaFactory
from oopscaptcha.generators.types import CaptchaType

# 創建圖像驗證碼生成器
generator = CaptchaFactory.create(CaptchaType.IMAGE)

# 生成並保存驗證碼
sample_path, label_path = generator.export()
print(f"驗證碼圖像已保存至：{sample_path}")
print(f"驗證碼標籤已保存至：{label_path}")
```

生成驗證碼資料集：

```bash
oops-captcha dataset --type image --size 1000 --parallel
```

## 使用方法

### 生成單個驗證碼

```python
from oopscaptcha.generators.factory import CaptchaFactory
from oopscaptcha.generators.types import CaptchaType

# 創建自定義設置的圖像驗證碼生成器
generator = CaptchaFactory.create(
    CaptchaType.IMAGE,
    width=200,
    height=80,
    length=6,
    characters="0123456789"
)

# 生成並保存
sample_path, label_path = generator.export("custom_output_dir")
```

### 生成驗證碼資料集

通過命令行：

```bash
oops-captcha dataset --type image --size 1000 --train-ratio 0.7 --val-ratio 0.2 --test-ratio 0.1 --parallel --output-dir custom_dataset
```

或通過程式碼：

```python
from oopscaptcha.generators.factory import CaptchaFactory
from oopscaptcha.generators.types import CaptchaType

# 創建圖像驗證碼生成器
generator = CaptchaFactory.create(CaptchaType.IMAGE)

# 生成資料集
dataset = generator.generate_dataset(
    size=1000,
    train_ratio=0.7,
    val_ratio=0.2,
    test_ratio=0.1,
    parallel=True,
    max_workers=4,
    seed=42,
    output_dir="custom_dataset"
)

# 輸出統計資訊
for split, samples in dataset.items():
    print(f"{split}: {len(samples)} 個樣本")
```

## 文檔

更詳細的信息，請參閱[文檔](docs/README_zh_TW.md)：

- [API 參考](docs/api-reference_zh_TW.md)
- [架構](docs/architecture_zh_TW.md)
- [配置](docs/configuration_zh_TW.md)
- [擴展](docs/extending_zh_TW.md)

## 命令行使用

安裝後，您可以使用 `oops-captcha` 命令：

### 生成單個驗證碼

```bash
# --type 參數是必須的
oops-captcha single --type image --output-dir ./output

# 使用自定義設置
oops-captcha single --type image --width 200 --height 80 --length 6 --output-dir ./output
```

### 生成驗證碼數據集

```bash
# 基本用法 (--type 是必須的)
oops-captcha dataset --type image --size 1000 --output-dir ./dataset

# 使用所有參數
oops-captcha dataset --type image --size 1000 --width 200 --height 80 \
  --length 6 --train-ratio 0.7 --val-ratio 0.2 --test-ratio 0.1 \
  --parallel --output-dir ./dataset
```

### 幫助信息

```bash
# 查看主命令幫助
oops-captcha --help

# 查看子命令幫助
oops-captcha single --help
oops-captcha dataset --help
```

## 授權協議

本項目使用 MIT 授權協議 - 詳見 LICENSE 文件。 