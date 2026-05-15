#!/usr/bin/env python3
"""
CLI AI — Terminal AI Assistant powered by Ollama (100% lokal, gratis)
"""
 
import os
import sys
import json
import datetime
import readline
import textwrap
import urllib.request
import urllib.error
from pathlib import Path
 
# ─── Cek & import ollama ──────────────────────────────────────────────────────
try:
    import ollama
except ImportError:
    print("❌ Library 'ollama' tidak ditemukan.")
    print("   Jalankan: pip install ollama")
    sys.exit(1)
 
# ─── Konfigurasi ──────────────────────────────────────────────────────────────
 
CONFIG_DIR  = Path.home() / ".cli_ai_ollama"
HISTORY_FILE = CONFIG_DIR / "history.json"
CONFIG_FILE  = CONFIG_DIR / "config.json"
 
# Model yang direkomendasikan sesuai RAM
RECOMMENDED_MODELS = [
    ("llama3.1:8b",     "LLaMA 3.1 8B  — Sangat pintar & serbaguna        (~5GB RAM)"),
    ("mistral:7b",      "Mistral 7B     — Cepat, analitis, bagus untuk kode (~4GB RAM)"),
    ("mistral:latest",  "Mistral Latest — Versi terbaru Mistral              (~4GB RAM)"),
    ("gemma2:9b",       "Gemma2 9B      — Buatan Google, akurat & efisien   (~6GB RAM)"),
    ("qwen2.5:7b",      "Qwen2.5 7B     — Kuat di coding & matematika       (~5GB RAM)"),
    ("deepseek-r1:8b",  "DeepSeek-R1 8B — Reasoning mendalam seperti o1    (~5GB RAM)"),
]
 
DEFAULT_CONFIG = {
    "model": "llama3.1:8b",
    "system_prompt": (
        "Kamu adalah asisten AI yang sangat cerdas, analitis, dan membantu. "
        "Kamu mampu berpikir mendalam, menganalisis masalah kompleks, menulis kode, "
        "menjelaskan konsep ilmiah, membantu riset, dan berdiskusi tentang berbagai topik. "
        "Jawab dalam bahasa yang sama dengan pengguna (Indonesia atau Inggris). "
        "Berikan jawaban yang akurat, terstruktur, dan mendalam."
    ),
    "max_history": 50,
    "show_stats": False,
    "stream": True,
}
 
# ─── Warna ANSI ───────────────────────────────────────────────────────────────
 
class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    CYAN    = "\033[96m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    RED     = "\033[91m"
    BLUE    = "\033[94m"
    GRAY    = "\033[90m"
    MAGENTA = "\033[95m"
 
# ─── Utilitas ─────────────────────────────────────────────────────────────────
 
def ensure_dir():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
 
def load_config() -> dict:
    ensure_dir()
    if CONFIG_FILE.exists():
        try:
            cfg = DEFAULT_CONFIG.copy()
            cfg.update(json.loads(CONFIG_FILE.read_text()))
            return cfg
        except Exception:
            pass
    return DEFAULT_CONFIG.copy()
 
def save_config(cfg: dict):
    ensure_dir()
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2, ensure_ascii=False))
 
def load_history() -> list:
    if HISTORY_FILE.exists():
        try:
            return json.loads(HISTORY_FILE.read_text())
        except Exception:
            pass
    return []
 
def save_history(history: list, max_h: int):
    ensure_dir()
    trimmed = history[-(max_h * 2):]
    HISTORY_FILE.write_text(json.dumps(trimmed, indent=2, ensure_ascii=False))
 
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")
 
def get_ts() -> str:
    return datetime.datetime.now().strftime("%H:%M:%S")
 
# ─── Cek Ollama berjalan ──────────────────────────────────────────────────────
 
def check_ollama_running() -> bool:
    try:
        req = urllib.request.urlopen("http://localhost:11434", timeout=2)
        return True
    except Exception:
        return False
 
def list_local_models() -> list:
    try:
        result = ollama.list()
        return [m.model for m in result.models]
    except Exception:
        return []
 
# ─── Tampilan ─────────────────────────────────────────────────────────────────
 
def print_banner(model: str):
    print(f"""
{C.CYAN}{C.BOLD}  ██████╗██╗     ██╗      █████╗ ██╗
 ██╔════╝██║     ██║     ██╔══██╗██║
 ██║     ██║     ██║     ███████║██║
 ██║     ██║     ██║     ██╔══██║██║
 ╚██████╗███████╗███████╗██║  ██║██║
  ╚═════╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝{C.RESET}
{C.GRAY}  Terminal AI — Ollama (100% Lokal & Gratis){C.RESET}
  {C.GRAY}Model aktif: {C.RESET}{C.CYAN}{C.BOLD}{model}{C.RESET}
  {C.GRAY}Ketik {C.GREEN}/help{C.GRAY} untuk bantuan{C.RESET}
{C.GRAY}{"─" * 55}{C.RESET}""")
 
def print_help():
    cmds = [
        ("/help",    "Tampilkan bantuan ini"),
        ("/clear",   "Bersihkan layar"),
        ("/reset",   "Hapus riwayat percakapan sesi ini"),
        ("/history", "Tampilkan ringkasan riwayat"),
        ("/save",    "Simpan percakapan ke file .txt"),
        ("/model",   "Ganti model AI"),
        ("/models",  "Lihat model yang sudah terdownload"),
        ("/pull",    "Download model baru dari Ollama"),
        ("/system",  "Ubah system prompt"),
        ("/stats",   "Toggle tampilan statistik respons"),
        ("/config",  "Tampilkan konfigurasi aktif"),
        ("/exit",    "Keluar"),
    ]
    print(f"\n{C.CYAN}{C.BOLD}━━━ Perintah ━━━{C.RESET}")
    for cmd, desc in cmds:
        print(f"  {C.GREEN}{cmd:<12}{C.RESET} {desc}")
    print(f"\n{C.GRAY}  Tip: ↑/↓ untuk navigasi riwayat input{C.RESET}\n")
 
def print_user(text: str):
    print(f"\n{C.GRAY}[{get_ts()}]{C.RESET} {C.BLUE}{C.BOLD}Anda{C.RESET}")
    print(f"{C.BLUE}▌{C.RESET} {text}\n")
 
def print_ai_header():
    print(f"{C.GRAY}[{get_ts()}]{C.RESET} {C.CYAN}{C.BOLD}AI{C.RESET}")
    print(f"{C.CYAN}▌{C.RESET} ", end="", flush=True)
 
# ─── Streaming ────────────────────────────────────────────────────────────────
 
def stream_response(messages: list, config: dict) -> tuple[str, dict]:
    full_text = ""
    stats = {}
    in_newline = False
 
    # Bangun messages dengan system prompt
    full_messages = [{"role": "system", "content": config["system_prompt"]}] + messages
 
    print_ai_header()
 
    try:
        start = datetime.datetime.now()
        stream = ollama.chat(
            model=config["model"],
            messages=full_messages,
            stream=True,
        )
 
        for chunk in stream:
            text = chunk.get("message", {}).get("content", "")
            if not text:
                continue
 
            # Indent tiap baris baru
            if in_newline:
                print(f"{C.CYAN}▌{C.RESET} ", end="", flush=True)
                in_newline = False
 
            parts = text.split("\n")
            for i, part in enumerate(parts):
                print(part, end="", flush=True)
                if i < len(parts) - 1:
                    print()
                    in_newline = True
 
            full_text += text
 
            # Ambil stats dari chunk terakhir
            if chunk.get("done"):
                elapsed = (datetime.datetime.now() - start).total_seconds()
                stats = {
                    "elapsed": elapsed,
                    "eval_count": chunk.get("eval_count", 0),
                    "tokens_per_sec": round(chunk.get("eval_count", 0) / max(elapsed, 0.1), 1),
                }
 
    except ollama.ResponseError as e:
        print(f"\n{C.RED}❌ Model error: {e.error}{C.RESET}")
        if "not found" in str(e.error).lower():
            print(f"{C.YELLOW}   Jalankan: /pull untuk download model{C.RESET}")
    except Exception as e:
        if "Connection refused" in str(e) or "connect" in str(e).lower():
            print(f"\n{C.RED}❌ Ollama tidak berjalan!{C.RESET}")
            print(f"{C.YELLOW}   Jalankan: ollama serve{C.RESET}")
        else:
            print(f"\n{C.RED}❌ Error: {e}{C.RESET}")
    except KeyboardInterrupt:
        print(f"\n{C.YELLOW}  [dihentikan]{C.RESET}")
 
    print("\n")
    return full_text, stats
 
# ─── Perintah Khusus ──────────────────────────────────────────────────────────
 
def cmd_models():
    models = list_local_models()
    if not models:
        print(f"  {C.YELLOW}Belum ada model yang terdownload.{C.RESET}")
        print(f"  {C.GRAY}Gunakan /pull untuk download model.{C.RESET}\n")
        return
    print(f"\n{C.CYAN}{C.BOLD}━━━ Model Terdownload ━━━{C.RESET}")
    for m in models:
        print(f"  {C.GREEN}•{C.RESET} {m}")
    print()
 
def cmd_pull():
    print(f"\n{C.CYAN}{C.BOLD}━━━ Download Model ━━━{C.RESET}")
    for i, (m, desc) in enumerate(RECOMMENDED_MODELS, 1):
        print(f"  {C.YELLOW}{i}.{C.RESET} {desc}")
    print(f"  {C.YELLOW}{len(RECOMMENDED_MODELS)+1}.{C.RESET} Masukkan nama model manual")
    print()
    try:
        choice = input(f"  {C.GRAY}Pilih (Enter=batal): {C.RESET}").strip()
        if not choice:
            return
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(RECOMMENDED_MODELS):
                model_name = RECOMMENDED_MODELS[idx][0]
            else:
                model_name = input(f"  {C.GRAY}Nama model: {C.RESET}").strip()
        else:
            model_name = choice
 
        if model_name:
            print(f"\n  {C.CYAN}⬇ Mendownload {model_name}...{C.RESET}")
            print(f"  {C.GRAY}(Ini mungkin memakan waktu beberapa menit){C.RESET}\n")
            # Pull dengan progress
            current_digest = ""
            for progress in ollama.pull(model_name, stream=True):
                status = progress.get("status", "")
                digest = progress.get("digest", "")
                total  = progress.get("total", 0)
                completed = progress.get("completed", 0)
                if digest and digest != current_digest:
                    current_digest = digest
                if total and completed:
                    pct = int((completed / total) * 100)
                    bar = "█" * (pct // 5) + "░" * (20 - pct // 5)
                    print(f"\r  [{bar}] {pct}% {status[:30]:<30}", end="", flush=True)
                else:
                    print(f"\r  {status:<50}", end="", flush=True)
            print(f"\n\n  {C.GREEN}✓ {model_name} berhasil didownload!{C.RESET}\n")
    except KeyboardInterrupt:
        print(f"\n  {C.YELLOW}Download dibatalkan.{C.RESET}\n")
    except Exception as e:
        print(f"\n  {C.RED}❌ Gagal download: {e}{C.RESET}\n")
 
def cmd_model(config: dict) -> dict:
    local = list_local_models()
    print(f"\n{C.CYAN}{C.BOLD}━━━ Ganti Model ━━━{C.RESET}")
    if local:
        print(f"  {C.GRAY}Model tersedia di komputer Anda:{C.RESET}")
        for i, m in enumerate(local, 1):
            active = f" {C.GREEN}← aktif{C.RESET}" if m == config["model"] else ""
            print(f"  {C.YELLOW}{i}.{C.RESET} {m}{active}")
        print()
        try:
            choice = input(f"  {C.GRAY}Pilih nomor (Enter=batal): {C.RESET}").strip()
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(local):
                    config["model"] = local[idx]
                    save_config(config)
                    print(f"  {C.GREEN}✓ Model diubah ke: {local[idx]}{C.RESET}\n")
        except KeyboardInterrupt:
            pass
    else:
        print(f"  {C.YELLOW}Belum ada model. Gunakan /pull untuk download.{C.RESET}\n")
    return config
 
def cmd_history(messages: list):
    if not messages:
        print(f"  {C.GRAY}Belum ada riwayat percakapan.{C.RESET}\n")
        return
    print(f"\n{C.CYAN}{C.BOLD}━━━ Riwayat ({len(messages)//2} pesan) ━━━{C.RESET}")
    for i, msg in enumerate(messages):
        label = f"{C.BLUE}Anda{C.RESET}" if msg["role"] == "user" else f"{C.CYAN}AI{C.RESET}"
        preview = msg["content"][:100] + "..." if len(msg["content"]) > 100 else msg["content"]
        print(f"  {C.GRAY}{i+1:>2}.{C.RESET} {label}: {preview}")
    print()
 
def cmd_save(messages: list):
    if not messages:
        print(f"  {C.GRAY}Tidak ada percakapan untuk disimpan.{C.RESET}\n")
        return
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"percakapan_{ts}.txt"
    with open(fname, "w", encoding="utf-8") as f:
        f.write(f"CLI AI (Ollama) — {datetime.datetime.now()}\n{'='*60}\n\n")
        for msg in messages:
            role = "ANDA" if msg["role"] == "user" else "AI"
            f.write(f"[{role}]\n{msg['content']}\n\n{'─'*40}\n\n")
    print(f"  {C.GREEN}✓ Disimpan ke: {fname}{C.RESET}\n")
 
def cmd_system(config: dict) -> dict:
    print(f"\n{C.CYAN}{C.BOLD}━━━ System Prompt ━━━{C.RESET}")
    print(f"  {C.GRAY}{config['system_prompt']}{C.RESET}\n")
    try:
        new = input(f"  {C.YELLOW}Masukkan prompt baru (Enter=batal):{C.RESET}\n  > ").strip()
        if new:
            config["system_prompt"] = new
            save_config(config)
            print(f"  {C.GREEN}✓ System prompt diperbarui.{C.RESET}")
    except KeyboardInterrupt:
        pass
    print()
    return config
 
def cmd_config(config: dict):
    print(f"\n{C.CYAN}{C.BOLD}━━━ Konfigurasi Aktif ━━━{C.RESET}")
    for k, v in config.items():
        val = (v[:70] + "...") if isinstance(v, str) and len(v) > 70 else v
        print(f"  {C.GREEN}{k:<15}{C.RESET} {val}")
    print()
 
# ─── Main ─────────────────────────────────────────────────────────────────────
 
def main():
    # Setup readline
    try:
        readline.parse_and_bind("tab: complete")
        readline.set_history_length(500)
    except Exception:
        pass
 
    config = load_config()
 
    # Cek Ollama berjalan
    if not check_ollama_running():
        print(f"\n{C.RED}❌ Ollama tidak berjalan!{C.RESET}")
        print(f"\n{C.YELLOW}   Jalankan perintah ini di terminal lain:{C.RESET}")
        print(f"   {C.CYAN}ollama serve{C.RESET}\n")
        print(f"   Jika Ollama belum terinstall:")
        print(f"   {C.CYAN}curl -fsSL https://ollama.com/install.sh | sh{C.RESET}\n")
        sys.exit(1)
 
    # Cek model tersedia
    local_models = list_local_models()
    if not local_models:
        print(f"\n{C.YELLOW}⚠  Belum ada model yang terdownload.{C.RESET}")
        print(f"\n   Rekomendasi untuk RAM 20GB Anda:")
        print(f"   {C.CYAN}ollama pull llama3.1:8b{C.RESET}   ← paling pintar")
        print(f"   {C.CYAN}ollama pull mistral:7b{C.RESET}    ← cepat & analitis")
        print(f"\n   Atau jalankan program ini dulu, lalu ketik {C.GREEN}/pull{C.RESET}\n")
 
    elif config["model"] not in local_models:
        print(f"\n{C.YELLOW}⚠  Model '{config['model']}' belum ada di komputer.{C.RESET}")
        print(f"   Model tersedia: {', '.join(local_models)}")
        config["model"] = local_models[0]
        save_config(config)
        print(f"   {C.GREEN}✓ Otomatis menggunakan: {config['model']}{C.RESET}\n")
 
    # Load history
    messages = load_history()
 
    # Tampilan awal
    clear_screen()
    print_banner(config["model"])
    if messages:
        print(f"  {C.GRAY}↻ Melanjutkan {len(messages)//2} pesan sebelumnya. Ketik /reset untuk mulai baru.{C.RESET}\n")
 
    # ── Loop Percakapan ──
    while True:
        try:
            prompt = input(f"{C.YELLOW}▶ Anda: {C.RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n\n{C.GRAY}Sampai jumpa!{C.RESET}\n")
            save_history(messages, config["max_history"])
            break
 
        if not prompt:
            continue
 
        lower = prompt.lower()
 
        if lower in ("/exit", "/quit", "/q"):
            print(f"\n{C.GRAY}Sampai jumpa!{C.RESET}\n")
            save_history(messages, config["max_history"])
            break
        elif lower == "/help":
            print_help()
        elif lower == "/clear":
            clear_screen()
            print_banner(config["model"])
        elif lower == "/reset":
            messages = []
            save_history(messages, config["max_history"])
            print(f"  {C.GREEN}✓ Riwayat dihapus.{C.RESET}\n")
        elif lower == "/history":
            cmd_history(messages)
        elif lower == "/save":
            cmd_save(messages)
        elif lower == "/model":
            config = cmd_model(config)
        elif lower == "/models":
            cmd_models()
        elif lower == "/pull":
            cmd_pull()
        elif lower == "/system":
            config = cmd_system(config)
        elif lower == "/stats":
            config["show_stats"] = not config["show_stats"]
            print(f"  {C.GREEN}✓ Statistik: {'aktif' if config['show_stats'] else 'nonaktif'}{C.RESET}\n")
        elif lower == "/config":
            cmd_config(config)
        elif lower.startswith("/"):
            print(f"  {C.YELLOW}⚠ Perintah tidak dikenal. Ketik /help.{C.RESET}\n")
        else:
            # Kirim ke AI
            messages.append({"role": "user", "content": prompt})
            print_user(prompt)
 
            ai_text, stats = stream_response(messages, config)
 
            if ai_text:
                messages.append({"role": "assistant", "content": ai_text})
                if config.get("show_stats") and stats:
                    print(f"{C.GRAY}  ↳ {stats.get('eval_count',0)} token | {stats.get('tokens_per_sec',0)} tok/s | {stats.get('elapsed',0):.1f}s{C.RESET}\n")
 
            save_history(messages, config["max_history"])
 
if __name__ == "__main__":
    main()