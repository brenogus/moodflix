from dataclasses import dataclass, field
from typing import Optional, Dict, List

@dataclass
class User:
    """
    Entidade que representa um usuário no domínio MoodFlix.
    
    Esta é uma entidade de domínio (Domain Entity) rica, que encapsula 
    propriedades e comportamentos. Ela não possui dependências externas.
    """
    id: str
    username: str  
    password_hash: str
    moodmap_list: List[Dict[str, str]] = field(default_factory=list) 
    default_moodmap: Optional[Dict[str, str]] = None

    def __post_init__(self):
        """Valida os atributos essenciais após a inicialização."""
        if not self.username or not self.username.strip():
            raise ValueError("O username do usuário não pode estar vazio") 
            
        if not self.password_hash or not self.password_hash.strip():
            raise ValueError("O hash da senha não pode estar vazio") 

    # Comportamentos da Entidade (Regras de Negócio Internas) 
    
    def add_new_moodmap(self, moodmap: Dict[str, str]):
        """
        Adiciona um novo moodmap à lista do usuário.
        A lógica de negócio (ex: limite de mapas) fica aqui. 
        """
        if len(self.moodmap_list) >= 5:
            raise ValueError("O usuário já atingiu o limite de 5 moodmaps") 
        
        self.moodmap_list.append(moodmap)

    def set_default_moodmap(self, moodmap_id: str):
        """Define qual moodmap da lista será o padrão."""
        for mmap in self.moodmap_list:
            if mmap.get("moodmap_id") == moodmap_id:
                self.default_moodmap = mmap
                return
        raise ValueError("Moodmap ID não encontrado na lista do usuário")