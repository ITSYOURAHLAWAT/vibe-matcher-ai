import React, { useState, useEffect } from 'react';
import { ChevronDown, ChevronRight, BrainCircuit, Terminal } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const ThoughtAccordion = ({ logs, extractedKeywords, isThinking }) => {
    const [isOpen, setIsOpen] = useState(true);

    // Auto-expand if thinking
    useEffect(() => {
        if (isThinking) setIsOpen(true);
    }, [isThinking]);

    return (
        <div className="w-full border border-cyber-gray bg-black/40 rounded-lg overflow-hidden mb-4 backdrop-blur-sm">
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="w-full flex items-center justify-between p-3 bg-cyber-gray/50 hover:bg-cyber-gray transition-colors text-xs uppercase tracking-wider font-mono text-gray-400"
            >
                <div className="flex items-center gap-2">
                    <BrainCircuit size={14} className={isThinking ? "text-cyber-neon animate-pulse" : "text-gray-500"} />
                    <span>Vibe Analyst Process</span>
                </div>
                {isOpen ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
            </button>

            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: "auto", opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        transition={{ duration: 0.2 }}
                        className="border-t border-cyber-gray"
                    >
                        <div className="p-4 space-y-3 font-mono text-xs">

                            {/* Keywords Section */}
                            {extractedKeywords.length > 0 && (
                                <div className="flex flex-wrap gap-2">
                                    <span className="text-gray-500">Keywords:</span>
                                    {extractedKeywords.map((k, i) => (
                                        <span key={i} className="px-2 py-0.5 rounded bg-cyber-purple/20 text-cyber-purple border border-cyber-purple/30">
                                            {k}
                                        </span>
                                    ))}
                                </div>
                            )}

                            {/* Console Logs */}
                            <div className="bg-black/80 rounded p-3 h-32 overflow-y-auto code-scroll text-green-400/90 whitespace-pre-wrap">
                                <div className="flex items-center gap-2 text-gray-600 mb-2 pb-2 border-b border-gray-800">
                                    <Terminal size={10} />
                                    <span>SYSTEM_LOGS</span>
                                </div>
                                {logs || <span className="text-gray-600 italic">Waiting for signal...</span>}
                            </div>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};

export default ThoughtAccordion;
