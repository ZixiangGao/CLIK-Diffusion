# CLIK-Diffusion 任务介绍与执行说明

## 📌 任务概述

**CLIK-Diffusion** 是一个创新的深度学习系统，用于自动化牙齿矫正方案的预测。本系统可以根据患者矫正前的牙齿位置，自动预测矫正后的理想牙齿位置，为口腔医生提供智能化的治疗规划支持。

---

## 🎯 项目目标

传统的牙齿矫正治疗规划需要口腔医生根据专业经验手动规划，既耗时又主观。CLIK-Diffusion 通过以下方式解决这个问题：

1. **自动化预测**：无需人工干预，自动生成矫正方案
2. **临床知识融合**：整合专业牙科知识，确保结果符合临床标准
3. **高效准确**：利用深度学习技术，快速给出准确预测

---

## 🔬 技术方案

### 核心创新点

1. **问题转化**
   - 将复杂的牙齿矫正问题转化为地标点变换问题
   - 使用扩散模型生成地标点坐标

2. **三层次约束**
   - **牙弓层次**：确保整体牙弓形态符合标准
   - **牙齿间层次**：维持相邻牙齿合理关系
   - **单牙层次**：保证每颗牙齿形态合理

3. **三阶段流程**
   - **阶段1**：地标点检测 - 识别关键位置点
   - **阶段2**：扩散模型预测 - 生成目标位置
   - **阶段3**：刚体变换 - 计算最终牙齿位置

### 技术架构

```
输入：矫正前的牙齿3D模型（.obj格式）
  ↓
[阶段1] 地标点检测网络
  - 门牙检测器
  - 尖牙检测器
  - 前磨牙检测器
  - 磨牙检测器
  ↓
[阶段2] 扩散模型
  - 融合临床知识约束
  - 预测目标地标点
  ↓
[阶段3] 刚体变换求解
  - 计算变换矩阵
  - 应用到原始网格
  ↓
输出：矫正后的牙齿3D模型
```

---

## 📚 快速入门

### 最快速的开始方式

```bash
# 1. 克隆仓库
git clone https://github.com/ShanghaiTech-IMPACT/CLIK-Diffusion.git
cd CLIK-Diffusion

# 2. 安装环境
conda create -n tooth python=3.8
conda activate tooth
pip install torch==1.10.0+cu113 torchvision==0.11.1+cu113
pip install -r requirements.txt

# 3. 下载模型（5个文件，从Google Drive）
# https://drive.google.com/drive/folders/1o9tVJ6p8Jbad3gu0ZUkX0tE5dp7Vkh9g
# 将文件放入 Code/checkpoint/ 目录

# 4. 运行演示
python demo.py
```

### 预期输出

运行成功后，您将在 `Output/` 目录中获得：
- 矫正后的牙齿3D模型文件（.obj格式）
- 对应的变换矩阵文件（.npy格式）
- 可选的地标点可视化文件

---

## 📖 详细文档

- **[README_CN.md](README_CN.md)** - 项目完整中文文档
- **[TASK_GUIDE_CN.md](TASK_GUIDE_CN.md)** - 任务执行详细指南
- **[README.md](README.md)** - English documentation

---

## 💡 使用场景

1. **研究目的**
   - 牙齿矫正算法研究
   - 医学影像分析
   - 深度学习在医疗领域的应用

2. **教学目的**
   - 了解扩散模型在医疗领域的应用
   - 学习三维网格处理技术
   - 研究临床知识与AI的结合

3. **临床参考**
   - 辅助治疗方案规划
   - 提供第二意见参考
   - 加速初步评估流程

---

## 🎓 项目成果

### 发表论文
- **期刊**：Medical Image Analysis (MedIA) 2025
- **标题**：CLIK-Diffusion: Clinical Knowledge-informed Diffusion Model for Tooth Alignment
- **链接**：https://doi.org/10.1016/j.media.2025.103746

### 开源数据集
- 提供研究用途的牙齿矫正数据集
- 需签署数据访问协议

---

## ⚙️ 系统要求

### 最低配置
- **操作系统**：Windows/Linux/macOS
- **Python**：3.7+
- **内存**：8GB RAM
- **存储**：5GB 可用空间

### 推荐配置
- **GPU**：NVIDIA GPU with CUDA 11.3+
- **显存**：6GB+
- **内存**：16GB+ RAM

---

## 🚀 执行任务

### 方法1：使用演示脚本（推荐）

```bash
# 基本使用
python demo.py

# 带可视化
python demo.py --visualize

# 指定患者
python demo.py --patient 275 --output ./MyResults
```

### 方法2：直接调用推理脚本

```bash
# 运行推理
python Code/infer.py -i "./Data/275" -o "./Output"

# 带地标点可视化
python Code/infer.py -i "./Data/275" -o "./Output" -v
```

---

## 📊 性能指标

根据论文报告：
- **处理时间**：约1-2分钟/病例（使用GPU）
- **精度**：达到临床可接受水平
- **稳定性**：在多种牙齿类型上表现良好

---

## 🔧 故障排除

### 常见问题

1. **依赖包安装失败**
   ```bash
   pip install -r requirements.txt --no-cache-dir
   ```

2. **找不到模型文件**
   - 确认已从Google Drive下载所有5个检查点文件
   - 检查文件位置：`Code/checkpoint/`

3. **GPU内存不足**
   - 使用CPU版本的PyTorch
   - 减少batch size（需修改代码）

4. **输入数据格式错误**
   - 确保使用.obj格式
   - 参考`Data/275/`中的示例数据

---

## 📞 联系方式

**技术支持**：
- GitHub Issues: https://github.com/ShanghaiTech-IMPACT/CLIK-Diffusion/issues

**学术联系**：
- Yulong Dou: douyl2023@shanghaitech.edu.cn
- Zhiming Cui: cuizhm@shanghaitech.edu.cn

**数据集申请**：
- 填写并签署 [Data_Access_Agreement.pdf](Data_Access_Agreement.pdf)
- 发送至上述邮箱，并抄送导师

---

## 📄 许可证

本项目遵循 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

---

## 🙏 致谢

感谢所有为本项目做出贡献的研究人员和合作者。本研究得到了相关科研基金的支持。

---

## 📈 项目状态

- ✅ 代码已发布（2025-07-25）
- ✅ 数据集已发布（2025-07-25）
- ✅ 论文已正式发表（2025-08-05）
- ✅ 中文文档已完善
- ✅ 演示脚本已提供

---

## 🔗 相关链接

- [论文全文](https://doi.org/10.1016/j.media.2025.103746)
- [Google Drive 模型下载](https://drive.google.com/drive/folders/1o9tVJ6p8Jbad3gu0ZUkX0tE5dp7Vkh9g)
- [GitHub 仓库](https://github.com/ShanghaiTech-IMPACT/CLIK-Diffusion)
- [研究组网站](https://shanghaitech-impact.github.io/)

---

**祝您使用愉快！如有任何问题，欢迎随时联系我们。**
