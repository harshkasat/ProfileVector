'use client'

import { useState, useEffect, useRef } from 'react'
import { Terminal } from 'lucide-react'

function formatText(text: string) {
  // Replace **bold** with <strong>bold</strong>
  text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
  
  // Replace URLs with clickable links
  text = text.replace(
    /(https?:\/\/[^\s]+)/g,
    '<a href="$1" target="_blank" rel="noopener noreferrer" class="text-blue-400 hover:underline">$1</a>'
  )
  
  return text
}

export default function Component() {
  const [messages, setMessages] = useState<string[]>([
    "Welcome to the Zedmate Terminal Chat. How can I assist you today?"
  ])
  const [input, setInput] = useState('')
  const [socket, setSocket] = useState<WebSocket | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    // Initialize WebSocket connection
    const ws = new WebSocket('wss://profilevector.onrender.com/ws/questions')
    // const ws = new WebSocket('ws://127.0.0.1:8000/ws/questions/stream')
    
    ws.onopen = () => {
      console.log('Connected to the server')
    }
    
    ws.onmessage = (event) => {
      setMessages(prev => {
        const newMessages = [...prev]
        const lastMessage = newMessages[newMessages.length - 1]
        if (lastMessage.startsWith('🤖 ')) {
          // Remove any newline characters and append the new chunk
          newMessages[newMessages.length - 1] = lastMessage + event.data.replace(/\n/g, ' ')
        } else {
          newMessages.push('🤖 ' + event.data.replace(/\n/g, ' '))
        }
        return newMessages
      })
    }
    
    ws.onerror = (error) => {
      console.error('WebSocket error:', error)
    }
    
    ws.onclose = () => {
      console.log('Disconnected from the server')
    }
    
    setSocket(ws)

    return () => {
      ws.close()
    }
  }, [])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (input.trim() && socket) {
      socket.send(input)
      setMessages(prev => [...prev, `> ${input}`])
      setInput('')
    }
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-900">
      <div className="w-full max-w-2xl bg-gray-800 rounded-lg shadow-lg overflow-hidden">
        <div className="flex items-center px-4 py-3 bg-gray-700">
          <div className="flex space-x-2">
            <div className="w-3 h-3 bg-red-500 rounded-full"></div>
            <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
            <div className="w-3 h-3 bg-green-500 rounded-full"></div>
          </div>
          <div className="ml-4 text-white font-semibold">Zedmate Terminal Chat</div>
        </div>
        <div className="h-96 overflow-y-auto p-4 space-y-2">
          {messages.map((msg, index) => (
            <div 
              key={index} 
              className={`text-sm ${msg.startsWith('>') ? 'text-blue-400' : 'text-green-400'}`}
              dangerouslySetInnerHTML={{ __html: formatText(msg) }}
            />
          ))}
          <div ref={messagesEndRef} />
        </div>
        <form onSubmit={handleSubmit} className="flex items-center p-4 bg-gray-700">
          <Terminal className="text-gray-400 mr-2" />
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            className="flex-grow bg-transparent text-white placeholder-gray-500 outline-none"
          />
          <button type="submit" className="ml-2 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors">
            Send
          </button>
        </form>
      </div>
    </div>
  )
}