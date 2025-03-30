import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from app.utils.paths import get_services

services = get_services()

MOCK_OPERATORS = [
    MagicMock(
        nome_fantasia="Operadora Teste",
        cnpj="12345678000190",
        razao_social="Operadora Teste LTDA",
        cidade="São Paulo",
        uf="SP",
        modalidade="Seguradora"
    )
]

@pytest.fixture
def mock_db():
    db = MagicMock(spec=Session)
    query_mock = MagicMock()
    filter_mock = MagicMock()
    
    db.query.return_value = query_mock
    query_mock.filter.return_value = filter_mock
    filter_mock.all.return_value = MOCK_OPERATORS
    
    return db

# Patch the models import to avoid actual database access
@pytest.fixture(autouse=True)
def mock_models():
    with patch('app.services.operadora.models') as mock:
        # Create mocks with side_effect for like method
        nome_fantasia_mock = MagicMock()
        nome_fantasia_mock.like = MagicMock(side_effect=lambda x: x)
        
        cnpj_mock = MagicMock()
        cnpj_mock.like = MagicMock(side_effect=lambda x: x)
        
        razao_social_mock = MagicMock()
        razao_social_mock.like = MagicMock(side_effect=lambda x: x)
        
        cidade_mock = MagicMock()
        cidade_mock.like = MagicMock(side_effect=lambda x: x)
        
        uf_mock = MagicMock()
        uf_mock.like = MagicMock(side_effect=lambda x: x)
        
        modalidade_mock = MagicMock()
        modalidade_mock.like = MagicMock(side_effect=lambda x: x)
        
        # Configure the ActiveOperator model attributes
        mock.ActiveOperator = MagicMock()
        mock.ActiveOperator.nome_fantasia = nome_fantasia_mock
        mock.ActiveOperator.cnpj = cnpj_mock
        mock.ActiveOperator.razao_social = razao_social_mock
        mock.ActiveOperator.cidade = cidade_mock
        mock.ActiveOperator.uf = uf_mock
        mock.ActiveOperator.modalidade = modalidade_mock
        
        yield mock

def test_buscar_operadoras(mock_db, mock_models):
    result = services.buscar_operadoras(mock_db, "Teste")
    
    mock_db.query.assert_called_once()
    mock_db.query().filter.assert_called_once()
    
    # Verify the like method was called with the correct format
    mock_models.ActiveOperator.nome_fantasia.like.assert_called_once_with("%Teste%")
    
    # Verify result
    assert result == MOCK_OPERATORS

def test_buscar_operadoras_cnpj(mock_db, mock_models):
    result = services.buscar_operadoras_cnpj(mock_db, "12345")
    
    mock_db.query.assert_called_once()
    mock_db.query().filter.assert_called_once()
    
    # Verify the like method was called with the correct format
    mock_models.ActiveOperator.cnpj.like.assert_called_once_with("%12345%")
    
    # Verify result
    assert result == MOCK_OPERATORS

def test_buscar_operadoras_razao_social(mock_db, mock_models):
    result = services.buscar_operadoras_razao_social(mock_db, "LTDA")

    mock_db.query.assert_called_once()
    mock_db.query().filter.assert_called_once()
    
    # Verify the like method was called with the correct format
    mock_models.ActiveOperator.razao_social.like.assert_called_once_with("%LTDA%")
    
    # Verify result
    assert result == MOCK_OPERATORS

def test_buscar_operadoras_cidade_uf(mock_db, mock_models):
    result = services.buscar_operadoras_cidade_uf(mock_db, "São Paulo", "SP")
    
    mock_db.query.assert_called_once()
    mock_db.query().filter.assert_called_once()
    
    # Verify the like methods were called with the correct formats
    mock_models.ActiveOperator.cidade.like.assert_called_once_with("%São Paulo%")
    mock_models.ActiveOperator.uf.like.assert_called_once_with("%SP%")
    
    # Verify result
    assert result == MOCK_OPERATORS

def test_buscar_operadoras_modalidade(mock_db, mock_models):
    result = services.buscar_operadoras_modalidade(mock_db, "Seguradora")
    
    mock_db.query.assert_called_once()
    mock_db.query().filter.assert_called_once()
    
    # Verify the like method was called with the correct format
    mock_models.ActiveOperator.modalidade.like.assert_called_once_with("%Seguradora%")
    
    # Verify result
    assert result == MOCK_OPERATORS