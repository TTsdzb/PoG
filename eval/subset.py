import json

def find_unique_strings(file1, file2):
    # 读取第一个JSON文件中的字符串数组
    with open(file1, 'r') as f1:
        data1 = json.load(f1)

    # 读取第二个JSON文件中的字符串数组
    with open(file2, 'r') as f2:
        data2 = json.load(f2)

    # 确保数据是数组格式
    if not (isinstance(data1, list) and isinstance(data2, list)):
        raise ValueError("两个JSON文件都应包含数组")

    # 将两个数组都转换为集合
    set1 = set(data1)
    set2 = set(data2)

    # 找出第一个数组中独有的字符串
    unique_strings = sorted(list(set1 - set2))  # 排序后输出

    return unique_strings

# 示例用法
if __name__ == "__main__":
    file1 = "err_qog_3.json"  # 替换为实际文件路径
    file2 = "err_pog.json"  # 替换为实际文件路径

    try:
        result = find_unique_strings(file1, file2)
        if result:
            print("第一个文件中独有的字符串:")
            for s in result:
                print(s)
        else:
            print("第一个文件中的所有字符串都存在于第二个文件中")
    except FileNotFoundError as e:
        print(f"文件未找到: {str(e)}")
    except json.JSONDecodeError:
        print("JSON解析错误: 文件格式不正确")
    except ValueError as e:
        print(f"数据格式错误: {str(e)}")
