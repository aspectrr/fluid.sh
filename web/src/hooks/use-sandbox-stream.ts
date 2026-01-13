import { useState, useEffect, useRef } from 'react'

interface StreamCommand {
  command_id: string
  command: string
  stdout?: string
  stderr?: string
  exit_code?: number
  started_at?: string
  ended_at?: string
}

interface ConnectionData {
  ip_address?: string
  state?: string
}

interface UseSandboxStreamReturn {
  isConnected: boolean
  commands: StreamCommand[]
  connectionData: ConnectionData | null
  error: Error | null
}

export function useSandboxStream(sandboxId: string): UseSandboxStreamReturn {
  const [isConnected, setIsConnected] = useState(false)
  const [commands, setCommands] = useState<StreamCommand[]>([])
  const [connectionData, setConnectionData] = useState<ConnectionData | null>(null)
  const [error, setError] = useState<Error | null>(null)
  const wsRef = useRef<WebSocket | null>(null)

  useEffect(() => {
    if (!sandboxId) return

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const wsUrl = `${protocol}//${window.location.host}/v1/sandboxes/${sandboxId}/stream`

    let ws: WebSocket
    try {
      ws = new WebSocket(wsUrl)
      wsRef.current = ws
    } catch (e) {
      setTimeout(() => setError(e as Error), 0)
      return
    }

    ws.onopen = () => {
      setIsConnected(true)
      setError(null)
    }

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)

        if (data.type === 'command') {
          setCommands((prev) => {
            const existing = prev.findIndex((c) => c.command_id === data.command_id)
            if (existing >= 0) {
              const updated = [...prev]
              updated[existing] = { ...updated[existing], ...data }
              return updated
            }
            return [...prev, data]
          })
        } else if (data.type === 'connection') {
          setConnectionData(data)
        }
      } catch (e) {
        console.error('Failed to parse WebSocket message:', e)
      }
    }

    ws.onclose = () => {
      setIsConnected(false)
    }

    ws.onerror = () => {
      setError(new Error('WebSocket connection error'))
      setIsConnected(false)
    }

    return () => {
      if (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING) {
        ws.close()
      }
    }
  }, [sandboxId])

  return {
    isConnected,
    commands,
    connectionData,
    error,
  }
}
