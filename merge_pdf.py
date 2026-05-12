import os
import re
from pypdf import PdfReader, PdfWriter


def natural_sort_key(path: str):
    """生成自然排序键，使 '2' 排在 '10' 前面"""
    # 提取文件名（不含扩展名）
    filename = os.path.basename(path)
    name_without_ext = os.path.splitext(filename)[0]
    # 提取文件名开头的数字
    match = re.match(r'^(\d+)', name_without_ext)
    if match:
        return (0, int(match.group(1)), path)  # 有数字序号的排前面
    return (1, 0, path)  # 无数字序号的排后面


def collect_pdfs(root: str, output_name: str):
    """递归收集 root 目录下所有 PDF 文件（排除输出文件本身），并按自然排序。"""
    pdf_paths = []
    for dirpath, _dirnames, filenames in os.walk(root):
        for filename in filenames:
            if not filename.lower().endswith(".pdf"):
                continue
            # 跳过之前已经合并生成的输出文件
            if filename == output_name:
                continue
            full_path = os.path.join(dirpath, filename)
            pdf_paths.append(full_path)

    pdf_paths.sort(key=natural_sort_key)  # 使用自然排序
    return pdf_paths


def merge_pdfs(root: str, output_name: str = "hive.pdf") -> None:
    pdf_paths = collect_pdfs(root, output_name)

    if not pdf_paths:
        print("没有找到任何 PDF 文件。")
        return

    writer = PdfWriter()

    for path in pdf_paths:
        print(f"添加：{path}")
        # 使用 append() 方法保留书签、超链接等元数据
        writer.append(path)

    output_path = os.path.join(root, output_name)
    with open(output_path, "wb") as f:
        writer.write(f)

    print(f"合并完成！输出文件：{output_path}")
    print(f"本次共合并 {len(pdf_paths)} 个 PDF。")


if __name__ == "__main__":
    # 根目录：hive（会递归合并其下所有 PDF）
    folder = r"C:\Users\cat\Desktop\hive"
    merge_pdfs(folder)