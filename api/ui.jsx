import { useState } from "react";

const theme = {
  bg: "#060910",
  surface: "#0c1220",
  surfaceHover: "#111a2e",
  border: "#1a2840",
  accent: "#00e5a0",
  accentDim: "#00a370",
  warn: "#ffb547",
  error: "#ff4f6a",
  blue: "#00c2ff",
  text: "#e8f4ff",
  textDim: "#5a7a9a",
  textMuted: "#2a3f5a",
};

const SUGGESTIONS = [
  "How many 5xx errors today?",
  "Summarize today's CDN traffic",
  "Have we had similar DDoS incidents before?",
  "Send an alert — error rate is above 15%",
  "How many requests came from Korea today?",
  "What was the cache hit rate today?",
];

const AGENT_COLORS = {
  QueryAgent: theme.blue,
  SummaryAgent: theme.accent,
  IncidentAgent: theme.warn,
  AlertAgent: theme.error,
};

export default function EdgeLogIntelligence() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (question) => {
    const q = question || input;
    if (!q.trim()) return;

    setInput("");
    setLoading(true);
    setMessages(prev => [...prev, { role: "user", content: q }]);

    try {
      const res = await fetch("https://giada-subuncinal-subspirally.ngrok-free.dev/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: q }),
      });
      const data = await res.json();
      setMessages(prev => [...prev, { role: "assistant", content: data.result }]);
    } catch (err) {
      setMessages(prev => [...prev, { role: "assistant", content: "⚠️ Could not connect to backend. Is the FastAPI server running?", error: true }]);
    }

    setLoading(false);
  };

  return (
    <div style={{ minHeight: "100vh", background: theme.bg, fontFamily: "'DM Mono', 'JetBrains Mono', monospace", color: theme.text, display: "flex", flexDirection: "column" }}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@400;500;600;700&display=swap');
        * { box-sizing: border-box; margin: 0; padding: 0; }
        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-thumb { background: ${theme.border}; border-radius: 2px; }
        @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0} }
        @keyndef fadeUp { from{opacity:0;transform:translateY(6px)} to{opacity:1;transform:translateY(0)} }
        @keyframes fadeUp { from{opacity:0;transform:translateY(6px)} to{opacity:1;transform:translateY(0)} }
        @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.3} }
        @keyframes spin { from{transform:rotate(0deg)} to{transform:rotate(360deg)} }
      `}</style>

      {/* Header */}
      <div style={{ padding: "16px 24px", borderBottom: `1px solid ${theme.border}`, display: "flex", alignItems: "center", gap: 12, background: theme.surface }}>
        <div style={{ display: "flex", gap: 6 }}>
          {[theme.error, theme.warn, theme.accent].map((c, i) => (
            <div key={i} style={{ width: 10, height: 10, borderRadius: "50%", background: c, opacity: 0.8 }} />
          ))}
        </div>
        <div style={{ flex: 1, textAlign: "center" }}>
          <span style={{ fontSize: 13, color: theme.textDim, fontFamily: "'DM Mono', monospace" }}>
            edgelog-intelligence <span style={{ color: theme.accent }}>●</span> connected
          </span>
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          {["Query", "Summary", "Incident", "Alert"].map(a => (
            <div key={a} style={{ fontSize: 10, padding: "2px 8px", borderRadius: 4, background: `${AGENT_COLORS[a + "Agent"]}18`, color: AGENT_COLORS[a + "Agent"], border: `1px solid ${AGENT_COLORS[a + "Agent"]}33` }}>
              {a}
            </div>
          ))}
        </div>
      </div>

      {/* Messages */}
      <div style={{ flex: 1, overflowY: "auto", padding: "24px", display: "flex", flexDirection: "column", gap: 16 }}>
        {messages.length === 0 && (
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", flex: 1, gap: 32 }}>
            <div style={{ textAlign: "center" }}>
              <div style={{ fontSize: 11, color: theme.accentDim, letterSpacing: 4, textTransform: "uppercase", marginBottom: 12 }}>EdgeOne Log Intelligence</div>
              <div style={{ fontSize: 28, fontFamily: "'DM Sans', sans-serif", fontWeight: 700, letterSpacing: -1, marginBottom: 8 }}>
                Ask anything about your CDN
              </div>
              <div style={{ fontSize: 13, color: theme.textDim }}>Powered by Multi-Agent RAG · Plan & Execute · ChromaDB</div>
            </div>

            {/* Suggestions */}
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8, maxWidth: 600, width: "100%" }}>
              {SUGGESTIONS.map((s, i) => (
                <button key={i} onClick={() => handleSubmit(s)}
                  style={{
                    background: theme.surface, border: `1px solid ${theme.border}`,
                    borderRadius: 8, padding: "10px 14px", color: theme.textDim,
                    fontSize: 12, textAlign: "left", cursor: "pointer",
                    transition: "all 0.15s", fontFamily: "'DM Sans', sans-serif",
                  }}
                  onMouseEnter={e => { e.target.style.borderColor = theme.accent + "66"; e.target.style.color = theme.text; }}
                  onMouseLeave={e => { e.target.style.borderColor = theme.border; e.target.style.color = theme.textDim; }}
                >
                  {s}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((msg, i) => (
          <div key={i} style={{ animation: "fadeUp 0.2s ease", display: "flex", gap: 12, flexDirection: msg.role === "user" ? "row-reverse" : "row" }}>
            {/* Avatar */}
            <div style={{
              width: 28, height: 28, borderRadius: "50%", flexShrink: 0,
              background: msg.role === "user" ? `${theme.blue}22` : `${theme.accent}22`,
              border: `1px solid ${msg.role === "user" ? theme.blue : theme.accent}44`,
              display: "flex", alignItems: "center", justifyContent: "center",
              fontSize: 11, color: msg.role === "user" ? theme.blue : theme.accent,
            }}>
              {msg.role === "user" ? "U" : "AI"}
            </div>

            {/* Bubble */}
            <div style={{
              maxWidth: "75%", padding: "12px 16px", borderRadius: 10,
              background: msg.role === "user" ? `${theme.blue}12` : theme.surface,
              border: `1px solid ${msg.role === "user" ? theme.blue + "33" : theme.border}`,
              fontSize: 13, lineHeight: 1.7, color: msg.error ? theme.error : theme.text,
              fontFamily: "'DM Sans', sans-serif", whiteSpace: "pre-wrap",
            }}>
              {msg.content}
            </div>
          </div>
        ))}

        {loading && (
          <div style={{ display: "flex", gap: 12, animation: "fadeUp 0.2s ease" }}>
            <div style={{ width: 28, height: 28, borderRadius: "50%", background: `${theme.accent}22`, border: `1px solid ${theme.accent}44`, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 11, color: theme.accent }}>AI</div>
            <div style={{ padding: "12px 16px", borderRadius: 10, background: theme.surface, border: `1px solid ${theme.border}`, display: "flex", gap: 6, alignItems: "center" }}>
              {[0, 1, 2].map(i => (
                <div key={i} style={{ width: 6, height: 6, borderRadius: "50%", background: theme.accent, animation: `pulse 1.2s ${i * 0.2}s infinite` }} />
              ))}
              <span style={{ fontSize: 12, color: theme.textDim, marginLeft: 4, fontFamily: "'DM Sans', sans-serif" }}>Planning & executing...</span>
            </div>
          </div>
        )}
      </div>

      {/* Input */}
      <div style={{ padding: "16px 24px", borderTop: `1px solid ${theme.border}`, background: theme.surface }}>
        <div style={{ display: "flex", gap: 10, maxWidth: 800, margin: "0 auto" }}>
          <div style={{ flex: 1, position: "relative" }}>
            <span style={{ position: "absolute", left: 14, top: "50%", transform: "translateY(-50%)", color: theme.accent, fontSize: 13 }}>›</span>
            <input
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => e.key === "Enter" && handleSubmit()}
              placeholder="Ask about your EdgeOne CDN logs..."
              style={{
                width: "100%", background: theme.surfaceHover,
                border: `1px solid ${theme.border}`, borderRadius: 8,
                padding: "12px 16px 12px 30px", color: theme.text,
                fontSize: 13, fontFamily: "'DM Mono', monospace",
              }}
              onFocus={e => e.target.style.borderColor = theme.accentDim}
              onBlur={e => e.target.style.borderColor = theme.border}
            />
          </div>
          <button onClick={() => handleSubmit()}
            style={{
              background: `linear-gradient(135deg, ${theme.accent}, ${theme.accentDim})`,
              border: "none", borderRadius: 8, padding: "0 20px",
              color: theme.bg, fontWeight: 700, fontSize: 13,
              cursor: "pointer", fontFamily: "'DM Sans', sans-serif",
              opacity: loading ? 0.5 : 1,
            }}>
            Run
          </button>
        </div>
        <div style={{ textAlign: "center", marginTop: 8, fontSize: 11, color: theme.textMuted, fontFamily: "'DM Sans', sans-serif" }}>
          Multi-Agent · Plan & Execute · LangChain · ChromaDB
        </div>
      </div>
    </div>
  );
}
