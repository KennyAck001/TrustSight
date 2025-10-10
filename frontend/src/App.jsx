import { useState, useRef, useEffect } from 'react';
import './Index.css';
import logo from './assets/logo.png';


const Index = () => {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isDark, setIsDark] = useState(() => {
    const saved = localStorage.getItem('theme');
    return saved === 'dark' || (!saved && window.matchMedia('(prefers-color-scheme: dark)').matches);
  });
  const messagesEndRef = useRef(null);

  useEffect(() => {
    document.body.classList.toggle('dark', isDark);
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
  }, [isDark]);

  const toggleTheme = () => {
    setIsDark(prev => !prev);
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e, followUpQuery) => {
    e?.preventDefault();
    const q = followUpQuery || query;
    if (!q.trim()) return;

    // Add user message
    const userMessage = { type: 'user', content: q };
    setMessages(prev => [...prev, userMessage]);
    setQuery('');
    setLoading(true);

    try {
      const res = await fetch('http://localhost:8000/research', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: q }),
      });
      const data = await res.json();
      
      // Add assistant response
      const assistantMessage = {
        type: 'assistant',
        content: 'Here are the research results:',
        data: data
      };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage = {
        type: 'assistant',
        content: 'Error fetching data.',
        data: { error: 'Error fetching data.' }
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const renderResponseContent = (data) => {
    if (data.error) {
      return (
        <div className="error-card">
          <p>{data.error}</p>
        </div>
      );
    }

    return (
      <div className="response-content">
        {data.points && (
          <div className="card points-card">
            <div className="card-header">
              <svg className="icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z"/>
              </svg>
              <h3>Key Points</h3>
            </div>
            <ul className="points-list">
              {Object.values(data.points).map((point, idx) => (
                <li key={idx}>
                  <span className="bullet">•</span>
                  <span>{point.text}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {data.table && data.table.length > 0 && (
          <div className="card table-card">
            <div className="card-header">
              <svg className="icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
              </svg>
              <h3>Data Table</h3>
            </div>
            <div className="table-wrapper">
              <table>
                <thead>
                  <tr>
                    {Object.keys(data.table[0] || {}).map(key => (
                      <th key={key}>{key}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {data.table.map((row, i) => (
                    <tr key={i}>
                      {Object.values(row).map((val, j) => (
                        <td key={j}>
                          {typeof val === 'object' ? JSON.stringify(val) : String(val)}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {data.graph && data.graph.image_base64 && (
          <div className="card graph-card">
            <h3>Visualization</h3>
            <p className="graph-explanation">{data.graph.explanation}</p>
            <div className="graph-container">
              <img 
                src={`data:image/png;base64,${data.graph.image_base64}`} 
                alt="Graph"
              />
            </div>
          </div>
        )}

        {data.related_insights && (
          <div className="card insights-card">
            <h3>Related Insights</h3>
            <ul className="insights-list">
              {Object.values(data.related_insights).map((insight, idx) => (
                <li key={idx}>
                  <span className="arrow">→</span>
                  <span>{insight.text}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {data.follow_up_suggestions && data.follow_up_suggestions.length > 0 && (
          <div className="card suggestions-card">
            <h3>Follow-up Questions</h3>
            <div className="suggestions-buttons">
              {data.follow_up_suggestions.map((suggestion, index) => (
                <button
                  key={index}
                  onClick={() => handleSubmit(undefined, suggestion)}
                  disabled={loading}
                  className="suggestion-btn"
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="chat-container">
      {/* Header */}
      <header className="chat-header">
        <div className="header-content">
          <div className="logo-container">
            <div className="logo-icon">
              <img width="50" height="50" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" src={logo}>
              </img>
            </div>
            <div>
              <h1>TrustSight</h1>
              <p className="subtitle">Powered by Impact Innovators</p>
            </div>
          </div>
          <button onClick={toggleTheme} className="theme-toggle" aria-label="Toggle theme">
            {isDark ? (
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="5"/>
                <line x1="12" y1="1" x2="12" y2="3"/>
                <line x1="12" y1="21" x2="12" y2="23"/>
                <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
                <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
                <line x1="1" y1="12" x2="3" y2="12"/>
                <line x1="21" y1="12" x2="23" y2="12"/>
                <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
                <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
              </svg>
            ) : (
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
              </svg>
            )}
          </button>
        </div>
      </header>

      {/* Messages Area */}
      <div className="messages-area">
        <div className="messages-content">
          {messages.length === 0 ? (
            <div className="welcome-screen">
              <div className="welcome-icon">
                <img width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" src={logo}>
                </img>
              </div>
              <div className="welcome-text">
                <h2>Welcome to AI Research</h2>
                <p>Ask me anything! I can provide insights, create tables, generate graphs, and more.</p>
              </div>
              <div className="example-prompts">
                <div 
                  className="example-card example-1" 
                  onClick={() => setQuery('What are the benefits of renewable energy?')}
                >
                  <p>What are the benefits of renewable energy?</p>
                </div>
                <div 
                  className="example-card example-2" 
                  onClick={() => setQuery('Compare programming languages in a table')}
                >
                  <p>Compare programming languages in a table</p>
                </div>
              </div>
            </div>
          ) : (
            <div className="messages-list">
              {messages.map((message, idx) => (
                <div
                  key={idx}
                  className={`message ${message.type === 'user' ? 'user-message' : 'assistant-message'}`}
                >
                  {message.type === 'assistant' && (
                    <div className="message-avatar">
                      <img width="25" height="25" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" src={logo}>
                </img>
                    </div>
                  )}
                  <div className="message-content-wrapper">
                    {message.type === 'user' ? (
                      <div className="user-bubble">
                        <p>{message.content}</p>
                      </div>
                    ) : (
                      <div className="assistant-content">
                        {message.data && renderResponseContent(message.data)}
                      </div>
                    )}
                  </div>
                </div>
              ))}
              {loading && (
                <div className="message assistant-message">
                  <div className="message-avatar loading-avatar">
                   <img width="50" height="50" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" src={logo}>
                </img>
                  </div>
                  <div className="loading-card">
                    <div className="loading-dots">
                      <div className="dot"></div>
                      <div className="dot"></div>
                      <div className="dot"></div>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>
      </div>

      {/* Input Area */}
      <div className="input-area">
        <div className="input-content">
          <form onSubmit={handleSubmit} className="input-form">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask anything... (e.g., 'What are the benefits of renewable energy?')"
              disabled={loading}
              className="message-input"
            />
            <button
              type="submit"
              disabled={loading || !query.trim()}
              className="send-button"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="22" y1="2" x2="11" y2="13"/>
                <polygon points="22 2 15 22 11 13 2 9 22 2"/>
              </svg>
            </button>
          </form>
          <p className="disclaimer">
            TrustSight can make mistakes. Verify important information.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Index;
