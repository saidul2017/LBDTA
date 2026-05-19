"""Wrapper LLM provider-agnostic.

Mendukung lima provider dengan API yang seragam:
- Groq (default, gratis di console.groq.com)
- Google Gemini (gratis di aistudio.google.com)
- OpenAI
- Anthropic Claude
- Ollama (lokal)

Provider dipilih lewat env var LLM_PROVIDER.
"""
from __future__ import annotations

import os
from typing import Iterator, List, Dict


DEFAULT_MODELS = {
    "groq": "llama-3.3-70b-versatile",
    "gemini": "gemini-2.5-flash",
    "openai": "gpt-4o-mini",
    "anthropic": "claude-3-5-haiku-latest",
    "ollama": "llama3.2",
}


def get_provider() -> str:
    return os.getenv("LLM_PROVIDER", "groq").lower().strip()


def get_model() -> str:
    provider = get_provider()
    return os.getenv("LLM_MODEL") or DEFAULT_MODELS.get(provider, "")


def get_temperature() -> float:
    return float(os.getenv("LLM_TEMPERATURE", "0.4"))


def chat_stream(
    system: str,
    messages: List[Dict[str, str]],
) -> Iterator[str]:
    """Stream respons dari provider LLM yang dikonfigurasi.

    Args:
        system: system prompt (lihat persona.build_system_prompt)
        messages: daftar {"role": "user"|"assistant", "content": str}

    Yields:
        potongan teks (delta) saat tiba dari LLM
    """
    provider = get_provider()
    if provider == "groq":
        yield from _chat_groq(system, messages)
    elif provider == "gemini":
        yield from _chat_gemini(system, messages)
    elif provider == "openai":
        yield from _chat_openai(system, messages)
    elif provider == "anthropic":
        yield from _chat_anthropic(system, messages)
    elif provider == "ollama":
        yield from _chat_ollama(system, messages)
    else:
        raise ValueError(
            f"LLM_PROVIDER '{provider}' tidak dikenal. "
            "Pilih: groq, gemini, openai, anthropic, ollama."
        )


def _require_key(env_name: str) -> str:
    key = os.getenv(env_name)
    if not key:
        raise RuntimeError(
            f"Environment variable {env_name} belum di-set. "
            f"Periksa berkas .env atau secrets di platform deploy."
        )
    return key


def _chat_groq(system, messages):
    from groq import Groq

    client = Groq(api_key=_require_key("GROQ_API_KEY"))
    full = [{"role": "system", "content": system}] + messages
    stream = client.chat.completions.create(
        model=get_model(),
        messages=full,
        temperature=get_temperature(),
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta


def _chat_openai(system, messages):
    from openai import OpenAI

    client = OpenAI(api_key=_require_key("OPENAI_API_KEY"))
    full = [{"role": "system", "content": system}] + messages
    stream = client.chat.completions.create(
        model=get_model(),
        messages=full,
        temperature=get_temperature(),
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta


def _chat_gemini(system, messages):
    import google.generativeai as genai

    genai.configure(api_key=_require_key("GEMINI_API_KEY"))
    model = genai.GenerativeModel(
        model_name=get_model(),
        system_instruction=system,
    )

    # Gemini menggunakan format role "user" / "model"
    history = []
    for m in messages[:-1]:
        role = "user" if m["role"] == "user" else "model"
        history.append({"role": role, "parts": [m["content"]]})

    chat = model.start_chat(history=history)
    response = chat.send_message(
        messages[-1]["content"],
        stream=True,
        generation_config={"temperature": get_temperature()},
    )
    for chunk in response:
        if hasattr(chunk, "text") and chunk.text:
            yield chunk.text


def _chat_anthropic(system, messages):
    import anthropic

    client = anthropic.Anthropic(api_key=_require_key("ANTHROPIC_API_KEY"))
    with client.messages.stream(
        model=get_model(),
        max_tokens=4096,
        system=system,
        messages=messages,
        temperature=get_temperature(),
    ) as stream:
        for text in stream.text_stream:
            yield text


def _chat_ollama(system, messages):
    import ollama

    full = [{"role": "system", "content": system}] + messages
    stream = ollama.chat(
        model=get_model(),
        messages=full,
        stream=True,
        options={"temperature": get_temperature()},
    )
    for chunk in stream:
        msg = chunk.get("message", {})
        content = msg.get("content")
        if content:
            yield content
