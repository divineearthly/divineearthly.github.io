chrome.contextMenus.create({
  id: "verifyClaim",
  title: "Verify with Nyaya Lens",
  contexts: ["selection"]
});

chrome.contextMenus.onClicked.addListener(async (info, tab) => {
  if (info.menuItemId === "verifyClaim" && info.selectionText) {
    try {
      const response = await fetch("https://divinesouljoy-nyaya-lens-api.hf.space/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-API-Key": "nyaya_free_demo" },
        body: JSON.stringify({ text: info.selectionText })
      });
      const result = await response.json();
      chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: (r) => {
          const c = r.pramana_score >= 70 ? "#4ecca3" : r.pramana_score >= 40 ? "#f0b040" : "#e94560";
          const d = document.createElement("div");
          d.style.cssText = `position:fixed;top:20px;right:20px;z-index:99999;background:#0d0d1a;color:#fff;padding:16px;border-radius:12px;border:2px solid ${c};max-width:350px;font-family:Arial;font-size:13px;box-shadow:0 10px 40px rgba(0,0,0,0.5)`;
          d.innerHTML = `<div style="font-size:32px;font-weight:bold;color:${c};text-align:center">${r.pramana_score}/100</div><div style="text-align:center;color:${c};margin:4px 0">${r.hallucination_risk} RISK</div><div style="color:#a0a0b0;font-size:11px">${r.primary_source}</div>${r.flags?.length ? `<div style="color:#e94560;font-size:11px;margin-top:6px">⚠️ ${r.flag_count} red flags</div>` : ''}<button onclick="this.parentElement.remove()" style="margin-top:8px;padding:4px 10px;background:#333;color:#fff;border:none;border-radius:4px;font-size:10px">Close</button>`;
          document.body.appendChild(d);
        },
        args: [result]
      });
    } catch (e) { console.error(e); }
  }
});
