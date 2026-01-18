import React, { useState, useRef, useEffect } from 'react';
import { Send, Zap, Settings, ShoppingBag } from 'lucide-react';
import ThoughtAccordion from './components/ThoughtAccordion';
import ConfidenceMeter from './components/ConfidenceMeter';
import clsx from 'clsx';
import { motion } from 'framer-motion';

function App() {
    const [input, setInput] = useState("");
    const [messages, setMessages] = useState([]); // {role: 'user'|'stylist', content: string}
    const [isThinking, setIsThinking] = useState(false);
    const [debugMode, setDebugMode] = useState(true);

    // Streaming State
    const [currentAnalystThoughts, setCurrentAnalystThoughts] = useState("");
    const [currentKeywords, setCurrentKeywords] = useState([]);
    const [currentRetrievedProducts, setCurrentRetrievedProducts] = useState([]);
    const [streamingContent, setStreamingContent] = useState("");

    const chatEndRef = useRef(null);

    const scrollToBottom = () => {
        chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, streamingContent, currentAnalystThoughts]);

    const handleSendMessage = async (e) => {
        e.preventDefault();
        if (!input.trim() || isThinking) return;

        const userMsg = { role: 'user', content: input };
        setMessages(prev => [...prev, userMsg]);
        setInput("");

        // Reset Stream State
        setIsThinking(true);
        setCurrentAnalystThoughts("");
        setCurrentKeywords([]);
        setCurrentRetrievedProducts([]);
        setStreamingContent("");

        try {
            // Using absolute URL as requested by user prompt for verifying integration
            const response = await fetch('http://localhost:8000/api/v1/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: userMsg.content }),
            });

            if (!response.ok) throw new Error("API Error");

            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            let buffer = "";

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value, { stream: true });
                buffer += chunk;

                const lines = buffer.split('\n');

                // Keep the last partial line in the buffer
                buffer = lines.pop() || "";

                for (const line of lines) {
                    if (!line.trim()) continue;
                    try {
                        const json = JSON.parse(line);

                        if (json.type === 'analyst_thoughts') {
                            setCurrentAnalystThoughts(prev => prev + json.data + "\n");
                        }
                        else if (json.type === 'analyst_keywords') {
                            setCurrentKeywords(json.data);
                        }
                        else if (json.type === 'retrieved_products') {
                            setCurrentRetrievedProducts(json.data);
                        }
                        else if (json.type === 'token') {
                            setStreamingContent(prev => prev + json.data);
                        }
                        else if (json.type === 'error') {
                            setStreamingContent(prev => prev + "\n[Error: " + json.data + "]");
                        }

                    } catch (err) {
                        console.error("Parse error for line:", line, err);
                    }
                }
            }

        } catch (error) {
            console.error("Fetch error", error);
            setStreamingContent("Error connecting to Vibe Matcher AI. Is the backend running?");
        } finally {
            setIsThinking(false);
            setMessages(prev => [...prev, { role: 'stylist', content: streamingContent, products: currentRetrievedProducts }]);
        }
    };

    // Only push final message when done?
    // Let's modify the UI to render `streamingContent` if isThinking is true (or just last message is user).
    // Actually, we can just push a placeholder message and update it?
    // Or simpler: Render messages list, AND if isThinking or (streamingContent !== "" && last message is user), render the "Partial" message.

    return (
        <div className="min-h-screen bg-cyber-dark text-gray-200 font-sans selection:bg-cyber-neon selection:text-black">
            {/* Header */}
            <header className="fixed top-0 w-full z-50 bg-cyber-dark/80 backdrop-blur-md border-b border-white/10">
                <div className="max-w-4xl mx-auto px-4 h-16 flex items-center justify-between">
                    <div className="flex items-center gap-2">
                        <div className="w-8 h-8 rounded bg-gradient-to-tr from-cyber-neon to-cyber-purple flex items-center justify-center">
                            <Zap size={18} className="text-white fill-current" />
                        </div>
                        <h1 className="font-bold tracking-tight text-xl">
                            VIBE<span className="text-cyber-neon">MATCHER</span>
                        </h1>
                    </div>

                    <button
                        onClick={() => setDebugMode(!debugMode)}
                        className={clsx(
                            "flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-mono border transition-all",
                            debugMode ? "border-cyber-neon text-cyber-neon bg-cyber-neon/10" : "border-gray-700 text-gray-500"
                        )}
                    >
                        <Settings size={12} />
                        DEBUG_MODE: {debugMode ? "ON" : "OFF"}
                    </button>
                </div>
            </header>

            {/* Main Content */}
            <main className="pt-24 pb-32 max-w-4xl mx-auto px-4">

                {/* Welcome State */}
                {messages.length === 0 && (
                    <div className="flex flex-col items-center justify-center min-h-[50vh] text-center space-y-6 opacity-60">
                        <ShoppingBag size={64} className="text-cyber-gray" />
                        <h2 className="text-2xl font-light">Describe your vibe. <br /> <span className="text-cyber-neon font-bold">We handle the rest.</span></h2>
                    </div>
                )}

                {/* Chat Stream */}
                <div className="space-y-8">
                    {messages.map((msg, i) => (
                        // Used index as key for simplicity in prototype
                        <div key={i} className={clsx("flex gap-4", msg.role === 'user' ? "flex-row-reverse" : "flex-row")}>

                            {/* Avatar */}
                            <div className={clsx(
                                "w-8 h-8 rounded-full flex-shrink-0 flex items-center justify-center",
                                msg.role === 'user' ? "bg-gray-700" : "bg-cyber-purple"
                            )}>
                                {msg.role === 'user' ? "U" : "S"}
                            </div>

                            {/* Bubble */}
                            <div className={clsx(
                                "max-w-[80%] rounded-2xl p-4 shadow-lg",
                                msg.role === 'user' ? "bg-gray-800 text-white rounded-tr-none" : "bg-white/5 border border-white/10 rounded-tl-none"
                            )}>
                                {msg.content.split('\n').map((line, j) => <p key={j} className="mb-1 last:mb-0">{line}</p>)}

                                {/* Product Cards in History */}
                                {msg.role === 'stylist' && msg.products && msg.products.length > 0 && (
                                    <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-3">
                                        {msg.products.map(p => (
                                            <div key={p.id} className="bg-black/40 rounded border border-white/10 p-3 flex gap-3 hover:border-cyber-neon/50 transition-colors group">
                                                {/* Placeholder Image */}
                                                <div className="w-16 h-16 bg-gray-800 rounded flex-shrink-0" />
                                                <div className="min-w-0">
                                                    <h4 className="font-bold text-sm truncate text-cyber-neon group-hover:text-white transition-colors">{p.metadata.name}</h4>
                                                    <p className="text-xs text-gray-400 line-clamp-2 mt-1">{p.metadata.desc}</p>
                                                    {/* We can calculate score from p.score (distance) -> similarity */}
                                                    {/* Mocking generic high score for demo if proper conversion missing */}
                                                    <div className="mt-2 flex items-center gap-2">
                                                        <div className="h-1 w-16 bg-gray-800 rounded-full overflow-hidden">
                                                            <div className="h-full bg-cyber-pink w-[80%]" />
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>
                        </div>
                    ))}

                    {/* Active Streaming Message */}
                    {isThinking && (
                        <div className="flex gap-4 animate-in fade-in slide-in-from-bottom-2 duration-300">
                            <div className="w-8 h-8 rounded-full flex-shrink-0 flex items-center justify-center bg-cyber-purple animate-pulse">S</div>
                            <div className="flex-1 space-y-4 max-w-[80%]">

                                {/* Debug Accordion */}
                                {debugMode && (
                                    <ThoughtAccordion
                                        logs={currentAnalystThoughts}
                                        extractedKeywords={currentKeywords}
                                        isThinking={true}
                                    />
                                )}

                                {/* Streaming Text */}
                                {streamingContent && (
                                    <div className="bg-white/5 border border-white/10 rounded-2xl rounded-tl-none p-4 shadow-lg">
                                        <p className="whitespace-pre-wrap border-l-2 border-cyber-neon pl-3">
                                            {streamingContent}
                                            <span className="inline-block w-2 h-4 bg-cyber-neon ml-1 animate-pulse" />
                                        </p>
                                    </div>
                                )}

                                {/* Live Products */}
                                {currentRetrievedProducts.length > 0 && !streamingContent && (
                                    <div className="flex gap-2 p-2 bg-cyber-neon/10 border border-cyber-neon/20 rounded text-xs text-cyber-neon">
                                        <ShoppingBag size={14} />
                                        <span>Found {currentRetrievedProducts.length} potential matches...</span>
                                    </div>
                                )}
                            </div>
                        </div>
                    )}

                    <div ref={chatEndRef} />
                </div>

            </main>

            {/* Input Area */}
            <footer className="fixed bottom-0 w-full bg-cyber-dark border-t border-white/10 p-4 pb-8 z-40">
                <form onSubmit={handleSendMessage} className="max-w-4xl mx-auto relative group">
                    <div className="absolute inset-0 bg-gradient-to-r from-cyber-neon to-cyber-pink opacity-20 blur-lg rounded-full group-hover:opacity-30 transition-opacity" />
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        disabled={isThinking}
                        placeholder="Ex: I want to look like a cyberpunk ninja..."
                        className="w-full bg-black/80 border border-white/20 rounded-full py-4 px-6 pr-12 text-white placeholder:text-gray-600 focus:outline-none focus:border-cyber-neon transition-colors relative z-10"
                    />
                    <button
                        type="submit"
                        disabled={!input || isThinking}
                        className="absolute right-2 top-2 p-2 bg-cyber-neon text-black rounded-full hover:bg-white transition-colors disabled:opacity-50 disabled:hover:bg-cyber-neon z-20"
                    >
                        <Send size={20} />
                    </button>
                </form>
            </footer>
        </div>
    );
}

export default App;
