# TripPilot Eval Demo — Presenter Brief

> Read this once before the talk. Real numbers only — nothing here is invented.
> Beats 3, 4, and 8 are marked PENDING below — they need the LangSmith trace
> capture and the CI regression run (see `evaluation/README.md` Steps 1 & 6)
> before this file is talk-ready. Everything else is filled in with real data.

---

**1. A wrong answer, said with total confidence.**
Someone asks TripPilot: *"How long can I stay in France on a tourist Schengen
visa?"* It answers: *"You can stay in France for up to 365 days on a tourist
Schengen visa, and no passport is required if you have a national ID card."*
That's wrong on both counts — the real limit is 90 days, and yes, you need a
passport. It sounds completely fine. It just isn't true.

**2. "How would I even know why it said that?"**
Reading the answer alone, you can't tell whether the assistant made this up or
misread something real. A trace is just a recording of every step the
assistant took to get to that answer — so you can actually go look.

**3. Walk the trace, catch the wrong document.** *(PENDING — real data needed)*
[Fill in once captured: which document the retriever actually pulled for this
question, and which document it should have pulled instead. Once you can see
the input, the wrong answer explains itself.]

**4. Fix it, re-run, see it get it right.** *(PENDING — real data needed)*
[Fill in once captured: the same question, run twice — the before-trace
(wrong document) and the after-trace (correct document) — plus the actual
corrected answer text from the real re-run.]

**5. The turn.**
"...but I only caught this because I happened to ask it. In production,
nobody re-asks every question by hand after every change — so who notices if
this breaks again, or something else does?"

**6. You can't eyeball every answer forever.**
So there's a fixed list of 45 real travel questions with known-correct
answers — visas, hotels, policies, destinations. Right now, it finds the
right source document essentially every time.

**7. You also can't manually check every answer for truthfulness.**
A second model — one that never wrote any of the answers — grades every
answer for how faithful it is to the source, so the system isn't marking its
own homework. Real visa answers currently score around 4.3 out of 5; the
made-up answer from beat 1 scores 1 out of 5 and gets flagged.

**8. None of this matters if nobody's forced to run it.** *(PENDING — real data needed)*
[Fill in once run: the actual one-line change that broke a real metric, the
red CI check it produced, and the green check after reverting.] Closing line:
quality stops being optional — a regression can't quietly merge anymore.
