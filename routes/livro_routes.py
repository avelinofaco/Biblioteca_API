from typing import List, Optional

from config.database import get_session
from config.logging_config import logger
from fastapi import APIRouter, Depends, HTTPException, Query
from schemas.schemas import (
    CountResponse,
    LivroCreate,
    LivroResponse,
    LivroUpdate,
    PaginatedResponse,
)
from services.livro_service import LivroService
from sqlmodel import Session

router = APIRouter(prefix='/livros', tags=['livros'])


@router.post('/', response_model=LivroResponse)
def create_livro(livro: LivroCreate, session: Session = Depends(get_session)):
    """F1: Inserir um livro no banco de dados"""
    try:
        return LivroService.create_livro(session, livro)
    except Exception as e:
        logger.error(f'Erro no endpoint create_livro: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))


from schemas.schemas import (
    LivroResponse,  # certifique-se de importar corretamente
)


@router.get('/', response_model=PaginatedResponse[LivroResponse])
def list_livros(
    page: int = Query(1, ge=1, description='Número da página'),
    limit: int = Query(10, ge=1, le=100, description='Limite de itens por página'),
    session: Session = Depends(get_session),
):
    """F2 e F5: Listar todos os livros com paginação"""
    try:
        skip = (page - 1) * limit
        result = LivroService.get_all_livros(session, skip, limit)

        livros_response = [
            LivroResponse.model_validate(livro) for livro in result['items']
        ]

        return PaginatedResponse[LivroResponse](
            items=livros_response,
            total=result['total'],
            page=result['page'],
            limit=result['limit'],
            total_pages=result['total_pages'],
        )
    except Exception as e:
        logger.error(f'Erro no endpoint list_livros: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/count', response_model=CountResponse)
def count_livros(session: Session = Depends(get_session)):
    """F4: Mostrar a quantidade de livros"""
    try:
        count = LivroService.count_livros(session)
        return CountResponse(total=count, entidade='livros')
    except Exception as e:
        logger.error(f'Erro no endpoint count_livros: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/search', response_model=List[LivroResponse])
def search_livros(
    titulo: Optional[str] = Query(None, description='Buscar por título'),
    autor: Optional[str] = Query(None, description='Filtrar por autor'),
    categoria: Optional[str] = Query(None, description='Filtrar por categoria'),
    ano_min: Optional[int] = Query(None, description='Ano mínimo de publicação'),
    ano_max: Optional[int] = Query(None, description='Ano máximo de publicação'),
    session: Session = Depends(get_session),
):
    """F6: Filtrar livros por atributos específicos"""
    try:
        livros = LivroService.search_livros(
            session, titulo, autor, categoria, ano_min, ano_max
        )
        return [LivroResponse.model_validate(livro) for livro in livros]
    except Exception as e:
        logger.error(f'Erro no endpoint search_livros: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/{livro_id}', response_model=LivroResponse)
def get_livro(livro_id: int, session: Session = Depends(get_session)):
    """F3: Ler um livro específico"""
    try:
        livro = LivroService.get_livro_by_id(session, livro_id)
        if not livro:
            raise HTTPException(status_code=404, detail='Livro não encontrado')
        return LivroResponse.model_validate(livro)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'Erro no endpoint get_livro: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))


@router.put('/{livro_id}', response_model=LivroResponse)
def update_livro(
    livro_id: int,
    livro_update: LivroUpdate,
    session: Session = Depends(get_session),
):
    """F3: Atualizar um livro"""
    try:
        livro = LivroService.update_livro(session, livro_id, livro_update)
        if not livro:
            raise HTTPException(status_code=404, detail='Livro não encontrado')
        return LivroResponse.model_validate(livro)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'Erro no endpoint update_livro: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))


@router.delete('/{livro_id}')
def delete_livro(livro_id: int, session: Session = Depends(get_session)):
    """F3: Excluir um livro"""
    try:
        success = LivroService.delete_livro(session, livro_id)
        if not success:
            raise HTTPException(status_code=404, detail='Livro não encontrado')
        return {'message': 'Livro excluído com sucesso'}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'Erro no endpoint delete_livro: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))
