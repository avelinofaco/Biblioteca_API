from math import ceil
from typing import List, Optional

from config.logging_config import logger
from models.models import PerfilUsuario, Usuario
from schemas.schemas import PerfilUsuarioCreate, PerfilUsuarioUpdate
from sqlmodel import Session, select


class PerfilUsuarioService:
    @staticmethod
    def create_perfil_usuario(
        session: Session, perfil_data: PerfilUsuarioCreate
    ) -> PerfilUsuario:
        try:
            # Verificar se o usuário existe
            usuario = session.get(Usuario, perfil_data.usuario_id)
            if not usuario:
                raise ValueError(
                    f'Usuário com ID {perfil_data.usuario_id} não encontrado'
                )

            # Verificar se já existe um perfil para este usuário
            existing = session.exec(
                select(PerfilUsuario).where(
                    PerfilUsuario.usuario_id == perfil_data.usuario_id
                )
            ).first()

            if existing:
                raise ValueError(
                    f'Perfil para usuário ID {perfil_data.usuario_id} já existe'
                )

            perfil = PerfilUsuario(**perfil_data.model_dump())
            session.add(perfil)
            session.commit()
            session.refresh(perfil)
            logger.info(f'Perfil de usuário criado com sucesso: ID {perfil.id}')
            return perfil
        except Exception as e:
            session.rollback()
            logger.error(f'Erro ao criar perfil de usuário: {str(e)}')
            raise

    @staticmethod
    def get_perfil_by_id(session: Session, perfil_id: int) -> Optional[PerfilUsuario]:
        try:
            perfil = session.get(PerfilUsuario, perfil_id)
            if perfil:
                logger.info(f'Perfil encontrado: ID {perfil_id}')
            else:
                logger.warning(f'Perfil não encontrado: ID {perfil_id}')
            return perfil
        except Exception as e:
            logger.error(f'Erro ao buscar perfil por ID {perfil_id}: {str(e)}')
            raise

    @staticmethod
    def get_perfil_by_usuario_id(
        session: Session, usuario_id: int
    ) -> Optional[PerfilUsuario]:
        try:
            perfil = session.exec(
                select(PerfilUsuario).where(PerfilUsuario.usuario_id == usuario_id)
            ).first()
            if perfil:
                logger.info(f'Perfil encontrado para usuário ID {usuario_id}')
            else:
                logger.warning(f'Perfil não encontrado para usuário ID {usuario_id}')
            return perfil
        except Exception as e:
            logger.error(f'Erro ao buscar perfil por usuário ID {usuario_id}: {str(e)}')
            raise

    @staticmethod
    def get_all_perfis(session: Session, skip: int = 0, limit: int = 100) -> dict:
        try:
            # Contagem total
            count_statement = select(PerfilUsuario)
            total = len(session.exec(count_statement).all())

            # Busca paginada
            statement = select(PerfilUsuario).offset(skip).limit(limit)
            perfis = session.exec(statement).all()

            total_pages = ceil(total / limit) if limit > 0 else 1
            page = (skip // limit) + 1 if limit > 0 else 1

            logger.info(f'Listagem de perfis: {len(perfis)} encontrados')

            return {
                'items': perfis,
                'total': total,
                'page': page,
                'limit': limit,
                'total_pages': total_pages,
            }
        except Exception as e:
            logger.error(f'Erro ao listar perfis: {str(e)}')
            raise

    @staticmethod
    def update_perfil(
        session: Session, perfil_id: int, perfil_update: PerfilUsuarioUpdate
    ) -> Optional[PerfilUsuario]:
        try:
            perfil = session.get(PerfilUsuario, perfil_id)
            if not perfil:
                logger.warning(f'Perfil não encontrado para atualização: ID {perfil_id}')
                return None

            update_data = perfil_update.model_dump(exclude_unset=True)

            for field, value in update_data.items():
                setattr(perfil, field, value)

            session.commit()
            session.refresh(perfil)
            logger.info(f'Perfil atualizado com sucesso: ID {perfil_id}')
            return perfil
        except Exception as e:
            session.rollback()
            logger.error(f'Erro ao atualizar perfil ID {perfil_id}: {str(e)}')
            raise

    @staticmethod
    def delete_perfil(session: Session, perfil_id: int) -> bool:
        try:
            perfil = session.get(PerfilUsuario, perfil_id)
            if not perfil:
                logger.warning(f'Perfil não encontrado para exclusão: ID {perfil_id}')
                return False

            session.delete(perfil)
            session.commit()
            logger.info(f'Perfil excluído com sucesso: ID {perfil_id}')
            return True
        except Exception as e:
            session.rollback()
            logger.error(f'Erro ao excluir perfil ID {perfil_id}: {str(e)}')
            raise

    @staticmethod
    def count_perfis(session: Session) -> int:
        try:
            statement = select(PerfilUsuario)
            count = len(session.exec(statement).all())
            logger.info(f'Contagem de perfis: {count}')
            return count
        except Exception as e:
            logger.error(f'Erro ao contar perfis: {str(e)}')
            raise

    @staticmethod
    def search_perfis(
        session: Session,
        profissao: Optional[str] = None,
        interesses: Optional[str] = None,
    ) -> List[PerfilUsuario]:
        try:
            statement = select(PerfilUsuario)

            if profissao:
                statement = statement.where(PerfilUsuario.profissao.contains(profissao))

            if interesses:
                statement = statement.where(
                    PerfilUsuario.interesses_literarios.contains(interesses)
                )

            perfis = session.exec(statement).all()
            logger.info(f'Busca de perfis: {len(perfis)} encontrados')
            return perfis
        except Exception as e:
            logger.error(f'Erro na busca de perfis: {str(e)}')
            raise
