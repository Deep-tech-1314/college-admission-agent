import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, GraduationCap, ArrowRight } from 'lucide-react';
import './index.css';

function App() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'bot',
      text: "Hi there! I'm the Global Tech Admission Agent powered by IBM Granite. How can I help you with your college application today?"
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const faqs = [
    "What are the eligibility criteria for CS?",
    "When are the application deadlines?",
    "What is the fee structure?",
    "Are there any scholarships available?",
    "Can I apply without SAT/ACT scores?",
    "Is on-campus housing mandatory?",
    "How can I change my major?",
    "Can international students work on campus?"
  ];

  const handleSend = async (text = input) => {
    if (!text.trim()) return;

    const userMessage = { id: Date.now(), sender: 'user', text };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // Connect to our FastAPI backend
      const response = await fetch('http://localhost:8000/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: text }),
      });

      if (!response.ok) {
        throw new Error('Failed to connect to the agent.');
      }

      const data = await response.json();
      
      const botMessage = {
        id: Date.now() + 1,
        sender: 'bot',
        text: data.answer,
        sources: data.sources
      };
      
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error(error);
      const errorMessage = {
        id: Date.now() + 1,
        sender: 'bot',
        text: "I'm sorry, I couldn't connect to my knowledge base right now. Please ensure the backend server is running."
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="app-container">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="brand">
          <GraduationCap size={28} color="#818CF8" />
          <h1>Global Tech Agent</h1>
        </div>
        
        <div className="sidebar-content">
          <h3 className="sidebar-title">Suggested Questions</h3>
          <div className="faq-list">
            {faqs.map((faq, idx) => (
              <button 
                key={idx} 
                className="faq-btn"
                onClick={() => handleSend(faq)}
                disabled={isLoading}
              >
                {faq}
              </button>
            ))}
          </div>
        </div>
        
        <div style={{ marginTop: 'auto', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
          Powered by IBM Granite & watsonx
        </div>
      </aside>

      {/* Main Chat Area */}
      <main className="chat-area">
        <header className="chat-header">
          <div>
            <h2>Admission Assistant</h2>
            <div className="status">
              <span className="status-dot"></span>
              Online
            </div>
          </div>
          <Bot size={24} color="var(--text-muted)" />
        </header>

        <div className="messages-container">
          {messages.map((msg) => (
            <div key={msg.id} className={`message-wrapper ${msg.sender}`}>
              <div className={`message ${msg.sender}`}>
                {msg.text}
              </div>
              {msg.sources && msg.sources.length > 0 && (
                <div className="sources">
                  <span>Source snippets:</span>
                  {msg.sources.map((src, i) => (
                    <span key={i} className="source-item" title={src}>
                      "{src.substring(0, 60)}..."
                    </span>
                  ))}
                </div>
              )}
            </div>
          ))}
          
          {isLoading && (
            <div className="message-wrapper bot">
              <div className="message bot" style={{ display: 'flex', alignItems: 'center', height: '44px' }}>
                <div className="typing-indicator">
                  <div className="typing-dot"></div>
                  <div className="typing-dot"></div>
                  <div className="typing-dot"></div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="input-area">
          <div className="input-container">
            <input
              type="text"
              className="chat-input"
              placeholder="Ask me about admissions, fees, or deadlines..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyPress}
              disabled={isLoading}
            />
            <button 
              className="send-btn" 
              onClick={() => handleSend()}
              disabled={!input.trim() || isLoading}
            >
              <Send size={18} />
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
