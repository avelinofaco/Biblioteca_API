from datetime import date
from typing import List, Optional

from config.database import get_session
from config.logging_config import logger
from fastapi import APIRouter, Depends, HTTPException, Query
from models.models import StatusEmprestimo
from schemas.schemas import (
    CountResponse,
    EmprestimoCreate,
    EmprestimoResponse,
    EmprestimoUpdate,
    PaginatedResponse,
)
from services.emprestimo_service import EmprestimoService
from sqlmodel import Session

router = APIRouter(prefix='/emprestimos', tags=['emprestimos'])


@router.post('/', response_model=EmprestimoResponse)
def create_emprestimo(
    emprestimo: EmprestimoCreate, session: Session = Depends(get_session)
):
    """F1: Inserir um empréstimo no banco de dados"""
    try:
        return EmprestimoService.create_emprestimo(session, emprestimo)
    except Exception as e:
        logger.error(f'Erro no endpoint create_emprestimo: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/', response_model=PaginatedResponse)
def list_emprestimos(
    page: int = Query(1, ge=1, description='Número da página'),
    limit: int = Query(10, ge=1, le=100, description='Limite de itens por página'),
    session: Session = Depends(get_session),
):
    """F2 e F5: Listar todos os empréstimos com paginação"""
    try:
        skip = (page - 1) * limit
        result = EmprestimoService.get_all_emprestimos(session, skip, limit)

        return PaginatedResponse(
            items=[
                EmprestimoResponse.model_validate(emprestimo)
                for emprestimo in result['items']
            ],
            total=result['total'],
            page=result['page'],
            limit=result['limit'],
            total_pages=result['total_pages'],
        )
    except Exception as e:
        logger.error(f'Erro no endpoint list_emprestimos: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/count', response_model=CountResponse)
def count_emprestimos(session: Session = Depends(get_session)):
    """F4: Mostrar a quantidade de empréstimos"""
    try:
        count = EmprestimoService.count_emprestimos(session)
        return CountResponse(total=count, entidade='emprestimos')
    except Exception as e:
        logger.error(f'Erro no endpoint count_emprestimos: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/search', response_model=List[EmprestimoResponse])
def search_emprestimos(
    usuario_id: Optional[int] = Query(None, description='Filtrar por usuário'),
    livro_id: Optional[int] = Query(None, description='Filtrar por livro'),
    status: Optional[StatusEmprestimo] = Query(None, description='Filtrar por status'),
    data_inicio: Optional[date] = Query(None, description='Data início do período'),
    data_fim: Optional[date] = Query(None, description='Data fim do período'),
    session: Session = Depends(get_session),
):
    """F6: Filtrar empréstimos por atributos específicos"""
    try:
        emprestimos = EmprestimoService.search_emprestimos(
            session, usuario_id, livro_id, status, data_inicio, data_fim
        )
        return [
            EmprestimoResponse.model_validate(emprestimo) for emprestimo in emprestimos
        ]
    except Exception as e:
        logger.error(f'Erro no endpoint search_emprestimos: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/{emprestimo_id}', response_model=EmprestimoResponse)
def get_emprestimo(emprestimo_id: int, session: Session = Depends(get_session)):
    """F3: Ler um empréstimo específico"""
    try:
        emprestimo = EmprestimoService.get_emprestimo_by_id(session, emprestimo_id)
        if not emprestimo:
            raise HTTPException(status_code=404, detail='Empréstimo não encontrado')
        return EmprestimoResponse.model_validate(emprestimo)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'Erro no endpoint get_emprestimo: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))


@router.put('/{emprestimo_id}', response_model=EmprestimoResponse)
def update_emprestimo(
    emprestimo_id: int,
    emprestimo_update: EmprestimoUpdate,
    session: Session = Depends(get_session),
):
    """F3: Atualizar um empréstimo"""
    try:
        emprestimo = EmprestimoService.update_emprestimo(
            session, emprestimo_id, emprestimo_update
        )
        if not emprestimo:
            raise HTTPException(status_code=404, detail='Empréstimo não encontrado')
        return EmprestimoResponse.model_validate(emprestimo)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'Erro no endpoint update_emprestimo: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))


@router.delete('/{emprestimo_id}')
def delete_emprestimo(emprestimo_id: int, session: Session = Depends(get_session)):
    """F3: Excluir um empréstimo"""
    try:
        success = EmprestimoService.delete_emprestimo(session, emprestimo_id)
        if not success:
            raise HTTPException(status_code=404, detail='Empréstimo não encontrado')
        return {'message': 'Empréstimo excluído com sucesso'}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'Erro no endpoint delete_emprestimo: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/{emprestimo_id}/devolver')
def devolver_livro(emprestimo_id: int, session: Session = Depends(get_session)):
    """Endpoint específico para devolução de livro"""
    try:
        emprestimo_update = EmprestimoUpdate(data_devolucao_real=date.today())
        emprestimo = EmprestimoService.update_emprestimo(
            session, emprestimo_id, emprestimo_update
        )
        if not emprestimo:
            raise HTTPException(status_code=404, detail='Empréstimo não encontrado')
        return {'message': 'Livro devolvido com sucesso'}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'Erro no endpoint devolver_livro: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))
