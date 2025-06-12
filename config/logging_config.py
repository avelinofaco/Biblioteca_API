import logging
import os
from datetime import datetime

import logging.config

def setup_logging():
    # --- Passo 1: Criar o diretório de logs se não existir ---
    log_directory = 'logs'
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # --- Passo 2: Definir o nome do arquivo de log com data atual ---
    log_filename = f'{log_directory}/biblioteca_{datetime.now().strftime("%Y_%m_%d")}.log'

    # --- Passo 3: Definir a configuração de logging usando um dicionário ---
    LOGGING_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False, # Manter loggers existentes (como os do Uvicorn e SQLAlchemy)

        'formatters': {
            'standard': { # Um formatador padrão para os seus logs
                'format': '%(levelname)s | %(asctime)s | %(name)s | %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
        },
        'handlers': {
            'file_handler': { # Handler para enviar os SEUS logs para o arquivo
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'standard',
                'filename': log_filename,
                'maxBytes': 10485760, # 10 MB por arquivo
                'backupCount': 5, # Mantém 5 arquivos de backup
            },
            'console_handler': { # NOVO: Handler para enviar os SEUS logs para o console
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
                'level': 'INFO', # Nível de log para o console (pode ser diferente do arquivo)
            },
            'null_handler': { # Um handler que simplesmente descarta os logs
                'class': 'logging.NullHandler',
            },
        },
        'loggers': {
            '': {  # O logger raiz (root logger) - Este é o logger padrão para os seus próprios logs
                'handlers': ['file_handler', 'console_handler'], # Direciona logs do logger raiz para o arquivo
                'level': 'INFO', # Nível mínimo de log para o logger raiz (seus logs)
                'propagate': False, # É importante que o logger raiz não propague logs para outros handlers que possam estar no console
            },
            # --- Configurações para loggers do Uvicorn e SQLAlchemy (DESABILITAR) ---
            'uvicorn': { # Logger principal do Uvicorn
                'handlers': ['null_handler'], # Envia logs para o handler que descarta
                'level': 'CRITICAL', # Define um nível tão alto que praticamente nada será logado
                'propagate': False, # Impede qualquer propagação para o logger raiz
            },
            'uvicorn.access': { # Logs de acesso HTTP do Uvicorn
                'handlers': ['null_handler'],
                'level': 'CRITICAL',
                'propagate': False,
            },
            'uvicorn.error': { # Logs de erro do Uvicorn (erros ainda podem ser importantes, mas desabilitamos aqui conforme seu pedido)
                'handlers': ['null_handler'],
                'level': 'CRITICAL',
                'propagate': False,
            },
            'sqlalchemy.engine': { # Logs do motor do SQLAlchemy
                'handlers': ['null_handler'],
                'level': 'CRITICAL',
                'propagate': False,
            },
            'sqlalchemy.pool': { # Logs do pool de conexões do SQLAlchemy
                'handlers': ['null_handler'],
                'level': 'CRITICAL',
                'propagate': False,
            },
            'watchfiles.main': { # O logger responsável pelas mensagens de detecção de mudança de arquivo
                'handlers': ['null_handler'],
                'level': 'CRITICAL',
                'propagate': False,
            },
        },
    }

    # --- Passo 4: Aplicar a configuração ---
    logging.config.dictConfig(LOGGING_CONFIG)

    # --- Passo 5: Retornar o logger para o módulo atual (seu logger) ---
    return logging.getLogger(__name__)

# Chamada para configurar o logging quando o arquivo é importado ou executado
# Isso garante que a configuração seja aplicada logo que o módulo é carregado.
logger = setup_logging()

# Exemplo de como usar o logger (no seu main.py ou em outros arquivos):
# import logging
# my_app_logger = logging.getLogger(__name__)
# my_app_logger.info("Minha aplicação iniciou! Esta mensagem irá para o arquivo.")
# my_app_logger.error("Este é um erro da minha aplicação. Também irá para o arquivo.")

"""
def setup_logging():
    # Criar diretório de logs se não existir
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Configurar formato do log
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    # Configurar arquivo de log com data atual
    log_filename = f'logs/biblioteca_{datetime.now().strftime("%Y_%m_%d")}.log'

    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler(log_filename), 
            logging.StreamHandler()
        ],
    )

    return logging.getLogger(__name__)


logger = setup_logging()
"""
