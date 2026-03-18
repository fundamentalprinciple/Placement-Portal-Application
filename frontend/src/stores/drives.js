import { defineStore } from 'pinia'
import { useAuthStore } from '@/stores/auth'

export const useDriveStore = defineStore('drive', {
  state: () => ({
    drives: []
  }),
  actions: {

    async fetchDrivesByCompany() {
      const auth = useAuthStore()
      try {
        const response = await fetch("http://localhost:3000/api/create-drive", {
          method: 'GET',
          headers: {
            'Authentication-Token': auth.token
          }
        })
        if (!response.ok) throw new Error('Failed to fetch drives')
        this.drives = await response.json()
      } catch (err) {
        this.error = err.message || 'Error fetching drives'
      }
    },

    async fetchAllDrives() {
      const auth = useAuthStore()
      try {
        const response = await fetch("http://localhost:3000/api/manage-drives", {
          method: 'GET',
          headers: {
            'Authentication-Token': auth.token
          }
        })
        if (!response.ok) throw new Error('Failed to fetch drives')
        this.drives = await response.json()
      } catch (err) {
        this.error = err.message || 'Error fetching drives'
      }
    },

    async createDrive(driveData) {
      const auth = useAuthStore()
      try {
        const response = await fetch('http://localhost:3000/api/create-drive', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': auth.token
          },
          body: JSON.stringify(driveData)
        })
        if (!response.ok) throw new Error('Failed to create drive')
      } catch (err) {
        this.error = err.message || 'Error creating drive'
      } 
    },

    async changeDriveStatus(driveId, newStatus) {
      const auth = useAuthStore()
      try {
        const response = await fetch('http://localhost:3000/api/manage-drives', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': auth.token
          },
          body: JSON.stringify({
            id: driveId,
            new_status: newStatus
          })
        })
        if (!response.ok) throw new Error('Failed to change drive status')
      } catch (err) {
        this.error = err.message || 'Error changing drive status'
      }
    },

    async deleteDrive(driveId) {
      const auth = useAuthStore()
      try {
        const response = await fetch('http://localhost:3000/api/create-drive', {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': auth.token
          },
          body: JSON.stringify({ id: driveId })
        })
        if (!response.ok) throw new Error('Failed to delete drive')
      } catch (err) {
        this.error = err.message || 'Error deleting drive'
      } finally {
        this.loading = false
      }
    }
}})
