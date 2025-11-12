#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CLIK-Diffusion 演示脚本 / Demo Script
This script provides a simple way to run the tooth alignment task.
本脚本提供了一个简单的方式来运行牙齿矫正任务。

Usage / 用法:
    python demo.py
    
Or with custom parameters / 或使用自定义参数:
    python demo.py --patient 275 --visualize
"""

import os
import sys
import argparse
from pathlib import Path


def check_environment():
    """
    检查运行环境是否满足要求
    Check if the environment meets the requirements
    """
    print("=" * 80)
    print("检查运行环境 / Checking Environment")
    print("=" * 80)
    
    # Check Python version
    python_version = sys.version_info
    print(f"Python版本 / Version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 7):
        print("警告 / Warning: Python 3.7+ is recommended")
    
    # Check required packages
    required_packages = ['torch', 'numpy', 'scipy', 'matplotlib', 'trimesh', 'natsort']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} 已安装 / installed")
        except ImportError:
            print(f"✗ {package} 未安装 / not installed")
            missing_packages.append(package)
    
    if missing_packages:
        print("\n缺少依赖包 / Missing packages:")
        print("请运行 / Please run: pip install -r requirements.txt")
        return False
    
    print("\n环境检查通过 / Environment check passed!\n")
    return True


def check_checkpoints():
    """
    检查模型检查点文件是否存在
    Check if model checkpoint files exist
    """
    print("=" * 80)
    print("检查模型文件 / Checking Model Checkpoints")
    print("=" * 80)
    
    checkpoint_dir = Path("Code/checkpoint")
    required_files = [
        "incisor-e965.pt",
        "cuspid-e920.pt",
        "premolar-e999.pt",
        "molar-e951.pt",
        "diffusion-e20000.pth"
    ]
    
    all_exist = True
    for filename in required_files:
        filepath = checkpoint_dir / filename
        if filepath.exists():
            print(f"✓ {filename} 存在 / exists")
        else:
            print(f"✗ {filename} 缺失 / missing")
            all_exist = False
    
    if not all_exist:
        print("\n" + "=" * 80)
        print("模型文件缺失 / Missing checkpoint files!")
        print("=" * 80)
        print("请从以下链接下载所有模型文件：")
        print("Please download all checkpoint files from:")
        print("https://drive.google.com/drive/folders/1o9tVJ6p8Jbad3gu0ZUkX0tE5dp7Vkh9g?usp=sharing")
        print("\n并将它们放置到 Code/checkpoint/ 目录")
        print("And place them in the Code/checkpoint/ directory")
        print("=" * 80)
        return False
    
    print("\n模型文件检查通过 / Checkpoint files check passed!\n")
    return True


def check_data(patient_id):
    """
    检查输入数据是否存在
    Check if input data exists
    """
    print("=" * 80)
    print("检查输入数据 / Checking Input Data")
    print("=" * 80)
    
    data_dir = Path("Data") / str(patient_id)
    
    if not data_dir.exists():
        print(f"✗ 数据目录不存在 / Data directory does not exist: {data_dir}")
        print("\n可用的测试数据 / Available test data:")
        data_root = Path("Data")
        if data_root.exists():
            for item in data_root.iterdir():
                if item.is_dir():
                    print(f"  - {item.name}")
        return False
    
    # Count mesh files
    mesh_files = list(data_dir.glob("*.obj"))
    print(f"✓ 找到数据目录 / Found data directory: {data_dir}")
    print(f"  包含 {len(mesh_files)} 个网格文件 / Contains {len(mesh_files)} mesh files")
    
    if len(mesh_files) == 0:
        print("✗ 警告 / Warning: 没有找到.obj文件 / No .obj files found")
        return False
    
    print("\n输入数据检查通过 / Input data check passed!\n")
    return True


def run_inference(patient_id, output_dir, visualize):
    """
    运行推理任务
    Run inference task
    """
    print("=" * 80)
    print("开始运行牙齿矫正任务 / Starting Tooth Alignment Task")
    print("=" * 80)
    print(f"患者ID / Patient ID: {patient_id}")
    print(f"输出目录 / Output directory: {output_dir}")
    print(f"可视化地标点 / Visualize landmarks: {visualize}")
    print("=" * 80 + "\n")
    
    # Prepare command
    patient_dir = f"./Data/{patient_id}"
    cmd_parts = [
        "python", "Code/infer.py",
        "-i", patient_dir,
        "-o", output_dir
    ]
    
    if visualize:
        cmd_parts.append("-v")
    
    cmd = " ".join(cmd_parts)
    print(f"执行命令 / Executing command:\n{cmd}\n")
    
    # Run inference
    exit_code = os.system(cmd)
    
    if exit_code == 0:
        print("\n" + "=" * 80)
        print("任务完成 / Task Completed Successfully!")
        print("=" * 80)
        print(f"结果已保存到 / Results saved to: {output_dir}")
        
        # List output files
        output_path = Path(output_dir) / str(patient_id)
        if output_path.exists():
            print("\n输出文件 / Output files:")
            for item in output_path.iterdir():
                print(f"  - {item.name}")
        
        return True
    else:
        print("\n" + "=" * 80)
        print("任务失败 / Task Failed!")
        print("=" * 80)
        return False


def main():
    parser = argparse.ArgumentParser(
        description="CLIK-Diffusion 演示脚本 / Demo Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例 / Examples:
  python demo.py                           # 使用默认参数 / Use default parameters
  python demo.py --patient 256             # 指定患者ID / Specify patient ID
  python demo.py --visualize               # 可视化地标点 / Visualize landmarks
  python demo.py --patient 275 --output ./MyOutput  # 自定义输出目录 / Custom output directory
        """
    )
    
    parser.add_argument(
        '--patient', 
        type=str, 
        default='275',
        help='患者ID（数据文件夹名称）/ Patient ID (data folder name). Default: 275'
    )
    
    parser.add_argument(
        '--output', 
        type=str, 
        default='./Output',
        help='输出目录 / Output directory. Default: ./Output'
    )
    
    parser.add_argument(
        '--visualize', '-v',
        action='store_true',
        help='保存并可视化地标点检测结果 / Save and visualize landmark detection results'
    )
    
    parser.add_argument(
        '--skip-checks',
        action='store_true',
        help='跳过环境检查（不推荐）/ Skip environment checks (not recommended)'
    )
    
    args = parser.parse_args()
    
    print("\n" + "=" * 80)
    print("CLIK-Diffusion 牙齿矫正演示")
    print("CLIK-Diffusion Tooth Alignment Demo")
    print("=" * 80 + "\n")
    
    # Run checks
    if not args.skip_checks:
        if not check_environment():
            print("\n环境检查失败，程序退出 / Environment check failed, exiting")
            return 1
        
        if not check_checkpoints():
            print("\n模型文件检查失败，程序退出 / Checkpoint check failed, exiting")
            return 1
        
        if not check_data(args.patient):
            print("\n数据检查失败，程序退出 / Data check failed, exiting")
            return 1
    
    # Run inference
    success = run_inference(args.patient, args.output, args.visualize)
    
    if success:
        print("\n" + "=" * 80)
        print("演示完成！/ Demo completed!")
        print("=" * 80)
        print("\n如需了解更多信息，请参考：")
        print("For more information, please refer to:")
        print("  - README.md (English)")
        print("  - README_CN.md (中文)")
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
