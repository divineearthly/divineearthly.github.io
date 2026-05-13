import re
from datetime import datetime

# ============================================================
# NYAYA LENS v2.0 — Production-Grade Hallucination Detector
# Sutra 65: Pramana-Nyaya Epistemic Kernel
# ============================================================

PRATYAKSHA_KEYWORDS = [
    "I measured", "I saw", "I observed", "I recorded", "I tested",
    "I witnessed", "I heard", "I counted", "I weighed",
    "reading was", "the meter showed", "my observation",
    "personally observed", "first-hand", "directly witnessed",
    "I found", "I noticed", "I detected", "lab results show",
    "experiment confirmed", "data confirms"
]

ANUMANA_KEYWORDS = [
    "therefore", "implies", "suggests", "indicates",
    "likely", "probability", "trend", "correlation",
    "because", "thus", "consequently", "probably",
    "might be", "could be", "appears to",
    "the pattern shows", "this means", "estimated",
    "chances are", "odds are", "projected"
]

UPAMANA_KEYWORDS = [
    "similar to", "like", "analogous", "comparable",
    "resembles", "just as", "same as", "parallel to",
    "reminds of", "akin to", "in the same way",
    "similarly", "likewise", "by comparison"
]

SHABDA_KEYWORDS = [
    "according to", "reportedly", "sources say",
    "experts claim", "studies show", "announced",
    "stated", "said", "told reporters", "allegedly",
    "purportedly", "reported by", "officials confirmed",
    "government announced", "sources confirmed",
    "has launched", "has announced", "has revealed",
    "successfully tested", "conducted a", "highlighted",
    "reported", "claims that", "believes that"
]

# ============================================================
# v2.0: Enhanced Hallucination Detection (15 patterns)
# ============================================================
HALLUCINATION_FLAGS = [
    # 1. Anonymous authority
    (r"(scientists|researchers|experts|doctors|professors)\s+(say|claim|believe|proved|discovered|revealed|announced|found|confirmed)",
     "Anonymous authority — no named individual or institution cited"),
    
    # 2. Ghost citation
    (r"(studies|research|reports|trials|experiments)\s+(show|prove|demonstrate|confirm|indicate|reveal|suggest)",
     "Citation without specific reference — which study? published where? by whom?"),
    
    # 3. Bare assertion
    (r"(it is known that|everyone knows|obviously|clearly|undoubtedly|without doubt|of course|naturally|needless to say)",
     "Bare assertion — stated as obvious fact without supporting evidence"),
    
    # 4. Absolute claim
    (r"\b(always|never|all|none|every|no one|everyone|nobody|invariably|without exception)\b",
     "Absolute claim — requires extraordinary evidence to support universal statement"),
    
    # 5. Hype language
    (r"(breakthrough|revolutionary|game.?changing|miracle|cure.?all|magic|wonder|amazing|incredible|unbelievable|astounding)",
     "Hype/clickbait language — emotional appeal instead of factual evidence"),
    
    # 6. Suspicious timeframe
    (r"(within|in just|in only)\s+\d+\s+(days?|hours?|minutes?|weeks?)",
     "Suspiciously specific immediate-result claim — real change rarely happens this fast"),
    
    # 7. Zero downside
    (r"(with zero|with no|without any)\s+(side effects|effort|cost|risk|downside|drawback|disadvantage)",
     "Zero-downside claim — statistically improbable; everything has trade-offs"),
    
    # 8. Total solution
    (r"(completely|100%|perfectly|totally|fully|absolutely)\s+(cures?|eliminates?|solves?|prevents?|heals?|fixes?)",
     "Oversimplified total-solution claim — complex problems rarely have simple fixes"),
    
    # 9. Emotional manipulation
    (r"[❤️🔥💯😱🚨‼️🎉🙏💪🧪💊💉🩺]",
     "Emoji-laden claim — emotional manipulation tactic, not evidence"),
    
    # 10. Conspiracy framing
    (r"(they don'?t want you to know|what (the|big) .* (hiding|don'?t tell|won'?t tell)|secret (cure|remedy|truth)|suppressed|banned|censored)",
     "Conspiracy framing — 'hidden truth' narrative common in misinformation"),
    
    # 11. Fake urgency
    (r"(act now|limited time|before it'?s too late|while supplies last|don'?t miss|urgent|breaking.*exclusive)",
     "Fake urgency — pressure tactic to bypass critical thinking"),
    
    # 12. Vague quantification
    (r"(a lot|many|some|several|various|numerous|countless)\s+(people|studies|doctors|experts|scientists)",
     "Vague quantification — 'many people' without actual numbers"),
    
    # 13. Celebrity/authority appeal
    (r"(elon|bezos|gates|modi|trump|obama|famous|celebrity|hollywood|bollywood)\s+(uses?|recommends?|endorses?|says?|claims?)",
     "Celebrity endorsement — famous name used as substitute for evidence"),
    
    # 14. Ancient/traditional appeal
    (r"(ancient|traditional|centuries.?old|thousands? of years|our ancestors|grandmother'?s|old.?fashioned)\s+(secret|remedy|cure|wisdom|knowledge)",
     "Ancient wisdom appeal — tradition used as proof without scientific validation"),
    
    # 15. Single cause fallacy
    (r"(the one|the only|the single|the sole)\s+(cause|reason|solution|cure|way|method)",
     "Single cause fallacy — complex issues rarely have one cause or solution"),
]

# ============================================================
# Credibility Boosters (increase score)
# ============================================================
CREDIBILITY_MARKERS = [
    (r'(doi:|https?://(dx\.)?doi\.org/)', 15, "DOI reference"),
    (r'(https?://(www\.)?(ncbi\.nlm\.nih\.gov|pubmed|sciencedirect|nature\.com|science\.org|ieee\.org|arxiv\.org))', 15, "Academic source"),
    (r'(published in|appears in|according to the journal)\s+[A-Z][a-z]+', 12, "Named publication"),
    (r'(Dr\.|Prof\.|Professor)\s+[A-Z][a-z]+\s+[A-Z][a-z]+', 10, "Named expert"),
    (r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}\b', 8, "Specific date"),
    (r'\b\d+(\.\d+)?%\b', 6, "Specific percentage"),
    (r'\b[A-Z][a-z]+\sUniversity\b', 10, "University named"),
    (r'(randomized|double.?blind|peer.?reviewed|controlled\s+trial)', 12, "Scientific method"),
]

def classify_pramana(text):
    text_lower = text.lower()
    scores = {
        "Pratyaksha (Direct Observation)": 0,
        "Anumana (Logical Inference)": 0,
        "Upamana (Comparison/Analogy)": 0,
        "Shabda (Testimony/Report)": 0
    }
    
    for kw in PRATYAKSHA_KEYWORDS:
        if re.search(kw, text_lower):
            scores["Pratyaksha (Direct Observation)"] += 1
    
    for kw in ANUMANA_KEYWORDS:
        if re.search(kw, text_lower):
            scores["Anumana (Logical Inference)"] += 1
    
    for kw in UPAMANA_KEYWORDS:
        if re.search(kw, text_lower):
            scores["Upamana (Comparison/Analogy)"] += 1
    
    for kw in SHABDA_KEYWORDS:
        if re.search(kw, text_lower):
            scores["Shabda (Testimony/Report)"] += 1
    
    # News detection
    news_markers = ["announced", "launched", "reported", "confirmed", "stated", "highlighted", "tested"]
    if any(m in text_lower for m in news_markers) and not re.search(r"\bI\s+(measured|saw|observed|tested|witnessed)", text_lower):
        scores["Shabda (Testimony/Report)"] += 2
    
    primary = max(scores, key=scores.get)
    if sum(scores.values()) == 0:
        primary = "Shabda (Testimony/Report) [unverified]"
    
    return primary, scores

def detect_hallucination_flags(text):
    flags = []
    for pattern, explanation in HALLUCINATION_FLAGS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            flags.append({
                "pattern": pattern,
                "matched": str(matches[0]) if matches else "",
                "explanation": explanation
            })
    return flags

def detect_credibility(text):
    bonuses = []
    for pattern, points, label in CREDIBILITY_MARKERS:
        if re.search(pattern, text, re.IGNORECASE):
            bonuses.append({"label": label, "points": points})
    return bonuses

def generate_five_step_scaffold(claim):
    primary_source, _ = classify_pramana(claim)
    flags = detect_hallucination_flags(claim)
    credibility = detect_credibility(claim)
    
    pratijna = f"Claim: '{claim[:150]}{'...' if len(claim) > 150 else ''}'"
    
    hetu = f"Epistemic Source: {primary_source}"
    if flags:
        hetu += f" | ⚠️ {len(flags)} grounding issues"
    if credibility:
        hetu += f" | ✅ {len(credibility)} credibility markers"
    
    udaharana = "Verification: "
    if "Pratyaksha" in primary_source:
        udaharana += "Direct observation — can be replicated by anyone present."
    elif "Anumana" in primary_source:
        udaharana += "Logical inference — check premises for validity."
    elif "Upamana" in primary_source:
        udaharana += "Analogical reasoning — verify the base comparison holds."
    else:
        udaharana += "Reported testimony — locate original source and named authority."
    
    upanaya = "Action: "
    if len(flags) >= 4:
        upanaya += "🚫 DO NOT SHARE. Multiple severe credibility issues. Likely misinformation."
    elif len(flags) >= 2:
        upanaya += "⚠️ Treat with caution. Verify with primary sources before accepting."
    elif len(flags) == 1:
        upanaya += "One concern detected. Quick fact-check recommended."
    else:
        upanaya += "No major red flags. Proceed with normal caution for this source type."
    
    nigamana = "Verdict: "
    if len(flags) >= 4:
        nigamana += "HIGH RISK — Strong indicators of misinformation. Reject unless verified by named, credible source."
    elif len(flags) >= 2:
        nigamana += "MODERATE RISK — Multiple credibility concerns. Cross-reference before relying on this."
    elif len(flags) == 1:
        nigamana += "LOW-MODERATE RISK — Minor concern. Quick verification recommended."
    else:
        if "Pratyaksha" in primary_source:
            nigamana += "LOW RISK — Direct observation. Reliable if observer is trustworthy and competent."
        elif credibility:
            nigamana += "LOW-MODERATE RISK — Testimony with credible markers. Likely reliable."
        else:
            nigamana += "CAUTION — Unverified testimony. Seek original source."
    
    return {
        "1. Pratijna (Hypothesis)": pratijna,
        "2. Hetu (Reason/Grounding)": hetu,
        "3. Udaharana (Verification Method)": udaharana,
        "4. Upanaya (Recommended Action)": upanaya,
        "5. Nigamana (Final Verdict)": nigamana
    }

def calculate_pramana_score(text):
    _, scores = classify_pramana(text)
    flags = detect_hallucination_flags(text)
    credibility = detect_credibility(text)
    
    base_score = 50
    
    # Source bonuses
    base_score += scores["Pratyaksha (Direct Observation)"] * 18
    base_score += scores["Anumana (Logical Inference)"] * 8
    base_score += scores["Upamana (Comparison/Analogy)"] * 4
    base_score -= scores["Shabda (Testimony/Report)"] * 6
    
    # Credibility bonuses
    for cred in credibility:
        base_score += cred["points"]
    
    # Flag penalties (escalating)
    if len(flags) == 1:
        base_score -= 12
    elif len(flags) == 2:
        base_score -= 22
    elif len(flags) == 3:
        base_score -= 30
    elif len(flags) >= 4:
        base_score -= 35 + (len(flags) - 4) * 8
    
    # Additional penalties
    hype_count = len(re.findall(r'(breakthrough|revolutionary|miracle|cure.all|magic|amazing|incredible)', text, re.IGNORECASE))
    base_score -= hype_count * 10
    
    absolute_count = len(re.findall(r'\b(always|never|all|none|every|no one|perfectly|completely)\b', text, re.IGNORECASE))
    base_score -= absolute_count * 6
    
    emoji_count = len(re.findall(r'[❤️🔥💯😱🚨‼️🎉🙏💪🧪💊]', text))
    base_score -= emoji_count * 5
    
    conspiracy_count = len(re.findall(r'(they don.t want you to know|secret cure|suppressed|banned|censored)', text, re.IGNORECASE))
    base_score -= conspiracy_count * 15
    
    # First-person bonus
    first_person = len(re.findall(r'\bI\s+(measured|saw|observed|recorded|tested|witnessed)\b', text, re.IGNORECASE))
    base_score += first_person * 8
    
    # Specific details bonus
    named_entities = len(re.findall(r'\b[A-Z][a-z]+\s[A-Z][a-z]+\b', text))
    base_score += min(named_entities * 3, 15)
    
    return max(0, min(100, base_score))

def analyze_claim(claim):
    primary_source, source_scores = classify_pramana(claim)
    flags = detect_hallucination_flags(claim)
    credibility = detect_credibility(claim)
    scaffold = generate_five_step_scaffold(claim)
    pramana_score = calculate_pramana_score(claim)
    
    return {
        "timestamp": datetime.now().isoformat(),
        "claim": claim,
        "primary_source": primary_source,
        "source_scores": source_scores,
        "pramana_score": pramana_score,
        "hallucination_flags": flags,
        "credibility_markers": credibility,
        "five_step_scaffold": scaffold
    }
