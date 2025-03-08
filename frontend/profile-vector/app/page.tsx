'use client';

import { useState, useRef, useEffect } from 'react';

export default function Home() {
  const [history, setHistory] = useState<string[]>([
    'Welcome to Zed Terminal UI v1.0.0',
    'Type "help" for available commands',
    'Any other input will be sent as a query to the server',
    '',
  ]);
  const [currentInput, setCurrentInput] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [socket, setSocket] = useState<WebSocket | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  // Set up WebSocket connection
  useEffect(() => {
    console.log("Initialize the websocket")
    
    // const ws = new WebSocket('ws://127.0.0.1:8000/ws/questions/stream');
    const ws = new WebSocket('wss://profilevector.onrender.com//ws/questions/stream')

    ws.onopen = () => {
      console.log('Connected to WebSocket server');
      setHistory(prev => [...prev, 'Connected to WebSocket server', '']);
    };

    ws.onmessage = (event) => {
      setIsLoading(false); // Hide loading indicator
      setHistory(prev => {
        const newHistory = [...prev];
        const loadingIndex = newHistory.findIndex(msg => msg.startsWith('🔄 Loading'));
        if (loadingIndex !== -1) {
      // Replace loading with actual response
      newHistory[loadingIndex] = '> ' + event.data;
    } else {
      // Check if the last message is from the bot to append to it (for streaming)
      const lastIndex = newHistory.length - 1;
      if (lastIndex >= 0 && newHistory[lastIndex].startsWith('> ')) {
        // Append to existing bot message
        newHistory[lastIndex] = newHistory[lastIndex] + event.data;
      } else {
        // Create a new bot message if no loading or existing bot message
        newHistory.push('> ' + event.data);
      }
    }
        return newHistory;
      });
    };
    
    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      setIsLoading(false); // Hide loading indicator on error
      setHistory(prev => [...prev, 'Error: WebSocket connection failed', '']);
    };
    
    ws.onclose = () => {
      console.log('Disconnected from the server');
      setIsLoading(false); // Hide loading indicator on error
      setHistory(prev => [...prev, 'Disconnected from WebSocket server', '']);
    };
    
    setSocket(ws);

    return () => {
      if (ws.readyState === 1) { 
        ws.close();
    }
    };
  }, []);

  const commands = {
    help: () => [
      'Available commands:',
      '  clear    - Clear the terminal',
      '  echo     - Echo back your input',
      '  date     - Show current date and time',
      '  help     - Show this help message',
    ],
    clear: () => [],
    date: () => [new Date().toLocaleString()],
    echo: (args: string) => [args],
  };

  const sendToServer = (message: string) => {
    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.send(message);
      return 
    } else {
      return ['Error: WebSocket not connected'];
    }
  };

  const handleCommand = (input: string) => {
    const [cmd, ...args] = input.trim().split(' ');
    const argsStr = args.join(' ');
  
    if (cmd in commands) {
      return commands[cmd as keyof typeof commands](argsStr);
    } else {
      // Send to server but don't return anything - the response will come through the WebSocket
      // setIsLoading(true);
      sendToServer(input);
      return ['🔄 Loading...']; // Return loading message
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!currentInput.trim()) return;

    const newHistory = [
      ...history,
      `$ ${currentInput}`,
      ...handleCommand(currentInput),
      '',
    ];

    setHistory(currentInput.trim() === 'clear' ? [] : newHistory);
    setCurrentInput('');
  };

  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }
  }, [history]);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  return (
    <main 
      className="min-h-screen p-4 font-mono text-sm bg-black text-green-400"
      onClick={() => inputRef.current?.focus()}
      >
      <div 
        ref={containerRef}
        className="max-h-screen overflow-auto"
      >
        {history.map((line, i) => (
          <div key={i} className={`whitespace-pre-wrap mb-1 ${line.startsWith('🔄 Loading') ? 'text-yellow-300 animate-pulse' : ''}`}>
            {line}
          </div>
        ))}
        <form onSubmit={handleSubmit} className="flex">
          <span>$&nbsp;</span>
          <input
            ref={inputRef}
            type="text"
            value={currentInput}
            onChange={(e) => setCurrentInput(e.target.value)}
            className="flex-1 bg-transparent outline-none"
            autoFocus
            spellCheck="false"
            disabled={isLoading} // Optionally disable input while loading
          />
        </form>
      </div>
    </main>
  );
}
