from datetime import date, datetime
from typing import Generic, List, Optional, TypeVar

from models.models import StatusEmprestimo
from pydantic import BaseModel, EmailStr
from pydantic.generics import GenericModel


# Schemas para Autor
class AutorCreate(BaseModel):
    nome: str
    sobrenome: str
    data_nascimento: date
    nacionalidade: str
    biografia: Optional[str] = None


class AutorUpdate(BaseModel):
    nome: Optional[str] = None
    sobrenome: Optional[str] = None
    data_nascimento: Optional[date] = None
    nacionalidade: Optional[str] = None
    biografia: Optional[str] = None


class AutorResponse(BaseModel):
    id: int
    nome: str
    sobrenome: str
    data_nascimento: date
    nacionalidade: str
    biografia: Optional[str]
    data_criacao: datetime

    class Config:
        from_attributes = True  # Para Pydantic v2


# Schemas para Categoria
class CategoriaCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None


class CategoriaUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    ativa: Optional[bool] = None


class CategoriaResponse(BaseModel):
    id: int
    nome: str
    descricao: Optional[str]
    ativa: bool
    data_criacao: datetime

    class Config:
        from_attributes = True


# Schemas para Usuario
class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    telefone: Optional[str] = None
    endereco: Optional[str] = None


class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    ativo: Optional[bool] = None


class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str
    telefone: Optional[str]
    endereco: Optional[str]
    data_cadastro: datetime
    ativo: bool

    class Config:
        from_attributes = True


# Schemas para Livro
class LivroCreate(BaseModel):
    titulo: str
    isbn: str
    ano_publicacao: int
    editora: str
    numero_paginas: int
    quantidade_total: int = 1
    autor_ids: List[int] = []
    categoria_ids: List[int] = []


class LivroUpdate(BaseModel):
    titulo: Optional[str] = None
    isbn: Optional[str] = None
    ano_publicacao: Optional[int] = None
    editora: Optional[str] = None
    numero_paginas: Optional[int] = None
    quantidade_total: Optional[int] = None
    autor_ids: Optional[List[int]] = None
    categoria_ids: Optional[List[int]] = None


class LivroResponse(BaseModel):
    id: int
    titulo: str
    isbn: str
    ano_publicacao: int
    editora: str
    numero_paginas: int
    quantidade_total: int
    quantidade_disponivel: int
    data_adicao: datetime
    autores: List[AutorResponse] = []
    categorias: List[CategoriaResponse] = []

    class Config:
        from_attributes = True  # Para permitir criar a partir de ORM


# Schemas para Emprestimo
class EmprestimoCreate(BaseModel):
    usuario_id: int
    livro_id: int
    data_devolucao_prevista: date
    observacoes: Optional[str] = None


class EmprestimoUpdate(BaseModel):
    data_devolucao_prevista: Optional[date] = None
    data_devolucao_real: Optional[date] = None
    status: Optional[StatusEmprestimo] = None
    observacoes: Optional[str] = None


class EmprestimoResponse(BaseModel):
    id: int
    data_emprestimo: datetime
    data_devolucao_prevista: date
    data_devolucao_real: Optional[date]
    status: StatusEmprestimo
    observacoes: Optional[str]
    usuario: UsuarioResponse
    livro: LivroResponse

    class Config:
        from_attributes = True


# Schemas para PerfilUsuario
class PerfilUsuarioCreate(BaseModel):
    usuario_id: int
    foto_url: Optional[str] = None
    profissao: Optional[str] = None
    interesses_literarios: Optional[str] = None
    livros_favoritos: Optional[str] = None


class PerfilUsuarioUpdate(BaseModel):
    foto_url: Optional[str] = None
    profissao: Optional[str] = None
    interesses_literarios: Optional[str] = None
    livros_favoritos: Optional[str] = None


class PerfilUsuarioResponse(BaseModel):
    id: int
    foto_url: Optional[str]
    profissao: Optional[str]
    interesses_literarios: Optional[str]
    livros_favoritos: Optional[str]
    data_criacao: datetime
    usuario: UsuarioResponse

    class Config:
        from_attributes = True


# Schema para paginação
T = TypeVar('T')


class PaginatedResponse(GenericModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    limit: int
    total_pages: int


# Schema para contagem
class CountResponse(BaseModel):
    total: int
    entidade: str
