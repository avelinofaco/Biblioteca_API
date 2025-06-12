from typing import List, Optional

from config.database import get_session
from config.logging_config import logger
from fastapi import APIRouter, Depends, HTTPException, Query
from schemas.schemas import (
    CategoriaCreate,
    CategoriaResponse,
    CategoriaUpdate,
    CountResponse,
    PaginatedResponse,
)
from services.categoria_service import CategoriaService
from sqlmodel import Session

router = APIRouter(prefix='/categorias', tags=['categorias'])


@router.post('/', response_model=CategoriaResponse)
def create_categoria(categoria: CategoriaCreate, session: Session = Depends(get_session)):
    """F1: Inserir uma categoria no banco de dados"""
    try:
        return CategoriaService.create_categoria(session, categoria)
    except Exception as e:
        logger.error(f'Erro no endpoint create_categoria: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/', response_model=PaginatedResponse)
def list_categorias(
    page: int = Query(1, ge=1, description='Número da página'),
    limit: int = Query(10, ge=1, le=100, description='Limite de itens por página'),
    session: Session = Depends(get_session),
):
    """F2 e F5: Listar todas as categorias com paginação"""
    try:
        skip = (page - 1) * limit
        result = CategoriaService.get_all_categorias(session, skip, limit)

        return PaginatedResponse(
            items=[
                CategoriaResponse.model_validate(categoria)
                for categoria in result['items']
            ],
            total=result['total'],
            page=result['page'],
            limit=result['limit'],
            total_pages=result['total_pages'],
        )
    except Exception as e:
        logger.error(f'Erro no endpoint list_categorias: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/count', response_model=CountResponse)
def count_categorias(session: Session = Depends(get_session)):
    """F4: Mostrar a quantidade de categorias"""
    try:
        count = CategoriaService.count_categorias(session)
        return CountResponse(total=count, entidade='categorias')
    except Exception as e:
        logger.error(f'Erro no endpoint count_categorias: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/search', response_model=List[CategoriaResponse])
def search_categorias(
    nome: Optional[str] = Query(None, description='Buscar por nome'),
    ativa: Optional[bool] = Query(None, description='Filtrar por status ativo'),
    session: Session = Depends(get_session),
):
    """F6: Filtrar categorias por atributos específicos"""
    try:
        categorias = CategoriaService.search_categorias(session, nome, ativa)
        return [CategoriaResponse.model_validate(categoria) for categoria in categorias]
    except Exception as e:
        logger.error(f'Erro no endpoint search_categorias: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/{categoria_id}', response_model=CategoriaResponse)
def get_categoria(categoria_id: int, session: Session = Depends(get_session)):
    """F3: Ler uma categoria específica"""
    try:
        categoria = CategoriaService.get_categoria_by_id(session, categoria_id)
        if not categoria:
            raise HTTPException(status_code=404, detail='Categoria não encontrada')
        return CategoriaResponse.model_validate(categoria)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'Erro no endpoint get_categoria: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))


@router.put('/{categoria_id}', response_model=CategoriaResponse)
def update_categoria(
    categoria_id: int,
    categoria_update: CategoriaUpdate,
    session: Session = Depends(get_session),
):
    """F3: Atualizar uma categoria"""
    try:
        categoria = CategoriaService.update_categoria(
            session, categoria_id, categoria_update
        )
        if not categoria:
            raise HTTPException(status_code=404, detail='Categoria não encontrada')
        return CategoriaResponse.model_validate(categoria)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'Erro no endpoint update_categoria: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))


@router.delete('/{categoria_id}')
def delete_categoria(categoria_id: int, session: Session = Depends(get_session)):
    """F3: Excluir uma categoria"""
    try:
        success = CategoriaService.delete_categoria(session, categoria_id)
        if not success:
            raise HTTPException(status_code=404, detail='Categoria não encontrada')
        return {'message': 'Categoria excluída com sucesso'}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'Erro no endpoint delete_categoria: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))
