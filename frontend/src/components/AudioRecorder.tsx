'use client'
import { useState, useRef } from 'react'
import { processAudio } from '@/lib/api'

export default function AudioRecorder() {
  const [isRecording, setIsRecording] = useState(false)
  const [audioUrl, setAudioUrl] = useState<string | null>(null)
  const [response, setResponse] = useState<string | null>(null)
  const [isProcessing, setIsProcessing] = useState(false)
  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const chunksRef = useRef<Blob[]>([])

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      const mediaRecorder = new MediaRecorder(stream)
      mediaRecorderRef.current = mediaRecorder
      chunksRef.current = []

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunksRef.current.push(e.data)
        }
      }

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(chunksRef.current, { type: 'audio/wav' })
        const audioUrl = URL.createObjectURL(audioBlob)
        setAudioUrl(audioUrl)
      }

      mediaRecorder.start()
      setIsRecording(true)
    } catch (error) {
      console.error('Error accessing microphone:', error)
    }
  }

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop()
      setIsRecording(false)
    }
  }

  const handleProcessAudio = async () => {
    if (!audioUrl) return

    try {
      setIsProcessing(true)
      const response = await fetch(audioUrl)
      const blob = await response.blob()
      const file = new File([blob], 'recording.wav', { type: 'audio/wav' })

      const result = await processAudio(file)
      setResponse(result.text)
    } catch (error) {
      console.error('Error processing audio:', error)
    } finally {
      setIsProcessing(false)
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex space-x-4">
        <button
          onClick={isRecording ? stopRecording : startRecording}
          className={`px-4 py-2 rounded-lg ${
            isRecording
              ? 'bg-red-500 hover:bg-red-600'
              : 'bg-blue-500 hover:bg-blue-600'
          } text-white transition-colors`}
        >
          {isRecording ? 'Stop Recording' : 'Start Recording'}
        </button>

        {audioUrl && (
          <button
            onClick={handleProcessAudio}
            disabled={isProcessing}
            className="px-4 py-2 rounded-lg bg-green-500 hover:bg-green-600 text-white transition-colors disabled:opacity-50"
          >
            {isProcessing ? 'Processing...' : 'Process Audio'}
          </button>
        )}
      </div>

      {audioUrl && (
        <div className="space-y-2">
          <h3 className="text-lg font-semibold">Recording:</h3>
          <audio src={audioUrl} controls className="w-full" />
        </div>
      )}

      {response && (
        <div className="space-y-2">
          <h3 className="text-lg font-semibold">Response:</h3>
          <p className="p-4 bg-gray-100 rounded-lg">{response}</p>
        </div>
      )}
    </div>
  )
}
