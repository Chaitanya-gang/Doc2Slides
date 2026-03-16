"""
newd2p - Custom Exception Classes
"""


class Newd2pError(Exception):
    pass


class ParsingError(Newd2pError):
    pass


class ChunkingError(Newd2pError):
    pass


class EmbeddingError(Newd2pError):
    pass


class VectorStoreError(Newd2pError):
    pass


class LLMError(Newd2pError):
    pass


class LLMConnectionError(LLMError):
    pass


class NarrativeGenerationError(Newd2pError):
    pass


class PPTGenerationError(Newd2pError):
    pass


class ChartGenerationError(Newd2pError):
    pass


class FileValidationError(Newd2pError):
    pass


class JobNotFoundError(Newd2pError):
    pass