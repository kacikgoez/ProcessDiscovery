import flask_injector
import injector

from app import PROCESS_MINING_SERVICE
from backend.src.flask.services.process_mining_service import ProcessMiningService


class ProcessMiningProvider(injector.Module):

    def configure(self, binder):
        binder.bind(ProcessMiningService,
                    to=self.create,
                    scope=flask_injector.request)

    def create(self) -> ProcessMiningService:
        return PROCESS_MINING_SERVICE
