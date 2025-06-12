from math import ceil
from typing import List, Optional

from config.logging_config import logger
from models.models import Usuario
from schemas.schemas import UsuarioCreate, UsuarioUpdate
from sqlmodel import Session, select


class UsuarioService:
    @staticmethod
    def create_usuario(session: Session, usuario_data: UsuarioCreate) -> Usuario:
        try:
            # Verificar se já existe um usuário com o mesmo email
            existing = session.exec(
                select(Usuario).where(Usuario.email == usuario_data.email)
            ).first()

            if existing:
                raise ValueError(f"Usuário com email '{usuario_data.email}' já existe")

            usuario = Usuario(**usuario_data.model_dump())
            session.add(usuario)
            session.commit()
            session.refresh(usuario)
            logger.info(f'Usuário criado com sucesso: ID {usuario.id}')
            return usuario
        except Exception as e:
            session.rollback()
            logger.error(f'Erro ao criar usuário: {str(e)}')
            raise

    @staticmethod
    def get_usuario_by_id(session: Session, usuario_id: int) -> Optional[Usuario]:
        try:
            usuario = session.get(Usuario, usuario_id)
            if usuario:
                logger.info(f'Usuário encontrado: ID {usuario_id}')
            else:
                logger.warning(f'Usuário não encontrado: ID {usuario_id}')
            return usuario
        except Exception as e:
            logger.error(f'Erro ao buscar usuário por ID {usuario_id}: {str(e)}')
            raise

    @staticmethod
    def get_all_usuarios(session: Session, skip: int = 0, limit: int = 100) -> dict:
        try:
            # Contagem total
            count_statement = select(Usuario)
            total = len(session.exec(count_statement).all())

            # Busca paginada
            statement = select(Usuario).offset(skip).limit(limit)
            usuarios = session.exec(statement).all()

            total_pages = ceil(total / limit) if limit > 0 else 1
            page = (skip // limit) + 1 if limit > 0 else 1

            logger.info(f'Listagem de usuários: {len(usuarios)} encontrados')

            return {
                'items': usuarios,
                'total': total,
                'page': page,
                'limit': limit,
                'total_pages': total_pages,
            }
        except Exception as e:
            logger.error(f'Erro ao listar usuários: {str(e)}')
            raise

    @staticmethod
    def update_usuario(
        session: Session, usuario_id: int, usuario_update: UsuarioUpdate
    ) -> Optional[Usuario]:
        try:
            usuario = session.get(Usuario, usuario_id)
            if not usuario:
                logger.warning(
                    f'Usuário não encontrado para atualização: ID {usuario_id}'
                )
                return None

            update_data = usuario_update.model_dump(exclude_unset=True)

            # Verificar se o novo email já existe (se estiver sendo alterado)
            if 'email' in update_data and update_data['email'] != usuario.email:
                existing = session.exec(
                    select(Usuario).where(Usuario.email == update_data['email'])
                ).first()
                if existing:
                    raise ValueError(
                        f"Usuário com email '{update_data['email']}' já existe"
                    )

            for field, value in update_data.items():
                setattr(usuario, field, value)

            session.commit()
            session.refresh(usuario)
            logger.info(f'Usuário atualizado com sucesso: ID {usuario_id}')
            return usuario
        except Exception as e:
            session.rollback()
            logger.error(f'Erro ao atualizar usuário ID {usuario_id}: {str(e)}')
            raise

    @staticmethod
    def delete_usuario(session: Session, usuario_id: int) -> bool:
        try:
            usuario = session.get(Usuario, usuario_id)
            if not usuario:
                logger.warning(f'Usuário não encontrado para exclusão: ID {usuario_id}')
                return False

            session.delete(usuario)
            session.commit()
            logger.info(f'Usuário excluído com sucesso: ID {usuario_id}')
            return True
        except Exception as e:
            session.rollback()
            logger.error(f'Erro ao excluir usuário ID {usuario_id}: {str(e)}')
            raise

    @staticmethod
    def count_usuarios(session: Session) -> int:
        try:
            statement = select(Usuario)
            count = len(session.exec(statement).all())
            logger.info(f'Contagem de usuários: {count}')
            return count
        except Exception as e:
            logger.error(f'Erro ao contar usuários: {str(e)}')
            raise

    @staticmethod
    def search_usuarios(
        session: Session,
        nome: Optional[str] = None,
        email: Optional[str] = None,
        ativo: Optional[bool] = None,
    ) -> List[Usuario]:
        try:
            statement = select(Usuario)

            if nome:
                statement = statement.where(Usuario.nome.contains(nome))

            if email:
                statement = statement.where(Usuario.email.contains(email))

            if ativo is not None:
                statement = statement.where(Usuario.ativo == ativo)

            usuarios = session.exec(statement).all()
            logger.info(f'Busca de usuários: {len(usuarios)} encontrados')
            return usuarios
        except Exception as e:
            logger.error(f'Erro na busca de usuários: {str(e)}')
            raise
