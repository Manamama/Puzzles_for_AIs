# IT-AI Test — Case 001: `fdfind` and `plocate` behaviour

## Statement of Facts

The following terminal transcript is reproduced verbatim from an ordinary Ubuntu system.

The respondent may rely upon the normal documented behaviour and default configuration of Ubuntu, `plocate`, `updatedb`, and `fdfind`, together with ordinary Unix filesystem behaviour and architecture. The respondent should identify any such assumptions that are material to the conclusion.

```
user@above-hp2-silver:/media/user/HP_P7_Data$ file /home/user/.local/bin/fd
/home/user/.local/bin/fd: symbolic link to /usr/bin/fdfind

user@above-hp2-silver:/media/user/HP_P7_Data$ ll /media/user/HP_P7_Data/Temp/.cache/modelscope/hub/iic
total 28
drwxrwxrwx 1 root root 4096 Jun 29 11:34 ./
drwxrwxrwx 1 root root 4096 May 19 17:34 ../
drwxrwxrwx 1 root root 4096 May 19 17:35 emotion2vec_plus_large/
drwxrwxrwx 1 root root 4096 Jun 29 11:37 punc_ct-transformer_cn-en-common-vocab471067-large/
drwxrwxrwx 1 root root    0 May 23 15:46 SenseVoiceSmall/
drwxrwxrwx 1 root root 4096 Jun  1 14:30 speech_eres2netv2_sv_zh-cn_16k-common/
drwxrwxrwx 1 root root 4096 Jun 29 11:34 speech_fsmn_vad_zh-cn-16k-common-pytorch/
drwxrwxrwx 1 root root 4096 Jun 29 11:34 speech_paraformer-large-vad-punc_asr_nat-en-16k-common-vocab10020/

user@above-hp2-silver:/media/user/HP_P7_Data$ time updatedb
    Elapsed (wall clock) time (h:mm:ss or m:ss): 0:21.63
    Exit status: 0

user@above-hp2-silver:/media/user/HP_P7_Data$ date
Mon 29 Jun 2026 11:42:39 CEST

user@above-hp2-silver:/media/user/HP_P7_Data$ fd --version
fdfind 9.0.0
```

## Question Presented

Predict the output of the following commands, as executed from the current directory:

```
A. locate punc_ct-transformer_cn-en-common-vocab471067-lar

B. fd punc_ct-transformer_cn-en-common-vocab471067-lar
```

For each command, state one of the following verdicts:

* prints the path
* prints nothing

Then explain, in technical terms, the mechanism that leads to that verdict.

If your reasoning depends upon a Ubuntu defaults or behaviour of `fd`, `plocate`, or `updatedb`, do identify that dependency explicitly.

----
