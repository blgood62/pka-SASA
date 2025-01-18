import pandas as pd
import os
from Bio.PDB import PDBParser
from Bio.PDB.SASA import ShrakeRupley
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# 设置PDB文件夹路径
pdb_folder_path = r"D:\Dayi_shang\CADD\E3\E3 123\AF_stru"

# 读取Excel文件
excel_file_path = r"D:\Dayi_shang\123456.xlsx"
df = pd.read_excel(excel_file_path)

# 创建SASA计算函数
def calculate_lys_sasa(pdb_id, pdb_folder_path):
    pdb_file_path = os.path.join(pdb_folder_path, f"{pdb_id}.pdb")
    start_time = time.time()
    try:
        # 解析PDB文件
        parser = PDBParser()
        structure = parser.get_structure(pdb_id, pdb_file_path)

        # 创建SASA计算对象
        sr = ShrakeRupley()

        # 初始化一个列表来存储Lys残基的SASA值
        lys_sasa_values = []

        # 计算所有链的SASA
        for model in structure:
            for chain in model:
                for residue in chain:
                    if residue.resname == 'LYS':
                        sr.compute(chain, level="R")  # 'R' 表示计算每个残基的SASA
                        lys_sasa_values.append(f"Lys {residue.id[1]} {residue.sasa:.2f}")

        end_time = time.time()
        print(f"Calculated SASA for {pdb_id} in {end_time - start_time:.2f} seconds")
        return lys_sasa_values
    except Exception as e:
        print(f"Error calculating SASA for {pdb_id}: {e}")
        end_time = time.time()
        print(f"Failed to calculate SASA for {pdb_id} in {end_time - start_time:.2f} seconds")
        return []

# 使用多线程计算SASA
def calculate_sasa_multithreaded(df, pdb_folder_path, max_workers=16):
    results = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(calculate_lys_sasa, pdb_id, pdb_folder_path): pdb_id for pdb_id in df['PDB'][912:]}
        for future in as_completed(futures):
            pdb_id, lys_sasa_values = future.result(), []
            results[pdb_id] = lys_sasa_values
    return results

# 计算每个PDB的SASA并添加到DataFrame中
start_time = time.time()
sasa_results = calculate_sasa_multithreaded(df, pdb_folder_path)
end_time = time.time()
print(f"Total time taken: {end_time - start_time} seconds")

# 将计算结果添加到DataFrame中
for index, row in df.iloc[912:].iterrows():
    pdb_id = row['PDB']
    lys_sasa_values = sasa_results[pdb_id]
    lys_sasa_str = "; ".join(lys_sasa_values)
    df.at[index, 'LYS SASA'] = lys_sasa_str

# 保存新的Excel文件
new_excel_file_path = r"D:\Dayi_shang\123456789.xlsx"
df.to_excel(new_excel_file_path, index=False)

print(f"New Excel file with Lys SASA values has been saved to {new_excel_file_path}")   
