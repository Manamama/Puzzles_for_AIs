This document is a practical guide to various Speech-to-Text (STT) workflows, based on a series of experiments. It provides a hands-on look at different STT engines and their integration with a command-line interface, offering insights into the user experience and the quality of the resulting transcriptions.

# Experiment Log: Speech-to-Text (STT) Engine Analysis

This document logs a series of experiments testing different Speech-to-Text (STT) engines and their integration with my workflow. The goal is to understand the characteristics and quality of different STT outputs as I receive them.

---

## A. STT Input via Termux + Gemini CLI (TUI)
   
This section documents STT inputs that are dictated directly into our terminal session.

### A.1. Sample 1 (Google STT)

```
all right user is pretty tired with typing with two fingers so after three many years users trying to use a couple of speech to text engines for example right now in order to actually say it to you because I'm not finger typing anymore I have to switch on the special somehow hidden a bar which is such you know the bar how to explain it to you okay in Google keyboard when you are in a special environment for example the mic button is actually hidden you have to do some secret trick of actually sliding the top how to explain it to you well you have to use imagination so there is a Google keyboard and on top it has a row of usually symbols but if you slide it suddenly like a mini editing window actually one line appears and the usual buttons of copy paste and the left and right and maybe even icons but especially the microphone button appears this is the way I'm using it right now and notice that there are no punctuation marks because Google text to speech is sorry sorry Google speech to text is pretty ancient and back then the model was was not good enough and it still does not contain punctuation all right so sorry for running sentence but this is how it all works I'm finishing now and I cannot use any even punctuation to mark that this is finished as a full stop
```

---

### A.2. Sample 2 (Google STT)

```
user used to have a number of Android phones and because user loves rooting and so on for many years actually Google speech to text did not work I think for 5 years the problem was that Google I'm actually good rid of most Google stuff and back then the bespoke Google likes replacement for the Google switch somehow were discovering that the main Google application was missing I forgot what it was called it was like Google package or Google switch something something for a route to linuxes I think was lineage OS anyhow for many years this Google speech to text I was not working they're just there was no microphone button whatsoever and now you understand that also the actual engine was missing and I think I said or something like this abbreviations with the actual mini small language models that is the voice models so they were missing but after user figure out how to convince Google that this is a regular Google phone Google was working again but the problem is that everybody knows that this speech to text by Google is mundane is not sophisticated it's a old it's a pretty tiny and despite the fact that this is entering as we speak it's still is not introducing punctuations and what's not why it's important in terms because usually in terms of user is entering command that is actually unix commands which are marquee which are bespoke which are hard to translate and every letter counts so it's impossible to just talk to you next and hope for the best however if one talks even with mistakes like this one Gemini it's actually makes sense because Jamie and I cloud cloud Gemini and cloudy I may understand the mistakes which are being introduced by speech to text and by the city user into the Gemini CLI C l I wonder if it's going to make make it as a three letter abbreviation that is too clear that is to actual the and the three which means the actual application okay user ends here
```

---

### A.3. Sample 3 (WhisperIME - Fast Model)

This sample was generated using the [WhisperIME keyboard](https://github.com/woheller69/whisperIME), which uses an English-only, fast model from OpenAI's Whisper.

```
Alright, this is actually more tricky because when you need the user is using what is being indicated as the engine, the actual keyboard does not appear in term of and the user knows why. because while for example Google board that is the keyboard has a Google board, maybe a board actually. So while Google board does indeed has the editing line where the microphone button appears, this very input IME does not have it. which means that the user has to go to a separate application, the whisper IME which is not IME anymore. It is not input anymore. And has to record it in this special very large window like an editor almost 30 seconds each. This is being transcribed by real whisper open AI whisper Model it is English only fast, but it seems to be very good Only that the user has to remember to stop after about 25 seconds It is not intuitive. There is a muscle memory that has to be adopted in that, mentally, the user has to have a counter in the head. How long, how many seconds are left for the thought to finish? Use a make, see 30 seconds, but then it's clipped and use a must repeat.
```

---

### A.4. Sample 4 (WhisperIME - Multilingual Slow Model)

This sample was generated using the WhisperIME keyboard, but with the more advanced `multilingual slow` model, with the language manually set to English.

```
User seems to be getting the hang of it all. Right now we are using multilingual slowmodel but we hand specify the English as the language and user knows how it works. Because this is just OpenAI whisper model which user knows very well from Ubuntu and from PC. Also the same model works in Teramux itself. The only trick is again that user must Mentally prepare for the recording snippet to finish. It is a bit meta, that is, it's like interpreting. The user must have a timer ticking at the back of the head to count the seconds that remain. Because there is no timer here, so more or less it's like a turn taking. The user must just shut up every 25 seconds. Interestingly the very 25 seconds that the user is discussing right now has taken 26 seconds to process. So this is a good time for gathering thoughts. Also the user is using the monitor with RAM and CPU to see the spikes. The RAM actually doesn't budge but CPU indeed is used from 20% jumps up to 80% which makes perfect sense.
```

---

## B. STT Input via Android GUI (MiXplorer Editor)

This section documents STT inputs that are first captured in a separate Android application and then read by me from the file.

### B.1. Google STT Raw Output

```
All right so this time user is directly talking to marker using Google board but I guess this is going to looks like a better than when a user was doing the same to terminal that is to thermos for a number of reasons reason one user is this time somehow more familiar after about 5 minutes of experiments it is it was still somehow new to the user back then about 5-10 minutes ago second reason is that actually and use a realizes that framework that is the affordability or there is a very fancy word for this accordance is the word it's important for example here user is talking directly so to say to Mark or m a r k o r which is an application which has a huge window very bright very well convenient and when One compares it to thermos which when you one uses Google board itself because user just has one line and doesn't see the complex and is even psychologically somehow scary why is it scary in terms because the user is associating quite righty so thermals with very precise unix commands and user nose if somebody if you use a right scrap grip is different than repetitions and LS which is means show me the files if you just change the letters then it becomes SL which is a funny name for a command which shows instead of a real files it shows usually some funny cows or is it maybe the railroads okay here spent some 10 seconds looking at the feedback and this is better than usually expected it is actually the question of being accustomed to how these things work for example there are no punctuation marks however the user may say., well. And, together doesn't make no sense does it? But user could say this is the end of the sentence. This is the next sentence. And user is wondering, is it clear? Well maybe it's not elegant. But if user knows that Gemini AI shall be reading it and can figure out that when the question mark is being used as a object to be discussed and when the actual sentence is being terminated there by Jim and I AI may actually understand when the s...
```

---

### B.2. Kaiboard IME, 1.0, probably this one: https://github.com/kaisoapbox/kaiboard

**Technical info displayed:** 
```
System Info: AVX = 0 | AVX2 = 0 | AVX512 = 0 | FMA = 0 | NEON = 1 | ARM_FMA = 1 | METAL = 0 | F16C = 0 | FP16_VA = 1 | WASM_SIMD = 0 | BLAS = 0 | SSE3 = 0 | SSSE3 = 0 | VSX = 0 | CUDA = 0 | COREML = 0 | OPENVINO = 0

7 threads out of 8. 

Loaded model ggml-tiny.en.bin
```

**Actual text:** 
```
Well, it is the most mysterious keyboard of them all because actually there is no keyboard. This is a hobby project which ha has 1, 2, 3, 4, 5, yes 5 buttons and there are as follows. At the bottom of the screen where the keyboard usually happens, there are buttons like "okay" with the timer, "cancer", I guess, "cancer recording", "backspace", I wonder why because there is no text yet, "enter" which is next line and the keyboard. That is the keyboard switch button. The keyboard switch button is the most mysterious because it does not show any keyboard by this keyboard thingy but it switches to the last keyboard which is just any other keyboard but not this one. So it is the well-dring because the user has to remember that to switch back into this voice-only keyboard, "well it is not a keyboard". Voice input which is this keyboard I me.  
```

---

### B.3. WhisperIME - Multilingual, Fast, EN selected:

```
Press and hold the microphone button while speaking. This one probably shall be last but one experiment because user has loads of ideas and we are drawing to a close but not yet. So this Skyboard, this experimental one was very experimental, almost nerve-wracking. It had its It had its good and bad sides. The good side is that there was actually a tiny timer in the actual talk button. So the user knew how much it has been going and running. The good thing also it was that it was not randomly disconnecting, that is after 30 seconds it was not disconnecting, it was still going on. But the very bad thing is, that the actual window of tokens, the size, well actually the time snippet, is indeed 30 seconds, which means well maybe one minute, which means that at least once everything was wiped because user was not aware and was talking for one minute and a half and nothing got recorded. So this is the most The most dangerous because the user is expecting everything to be recorded well because the timer is coming on. But unless the user is very well aware of the limitations of these tiny models, then the user would just be talking for the no five minutes and everything will be gone. So it is just too experimental. Now we are back to this multilingual fast whisper, the actual whisper model. It's a pity that they do not show whether this is tiny, medium or whatever, but we can hack it. So in a way, it has its good aspects in that every 30 seconds user must pause, because well, it just stops. But then the user sees every 30 seconds The user sees every 30 seconds what has been displayed. So it is also a safety switch that is what you see is what you get. That is user sees every 30 seconds snippets into the window and user is more or less secure that user is not talking to the wall. But still about 10 seconds pause after every 30 seconds it's pain the neck. So the user has the idea for a very interesting I guess for Gemini AI, the last experiment which I'll follow soon.
```

---

### B.4. Whisperx - Multilingual, Small, language autodetected:

**Technical info displayed:** 
```
Processing:  /data/data/com.termux/files/home/downloads/20250801T023315.mp3 

🗃️  Input file duration: 3 min 58 s

Running whisperx with highlighted words, with float32 precision, --model small
>>Performing transcription...
Detected language: en (0.99) in first 30s of audio...
Progress: 11.11%...
Transcript: [2.174 --> 26.002]  All right, so this is a completely different method. In that there is actually no input IME, I wonder what it is, input method editor or something like that. There is none. The user is actually talking to, well, to mp3 file.
Progress: 22.22%...
Transcript: [26.66 --> 53.592]  There is nothing to press, there is nothing to type, there is no timer, there is no worry that something may be misheard. Well, okay, there is a worry that it can be misheard, but there is no worry about timers ticking, about interface disappearing, about files go missing or text,
Progress: 33.33%...
Transcript: [54.014 --> 71.159]  There is almost none. Why is this so? Because the user pressed Audio Recorder, that is, selected Audio Recorder, the actual just very common application for Android, pressed Record,
Progress: 44.44%...
Transcript: [71.513 --> 100.117]  Yes, there is a timer ticking, but it is not scary this time. And user can talk to users hard content, freely expressing the thoughts. How come that Gemini AI is actually seeing it as text? Well, there is a mystery. Because many years ago, I think three, user learned how LLM, the actual application LLM,
Progress: 55.56%...
Transcript: [100.454 --> 125.48]  works in Android. It is a very robust and universal thing which can transcribe voices, which can actually talk. There are offline large language models. Well, it can do, I think, everything that the same application can do on a huge server only, server computers.
Progress: 66.67%...
Transcript: [126.087 --> 155.399]  So user is not analyzing images, which also can be done this. User is not writing poetry with this offline LLMs, but using WhisperX, which is a specialized audio model, or is it Whisper? I think it's the same actually, but the application's called WhisperX. So using this, user is going to transcribe this very text, well, it's the text, this very audio,
Progress: 77.78%...
Transcript: [155.72 --> 184.12]  into a, well, a regular, regular file. Actually, you know what? Ha, I know. I can switch on, yes, I think I can switch on even the time codes. Yes, there will be time codes and I think each sentence will be separate and time coded. But I must remember
Progress: 88.89%...
Transcript: [184.188 --> 209.028]  not to switch the higherization, another option of WhisperX, because then it takes three times as long. So let me see. This is three minutes, 40 seconds long. So it would be, I think, four minutes by the time I finish. And it's likely to take twice as much. So either 8 up to 12 minutes to transcribe
Progress: 100.00%...
Transcript: [209.281 --> 237.293]  using, I think, medium or small quality, which is good enough trade-off between quality and time and also the requirements of the device, because large language model is actually, sorry, large audio model, the largest, I think is large V3, is actually crashing Android unless one is very careful. Thank you. See you soon.
```


B.5. Gemini AI processes audio file: 

Ref: 
The content was presented to Gemini as a text output from the `read_file` tool, with the additional information: `{"read_file_response": {"output": "Binary content of type audio/mpeg was processed."}}`

---

See Also:

*   [speech_recognition_systems_analysis.md](../concepts/speech_recognition_systems_analysis.md)