#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将Markdown文件中的图片引用格式从 !xxx.jpg 转换为 ![](xxx.jpg)
"""

import re
import os
import sys

def convert_image_references(content):
    # 匹配 ! 开头的图片引用，支持文件名包含连字符和数字
    pattern = r'!([a-zA-Z0-9_-]+\.(?:jpg|png|gif|jpeg|bmp|svg))'
    
    def replace_func(match):
        filename = match.group(1)
        return f'![]({filename})'
    
    # 使用正则表达式进行替换
    converted_content = re.sub(pattern, replace_func, content)
    
    return converted_content

def process_file(filepath):
    """处理单个文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 统计转换前的数量
        before_count = len(re.findall(r'![a-zA-Z0-9_-]+\.(?:jpg|png|gif|jpeg|bmp|svg)', content))
        
        # 转换内容
        converted_content = convert_image_references(content)
        
        # 统计转换后的数量
        after_count = len(re.findall(r'![a-zA-Z0-9_-]+\.(?:jpg|png|gif|jpeg|bmp|svg)', converted_content))
        
        # 写入文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(converted_content)
        
        print(f"处理文件: {filepath}")
        print(f"  转换前错误格式数量: {before_count}")
        print(f"  转换后错误格式数量: {after_count}")
        print(f"  成功转换: {before_count - after_count} 个图片引用")
        
        return before_count - after_count
        
    except Exception as e:
        print(f"处理文件 {filepath} 时出错: {e}")
        return 0

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python convert_images.py <markdown文件路径>")
        print("示例: python convert_images.py ocr2/2.hive安装详解.md")
        return
    
    filepath = sys.argv[1]
    
    if not os.path.exists(filepath):
        print(f"文件不存在: {filepath}")
        return
    
    total_converted = process_file(filepath)
    
    if total_converted > 0:
        print(f"\n✅ 转换完成！共转换 {total_converted} 个图片引用。")
    else:
        print(f"\nℹ️  没有需要转换的图片引用。")

if __name__ == "__main__":
    main()