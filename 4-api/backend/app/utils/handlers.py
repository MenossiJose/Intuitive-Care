from fastapi import HTTPException
from typing import List, TypeVar, Generic, Dict, Any, Optional

T = TypeVar('T')

def check_empty_results(results: List[T], termo: str, search_type: str = "nome") -> List[T]:
    """Check if results are empty and raise appropriate exception"""
    if not results:
        raise HTTPException(
            status_code=404, 
            detail=f"Nenhuma operadora encontrada com {search_type}: '{termo}'"
        )
    
    # Validate data fields
    for item in results:
        # Check if nome_fantasia is None and provide a default
        if hasattr(item, 'nome_fantasia') and item.nome_fantasia is None:
            item.nome_fantasia = "Nome não disponível"
        
        # Check if cnpj is None and provide a default
        if hasattr(item, 'cnpj') and item.cnpj is None:
            item.cnpj = "CNPJ não disponível"
            
        # Check if modalidade is None and provide a default
        if hasattr(item, 'modalidade') and item.modalidade is None:
            item.modalidade = "Modalidade não disponível"
            
        # Check if cidade is None and provide a default
        if hasattr(item, 'cidade') and item.cidade is None:
            item.cidade = "Cidade não disponível"
            
        # Check if uf is None and provide a default
        if hasattr(item, 'uf') and item.uf is None:
            item.uf = "UF não disponível"
    
    return results