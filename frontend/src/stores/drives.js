import { defineStore } from 'pinia'
import { useAuthStore } from '@/stores/auth'

export const useDriveStore = defineStore('drive', {
  state: () => ({
    drives: [],
    applications: [],
    interviews: [],
    studentInterviews: [],
    error: "",
    loading: false
  }),
  actions: {

    async fetchCompanyInterviews() {
      const auth = useAuthStore()
      try {
        const response = await fetch('http://localhost:3000/api/schedule-interview', {
          method: 'GET',
          headers: {
            'Authentication-Token': auth.token
          }
        })
        if (!response.ok) throw new Error('Failed to fetch interviews')
        this.interviews = await response.json()
      } catch (err) {
        this.error = err.message || 'Error fetching interviews'
      }
    },

    async cancelCompanyInterview(interview_id) {
      const auth = useAuthStore()
      try {
        const response = await fetch('http://localhost:3000/api/schedule-interview', {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': auth.token
          },
          body: JSON.stringify({ interview_id })
        })
        if (!response.ok) throw new Error('Failed to cancel interview')
      } catch (err) {
        this.error = err.message || 'Error cancelling interview'
      }
    },

    async completeCompanyInterview(interview_id) {
      const auth = useAuthStore()
      try {
        const response = await fetch('http://localhost:3000/api/schedule-interview', {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': auth.token
          },
          body: JSON.stringify({ interview_id, completed: true })
        })
        if (!response.ok) throw new Error('Failed to complete interview')
      } catch (err) {
        this.error = err.message || 'Error completing interview'
      }
    },

    async fetchStudentInterviews() {
      const auth = useAuthStore()
      try {
        const response = await fetch('http://localhost:3000/api/manage-interview-request', {
          method: 'GET',
          headers: {
            'Authentication-Token': auth.token
          }
        })
        if (!response.ok) throw new Error('Failed to fetch student interviews')
        this.studentInterviews = await response.json()
      } catch (err) {
        this.error = err.message || 'Error fetching student interviews'
      }
    },

    async respondInterview(interview_id, accept) {
      const auth = useAuthStore()
      try {
        const response = await fetch('http://localhost:3000/api/manage-interview-request', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': auth.token
          },
          body: JSON.stringify({ interview_id, accept })
        })
        if (!response.ok) throw new Error('Failed to respond to interview')
      } catch (err) {
        this.error = err.message || 'Error responding to interview'
      }
    },

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
    },

    async applyDrive(driveId) {
      const auth = useAuthStore()
      try {
        const response = await fetch('http://localhost:3000/api/apply-placement-drive', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': auth.token
          },
          body: JSON.stringify({
            drive_id: driveId,
          })
        })
        if (!response.ok) throw new Error('Failed.')
      } catch (err) {
        this.error = err.message || 'Error applying for drive.'
      }
        
    },

    async deleteApplication(app_id) {
        const auth = useAuthStore()
        try {
            const response = await fetch('http://localhost:3000/api/apply-placement-drive', {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': auth.token
                },
                body: JSON.stringify({
                    app_id: app_id,
                })
            })
            if (!response.ok) throw new Error('Failed to change delete application.')
        } catch (err) {
            this.error = err.message || 'Error'
        }
    },
    
    async fetchAppliedDrives() {
      const auth = useAuthStore()
      try {
        const response = await fetch("http://localhost:3000/api/apply-placement-drive", {
          method: 'GET',
          headers: {
            'Authentication-Token': auth.token
          }
        })
        if (!response.ok) throw new Error('Failed to fetch drives')
        this.applications = await response.json()
      } catch (err) {
        this.error = err.message || 'Error fetching drives'
      }        
    },

    async fetchApplicationsByCompany() {
        const auth = useAuthStore()
        try {
            this.loading = true;
            const response = await fetch("http://localhost:3000/api/manage-applications", {
                method: 'GET',
                headers: {
                    'Authentication-Token': auth.token
                }
            })
            if (!response.ok) throw new Error('Failed to fetch applications.')
            this.applications = await response.json()
            this.loading = false;
        } catch (err) {
            this.error = err.message || 'Error fetching drives'
        }
    },

    async updateApplicationStatus(app_id,new_status) {
      const auth = useAuthStore()
      try {
        const response = await fetch('http://localhost:3000/api/manage-applications', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': auth.token
          },
          body: JSON.stringify({
            application_id: app_id,
            new_status: new_status
          })
        })
        if (!response.ok) throw new Error('Failed to change application status')
      } catch (err) {
        this.error = err.message || 'Error changing application status'
      }
        
    }

}})







