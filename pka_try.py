import os
import propka

def find_pdb_file(pdb_id, search_dir):
    # 构建 PDB 文件名
    pdb_file_name = f"{pdb_id}.pdb"
    
    # 遍历指定目录及其子目录
    for root, dirs, files in os.walk(search_dir):
        if pdb_file_name in files:
            pdb_file_path = os.path.join(root, pdb_file_name)
            print(f"PDB 文件 {pdb_file_name} 找到于：{pdb_file_path}")
            return pdb_file_path
    
    print(f"PDB 文件 {pdb_file_name} 未找到于目录 {search_dir}")
    return None

def calculate_lysin_pka(pdb_file):
    # 创建 PropKa 结构对象
    structure = propka.Structure(pdb_file)
    
    # 计算 pKa 值
    structure.calculate_pka()
    
    # 输出 Lys 残基的 pKa 值
    for residue in structure.residues:
        if residue.name == 'LYS' and residue.has_pka():
            print(f"Residue: {residue.name} {residue.number} - pKa: {residue.pka:.2f}")

if __name__ == "__main__":
    # 获取用户输入的 PDB_ID 和搜索目录
    pdb_id = input("请输入 PDB_ID：")
    search_dir = input("请输入搜索目录：")
    
    # 查找 PDB 文件
    pdb_file_path = find_pdb_file(pdb_id, search_dir)
    
    if pdb_file_path:
        # 计算 Lys 残基的 pKa 值
        calculate_lysin_pka(pdb_file_path)
