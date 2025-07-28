import { defineStore } from 'pinia'
import type { Job } from '../types/Job'
import { useAuthStore } from './authStore'
import type { User } from '@/types/User'
import { useToast } from '@/components/ui/toast/use-toast'
import { h } from 'vue'
import ToastHeartFillUp from '@/animations/ToastHeartFillUp.vue'
import { showNetworkErrorToast } from '@/utils/toastUtils'

const { toast } = useToast()

const API_URL = import.meta.env.VITE_API_URL

export const useJobStore = defineStore('jobStore', {
  state: () => ({
    jobs: [] as Job[],
    isLoading: false,
    hasMore: true,
    offset: 0,
    limit: 20,
    searchQuery: '',
  }),
  getters: {
    isJobAlreadyLiked: (state) => (jobId: string) => {
      return state.jobs.some((job) => job.id === jobId && job.liked)
    },
    isJobAlreadySeen: (state) => (jobId: string) => {
      return state.jobs.some((job) => job.id === jobId && job.seen)
    },
    currentUser: (): User | null => useAuthStore().currentUser,
    getJobById: (state) => (id: string) => state.jobs.find((job) => job.id === id),
    likedJobs: (state) => state.jobs.filter((job) => job.liked),
    seenJobs: (state) => state.jobs.filter((job) => job.seen),
    appliedJobs: (state) => state.jobs.filter((job) => job.seen && job.applicationSent),
    displayedJobs: (state) => {
      if (!state.searchQuery) {
        return state.jobs
      }
      const lowerQuery = state.searchQuery.toLowerCase() ?? ''
      return state.jobs.filter(
        (job) =>
          (job.title && job.title.toLowerCase().includes(lowerQuery)) ||
          (job.company && job.company.toLowerCase().includes(lowerQuery)) ||
          (job.location && job.location.toLowerCase().includes(lowerQuery)),
      )
    },
  },
  actions: {
    setSearchQuery(query: string) {
      this.searchQuery = query
    },
    async toggleLikeWithFeedback(jobId: string) {
      const job = this.getJobById(jobId)
      if (!job) return

      const isAlreadyLiked = job.liked

      const result = await this.toggleLikeJob(jobId, isAlreadyLiked)

      if (result) {
        toast({
          title: isAlreadyLiked ? 'Job retiré !' : 'Job liké !',
          description: isAlreadyLiked
            ? `Le job ${job.title} a été retiré de vos favoris.`
            : h('div', { class: 'flex items-center space-x-2' }, [
                h('span', 'Le job a été ajouté à vos favoris !'),
                h(ToastHeartFillUp, {}),
              ]),
          class: isAlreadyLiked ? 'bg-gray-300 text-orange-700' : 'bg-gray-100 text-green-700',
        })
      }
    },
    async fetchJobs(offset: number = 0, limit: number = 20) {
      this.isLoading = true
      try {
        const res = await fetch(`${API_URL}/api/jobs?offset=${offset}&limit=${limit}`)

        if (!res.ok) {
          const errorText = await res.text()
          console.error(`HTTP error! status: ${res.status}, body: ${errorText}`)
          return
        }

        const data: Job[] = await res.json()

        const jobsWithInitialStatus = data.map((job) => ({
          ...job,
          liked: false,
          seen: false,
          applicationSent: false,
        }))

        this.jobs = offset === 0 ? jobsWithInitialStatus : [...this.jobs, ...jobsWithInitialStatus]

        await this.fetchLikedJobs()
        await this.fetchSeenJobs()

        if (data.length < limit) this.hasMore = false
      } catch (error) {
        console.error('Failed to fetch jobs:', error)
      } finally {
        this.isLoading = false
      }
    },
    async _fetchUserJobStatus(endpoint: string): Promise<Job[]> {
      if (!this.currentUser?.id) {
        console.error(`User ID missing — impossible to fetch jobs status for ${endpoint}.`)
        return []
      }
      try {
        const response = await fetch(`${API_URL}/api/jobs/${endpoint}/${this.currentUser.id}`)
        if (!response.ok) {
          const errorText = await response.text()
          console.error(
            `Erreur HTTP pour ${endpoint}! statut: ${response.status}, corps: ${errorText}`,
          )
          return []
        }
        return await response.json()
      } catch (error) {
        console.error(`Échec de la récupération de ${endpoint} en interne:`, error)
        return []
      }
    },
    async fetchJobById(id: string) {
      try {
        const res = await fetch(`${API_URL}/api/jobs/${id}`)

        if (!res.ok) {
          const errorText = await res.text()
          console.error(`HTTP error! status: ${res.status}, body: ${errorText}`)
          return
        }

        const data: Job = await res.json()

        const jobFromApi: Job = { ...data, liked: false, seen: false, applicationSent: false }

        if (this.currentUser?.id) {
          const likedJobsForUser = await this._fetchUserJobStatus('liked-jobs')
          jobFromApi.liked = likedJobsForUser.some((likedJob) => likedJob.id === data.id)

          const seenJobsForUser = await this._fetchUserJobStatus('seen-jobs')
          jobFromApi.seen = seenJobsForUser.some((seenJob) => seenJob.id === data.id)
        }
        return jobFromApi
      } catch (error) {
        console.error('Failed to fetch job id:', error)
        return null
      }
    },
    async likeJob(jobId: string) {
      const jobIdStr = jobId.toString()
      const job = this.jobs.find((j) => j.id === jobIdStr)
      if (!job) return false
      if (this.isJobAlreadyLiked(jobId)) {
        console.log(`Job ${jobIdStr} is already liked locally.`)
        return true
      }

      if (job.liked) {
        console.log(`Job ${jobId} is already liked locally.`)
        return true
      }
      const originalLikedStatus = job.liked
      job.liked = true

      try {
        const authStore = useAuthStore()
        const token = authStore.token
        if (!token) {
          console.error('Auth token missing to like')
          job.liked = originalLikedStatus
          return false
        }

        const response = await fetch(`${API_URL}/api/jobs/liked-jobs`, {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ job_id: jobIdStr }),
        })

        if (!response.ok) {
          if (response.status === 409) {
            console.warn(`Job ${jobIdStr} is already liked by the server`)
          } else {
            const errorText = await response.text()
            throw new Error(`Faile on liking job action: ${response.status} - ${errorText}`)
          }
        }
        console.log(`Job ${jobId} liked successfully.`)
        return true
      } catch (error) {
        console.error('Failed to like job:', error)
        showNetworkErrorToast()
        job.liked = originalLikedStatus
        return false
      }
    },
    async unlikeJob(jobId: string) {
      const job = this.jobs.find((j) => j.id === jobId)
      if (!job) return false

      if (!job.liked) {
        console.log(`Job ${jobId} is already unliked locally.`)
        return true
      }

      const originalLikedStatus = job.liked
      job.liked = false

      try {
        const authStore = useAuthStore()
        const userId = authStore.currentUser?.id
        const token = authStore.token

        if (!userId || !token) {
          console.error('User ID or auth token is missing for unlike action.')
          job.liked = originalLikedStatus
          return false
        }

        const response = await fetch(`${API_URL}/api/jobs/liked-jobs/${jobId}?user_id=${userId}`, {
          method: 'DELETE',
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })

        if (!response.ok) {
          if (response.status === 404) {
            console.warn(
              `Like for the ${jobId} not found on the server. Original liked status: ${originalLikedStatus}`,
            )
          } else {
            const errorText = await response.text()
            throw new Error(`Échec du délike du job: ${response.status} - ${errorText}`)
          }
        }
        console.log(`Job ${jobId} unliked successfully.`)
        return true
      } catch (error) {
        console.error('Failed to unlike job:', error)
        showNetworkErrorToast()
        job.liked = originalLikedStatus
        return false
      }
    },
    async fetchLikedJobs() {
      if (!this.currentUser?.id) {
        console.error('User ID is missing — cannot fetch liked jobs.')
        return
      }

      const likedJobsData = await this._fetchUserJobStatus('liked-jobs')

      this.jobs.forEach((job) => {
        job.liked = likedJobsData.some((likedJob) => likedJob.id === job.id)
      })
      console.log('Liked jobs status synchronized.')
    },
    async toggleLikeJob(jobId: string, isAlreadyLiked: boolean) {
      return isAlreadyLiked ? await this.unlikeJob(jobId) : await this.likeJob(jobId)
    },
    updateJob(updatedJob: Job) {
      const index = this.jobs.findIndex((job) => job.id === updatedJob.id)
      if (index !== -1) Object.assign(this.jobs[index], updatedJob)
    },
    async seeJob(jobId: string) {
      const job = this.jobs.find((j) => j.id === jobId)
      if (!job) return false
      if (job.seen) {
        console.log(`Job ${jobId} is already seen locally.`)
        return true
      }

      const originalSeenStatus = job.seen
      job.seen = true

      try {
        const authStore = useAuthStore()
        const token = authStore.token
        if (!token) {
          console.error('auht token missing to see the job')
          job.seen = originalSeenStatus
          return false
        }
        const response = await fetch(`${API_URL}/api/jobs/${authStore.currentUser?.id}/seen-jobs`, {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ job_id: jobId }),
        })

        if (!response.ok) {
          if (response.status === 409) {
            console.warn(`Job ${jobId} already seen on the server`)
          } else {
            const errorText = await response.text()
            throw new Error(`Fail on action see job: ${response.status} - ${errorText}`)
          }
        }
        console.log(`Job ${jobId} seen successfully.`)
        return true
      } catch (error) {
        console.error('Failed to see job:', error)
        showNetworkErrorToast()
        job.seen = originalSeenStatus
        return false
      }
    },
    async fetchSeenJobs() {
      if (!this.currentUser?.id) {
        console.error('User ID is missing — cannot fetch liked jobs.')
        return
      }

      const seenJobsData = await this._fetchUserJobStatus('seen-jobs')

      this.jobs.forEach((job) => {
        job.seen = seenJobsData.some((seenJob) => seenJob.id === job.id)
      })
      console.log('Seen jobs status synchronized.')
    },
  },
})
