from typing import List, Optional

from config.database import get_session
from config.logging_config import logger
from fastapi import APIRouter, Depends, HTTPException, Query
from schemas.schemas import (
    CountResponse,
    PaginatedResponse,
    UsuarioCreate,
    UsuarioResponse,
    UsuarioUpdate,
)
from services.usuario_service import UsuarioService
from sqlmodel import Session

router = APIRouter(prefix='/usuarios', tags=['usuarios'])


@router.post('/', response_model=UsuarioResponse)
def create_usuario(usuario: UsuarioCreate, session: Session = Depends(get_session)):
    """F1: Inserir um usuário no banco de dados"""
    try:
        return UsuarioService.create_usuario(session, usuario)
    except Exception as e:
        logger.error(f'Erro no endpoint create_usuario: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/', response_model=PaginatedResponse)
def list_usuarios(
    page: int = Query(1, ge=1, description='Número da página'),
    limit: int = Query(10, ge=1, le=100, description='Limite de itens por página'),
    session: Session = Depends(get_session),
):
    """F2 e F5: Listar todos os usuários com paginação"""
    try:
        skip = (page - 1) * limit
        result = UsuarioService.get_all_usuarios(session, skip, limit)

        return PaginatedResponse(
            items=[
                UsuarioResponse.model_validate(usuario) for usuario in result['items']
            ],
            total=result['total'],
            page=result['page'],
            limit=result['limit'],
            total_pages=result['total_pages'],
        )
    except Exception as e:
        logger.error(f'Erro no endpoint list_usuarios: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/count', response_model=CountResponse)
def count_usuarios(session: Session = Depends(get_session)):
    """F4: Mostrar a quantidade de usuários"""
    try:
        count = UsuarioService.count_usuarios(session)
        return CountResponse(total=count, entidade='usuarios')
    except Exception as e:
        logger.error(f'Erro no endpoint count_usuarios: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/search', response_model=List[UsuarioResponse])
def search_usuarios(
    nome: Optional[str] = Query(None, description='Buscar por nome'),
    email: Optional[str] = Query(None, description='Filtrar por email'),
    ativo: Optional[bool] = Query(None, description='Filtrar por status ativo'),
    session: Session = Depends(get_session),
):
    """F6: Filtrar usuários por atributos específicos"""
    try:
        usuarios = UsuarioService.search_usuarios(session, nome, email, ativo)
        return [UsuarioResponse.model_validate(usuario) for usuario in usuarios]
    except Exception as e:
        logger.error(f'Erro no endpoint search_usuarios: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/{usuario_id}', response_model=UsuarioResponse)
def get_usuario(usuario_id: int, session: Session = Depends(get_session)):
    """F3: Ler um usuário específico"""
    try:
        usuario = UsuarioService.get_usuario_by_id(session, usuario_id)
        if not usuario:
            raise HTTPException(status_code=404, detail='Usuário não encontrado')
        return UsuarioResponse.model_validate(usuario)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'Erro no endpoint get_usuario: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))


@router.put('/{usuario_id}', response_model=UsuarioResponse)
def update_usuario(
    usuario_id: int,
    usuario_update: UsuarioUpdate,
    session: Session = Depends(get_session),
):
    """F3: Atualizar um usuário"""
    try:
        usuario = UsuarioService.update_usuario(session, usuario_id, usuario_update)
        if not usuario:
            raise HTTPException(status_code=404, detail='Usuário não encontrado')
        return UsuarioResponse.model_validate(usuario)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'Erro no endpoint update_usuario: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))


@router.delete('/{usuario_id}')
def delete_usuario(usuario_id: int, session: Session = Depends(get_session)):
    """F3: Excluir um usuário"""
    try:
        success = UsuarioService.delete_usuario(session, usuario_id)
        if not success:
            raise HTTPException(status_code=404, detail='Usuário não encontrado')
        return {'message': 'Usuário excluído com sucesso'}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'Erro no endpoint delete_usuario: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))
