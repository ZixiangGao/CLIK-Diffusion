# CLIK-Diffusion 任务执行指南

## 任务概述

本指南将帮助您理解并执行 CLIK-Diffusion 牙齿矫正任务。CLIK-Diffusion 是一个基于扩散模型的自动化牙齿矫正方案预测系统，能够根据患者矫正前的牙齿位置，自动预测矫正后的理想牙齿位置。

## 任务介绍

### 什么是牙齿矫正？
牙齿矫正（Tooth Alignment）是口腔医学中的重要治疗方案，旨在将患者不整齐或错位的牙齿调整到理想的位置。传统上，这个过程需要口腔医生根据经验和临床知识手动规划治疗方案，既耗时又需要专业技能。

### CLIK-Diffusion 如何解决这个问题？
CLIK-Diffusion 采用了创新的三阶段方法：

1. **地标点检测**：自动识别每颗牙齿上的关键位置点
2. **扩散模型预测**：使用深度学习模型预测矫正后的地标点位置
3. **刚体变换**：计算并应用变换，生成矫正后的牙齿模型

这个过程融合了临床知识，确保预测结果符合牙科治疗的专业标准。

## 执行任务

### 前置要求

1. **硬件要求**
   - GPU：建议使用 NVIDIA GPU（CUDA 11.3 或更高版本）
   - 内存：至少 8GB RAM
   - 存储：至少 5GB 可用空间（用于模型和数据）

2. **软件要求**
   - Python 3.7 或更高版本
   - CUDA 11.3（如果使用 GPU）

### 步骤 1：环境准备

#### 1.1 克隆仓库
```bash
git clone https://github.com/ShanghaiTech-IMPACT/CLIK-Diffusion.git
cd CLIK-Diffusion
```

#### 1.2 创建 Python 环境
```bash
# 使用 conda（推荐）
conda create -n tooth python=3.8
conda activate tooth

# 或使用 venv
python -m venv tooth_env
source tooth_env/bin/activate  # Linux/Mac
# 或
tooth_env\Scripts\activate  # Windows
```

#### 1.3 安装依赖包
```bash
# 安装 PyTorch（GPU 版本）
pip install torch==1.10.0+cu113 torchvision==0.11.1+cu113 -f https://download.pytorch.org/whl/torch_stable.html

# 安装其他依赖
pip install -r requirements.txt
```

如果只有 CPU，安装：
```bash
pip install torch==1.10.0+cpu torchvision==0.11.1+cpu -f https://download.pytorch.org/whl/torch_stable.html
```

### 步骤 2：下载模型

#### 2.1 获取模型文件
从 Google Drive 下载所有模型检查点：
https://drive.google.com/drive/folders/1o9tVJ6p8Jbad3gu0ZUkX0tE5dp7Vkh9g?usp=sharing

需要下载 5 个文件：
- `incisor-e965.pt` - 门牙地标点检测模型（~50MB）
- `cuspid-e920.pt` - 尖牙地标点检测模型（~50MB）
- `premolar-e999.pt` - 前磨牙地标点检测模型（~50MB）
- `molar-e951.pt` - 磨牙地标点检测模型（~50MB）
- `diffusion-e20000.pth` - 扩散模型（~100MB）

#### 2.2 放置模型文件
创建检查点目录（如果不存在）：
```bash
mkdir -p Code/checkpoint
```

将下载的 5 个文件放入 `Code/checkpoint/` 目录：
```
Code/
└── checkpoint/
    ├── incisor-e965.pt
    ├── cuspid-e920.pt
    ├── premolar-e999.pt
    ├── molar-e951.pt
    └── diffusion-e20000.pth
```

### 步骤 3：准备输入数据

#### 3.1 数据格式要求
- 文件格式：.obj（三维网格格式）
- 每颗牙齿一个单独的文件
- 文件命名：按照牙齿编号命名（如 11.obj, 12.obj 等）

#### 3.2 使用示例数据
仓库已包含两个示例患者数据：
- `Data/256/` - 患者 256 的牙齿数据
- `Data/275/` - 患者 275 的牙齿数据

查看数据内容：
```bash
ls Data/275/
```

您应该看到多个 .obj 文件，每个代表一颗牙齿。

### 步骤 4：执行任务

#### 方法 A：使用演示脚本（推荐新手）

演示脚本会自动检查环境并运行任务：

```bash
# 基本用法（使用默认患者 275）
python demo.py

# 指定患者并可视化地标点
python demo.py --patient 275 --visualize

# 自定义输出目录
python demo.py --patient 275 --output ./MyResults
```

演示脚本会：
1. ✓ 检查 Python 版本和依赖包
2. ✓ 验证模型文件是否存在
3. ✓ 确认输入数据可用
4. ✓ 运行完整的推理流程
5. ✓ 显示结果位置

#### 方法 B：直接运行推理脚本

如果您熟悉深度学习流程，可以直接运行：

```bash
# 基本推理
python Code/infer.py -i "./Data/275" -o "./Output"

# 带地标点可视化
python Code/infer.py -i "./Data/275" -o "./Output" -v

# 使用不同患者
python Code/infer.py -i "./Data/256" -o "./Output" -v
```

### 步骤 5：查看结果

#### 5.1 输出位置
结果默认保存在 `Output/` 目录下，按患者ID组织：
```
Output/
└── 275/
    ├── 11_transformed.obj
    ├── 12_transformed.obj
    ├── ...
    ├── transformation_matrix_11.npy
    ├── transformation_matrix_12.npy
    └── ...
```

#### 5.2 输出文件说明
- `*_transformed.obj` - 矫正后的牙齿网格模型
- `transformation_matrix_*.npy` - 对应的变换矩阵
- `landmarks_*.ply`（如果使用 -v）- 检测到的地标点可视化

#### 5.3 可视化结果
您可以使用以下工具打开 .obj 文件：
- **MeshLab**（免费，跨平台）
- **Blender**（免费，功能强大）
- **CloudCompare**（免费，专业）
- 在线查看器：https://3dviewer.net/

## 任务执行流程详解

### 阶段 1：地标点检测（约 10-30 秒）
```
输入：矫正前的牙齿网格
↓
处理：针对每颗牙齿运行对应的检测网络
- 门牙 → incisor-e965.pt
- 尖牙 → cuspid-e920.pt
- 前磨牙 → premolar-e999.pt
- 磨牙 → molar-e951.pt
↓
输出：每颗牙齿的关键地标点坐标
```

### 阶段 2：扩散模型预测（约 30-60 秒）
```
输入：检测到的地标点 + 牙齿特征
↓
处理：使用扩散模型生成目标位置
- 应用牙弓层次约束
- 应用牙齿间约束
- 应用单牙约束
↓
输出：预测的矫正后地标点坐标
```

### 阶段 3：刚体变换（约 5-10 秒）
```
输入：初始地标点 + 目标地标点 + 原始网格
↓
处理：求解最优刚体变换矩阵
- 计算旋转矩阵
- 计算平移向量
- 应用变换到网格
↓
输出：矫正后的牙齿网格
```

## 常见问题与解决

### Q1: 环境检查失败
**问题**：运行 demo.py 提示缺少依赖包

**解决**：
```bash
# 确保激活了正确的 Python 环境
conda activate tooth  # 或您的环境名称

# 重新安装依赖
pip install -r requirements.txt
```

### Q2: 模型文件缺失
**问题**：提示找不到检查点文件

**解决**：
1. 确认已从 Google Drive 下载所有 5 个文件
2. 检查文件路径：`Code/checkpoint/` 目录必须存在
3. 验证文件名完全匹配（包括扩展名）

### Q3: CUDA 错误
**问题**：提示 CUDA 相关错误

**解决**：
```bash
# 检查 CUDA 是否可用
python -c "import torch; print(torch.cuda.is_available())"

# 如果返回 False，安装 CPU 版本的 PyTorch
pip uninstall torch torchvision
pip install torch==1.10.0+cpu torchvision==0.11.1+cpu -f https://download.pytorch.org/whl/torch_stable.html
```

### Q4: 内存不足
**问题**：运行时内存溢出

**解决**：
- 关闭其他占用内存的程序
- 如果使用 GPU，确保 GPU 内存充足（建议 6GB+）
- 考虑在 CPU 上运行（会更慢但内存需求更低）

### Q5: 输入数据格式错误
**问题**：无法读取输入文件

**解决**：
1. 确保输入文件为 .obj 格式
2. 检查文件编码（应为 UTF-8）
3. 参考 `Data/275/` 中的示例格式

## 进阶使用

### 自定义参数
```bash
python Code/infer.py \
  -i "./Data/275" \
  -o "./CustomOutput" \
  -v \
  --seed 42 \
  --incisor_ckpt "path/to/custom/incisor.pt" \
  --diffusion_ckpt "path/to/custom/diffusion.pth"
```

### 批量处理
创建脚本 `batch_process.sh`：
```bash
#!/bin/bash
for patient in Data/*; do
  patient_id=$(basename $patient)
  echo "Processing patient $patient_id..."
  python Code/infer.py -i "$patient" -o "./BatchOutput"
done
```

运行：
```bash
chmod +x batch_process.sh
./batch_process.sh
```

### Python 脚本调用
```python
import os
from model.core_util import set_seed
from s1_LandmarkDetection import load_detection, detect_one_patient
from s2_LandmarkDiffusion import load_diffusion, organize_input, query_points, diffusion_one_patient
from s3_SolveMatrix import solve_and_trans_mesh, save_mesh

# 设置参数
patient_dir = "./Data/275"
output_dir = "./Output"

# 运行推理
# ... 参考 Code/infer.py 的实现
```

## 性能优化建议

1. **使用 GPU**：在支持 CUDA 的 GPU 上运行可提速 10-50 倍
2. **批量处理**：一次处理多个患者数据更高效
3. **缓存模型**：避免重复加载模型检查点
4. **调整采样数**：在 `infer.py` 中可调整 `num_samples` 参数平衡速度和精度

## 引用与致谢

如果本项目对您的研究有帮助，请引用我们的论文：

```bibtex
@article{DOU2025103746,
  title = {CLIK-Diffusion: Clinical Knowledge-informed Diffusion Model for Tooth Alignment},
  author = {Yulong Dou and Han Wu and Changjian Li and Chen Wang and Tong Yang and Min Zhu and Dinggang Shen and Zhiming Cui},
  journal = {Medical Image Analysis},
  volume = {106},
  pages = {103746},
  year = {2025}
}
```

## 获取帮助

如有问题或需要支持：
1. 查看 [README_CN.md](README_CN.md) 获取项目概述
2. 查看 [FAQ](README_CN.md#常见问题) 部分
3. 提交 GitHub Issue
4. 联系作者：
   - Yulong Dou: douyl2023@shanghaitech.edu.cn
   - Zhiming Cui: cuizhm@shanghaitech.edu.cn

---

**祝您使用愉快！**
