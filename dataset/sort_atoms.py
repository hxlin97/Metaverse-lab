def sort_and_process_file(file_path, output_path):
    with open(file_path, 'r') as file, open(output_path, 'w') as output_file:
        current_section = []
        header_section = []
        processing_section = False
        line_count = 0

        for line in file:
            line_count += 1

            if "ITEM: ATOMS id type xs ys zs" in line:
                # 将 header_section 写入输出文件
                for header_line in header_section:
                    output_file.write(header_line)
                output_file.write(line)

                if current_section:
                    # 对当前片段进行排序并处理
                    process_section(current_section, output_file)
                    current_section = []
                processing_section = True
                header_section = []  # 清空 header_section 以备下次使用
            elif processing_section:
                if line.startswith("ITEM:"):
                    # 遇到新的片段开始，结束当前片段的处理
                    process_section(current_section, output_file)
                    current_section = []
                    processing_section = False
                    header_section.append(line)  # 开始收集新的 header_section
                else:
                    current_section.append(line)
            else:
                header_section.append(line)

            # 每读取一定数量的行，输出进度
            if line_count % 10000 == 0:
                print(f"Processed {line_count} lines.")

        # 确保最后一个片段也被处理
        if current_section:
            process_section(current_section, output_file)

def process_section(section, output_file):
    sorted_section = sorted(section, key=lambda x: int(x.split()[0]))
    for line in sorted_section:
        output_file.write(line)

# 使用脚本
sort_and_process_file('dump-8.reax.mgNO3', 'mgno3_8.lammpstrj')
