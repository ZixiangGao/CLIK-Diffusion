# CLIK-Diffusion: 临床知识引导的牙齿矫正扩散模型

[Yulong Dou](https://douyl.github.io/), [Han Wu](https://hanwu.website/), [Changjian Li](https://enigma-li.github.io/), [Chen Wang](https://www.igiplab.com/members/166), Tong Yang, Min Zhu, [Dinggang Shen](https://idea.bme.shanghaitech.edu.cn/), and [Zhiming Cui](https://shanghaitech-impact.github.io/).

### [论文](https://doi.org/10.1016/j.media.2025.103746) | [数据集](https://github.com/ShanghaiTech-IMPACT/CLIK-Diffusion/blob/main/Data_Access_Agreement.pdf)

这是我们发表在 **Medical Image Analysis (MedIA) 2025** 期刊上的论文 **CLIK-Diffusion: Clinical Knowledge-informed Diffusion Model for Tooth Alignment** 的官方代码仓库。在本工作中，我们将复杂的牙齿矫正问题转化为更易处理的地标点变换问题，并通过扩散模型进一步细化为地标点坐标生成任务。为了进一步融合必要的临床知识，我们从三个层次设计了层次化约束：牙弓层次、牙齿间层次和单个牙齿层次。

![](./image/CLIK-Diffusion.png)


## 项目简介

### 研究背景
牙齿矫正是口腔医学中的重要治疗方案，目标是将患者的牙齿从矫正前的位置调整到理想的矫正后位置。传统的治疗规划依赖于医生的专业经验，耗时且主观性强。本研究提出了一种基于扩散模型的自动化牙齿矫正方案预测方法。

### 核心创新
1. **问题转化**: 将牙齿矫正问题转化为地标点变换问题
2. **扩散模型**: 使用扩散模型生成矫正后的地标点坐标
3. **临床知识融合**: 设计三层次约束（牙弓-牙齿间-单牙）融合临床知识
4. **三阶段流程**: 地标点检测 → 扩散模型预测 → 刚体变换

### 技术架构
- **阶段1**: 地标点检测网络 - 从牙齿网格中检测关键地标点
- **阶段2**: 地标点扩散模型 - 预测矫正后的地标点位置
- **阶段3**: 刚体变换求解 - 计算并应用变换矩阵到牙齿网格


## 更新日志
- **[2025-08-05]** 论文正式版已在线发布，见 [Paper](https://doi.org/10.1016/j.media.2025.103746)!
- **[2025-07-25]** 数据集发布！
- **[2025-07-25]** 代码发布！
- **[2025-07-22]** 论文被 *MedIA 2025* 接收！


## 快速开始

### 环境配置
首先克隆本仓库，然后创建环境并安装依赖包：

```bash
# 克隆仓库
git clone https://github.com/ShanghaiTech-IMPACT/CLIK-Diffusion.git
cd CLIK-Diffusion

# 创建conda环境
conda create -n tooth python=3.8
conda activate tooth

# 安装PyTorch和依赖包
pip install torch==1.10.0+cu113 torchvision==0.11.1+cu113
pip install -r requirements.txt
```

### 模型测试

#### 方法一：使用演示脚本（推荐）

我们提供了一个演示脚本，可以简化测试流程并进行环境检查：

```bash
# 使用默认设置运行（使用患者275）
python demo.py

# 使用自定义患者ID并可视化
python demo.py --patient 275 --visualize

# 查看所有选项帮助
python demo.py --help
```

演示脚本将自动：
- 检查Python环境和依赖包
- 验证所有模型检查点是否已下载
- 确认输入数据存在
- 自动运行推理
- 显示结果

#### 方法二：手动测试

如果您希望手动控制整个流程：

##### 步骤1：下载模型权重
从以下链接下载地标点检测网络和扩散模型的所有检查点：
https://drive.google.com/drive/folders/1o9tVJ6p8Jbad3gu0ZUkX0tE5dp7Vkh9g?usp=sharing

需要下载的文件（共5个）：
- `incisor-e965.pt` (门牙地标点检测网络)
- `cuspid-e920.pt` (尖牙地标点检测网络)
- `premolar-e999.pt` (前磨牙地标点检测网络)
- `molar-e951.pt` (磨牙地标点检测网络)
- `diffusion-e20000.pth` (扩散模型)

##### 步骤2：放置模型文件
将下载的所有5个检查点文件放入 [`./Code/checkpoint`](./Code/checkpoint) 目录。

##### 步骤3：运行推理
我们已经准备了一些数据样本供您快速测试。矫正前的牙齿网格存储在 [`./Data`](./Data) 目录中。

运行以下命令：
```bash
python Code/infer.py -i "./Data/275" -o "./Output"

# 如果想要查看地标点检测网络的结果，添加 -v 参数
python Code/infer.py -i "./Data/275" -o "./Output" -v
```

##### 步骤4：查看结果
运行完成后，您将在 [`./Output`](./Output) 目录中找到我们的方法预测的矫正后牙齿网格。

### 输入输出说明

**输入格式**：
- 矫正前的牙齿网格文件（.obj 格式）
- 每颗牙齿一个单独的网格文件
- 文件应按照特定的命名规范组织

**输出格式**：
- 矫正后的牙齿网格文件（.obj 格式）
- 变换矩阵文件（.npy 格式）
- 可选：地标点可视化结果

### 命令行参数说明

```bash
python Code/infer.py [选项]

必需参数：
  -i, --patient_dir     患者数据目录路径（如 "./Data/275"）
  
可选参数：
  -o, --save_dir        结果保存目录（默认："Output"）
  -v, --visualize_landmarks  是否保存并可视化阶段1检测的地标点
  --seed                随机种子（默认：1）
  --incisor_ckpt        门牙地标点检测网络检查点路径
  --cuspid_ckpt         尖牙地标点检测网络检查点路径
  --premolar_ckpt       前磨牙地标点检测网络检查点路径
  --molar_ckpt          磨牙地标点检测网络检查点路径
  --diffusion_ckpt      扩散模型检查点路径
```


## 数据集获取

★ 我们的数据集仅供研究使用。如需申请 *CLIK-Diffusion* 数据集，请填写 [数据访问协议](./Data_Access_Agreement.pdf)，并将**签署后的电子版**发送至 <u>Yulong Dou (邮箱: douyl2023@shanghaitech.edu.cn)</u> 和 <u>Zhiming Cui (邮箱: cuizhm@shanghaitech.edu.cn)</u>，同时**抄送您的导师**。收到数据访问表后，我们将发送数据集链接和密码。


## 代码结构

```
CLIK-Diffusion/
├── Code/
│   ├── checkpoint/          # 模型检查点目录（需要下载）
│   ├── model/              # 模型定义
│   ├── infer.py            # 主推理脚本
│   ├── s1_LandmarkDetection.py    # 阶段1：地标点检测
│   ├── s2_LandmarkDiffusion.py    # 阶段2：扩散模型预测
│   └── s3_SolveMatrix.py          # 阶段3：变换矩阵求解
├── Data/                   # 测试数据样本
├── image/                  # README图片
├── README.md              # 英文说明文档
├── README_CN.md           # 中文说明文档（本文件）
└── requirements.txt       # Python依赖包
```


## 方法详解

### 阶段1：地标点检测
使用针对不同牙齿类型（门牙、尖牙、前磨牙、磨牙）训练的专用神经网络，从输入的牙齿网格中自动检测关键地标点。

### 阶段2：扩散模型预测
基于检测到的初始地标点，使用融合临床知识的扩散模型预测矫正后的目标地标点位置。模型通过以下三层次约束确保结果的临床合理性：
- **牙弓层次约束**: 确保整体牙弓形态符合临床标准
- **牙齿间约束**: 维持相邻牙齿间的合理关系
- **单牙约束**: 保证每颗牙齿的形态和方向合理

### 阶段3：刚体变换
根据初始地标点和预测的目标地标点，求解最优刚体变换矩阵，并将其应用到原始牙齿网格上，得到最终的矫正后牙齿位置。


## 常见问题

### Q1: 如何处理自己的数据？
A: 需要将牙齿数据组织成与提供的样本数据相同的格式，每颗牙齿保存为单独的.obj网格文件。

### Q2: 是否支持其他牙齿数据格式？
A: 目前主要支持.obj格式的三维网格数据。如需使用其他格式，可能需要先转换为.obj格式。

### Q3: 训练代码何时发布？
A: 训练代码的发布计划请关注我们的GitHub仓库更新。

### Q4: 能否在CPU上运行？
A: 理论上可以，但推理速度会较慢。建议使用GPU以获得更好的性能。


## 引用

如果您觉得本代码或数据集有用，请引用我们的论文：

```BibTeX
@article{DOU2025103746,
title = {CLIK-Diffusion: Clinical Knowledge-informed Diffusion Model for Tooth Alignment},
journal = {Medical Image Analysis},
volume = {106},
pages = {103746},
year = {2025},
issn = {1361-8415},
doi = {https://doi.org/10.1016/j.media.2025.103746},
url = {https://www.sciencedirect.com/science/article/pii/S1361841525002932},
author = {Yulong Dou and Han Wu and Changjian Li and Chen Wang and Tong Yang and Min Zhu and Dinggang Shen and Zhiming Cui}
}
```


## 许可证

本项目遵循 MIT 许可证。详见 [LICENSE](LICENSE) 文件。


## 联系方式

如有任何问题或建议，欢迎通过以下方式联系我们：
- Yulong Dou: douyl2023@shanghaitech.edu.cn
- Zhiming Cui: cuizhm@shanghaitech.edu.cn


## 致谢

感谢所有为本项目做出贡献的研究人员和合作者。本研究得到了相关科研基金的支持。
