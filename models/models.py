from datetime import date, datetime
from enum import Enum
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


# Tabela de associação para relacionamento N:N entre Livro e Autor
class LivroAutorLink(SQLModel, table=True):
    __tablename__ = 'livro_autor'

    livro_id: Optional[int] = Field(
        default=None, foreign_key='livro.id', primary_key=True
    )
    autor_id: Optional[int] = Field(
        default=None, foreign_key='autor.id', primary_key=True
    )


# Tabela de associação para relacionamento N:N entre Livro e Categoria
class LivroCategoriaLink(SQLModel, table=True):
    __tablename__ = 'livro_categoria'

    livro_id: Optional[int] = Field(
        default=None, foreign_key='livro.id', primary_key=True
    )
    categoria_id: Optional[int] = Field(
        default=None, foreign_key='categoria.id', primary_key=True
    )


class StatusEmprestimo(str, Enum):
    ATIVO = 'ativo'
    DEVOLVIDO = 'devolvido'
    ATRASADO = 'atrasado'


# Entidade 1: Autor
class Autor(SQLModel, table=True):
    __tablename__ = 'autor'

    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(max_length=100)
    sobrenome: str = Field(max_length=100)
    data_nascimento: date
    nacionalidade: str = Field(max_length=50)
    biografia: Optional[str] = Field(default=None)
    data_criacao: datetime = Field(default_factory=datetime.now)
    cpf: Optional[str] = Field(default=None, index=True)

    # Relacionamentos
    livros: List['Livro'] = Relationship(
        back_populates='autores', link_model=LivroAutorLink
    )


# Entidade 2: Categoria
class Categoria(SQLModel, table=True):
    __tablename__ = 'categoria'

    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(max_length=50, unique=True)
    descricao: Optional[str] = Field(default=None)
    ativa: bool = Field(default=True)
    data_criacao: datetime = Field(default_factory=datetime.now)

    # Relacionamentos
    livros: List['Livro'] = Relationship(
        back_populates='categorias', link_model=LivroCategoriaLink
    )


# Entidade 3: Usuario
class Usuario(SQLModel, table=True):
    __tablename__ = 'usuario'

    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(max_length=100)
    email: str = Field(unique=True)
    telefone: Optional[str] = Field(default=None, max_length=20)
    endereco: Optional[str] = Field(default=None)
    data_cadastro: datetime = Field(default_factory=datetime.now)
    ativo: bool = Field(default=True)

    # Relacionamentos 1:N
    emprestimos: List['Emprestimo'] = Relationship(back_populates='usuario')
    # Relacionamento 1:1
    perfil: Optional['PerfilUsuario'] = Relationship(back_populates='usuario')


# Entidade 4: Livro
class Livro(SQLModel, table=True):
    __tablename__ = 'livro'

    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str = Field(max_length=200)
    isbn: str = Field(unique=True, max_length=20)
    ano_publicacao: int
    editora: str = Field(max_length=100)
    numero_paginas: int
    quantidade_total: int = Field(default=1)
    quantidade_disponivel: int = Field(default=1)
    data_adicao: datetime = Field(default_factory=datetime.now)

    # Relacionamentos N:N
    autores: List[Autor] = Relationship(
        back_populates='livros', link_model=LivroAutorLink
    )
    categorias: List[Categoria] = Relationship(
        back_populates='livros', link_model=LivroCategoriaLink
    )

    # Relacionamento 1:N
    emprestimos: List['Emprestimo'] = Relationship(back_populates='livro')


# Entidade 5: Emprestimo
class Emprestimo(SQLModel, table=True):
    __tablename__ = 'emprestimo'

    id: Optional[int] = Field(default=None, primary_key=True)
    data_emprestimo: datetime = Field(default_factory=datetime.now)
    data_devolucao_prevista: date
    data_devolucao_real: Optional[date] = Field(default=None)
    status: StatusEmprestimo = Field(default=StatusEmprestimo.ATIVO)
    observacoes: Optional[str] = Field(default=None)

    # Foreign Keys
    usuario_id: int = Field(foreign_key='usuario.id')
    livro_id: int = Field(foreign_key='livro.id')

    # Relacionamentos N:1
    usuario: Usuario = Relationship(back_populates='emprestimos')
    livro: Livro = Relationship(back_populates='emprestimos')


# Entidade adicional para relacionamento 1:1
class PerfilUsuario(SQLModel, table=True):
    __tablename__ = 'perfil_usuario'

    id: Optional[int] = Field(default=None, primary_key=True)
    foto_url: Optional[str] = Field(default=None)
    profissao: Optional[str] = Field(default=None, max_length=100)
    interesses_literarios: Optional[str] = Field(default=None)
    livros_favoritos: Optional[str] = Field(default=None)
    data_criacao: datetime = Field(default_factory=datetime.now)

    # Foreign Key - relacionamento 1:1
    usuario_id: int = Field(foreign_key='usuario.id', unique=True)

    # Relacionamento 1:1
    usuario: Usuario = Relationship(back_populates='perfil')
