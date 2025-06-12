from typing import List, Optional

from config.database import get_session
from config.logging_config import logger
from fastapi import APIRouter, Depends, HTTPException, Query
from schemas.schemas import (
    CountResponse,
    PaginatedResponse,
    PerfilUsuarioCreate,
    PerfilUsuarioResponse,
    PerfilUsuarioUpdate,
)
from services.perfil_usuario_service import PerfilUsuarioService
from sqlmodel import Session

router = APIRouter(prefix='/perfis', tags=['perfis-usuario'])


@router.post('/', response_model=PerfilUsuarioResponse)
def create_perfil_usuario(
    perfil: PerfilUsuarioCreate, session: Session = Depends(get_session)
):
    """F1: Inserir um perfil de usuário no banco de dados"""
    try:
        return PerfilUsuarioService.create_perfil_usuario(session, perfil)
    except Exception as e:
        logger.error(f'Erro no endpoint create_perfil_usuario: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/', response_model=PaginatedResponse)
def list_perfis_usuario(
    page: int = Query(1, ge=1, description='Número da página'),
    limit: int = Query(10, ge=1, le=100, description='Limite de itens por página'),
    session: Session = Depends(get_session),
):
    """F2 e F5: Listar todos os perfis com paginação"""
    try:
        skip = (page - 1) * limit
        result = PerfilUsuarioService.get_all_perfis(session, skip, limit)

        return PaginatedResponse(
            items=[
                PerfilUsuarioResponse.model_validate(perfil) for perfil in result['items']
            ],
            total=result['total'],
            page=result['page'],
            limit=result['limit'],
            total_pages=result['total_pages'],
        )
    except Exception as e:
        logger.error(f'Erro no endpoint list_perfis_usuario: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/count', response_model=CountResponse)
def count_perfis_usuario(session: Session = Depends(get_session)):
    """F4: Mostrar a quantidade de perfis"""
    try:
        count = PerfilUsuarioService.count_perfis(session)
        return CountResponse(total=count, entidade='perfis')
    except Exception as e:
        logger.error(f'Erro no endpoint count_perfis_usuario: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/search', response_model=List[PerfilUsuarioResponse])
def search_perfis_usuario(
    profissao: Optional[str] = Query(None, description='Buscar por profissão'),
    interesses: Optional[str] = Query(
        None, description='Filtrar por interesses literários'
    ),
    session: Session = Depends(get_session),
):
    """F6: Filtrar perfis por atributos específicos"""
    try:
        perfis = PerfilUsuarioService.search_perfis(session, profissao, interesses)
        return [PerfilUsuarioResponse.model_validate(perfil) for perfil in perfis]
    except Exception as e:
        logger.error(f'Erro no endpoint search_perfis_usuario: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/usuario/{usuario_id}', response_model=PerfilUsuarioResponse)
def get_perfil_by_usuario(usuario_id: int, session: Session = Depends(get_session)):
    """Buscar perfil por ID do usuário"""
    try:
        perfil = PerfilUsuarioService.get_perfil_by_usuario_id(session, usuario_id)
        if not perfil:
            raise HTTPException(
                status_code=404,
                detail='Perfil não encontrado para este usuário',
            )
        return PerfilUsuarioResponse.model_validate(perfil)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'Erro no endpoint get_perfil_by_usuario: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/{perfil_id}', response_model=PerfilUsuarioResponse)
def get_perfil_usuario(perfil_id: int, session: Session = Depends(get_session)):
    """F3: Ler um perfil específico"""
    try:
        perfil = PerfilUsuarioService.get_perfil_by_id(session, perfil_id)
        if not perfil:
            raise HTTPException(status_code=404, detail='Perfil não encontrado')
        return PerfilUsuarioResponse.model_validate(perfil)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'Erro no endpoint get_perfil_usuario: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))


@router.put('/{perfil_id}', response_model=PerfilUsuarioResponse)
def update_perfil_usuario(
    perfil_id: int,
    perfil_update: PerfilUsuarioUpdate,
    session: Session = Depends(get_session),
):
    """F3: Atualizar um perfil"""
    try:
        perfil = PerfilUsuarioService.update_perfil(session, perfil_id, perfil_update)
        if not perfil:
            raise HTTPException(status_code=404, detail='Perfil não encontrado')
        return PerfilUsuarioResponse.model_validate(perfil)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'Erro no endpoint update_perfil_usuario: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))


@router.delete('/{perfil_id}')
def delete_perfil_usuario(perfil_id: int, session: Session = Depends(get_session)):
    """F3: Excluir um perfil"""
    try:
        success = PerfilUsuarioService.delete_perfil(session, perfil_id)
        if not success:
            raise HTTPException(status_code=404, detail='Perfil não encontrado')
        return {'message': 'Perfil excluído com sucesso'}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'Erro no endpoint delete_perfil_usuario: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))
