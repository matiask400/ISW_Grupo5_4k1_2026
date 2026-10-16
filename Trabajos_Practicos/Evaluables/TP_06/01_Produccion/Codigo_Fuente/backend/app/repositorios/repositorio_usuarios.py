class RepositorioUsuariosEnMemoria:

    def __init__(self, emails_registrados: set[str]) -> None:
        self._emails = set(emails_registrados)

    def esta_registrado(self, email: str) -> bool:
        return email in self._emails
