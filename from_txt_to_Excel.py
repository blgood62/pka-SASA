import pandas as pd

# 输入和输出文件路径
input_file = 'input.txt'
output_file = 'output.xlsx'

# 初始化一个空字典来存储PDB ID和对应的LYS pKa值
lys_pka_dict = {}

# 读取txt文件并处理数据
with open(input_file, 'r') as file:
    for line in file:
        # 移除行首行尾的空白字符并分割字符串
        parts = line.strip().split()
        # 提取PDB ID和LYS的pKa信息
        pdb_id = parts[2]
        lys_info = f"LYS {parts[3]} {parts[4]} {parts[5]}"
        
        # 如果PDB ID不在字典中，则添加它
        if pdb_id not in lys_pka_dict:
            lys_pka_dict[pdb_id] = []
        # 将LYS的pKa信息添加到对应PDB ID的列表中
        lys_pka_dict[pdb_id].append(lys_info)

# 准备数据用于创建DataFrame
data = []
for pdb_id, lys_infos in lys_pka_dict.items():
    data.append([pdb_id, '，'.join(lys_infos)])

# 创建DataFrame
df = pd.DataFrame(data, columns=['PDB ID', 'LYS pKa'])

# 将DataFrame保存到xlsx文件
df.to_excel(output_file, index=False, engine='openpyxl')

print(f"已成功将数据保存到：{output_file}")
