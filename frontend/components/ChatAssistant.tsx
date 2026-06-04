"use client";

import { Fragment, useEffect, useRef, useState } from "react";
import { Bot, Maximize2, MessageCircle, Minimize2, Send, X } from "lucide-react";

type Message = {
  role: "user" | "assistant";
  text: string;
};

const WELCOME: Message = {
  role: "assistant",
  text: "Xin chào! Tôi là trợ lý SmartTravel. Tôi có thể gợi ý vé xe, tàu, máy bay, lịch trình, điểm du lịch, trải nghiệm địa phương và lựa chọn đặt phòng."
};

const SUGGESTED_PROMPTS = [
  "Gợi ý lịch trình Đà Nẵng 3 ngày 2 đêm",
  "Đi Huế nên ăn gì và chơi ở đâu?",
  "Tìm vé và phòng cho chuyến Nha Trang"
];

const INLINE_MARKDOWN_RE = /(\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)|\*\*([^*]+)\*\*|(https?:\/\/[^\s]+))/g;

function isSafeHttpUrl(value: string) {
  try {
    const url = new URL(value);
    return url.protocol === "http:" || url.protocol === "https:";
  } catch {
    return false;
  }
}

function compactUrl(value: string) {
  try {
    const url = new URL(value);
    return url.hostname.replace(/^www\./, "");
  } catch {
    return value;
  }
}

function renderInlineMarkdown(text: string) {
  const nodes = [];
  let lastIndex = 0;

  for (const match of text.matchAll(INLINE_MARKDOWN_RE)) {
    const index = match.index ?? 0;
    if (index > lastIndex) {
      nodes.push(text.slice(lastIndex, index));
    }

    const [, raw, linkLabel, markdownHref, boldText, plainHref] = match;
    const href = markdownHref || plainHref;

    if (href && isSafeHttpUrl(href)) {
      nodes.push(
        <a key={`${index}-${href}`} href={href} target="_blank" rel="noreferrer">
          {linkLabel || compactUrl(href)}
        </a>
      );
    } else if (boldText) {
      nodes.push(<strong key={`${index}-${boldText}`}>{boldText}</strong>);
    } else {
      nodes.push(raw);
    }

    lastIndex = index + raw.length;
  }

  if (lastIndex < text.length) {
    nodes.push(text.slice(lastIndex));
  }

  return nodes;
}

function ChatMessageContent({ text }: { text: string }) {
  const lines = text.split("\n");

  return (
    <>
      {lines.map((line, index) => {
        const ordered = line.match(/^\s*(\d+)\.\s+(.*)$/);
        const bullet = line.match(/^\s*[-*]\s+(.*)$/);

        if (!line.trim()) {
          return <br key={index} />;
        }

        if (ordered) {
          return (
            <div className="chat-list-item" key={index}>
              <span className="chat-list-marker">{ordered[1]}</span>
              <span>{renderInlineMarkdown(ordered[2])}</span>
            </div>
          );
        }

        if (bullet) {
          return (
            <div className="chat-list-item" key={index}>
              <span className="chat-list-marker">•</span>
              <span>{renderInlineMarkdown(bullet[1])}</span>
            </div>
          );
        }

        return (
          <Fragment key={index}>
            {index > 0 ? <br /> : null}
            {renderInlineMarkdown(line)}
          </Fragment>
        );
      })}
    </>
  );
}

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
        <div className={`chat-window${fullscreen ? " fullscreen" : ""}`} role="dialog" aria-label="Trợ lý SmartTravel">
          <div className="chat-header">
            <Bot size={18} aria-hidden="true" />
            <span>Trợ lý SmartTravel</span>
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
                <ChatMessageContent text={m.text} />
              </div>
            ))}
            {messages.length === 1 && !loading ? (
              <div className="chat-suggestions" aria-label="Gợi ý câu hỏi">
                {SUGGESTED_PROMPTS.map((prompt) => (
                  <button
                    key={prompt}
                    onClick={() => setInput(prompt)}
                    type="button"
                  >
                    {prompt}
                  </button>
                ))}
              </div>
            ) : null}
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
              placeholder="Hỏi lịch trình, vé, khách sạn..."
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
