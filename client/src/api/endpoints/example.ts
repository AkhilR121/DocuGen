import { apiClient } from '../client'

export const exampleApi = {
  getAll: async () => {
    const response = await apiClient.get('/api/v1/example')
    return response.data
  },

  getById: async (id: string) => {
    const response = await apiClient.get(`/api/v1/example/${id}`)
    return response.data
  },

  create: async (data: unknown) => {
    const response = await apiClient.post('/api/v1/example', data)
    return response.data
  },

  update: async (id: string, data: unknown) => {
    const response = await apiClient.put(`/api/v1/example/${id}`, data)
    return response.data
  },

  delete: async (id: string) => {
    const response = await apiClient.delete(`/api/v1/example/${id}`)
    return response.data
  },
}
