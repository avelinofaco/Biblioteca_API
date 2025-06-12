from datetime import date, datetime
from math import ceil
from typing import List, Optional

from config.logging_config import logger
from models.models import Emprestimo, Livro, StatusEmprestimo, Usuario
from schemas.schemas import EmprestimoCreate, EmprestimoUpdate
from sqlmodel import Session, select


class EmprestimoService:
    @staticmethod
    def create_emprestimo(
        session: Session, emprestimo_data: EmprestimoCreate
    ) -> Emprestimo:
        try:
            # Verificar se o usuário existe
            usuario = session.get(Usuario, emprestimo_data.usuario_id)
            if not usuario:
                raise ValueError(
                    f'Usuário com ID {emprestimo_data.usuario_id} não encontrado'
                )

            if not usuario.ativo:
                raise ValueError('Usuário não está ativo')

            # Verificar se o livro existe e está disponível
            livro = session.get(Livro, emprestimo_data.livro_id)
            if not livro:
                raise ValueError(
                    f'Livro com ID {emprestimo_data.livro_id} não encontrado'
                )

            if livro.quantidade_disponivel <= 0:
                raise ValueError('Livro não está disponível para empréstimo')

            # Criar o empréstimo
            emprestimo = Emprestimo(**emprestimo_data.model_dump())
            session.add(emprestimo)

            # Atualizar quantidade disponível do livro
            livro.quantidade_disponivel -= 1

            session.commit()
            session.refresh(emprestimo)
            logger.info(f'Empréstimo criado com sucesso: ID {emprestimo.id}')
            return emprestimo
        except Exception as e:
            session.rollback()
            logger.error(f'Erro ao criar empréstimo: {str(e)}')
            raise

    @staticmethod
    def get_emprestimo_by_id(
        session: Session, emprestimo_id: int
    ) -> Optional[Emprestimo]:
        try:
            emprestimo = session.get(Emprestimo, emprestimo_id)
            if emprestimo:
                logger.info(f'Empréstimo encontrado: ID {emprestimo_id}')
            else:
                logger.warning(f'Empréstimo não encontrado: ID {emprestimo_id}')
            return emprestimo
        except Exception as e:
            logger.error(f'Erro ao buscar empréstimo por ID {emprestimo_id}: {str(e)}')
            raise

    @staticmethod
    def get_all_emprestimos(session: Session, skip: int = 0, limit: int = 100) -> dict:
        try:
            # Contagem total
            count_statement = select(Emprestimo)
            total = len(session.exec(count_statement).all())

            # Busca paginada
            statement = select(Emprestimo).offset(skip).limit(limit)
            emprestimos = session.exec(statement).all()

            total_pages = ceil(total / limit) if limit > 0 else 1
            page = (skip // limit) + 1 if limit > 0 else 1

            logger.info(f'Listagem de empréstimos: {len(emprestimos)} encontrados')

            return {
                'items': emprestimos,
                'total': total,
                'page': page,
                'limit': limit,
                'total_pages': total_pages,
            }
        except Exception as e:
            logger.error(f'Erro ao listar empréstimos: {str(e)}')
            raise

    @staticmethod
    def update_emprestimo(
        session: Session,
        emprestimo_id: int,
        emprestimo_update: EmprestimoUpdate,
    ) -> Optional[Emprestimo]:
        try:
            emprestimo = session.get(Emprestimo, emprestimo_id)
            if not emprestimo:
                logger.warning(
                    f'Empréstimo não encontrado para atualização: ID {emprestimo_id}'
                )
                return None

            update_data = emprestimo_update.model_dump(exclude_unset=True)

            # Se está devolvendo o livro
            if (
                'data_devolucao_real' in update_data
                and update_data['data_devolucao_real'] is not None
            ):
                if emprestimo.status == StatusEmprestimo.ATIVO:
                    livro = session.get(Livro, emprestimo.livro_id)
                    if livro:
                        livro.quantidade_disponivel += 1
                    update_data['status'] = StatusEmprestimo.DEVOLVIDO

            for field, value in update_data.items():
                setattr(emprestimo, field, value)

            session.commit()
            session.refresh(emprestimo)
            logger.info(f'Empréstimo atualizado com sucesso: ID {emprestimo_id}')
            return emprestimo
        except Exception as e:
            session.rollback()
            logger.error(f'Erro ao atualizar empréstimo ID {emprestimo_id}: {str(e)}')
            raise

    @staticmethod
    def delete_emprestimo(session: Session, emprestimo_id: int) -> bool:
        try:
            emprestimo = session.get(Emprestimo, emprestimo_id)
            if not emprestimo:
                logger.warning(
                    f'Empréstimo não encontrado para exclusão: ID {emprestimo_id}'
                )
                return False

            # Se o empréstimo estava ativo, devolver o livro
            if emprestimo.status == StatusEmprestimo.ATIVO:
                livro = session.get(Livro, emprestimo.livro_id)
                if livro:
                    livro.quantidade_disponivel += 1

            session.delete(emprestimo)
            session.commit()
            logger.info(f'Empréstimo excluído com sucesso: ID {emprestimo_id}')
            return True
        except Exception as e:
            session.rollback()
            logger.error(f'Erro ao excluir empréstimo ID {emprestimo_id}: {str(e)}')
            raise

    @staticmethod
    def count_emprestimos(session: Session) -> int:
        try:
            statement = select(Emprestimo)
            count = len(session.exec(statement).all())
            logger.info(f'Contagem de empréstimos: {count}')
            return count
        except Exception as e:
            logger.error(f'Erro ao contar empréstimos: {str(e)}')
            raise

    @staticmethod
    def search_emprestimos(
        session: Session,
        usuario_id: Optional[int] = None,
        livro_id: Optional[int] = None,
        status: Optional[StatusEmprestimo] = None,
        data_inicio: Optional[date] = None,
        data_fim: Optional[date] = None,
    ) -> List[Emprestimo]:
        try:
            statement = select(Emprestimo)

            if usuario_id:
                statement = statement.where(Emprestimo.usuario_id == usuario_id)

            if livro_id:
                statement = statement.where(Emprestimo.livro_id == livro_id)

            if status:
                statement = statement.where(Emprestimo.status == status)

            if data_inicio:
                statement = statement.where(
                    Emprestimo.data_emprestimo
                    >= datetime.combine(data_inicio, datetime.min.time())
                )

            if data_fim:
                statement = statement.where(
                    Emprestimo.data_emprestimo
                    <= datetime.combine(data_fim, datetime.max.time())
                )

            emprestimos = session.exec(statement).all()
            logger.info(f'Busca de empréstimos: {len(emprestimos)} encontrados')
            return emprestimos
        except Exception as e:
            logger.error(f'Erro na busca de empréstimos: {str(e)}')
            raise
