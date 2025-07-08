from loguru import logger

def calcul_carre(n: int) -> int:
    logger.info(f"Calcul du carré de {n}")
    return n * n
