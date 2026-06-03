"use client";

import { useEffect, useRef, useState } from "react";
import { Bot, Maximize2, MessageCircle, Minimize2, Send, X } from "lucide-react";

type Message = {
  role: "user" | "assistant";
  text: string;
};

const WELCOME: Message = {
  role: "assistant",
  text: "Xin chào! Tôi là trợ lý SmartBus. Tôi có thể giúp bạn tìm vé xe, giải đáp thắc mắc về tuyến đường hoặc hướng dẫn sử dụng ứng dụng."
};

export function ChatAssistant() {
  const [open, setOpen] = useState(false);
  const [fullscreen, setFullscreen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([WELCOME]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  useEffect(() => {
    if (open) inputRef.current?.focus();
  }, [open]);

  async function send() {
    const text = input.trim();
    if (!text || loading) return;

    const next: Message[] = [...messages, { role: "user", text }];
    setMessages(next);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text, history: next })
      });
      const data = await res.json();
      setMessages([...next, { role: "assistant", text: data.reply }]);
    } catch {
      setMessages([...next, { role: "assistant", text: "Xin lỗi, có lỗi xảy ra. Vui lòng thử lại." }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <button
        className="chat-toggle"
        onClick={() => setOpen((v) => !v)}
        aria-label={open ? "Đóng trợ lý" : "Mở trợ lý"}
      >
        {open ? <X size={22} /> : <MessageCircle size={22} />}
      </button>

      {open && (
        <div className={`chat-window${fullscreen ? " fullscreen" : ""}`} role="dialog" aria-label="Trợ lý SmartBus">
          <div className="chat-header">
            <Bot size={18} aria-hidden="true" />
            <span>Trợ lý SmartBus</span>
            <button
              className="chat-header-btn"
              onClick={() => setFullscreen((v) => !v)}
              aria-label={fullscreen ? "Thu nhỏ" : "Toàn màn hình"}
            >
              {fullscreen ? <Minimize2 size={15} /> : <Maximize2 size={15} />}
            </button>
          </div>

          <div className="chat-messages">
            {messages.map((m, i) => (
              <div key={i} className={`chat-bubble ${m.role}`}>
                {m.text}
              </div>
            ))}
            {loading && (
              <div className="chat-bubble assistant chat-typing" aria-label="Đang trả lời">
                <span /><span /><span />
              </div>
            )}
            <div ref={bottomRef} />
          </div>

          <div className="chat-input-row">
            <input
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && send()}
              placeholder="Nhập câu hỏi..."
              disabled={loading}
            />
            <button
              onClick={send}
              disabled={loading || !input.trim()}
              aria-label="Gửi"
            >
              <Send size={16} />
            </button>
          </div>
        </div>
      )}
    </>
  );
}
