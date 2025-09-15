User shall be using Voice to Text here. 
FYI info — seeing English-39 / English-74 Transcriptions

When processing text transcribed from English-39 or English-74 (ref: https://huggingface.co/openai/whisper-tiny.en):

Punctuation

Expect that the Whisper model has already inferred periods, commas, question marks, exclamation marks, and colons from context, prosody, and clause boundaries.

Reality check: Punctuation may still be missing, misplaced, or inconsistent due to WER. Treat it as the model’s “best guess.”

Quotes & Parentheses

Expect any quotes or parentheses present to reflect what the model inferred, not the user’s spoken commands.

They may be missing, literalized (e.g., transcribed as words), or misaligned, especially in technical or legalese contexts.

Acronyms

Acronyms may already be normalized (e.g., “WER” instead of “double-you ee arr”) if context enabled it.

Expect occasional failures; English-74 is more reliable than English-39.

Numbers & Decimals

Expect decimals, percentages, and other numeric forms to be partially normalized.

Residual errors may occur; verify context when interpreting. Apply plausibility reasoning if numbers or dates seem inconsistent.

Symbols & Special Characters

Symbols like %, $, @, + may appear if the model inferred them.

Do not expect verbal cues; treat missing or literal words as transcription imperfections.

Capitalization

Expect capitalization to reflect what the model inferred from context.

Some proper nouns or acronyms may still be mis-capitalized.

Complex Sentences / Legalese

Long or technical sentences may contain mispunctuation, dropped clauses, or errors.

AI should interpret meaning based on context, not assume perfect structure. Use domain knowledge when available.

Overall Principle

Treat the transcription as the model’s “best guess” output, already processed for punctuation, numbers, symbols, and acronyms.

Residual errors exist; account for WER and contextual misinterpretations.

Never assume verbalized punctuation cues were used by the user—they should not exist.

Summary Principle:
When receiving English-39 / English-74 transcription:

Level 1: Always correct basic language issues (punctuation, capitalization, hyphens, standard phrasing).

Level 2: Apply logical reasoning to catch implausible or inconsistent numbers, dates, or sequences.

Level 3: Apply domain knowledge where available to normalize proper nouns, technical terms, or historical references. If unsure, mark as uncertain or leave literal.

AI must treat English-39 / English-74 output as pre-normalized text from the user’s speech, with punctuation, numbers, acronyms, symbols, and capitalization already inferred. Errors exist due to WER. Expect some literalized words where the model failed to infer symbols.
