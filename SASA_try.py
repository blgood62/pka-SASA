import os
from Bio.PDB import PDBParser
from Bio.PDB.SASA import ShrakeRupley

# 设置PDB文件夹路径
pdb_folder_path = ""

# 获取文件夹中第一个PDB文件的路径
pdb_files = [f for f in os.listdir(pdb_folder_path) if f.endswith('.pdb')]
if not pdb_files:
    print("No PDB files found in the directory.")
else:
    first_pdb_file = os.path.join(pdb_folder_path, pdb_files[0])

    # 解析PDB文件
    parser = PDBParser()
    structure = parser.get_structure("first_structure", first_pdb_file)

    # 创建SASA计算对象
    sr = ShrakeRupley()

    # 计算所有链的SASA
    for model in structure:
        for chain in model:
            sr.compute(chain, level="R")  # 'R' 表示计算每个残基的SASA

            # 打印每个Lys残基的SASA
            for residue in chain:
                if residue.resname == 'LYS':
                    residue_sasa = residue.sasa
                    print(f"Residue {residue.id[1]} ({residue.resname} {residue.id[2]}) SASA: {residue_sasa:.2f}")
