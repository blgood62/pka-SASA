import pandas as pd
import os
from Bio.PDB import PDBParser
from Bio.PDB.SASA import ShrakeRupley
from concurrent.futures import ProcessPoolExecutor, as_completed
import time
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 设置PDB文件夹路径
pdb_folder_path = 

# 读取Excel文件
excel_file_path = 
df = pd.read_excel(excel_file_path)

# 创建SASA计算函数
def calculate_lys_sasa(pdb_id, pdb_folder_path):
    pdb_file_path = os.path.join(pdb_folder_path, f"{pdb_id}.pdb")
    start_time = time.time()
    lys_sasa_values = []

    try:
        # 解析PDB文件
        parser = PDBParser(QUIET=True)
        structure = parser.get_structure(pdb_id, pdb_file_path)

        # 创建SASA计算对象
        sr = ShrakeRupley()

        # 只计算第一个模型的SASA
        for model in structure:
            for chain in model:
                sr.compute(chain, level="R")  # 计算每个残基的SASA
                # 遍历链中的所有残基，收集LYS残基的SASA
                for residue in chain:
                    if residue.resname == 'LYS':
                        lys_sasa_values.append(f"Lys {residue.id[1]} {residue.sasa:.2f}")
                        logging.info(f"Calculated SASA for Lys {residue.id[1]} in PDB {pdb_id}: {residue.sasa:.2f} Å²")

        # 记录PDB计算完成的时间
        end_time = time.time()
        total_time = end_time - start_time
        logging.info(f"Finished calculating SASA for PDB: {pdb_id} in {total_time:.2f} seconds")

        return lys_sasa_values
    except Exception as e:
        logging.error(f"Error calculating SASA for {pdb_id}: {e}")
        return []

# 使用多进程计算SASA
def calculate_sasa_multiprocessed(df, pdb_folder_path, max_workers=16):
    results = {}
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(calculate_lys_sasa, pdb_id, pdb_folder_path): pdb_id for pdb_id in df['PDB'][1:912]}
        for future in as_completed(futures):
            pdb_id = futures[future]
            lys_sasa_values = future.result()
            results[pdb_id] = lys_sasa_values
    return results

# 计算每个PDB的SASA并添加到DataFrame中
def main():
    start_time = time.time()
    sasa_results = calculate_sasa_multiprocessed(df, pdb_folder_path)
    end_time = time.time()
    logging.info(f"Total time taken: {end_time - start_time:.2f} seconds")

    # 将计算结果添加到DataFrame中
    for index, row in df.iloc[1:912].iterrows():
        pdb_id = row['PDB']
        lys_sasa_values = sasa_results.get(pdb_id, [])
        lys_sasa_str = "; ".join(lys_sasa_values)
        df.at[index, 'LYS SASA'] = lys_sasa_str

    # 保存新的Excel文件
    new_excel_file_path = 
    df.to_excel(new_excel_file_path, index=False)

    logging.info(f"New Excel file with Lys SASA values has been saved to {new_excel_file_path}")

if __name__ == '__main__':
    main()
