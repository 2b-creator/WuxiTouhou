import os
from PIL import Image

# 设定路径
input_dir = r'D:\Codes\blog\WuxiTHP\docs\.vuepress\public\2.22'
# 建议先输出到一个新文件夹，确认没问题再覆盖
output_dir = os.path.join(input_dir, 'optimized') 

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 设定目标最大宽度 (2560px 足以应对 2K/4K 屏幕展示)
MAX_WIDTH = 2560
QUALITY = 80 # 压缩质量 1-95

def process_images():
    # 获取所有 webp 文件并排序（确保 1.webp, 2.webp 的顺序）
    files = [f for f in os.listdir(input_dir) if f.lower().endswith('.webp')]
    # 如果文件名本来就是数字，按数字大小排序；否则按字母序
    files.sort(key=lambda x: int(x.split('.')[0]) if x.split('.')[0].isdigit() else x)

    for index, filename in enumerate(files, start=1):
        img_path = os.path.join(input_dir, filename)
        
        try:
            with Image.open(img_path) as img:
                # 1. 计算缩放比例
                width, height = img.size
                if width > MAX_WIDTH:
                    new_height = int((MAX_WIDTH / width) * height)
                    img = img.resize((MAX_WIDTH, new_height), Image.Resampling.LANCZOS)
                    print(f"正在缩放 {filename}: {width}x{height} -> {MAX_WIDTH}x{new_height}")
                
                # 2. 构造新文件名 (1.webp, 2.webp...)
                new_name = f"{index}.webp"
                save_path = os.path.join(output_dir, new_name)
                
                # 3. 保存并压缩
                img.save(save_path, "WEBP", quality=QUALITY, lossless=False)
                print(f"已保存: {save_path}")
                
        except Exception as e:
            print(f"处理 {filename} 出错: {e}")

if __name__ == "__main__":
    process_images()
    print("\n处理完成！请查看 optimized 文件夹。")
