from __future__ import annotations

import math

import torch
import torch.nn as nn
import torch.nn.functional as F


def apply_rope(x: torch.Tensor, rope_scale: float = 1.0) -> torch.Tensor:
    """Apply rotary position embeddings to a [B, H, T, D] tensor."""

    bsz, heads, seq_len, dim = x.shape
    if dim % 2 != 0:
        return x
    half = dim // 2
    device = x.device
    positions = torch.arange(seq_len, device=device, dtype=x.dtype) / rope_scale
    freqs = torch.exp(
        -math.log(10000.0) * torch.arange(0, half, device=device, dtype=x.dtype) / half
    )
    angles = positions[:, None] * freqs[None, :]
    cos = torch.cos(angles)[None, None, :, :]
    sin = torch.sin(angles)[None, None, :, :]
    x1, x2 = x[..., :half], x[..., half:]
    return torch.cat([x1 * cos - x2 * sin, x1 * sin + x2 * cos], dim=-1)


class CausalSelfAttention(nn.Module):
    def __init__(self, dim: int, heads: int, dropout: float = 0.0):
        super().__init__()
        assert dim % heads == 0
        self.heads = heads
        self.head_dim = dim // heads
        self.qkv = nn.Linear(dim, 3 * dim)
        self.out = nn.Linear(dim, dim)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x: torch.Tensor, rope_scale: float = 1.0) -> torch.Tensor:
        bsz, seq_len, dim = x.shape
        qkv = self.qkv(x).view(bsz, seq_len, 3, self.heads, self.head_dim)
        q, k, v = qkv.unbind(dim=2)
        q = q.transpose(1, 2)
        k = k.transpose(1, 2)
        v = v.transpose(1, 2)
        q = apply_rope(q, rope_scale=rope_scale)
        k = apply_rope(k, rope_scale=rope_scale)
        y = F.scaled_dot_product_attention(q, k, v, is_causal=True)
        y = y.transpose(1, 2).contiguous().view(bsz, seq_len, dim)
        return self.dropout(self.out(y))


class Block(nn.Module):
    def __init__(self, dim: int, heads: int, dropout: float = 0.0):
        super().__init__()
        self.ln1 = nn.LayerNorm(dim)
        self.attn = CausalSelfAttention(dim, heads, dropout)
        self.ln2 = nn.LayerNorm(dim)
        self.mlp = nn.Sequential(
            nn.Linear(dim, 4 * dim),
            nn.GELU(),
            nn.Linear(4 * dim, dim),
            nn.Dropout(dropout),
        )

    def forward(self, x: torch.Tensor, rope_scale: float = 1.0) -> torch.Tensor:
        x = x + self.attn(self.ln1(x), rope_scale=rope_scale)
        x = x + self.mlp(self.ln2(x))
        return x


class TinyCausalLM(nn.Module):
    """A tiny RoPE-based decoder-only transformer."""

    def __init__(
        self,
        vocab_size: int,
        dim: int = 96,
        heads: int = 4,
        layers: int = 2,
        dropout: float = 0.0,
    ):
        super().__init__()
        self.vocab_size = vocab_size
        self.token_embedding = nn.Embedding(vocab_size, dim)
        self.blocks = nn.ModuleList([Block(dim, heads, dropout) for _ in range(layers)])
        self.ln = nn.LayerNorm(dim)
        self.head = nn.Linear(dim, vocab_size, bias=False)
        self.head.weight = self.token_embedding.weight

    def forward(self, input_ids: torch.Tensor, rope_scale: float = 1.0) -> torch.Tensor:
        x = self.token_embedding(input_ids)
        for block in self.blocks:
            x = block(x, rope_scale=rope_scale)
        return self.head(self.ln(x))

    @torch.no_grad()
    def generate(
        self,
        input_ids: torch.Tensor,
        max_new_tokens: int,
        eos_id: int | None = None,
        temperature: float = 0.8,
        rope_scale: float = 1.0,
    ) -> torch.Tensor:
        self.eval()
        out = input_ids
        for _ in range(max_new_tokens):
            logits = self(out, rope_scale=rope_scale)[:, -1, :]
            if temperature <= 0:
                next_id = torch.argmax(logits, dim=-1, keepdim=True)
            else:
                probs = torch.softmax(logits / temperature, dim=-1)
                next_id = torch.multinomial(probs, num_samples=1)
            out = torch.cat([out, next_id], dim=1)
            if eos_id is not None and torch.all(next_id == eos_id):
                break
        return out

