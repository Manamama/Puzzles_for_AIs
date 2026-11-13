#!/usr/bin/env python
# Template: one-shot GPU transcription of a long audio file on a Colab VM,
# driven through the colab CLI's doors (tested 2026-11-13 with
# OpenMOSS/MOSS-Transcribe-Diarize on a T4: 8.7 s setup, 33 s model download,
# 354 s transcription, transcript reproducible to the byte).
#
# Staged flow (each step observable, no sleeps, no ssh):
#   colab upload -s NAME  audio.mp3  /content/audio.mp3   # data door: 34 MB in 46 s
#   colab exec  -s NAME --timeout 7200 -f mtd_colab_driver.py
#   colab stop  -s NAME
#
# Why not `colab run` with the audio embedded: script args and the script body
# travel through the kernel code channel, which is upload-bound — a 47 MB
# payload never landed in 15 min, while `colab upload` moved 34 MB in 46 s.
# `colab run` remains ideal for compute-only scripts (13.5 s session overhead).
#
# Notes baked in from the test run:
#   - T4 (sm_75): load weights fp16 and force SDPA on the inner LM. bf16 falls
#     back to the fp32 maths kernel and OOMs; eager attention OOMs outright
#     (N_heads x L^2 scores).
#   - Set --timeout well above the default 30 s, or the exec dies mid-run.
#   - Record the installed repo head in the summary: a local clone's pin may
#     not exist on the public remote, so the VM may run upstream HEAD.
import hashlib, json, os, subprocess, sys, time

# ---- knobs -----------------------------------------------------------------
REPO_URL = "https://github.com/OpenMOSS/MOSS-Transcribe-Diarize.git"
HF_REPO = "OpenMOSS-Team/MOSS-Transcribe-Diarize"
AUDIO = "/content/audio.mp3"          # put here by `colab upload`
AUDIO_MD5 = "<md5-of-input-file>"     # guard against a stale upload
MAX_NEW_TOKENS = 8192                 # stock CLI default 2048 truncates long audio
DEVICE = "cuda"                       # "cpu" forces fp32 upstream and needs ~7 GB RAM
DTYPE = "float16" if DEVICE == "cuda" else "float32"
# ----------------------------------------------------------------------------

T0 = time.time()


def step(msg):
    print(f"[step +{time.time()-T0:6.1f}s] {msg}", flush=True)


step("input md5 check")
got = hashlib.md5(open(AUDIO, "rb").read()).hexdigest()
if got != AUDIO_MD5:
    print(f"MD5-MISMATCH got={got} (stale or partial upload?)", flush=True)
    sys.exit(1)
step(f"input ok ({os.path.getsize(AUDIO)} bytes)")

step("git clone + pip install .")
r = subprocess.run(
    f"rm -rf /tmp/mtd_repo && git clone -q {REPO_URL} /tmp/mtd_repo && "
    "pip install -q /tmp/mtd_repo",
    shell=True, capture_output=True, text=True,
)
if r.returncode != 0:
    print("SETUP-FAILED " + r.stderr[-2000:], flush=True)
    sys.exit(1)
head = subprocess.run(
    ["git", "-C", "/tmp/mtd_repo", "log", "-1", "--format=%H %ad %s"],
    capture_output=True, text=True,
).stdout.strip()
step(f"installed repo head: {head}")

step("hf model download")
from huggingface_hub import snapshot_download

MODEL = snapshot_download(HF_REPO)
step("model at " + MODEL)

import torch
from transformers import AutoModelForCausalLM, AutoProcessor
from moss_transcribe_diarize.inference_utils import (
    DEFAULT_PROMPT, build_transcription_messages, generate_transcription,
)
from moss_transcribe_diarize.subtitle import (
    subtitle_segments_from_transcript,
)

t_load0 = time.time()
model = AutoModelForCausalLM.from_pretrained(MODEL, trust_remote_code=True, dtype="auto")
processor = AutoProcessor.from_pretrained(MODEL, trust_remote_code=True, fix_mistral_regex=True)
# dispatch is read at forward time (ALL_ATTENTION_FUNCTIONS.get_interface), so
# setting the attribute on the loaded model is the lever -- no package edit.
model.config.text_config._attn_implementation = "sdpa"
model.config._attn_implementation = "sdpa"
model = model.to(DEVICE, dtype=getattr(torch, DTYPE)).eval()
step(f"model loaded {DTYPE}+sdpa in {time.time()-t_load0:.1f}s")
if DEVICE == "cuda":
    torch.cuda.reset_peak_memory_stats()

_t_gen0 = time.time()
_last = {"n": 0}


def _on_tokens(n):
    if n - _last["n"] >= 500:
        _last["n"] = n
        step(f"{n} tokens")


result = generate_transcription(
    model, processor, build_transcription_messages(AUDIO, DEFAULT_PROMPT),
    max_length=131072, max_new_tokens=MAX_NEW_TOKENS, do_sample=False,
    device=torch.device(DEVICE), dtype=getattr(torch, DTYPE),
    token_callback=_on_tokens,
)
t_gen = time.time() - _t_gen0
peak = torch.cuda.max_memory_allocated() / 1e9 if DEVICE == "cuda" else 0.0
step(f"generated {result['generated_tokens']} tokens in {t_gen:.0f}s "
     f"({result['generated_tokens']/max(t_gen,1e-9):.2f} tok/s), peak GPU {peak:.2f} GB")

segments = subtitle_segments_from_transcript(result["text"], postprocess=False)
print("SUMMARY " + json.dumps({
    "repo_head": head,
    "hf_repo": HF_REPO,
    "audio": os.path.basename(AUDIO),
    "segments": len(segments),
    "transcribe_sec": round(t_gen, 1),
    "prompt_len": result["prompt_len"],
    "generated_tokens": result["generated_tokens"],
    "peak_gpu_alloc_gb": round(peak, 2),
    "attn": "sdpa", "dtype": DTYPE, "decoding": "greedy",
    "total_in_vm_sec": round(time.time() - T0, 1),
}, ensure_ascii=False), flush=True)
print("TRANSCRIPT-BELOW", flush=True)
print(result["text"], flush=True)
sys.exit(0)
