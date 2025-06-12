from math import ceil
from typing import List, Optional

from config.logging_config import logger
from models.models import Categoria
from schemas.schemas import CategoriaCreate, CategoriaUpdate
from sqlmodel import Session, select


class CategoriaService:
    @staticmethod
    def create_categoria(session: Session, categoria_data: CategoriaCreate) -> Categoria:
        try:
            # Verificar se já existe uma categoria com o mesmo nome
            existing = session.exec(
                select(Categoria).where(Categoria.nome == categoria_data.nome)
            ).first()

            if existing:
                raise ValueError(f"Categoria com nome '{categoria_data.nome}' já existe")

            categoria = Categoria(**categoria_data.model_dump())
            session.add(categoria)
            session.commit()
            session.refresh(categoria)
            logger.info(f'Categoria criada com sucesso: ID {categoria.id}')
            return categoria
        except Exception as e:
            session.rollback()
            logger.error(f'Erro ao criar categoria: {str(e)}')
            raise

    @staticmethod
    def get_categoria_by_id(session: Session, categoria_id: int) -> Optional[Categoria]:
        try:
            categoria = session.get(Categoria, categoria_id)
            if categoria:
                logger.info(f'Categoria encontrada: ID {categoria_id}')
            else:
                logger.warning(f'Categoria não encontrada: ID {categoria_id}')
            return categoria
        except Exception as e:
            logger.error(f'Erro ao buscar categoria por ID {categoria_id}: {str(e)}')
            raise

    @staticmethod
    def get_all_categorias(session: Session, skip: int = 0, limit: int = 100) -> dict:
        try:
            # Contagem total
            count_statement = select(Categoria)
            total = len(session.exec(count_statement).all())

            # Busca paginada
            statement = select(Categoria).offset(skip).limit(limit)
            categorias = session.exec(statement).all()

            total_pages = ceil(total / limit) if limit > 0 else 1
            page = (skip // limit) + 1 if limit > 0 else 1

            logger.info(f'Listagem de categorias: {len(categorias)} encontradas')

            return {
                'items': categorias,
                'total': total,
                'page': page,
                'limit': limit,
                'total_pages': total_pages,
            }
        except Exception as e:
            logger.error(f'Erro ao listar categorias: {str(e)}')
            raise

    @staticmethod
    def update_categoria(
        session: Session, categoria_id: int, categoria_update: CategoriaUpdate
    ) -> Optional[Categoria]:
        try:
            categoria = session.get(Categoria, categoria_id)
            if not categoria:
                logger.warning(
                    f'Categoria não encontrada para atualização: ID {categoria_id}'
                )
                return None

            update_data = categoria_update.model_dump(exclude_unset=True)

            # Verificar se o novo nome já existe (se estiver sendo alterado)
            if 'nome' in update_data and update_data['nome'] != categoria.nome:
                existing = session.exec(
                    select(Categoria).where(Categoria.nome == update_data['nome'])
                ).first()
                if existing:
                    raise ValueError(
                        f"Categoria com nome '{update_data['nome']}' já existe"
                    )

            for field, value in update_data.items():
                setattr(categoria, field, value)

            session.commit()
            session.refresh(categoria)
            logger.info(f'Categoria atualizada com sucesso: ID {categoria_id}')
            return categoria
        except Exception as e:
            session.rollback()
            logger.error(f'Erro ao atualizar categoria ID {categoria_id}: {str(e)}')
            raise

    @staticmethod
    def delete_categoria(session: Session, categoria_id: int) -> bool:
        try:
            categoria = session.get(Categoria, categoria_id)
            if not categoria:
                logger.warning(
                    f'Categoria não encontrada para exclusão: ID {categoria_id}'
                )
                return False

            session.delete(categoria)
            session.commit()
            logger.info(f'Categoria excluída com sucesso: ID {categoria_id}')
            return True
        except Exception as e:
            session.rollback()
            logger.error(f'Erro ao excluir categoria ID {categoria_id}: {str(e)}')
            raise

    @staticmethod
    def count_categorias(session: Session) -> int:
        try:
            statement = select(Categoria)
            count = len(session.exec(statement).all())
            logger.info(f'Contagem de categorias: {count}')
            return count
        except Exception as e:
            logger.error(f'Erro ao contar categorias: {str(e)}')
            raise

    @staticmethod
    def search_categorias(
        session: Session,
        nome: Optional[str] = None,
        ativa: Optional[bool] = None,
    ) -> List[Categoria]:
        try:
            statement = select(Categoria)

            if nome:
                statement = statement.where(Categoria.nome.contains(nome))

            if ativa is not None:
                statement = statement.where(Categoria.ativa == ativa)

            categorias = session.exec(statement).all()
            logger.info(f'Busca de categorias: {len(categorias)} encontradas')
            return categorias
        except Exception as e:
            logger.error(f'Erro na busca de categorias: {str(e)}')
