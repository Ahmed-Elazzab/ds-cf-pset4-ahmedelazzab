"""Base class for all the orchestrators.

The parameters (attributes) are initialized by the child model class.
"""
import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class OrchestratorABC(ABC):
    """Abstract class for all Predictor types."""

    def __init__(self):
        """Initialize the orchestrator."""

    @abstractmethod
    def run(self):
        """
        """
        raise NotImplementedError()

    @abstractmethod
    def train(self):
        """
        """
        raise NotImplementedError()

    @abstractmethod
    def load_predict(self):
        """
        """
        raise NotImplementedError()