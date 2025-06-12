from typing import List, Optional

from config.database import get_session
from config.logging_config import logger
from fastapi import APIRouter, Depends, HTTPException, Query
from schemas.schemas import (
    AutorCreate,
    AutorResponse,
    AutorUpdate,
    CountResponse,
    PaginatedResponse,
)
from services.autor_service import AutorService
from sqlmodel import Session

router = APIRouter(prefix='/autores', tags=['autores'])


@router.post('/', response_model=AutorResponse)
def create_autor(autor: AutorCreate, session: Session = Depends(get_session)):
    """F1: Inserir um autor no banco de dados"""
    try:
        return AutorService.create_autor(session, autor)
    except Exception as e:
        logger.error(f'Erro no endpoint create_autor: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/', response_model=PaginatedResponse[AutorResponse])
def list_autores(
    page: int = Query(1, ge=1, description='Número da página'),
    limit: int = Query(10, ge=1, le=100, description='Limite de itens por página'),
    session: Session = Depends(get_session),
):
    """F2 e F5: Listar todos os autores com paginação"""
    try:
        skip = (page - 1) * limit
        result = AutorService.get_all_autores(session, skip, limit)

        autores_response = [
            AutorResponse.model_validate(autor) for autor in result['items']
        ]

        return PaginatedResponse[AutorResponse](
            items=autores_response,
            total=result['total'],
            page=result['page'],
            limit=result['limit'],
            total_pages=result['total_pages'],
        )
    except Exception as e:
        logger.error(f'Erro no endpoint list_autores: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/count', response_model=CountResponse)
def count_autores(session: Session = Depends(get_session)):
    """F4: Mostrar a quantidade de autores"""
    try:
        count = AutorService.count_autores(session)
        return CountResponse(total=count, entidade='autores')
    except Exception as e:
        logger.error(f'Erro no endpoint count_autores: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/search', response_model=List[AutorResponse])
def search_autores(
    nome: Optional[str] = Query(None, description='Buscar por nome ou sobrenome'),
    nacionalidade: Optional[str] = Query(None, description='Filtrar por nacionalidade'),
    session: Session = Depends(get_session),
):
    """F6: Filtrar autores por atributos específicos"""
    try:
        autores = AutorService.search_autores(session, nome, nacionalidade)
        return [AutorResponse.model_validate(autor) for autor in autores]
    except Exception as e:
        logger.error(f'Erro no endpoint search_autores: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/{autor_id}', response_model=AutorResponse)
def get_autor(autor_id: int, session: Session = Depends(get_session)):
    """F3: Ler um autor específico"""
    try:
        autor = AutorService.get_autor_by_id(session, autor_id)
        if not autor:
            raise HTTPException(status_code=404, detail='Autor não encontrado')
        return AutorResponse.model_validate(autor)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'Erro no endpoint get_autor: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))


@router.put('/{autor_id}', response_model=AutorResponse)
def update_autor(
    autor_id: int,
    autor_update: AutorUpdate,
    session: Session = Depends(get_session),
):
    """F3: Atualizar um autor"""
    try:
        autor = AutorService.update_autor(session, autor_id, autor_update)
        if not autor:
            raise HTTPException(status_code=404, detail='Autor não encontrado')
        return AutorResponse.model_validate(autor)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'Erro no endpoint update_autor: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))


@router.delete('/{autor_id}')
def delete_autor(autor_id: int, session: Session = Depends(get_session)):
    """F3: Excluir um autor"""
    try:
        success = AutorService.delete_autor(session, autor_id)
        if not success:
            raise HTTPException(status_code=404, detail='Autor não encontrado')
        return {'message': 'Autor excluído com sucesso'}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'Erro no endpoint delete_autor: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))
