from config.database import create_db_and_tables
from config.logging_config import logger
from fastapi import FastAPI
from routes import (
    autor_routes,
    categoria_routes,
    emprestimo_routes,
    livro_routes,
    perfil_usuario_routes,
    usuario_routes,
)

# Criar aplicação FastAPI
app = FastAPI(
    title='Sistema de Biblioteca Digital',
    description='API para gerenciamento de biblioteca com SQLModel e FastAPI',
    version='1.0.0',
)

# Incluir todas as rotas
app.include_router(autor_routes.router)
app.include_router(livro_routes.router)
app.include_router(categoria_routes.router)
app.include_router(usuario_routes.router)
app.include_router(emprestimo_routes.router)
app.include_router(perfil_usuario_routes.router)


@app.on_event('startup')
def on_startup():
    """Criar tabelas do banco de dados na inicialização"""
    create_db_and_tables()
    logger.info('Aplicação iniciada e tabelas criadas')


@app.get('/')
def read_root():
    """Endpoint raiz"""
    return {'message': 'Sistema de Biblioteca Digital'}
