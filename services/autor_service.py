from math import ceil
from typing import List, Optional

from config.logging_config import logger
from models.models import Autor
from schemas.schemas import AutorCreate, AutorUpdate
from sqlmodel import Session, select


class AutorService:
    @staticmethod
    def create_autor(session: Session, autor_data: AutorCreate) -> Autor:
        try:
            autor = Autor(**autor_data.model_dump())
            session.add(autor)
            session.commit()
            session.refresh(autor)
            logger.info(f'Autor criado com sucesso: ID {autor.id}')
            return autor
        except Exception as e:
            session.rollback()
            logger.error(f'Erro ao criar autor: {str(e)}')
            raise

    @staticmethod
    def get_autor_by_id(session: Session, autor_id: int) -> Optional[Autor]:
        try:
            autor = session.get(Autor, autor_id)
            if autor:
                logger.info(f'Autor encontrado: ID {autor_id}')
            else:
                logger.warning(f'Autor não encontrado: ID {autor_id}')
            return autor
        except Exception as e:
            logger.error(f'Erro ao buscar autor por ID {autor_id}: {str(e)}')
            raise

    @staticmethod
    def get_all_autores(session: Session, skip: int = 0, limit: int = 100) -> dict:
        try:
            # Contagem total
            count_statement = select(Autor)
            total = len(session.exec(count_statement).all())

            # Busca paginada
            statement = select(Autor).offset(skip).limit(limit)
            autores = session.exec(statement).all()

            total_pages = ceil(total / limit) if limit > 0 else 1
            page = (skip // limit) + 1 if limit > 0 else 1

            logger.info(f'Listagem de autores: {len(autores)} encontrados')

            return {
                'items': autores,
                'total': total,
                'page': page,
                'limit': limit,
                'total_pages': total_pages,
            }
        except Exception as e:
            logger.error(f'Erro ao listar autores: {str(e)}')
            raise

    @staticmethod
    def update_autor(
        session: Session, autor_id: int, autor_update: AutorUpdate
    ) -> Optional[Autor]:
        try:
            autor = session.get(Autor, autor_id)
            if not autor:
                logger.warning(f'Autor não encontrado para atualização: ID {autor_id}')
                return None

            update_data = autor_update.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(autor, field, value)

            session.commit()
            session.refresh(autor)
            logger.info(f'Autor atualizado com sucesso: ID {autor_id}')
            return autor
        except Exception as e:
            session.rollback()
            logger.error(f'Erro ao atualizar autor ID {autor_id}: {str(e)}')
            raise

    @staticmethod
    def delete_autor(session: Session, autor_id: int) -> bool:
        try:
            autor = session.get(Autor, autor_id)
            if not autor:
                logger.warning(f'Autor não encontrado para exclusão: ID {autor_id}')
                return False

            session.delete(autor)
            session.commit()
            logger.info(f'Autor excluído com sucesso: ID {autor_id}')
            return True
        except Exception as e:
            session.rollback()
            logger.error(f'Erro ao excluir autor ID {autor_id}: {str(e)}')
            raise

    @staticmethod
    def count_autores(session: Session) -> int:
        try:
            statement = select(Autor)
            count = len(session.exec(statement).all())
            logger.info(f'Contagem de autores: {count}')
            return count
        except Exception as e:
            logger.error(f'Erro ao contar autores: {str(e)}')
            raise

    @staticmethod
    def search_autores(
        session: Session,
        nome: Optional[str] = None,
        nacionalidade: Optional[str] = None,
    ) -> List[Autor]:
        try:
            statement = select(Autor)

            if nome:
                statement = statement.where(
                    (Autor.nome.contains(nome)) | (Autor.sobrenome.contains(nome))
                )

            if nacionalidade:
                statement = statement.where(Autor.nacionalidade.contains(nacionalidade))

            autores = session.exec(statement).all()
            logger.info(f'Busca de autores: {len(autores)} encontrados')
            return autores
        except Exception as e:
            logger.error(f'Erro na busca de autores: {str(e)}')
            raise
