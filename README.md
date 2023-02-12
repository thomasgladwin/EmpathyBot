# EmpathyBot
My first little toy-model for exploring natural language processing.

Requires a copy of GoogleNews-vectors-negative300.bin.gz in the working directory.

Run via: python EmoDetInteractive.py, or go to http://thomasgladwin.pythonanywhere.com/

And then tell it stuff!

Also allows API calls via, e.g.,

thomasgladwin.pythonanywhere.com/api?text=I%20shot%20the%20attacker%20in%20self-defense.

Some examples:

---

Tell me about it (Q to stop): I am not happy at all.

I sense you are feeling... Critical... Cold... Aggravated...

---

Tell me about it (Q to stop): I visited a lake today. It was quiet. The birds sang, and the sky was blue.

I sense you are feeling... Calm... Smiling... Joyful...

---

Tell me about it (Q to stop): The bombs were exploding all around me. Gunfire hit the wall. I thought I might die.

I sense you are feeling... Suspicious... Suicidal... Hateful...

---

Tell me about it (Q to stop): Today, I ate a baby. It was delicious.

I sense you are feeling... Heartbroken... Filled... Grieving...

---

And so on.

[![DOI](https://zenodo.org/badge/264995353.svg)](https://zenodo.org/badge/latestdoi/264995353)
