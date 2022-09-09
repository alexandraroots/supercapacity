import numpy as np
import pubchempy as pcp
from rdkit import Chem
from rdkit.Chem import AllChem


def preproc_material(mol_name, elem):
    print(mol_name, elem)
    # if elem is np.nan:
    #     return np.nan
    smi = mol_name_to_smiles(mol_name)
    value, measure = elem.split()
    if measure == 'mmol':
        return float(value)
    if measure == 'g':
        return float(value) / smiles_to_mol(smi)
    if measure == 'ml':
        return float(value)


def mol_name_to_smiles(name: str):
    return pcp.get_compounds(name, 'name')[0].isomeric_smiles


def smiles_to_mol(smi):
    return Chem.MolFromSmiles(smi)


def morgan_fingerprint(smi):
    mol = smiles_to_mol(smi)
    return np.array(AllChem.GetMorganFingerprintAsBitVect(mol, useChirality=True, radius=2, nBits=100))


def smi_to_mmol_mass(smi):
    m = 0
    mol = smiles_to_mol(smi)
    for atom in mol.GetAtoms():
        m += atom.GetMass()
    return m