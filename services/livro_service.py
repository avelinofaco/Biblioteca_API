from math import ceil
from typing import List, Optional

from config.logging_config import logger
from models.models import (
    Autor,
    Categoria,
    Livro,
)
from schemas.schemas import LivroCreate, LivroUpdate
from sqlalchemy import func
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select


class LivroService:
    @staticmethod
    def create_livro(session: Session, livro_data: LivroCreate) -> Livro:
        try:
            # Extrair IDs de autores e categorias
            autor_ids = livro_data.autor_ids
            categoria_ids = livro_data.categoria_ids

            # Criar dados do livro sem os IDs
            livro_dict = livro_data.model_dump(exclude={'autor_ids', 'categoria_ids'})
            livro_dict['quantidade_disponivel'] = livro_dict['quantidade_total']

            livro = Livro(**livro_dict)
            session.add(livro)
            session.commit()
            session.refresh(livro)

            # Adicionar relacionamentos com autores
            for autor_id in autor_ids:
                autor = session.get(Autor, autor_id)
                if autor:
                    livro.autores.append(autor)

            # Adicionar relacionamentos com categorias
            for categoria_id in categoria_ids:
                categoria = session.get(Categoria, categoria_id)
                if categoria:
                    livro.categorias.append(categoria)

            session.commit()
            session.refresh(livro)
            logger.info(f'Livro criado com sucesso: ID {livro.id}')
            return livro
        except Exception as e:
            session.rollback()
            logger.error(f'Erro ao criar livro: {str(e)}')
            raise

    @staticmethod
    def get_livro_by_id(session: Session, livro_id: int) -> Optional[Livro]:
        try:
            livro = session.get(Livro, livro_id)
            if livro:
                logger.info(f'Livro encontrado: ID {livro_id}')
            else:
                logger.warning(f'Livro não encontrado: ID {livro_id}')
            return livro
        except Exception as e:
            logger.error(f'Erro ao buscar livro por ID {livro_id}: {str(e)}')
            raise

    @staticmethod
    def get_all_livros(session: Session, skip: int = 0, limit: int = 100) -> dict:
        try:
            # Contagem total otimizada
            total = session.exec(select(func.count()).select_from(Livro)).one()

            # Busca paginada com carregamento das relações
            statement = (
                select(Livro)
                .options(selectinload(Livro.autores), selectinload(Livro.categorias))
                .offset(skip)
                .limit(limit)
            )
            livros = session.exec(statement).all()

            total_pages = ceil(total / limit) if limit > 0 else 1
            page = (skip // limit) + 1 if limit > 0 else 1

            logger.info(f'Listagem de livros: {len(livros)} encontrados')

            return {
                'items': livros,
                'total': total,
                'page': page,
                'limit': limit,
                'total_pages': total_pages,
            }
        except Exception as e:
            logger.error(f'Erro ao listar livros: {str(e)}')
            raise

    @staticmethod
    def update_livro(
        session: Session, livro_id: int, livro_update: LivroUpdate
    ) -> Optional[Livro]:
        try:
            livro = session.get(Livro, livro_id)
            if not livro:
                logger.warning(f'Livro não encontrado para atualização: ID {livro_id}')
                return None

            update_data = livro_update.model_dump(exclude_unset=True)

            # Tratar relacionamentos
            if 'autor_ids' in update_data:
                autor_ids = update_data.pop('autor_ids')
                livro.autores.clear()
                for autor_id in autor_ids:
                    autor = session.get(Autor, autor_id)
                    if autor:
                        livro.autores.append(autor)

            if 'categoria_ids' in update_data:
                categoria_ids = update_data.pop('categoria_ids')
                livro.categorias.clear()
                for categoria_id in categoria_ids:
                    categoria = session.get(Categoria, categoria_id)
                    if categoria:
                        livro.categorias.append(categoria)

            # Atualizar campos simples
            for field, value in update_data.items():
                setattr(livro, field, value)

            session.commit()
            session.refresh(livro)
            logger.info(f'Livro atualizado com sucesso: ID {livro_id}')
            return livro
        except Exception as e:
            session.rollback()
            logger.error(f'Erro ao atualizar livro ID {livro_id}: {str(e)}')
            raise

    @staticmethod
    def delete_livro(session: Session, livro_id: int) -> bool:
        try:
            livro = session.get(Livro, livro_id)
            if not livro:
                logger.warning(f'Livro não encontrado para exclusão: ID {livro_id}')
                return False

            session.delete(livro)
            session.commit()
            logger.info(f'Livro excluído com sucesso: ID {livro_id}')
            return True
        except Exception as e:
            session.rollback()
            logger.error(f'Erro ao excluir livro ID {livro_id}: {str(e)}')
            raise

    @staticmethod
    def count_livros(session: Session) -> int:
        try:
            statement = select(Livro)
            count = len(session.exec(statement).all())
            logger.info(f'Contagem de livros: {count}')
            return count
        except Exception as e:
            logger.error(f'Erro ao contar livros: {str(e)}')
            raise

    @staticmethod
    def search_livros(
        session: Session,
        titulo: Optional[str] = None,
        autor: Optional[str] = None,
        categoria: Optional[str] = None,
        ano_min: Optional[int] = None,
        ano_max: Optional[int] = None,
    ) -> List[Livro]:
        try:
            statement = select(Livro)

            if titulo:
                statement = statement.where(Livro.titulo.contains(titulo))

            if ano_min:
                statement = statement.where(Livro.ano_publicacao >= ano_min)

            if ano_max:
                statement = statement.where(Livro.ano_publicacao <= ano_max)

            livros = session.exec(statement).all()

            # Filtrar por autor se especificado
            if autor:
                livros_filtrados = []
                for livro in livros:
                    for livro_autor in livro.autores:
                        if (
                            autor.lower() in livro_autor.nome.lower()
                            or autor.lower() in livro_autor.sobrenome.lower()
                        ):
                            livros_filtrados.append(livro)
                            break
                livros = livros_filtrados

            # Filtrar por categoria se especificado
            if categoria:
                livros_filtrados = []
                for livro in livros:
                    for livro_categoria in livro.categorias:
                        if categoria.lower() in livro_categoria.nome.lower():
                            livros_filtrados.append(livro)
                            break
                livros = livros_filtrados

            logger.info(f'Busca de livros: {len(livros)} encontrados')
            return livros
        except Exception as e:
            logger.error(f'Erro na busca de livros: {str(e)}')
            raise
