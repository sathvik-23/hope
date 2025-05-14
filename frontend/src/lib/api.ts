const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export interface AudioResponse {
  audioPath: string
  text: string
}

export const processAudio = async (audioFile: File): Promise<AudioResponse> => {
  const formData = new FormData()
  formData.append('audio', audioFile)

  const response = await fetch(`${API_BASE_URL}/process-audio`, {
    method: 'POST',
    body: formData,
  })

  if (!response.ok) {
    throw new Error('Failed to process audio')
  }

  return response.json()
}

export const listModels = async (): Promise<string[]> => {
  const response = await fetch(`${API_BASE_URL}/list-models`)

  if (!response.ok) {
    throw new Error('Failed to fetch models')
  }

  return response.json()
}
