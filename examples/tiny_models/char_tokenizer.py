from __future__ import annotations


class CharTokenizer:
    """A tiny character tokenizer for readable local runs."""

    pad_token = "<pad>"
    bos_token = "<bos>"
    eos_token = "<eos>"
    unk_token = "<unk>"

    def __init__(self, texts: list[str] | None = None):
        special = [self.pad_token, self.bos_token, self.eos_token, self.unk_token]
        chars = sorted(set("".join(texts or [])))
        self.itos = special + [ch for ch in chars if ch not in special]
        self.stoi = {token: idx for idx, token in enumerate(self.itos)}

    @property
    def pad_id(self) -> int:
        return self.stoi[self.pad_token]

    @property
    def bos_id(self) -> int:
        return self.stoi[self.bos_token]

    @property
    def eos_id(self) -> int:
        return self.stoi[self.eos_token]

    @property
    def unk_id(self) -> int:
        return self.stoi[self.unk_token]

    @property
    def vocab_size(self) -> int:
        return len(self.itos)

    def encode(self, text: str, add_bos: bool = False, add_eos: bool = False) -> list[int]:
        ids = [self.stoi.get(ch, self.unk_id) for ch in text]
        if add_bos:
            ids.insert(0, self.bos_id)
        if add_eos:
            ids.append(self.eos_id)
        return ids

    def decode(self, ids: list[int]) -> str:
        chars: list[str] = []
        for idx in ids:
            if idx in (self.pad_id, self.bos_id):
                continue
            if idx == self.eos_id:
                break
            chars.append(self.itos[idx] if 0 <= idx < len(self.itos) else "?")
        return "".join(chars)
