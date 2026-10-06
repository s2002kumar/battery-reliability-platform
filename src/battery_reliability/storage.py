"""Generic URI and filesystem interfaces without provider-specific behavior."""

from contextlib import AbstractContextManager
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO, Literal, Protocol
from urllib.parse import urlsplit

BinaryMode = Literal["rb", "wb"]


@dataclass(frozen=True, slots=True)
class StorageURI:
    """An absolute URI naming a storage location, with no domain semantics."""

    value: str

    def __post_init__(self) -> None:
        """Reject empty values and relative URI strings."""
        if not self.value.strip():
            raise ValueError("storage URI must not be empty")
        if not urlsplit(self.value).scheme:
            raise ValueError("storage URI must include a scheme; use from_path for local paths")

    @classmethod
    def from_path(cls, path: Path) -> "StorageURI":
        """Create a file URI for a local path."""
        return cls(path.expanduser().resolve().as_uri())

    @property
    def scheme(self) -> str:
        """Return the normalized URI scheme."""
        return urlsplit(self.value).scheme.lower()


class FileSystem(Protocol):
    """Provider-neutral interface for opening binary storage objects."""

    def open_binary(
        self, location: StorageURI, mode: BinaryMode = "rb"
    ) -> AbstractContextManager[BinaryIO]:
        """Open a binary object; provider support is defined by an implementation."""
