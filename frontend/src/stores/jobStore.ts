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
    filteredJobs: (state) => (query: string) => {
      const lower = query.toLowerCase() ?? ''
      return state.jobs.filter(
        (job) =>
          (job.title && job.title.toLowerCase().includes(lower)) ||
          (job.company && job.company.toLowerCase().includes(lower)) ||
          (job.location && job.location.toLowerCase().includes(lower)),
      )
    },
  },
  actions: {
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

        const jobsWithLikedStatus = data.map((job) => ({ ...job, liked: false, seen: false }))

        this.jobs = offset === 0 ? jobsWithLikedStatus : [...this.jobs, ...jobsWithLikedStatus]

        await this.fetchLikedJobs()
        await this.fetchSeenJobs()

        if (data.length < limit) this.hasMore = false
      } catch (error) {
        console.error('Failed to fetch jobs:', error)
      } finally {
        this.isLoading = false
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

        if (this.currentUser?.id) {
          const likedJobsForUser = await this.fetchLikedJobsInternal()
          data.liked = likedJobsForUser.some((likedJob) => likedJob.id === data.id)

          const seenJobsForUser = await this.fetchSeenJobsInternal()
          data.seen = seenJobsForUser.some((seenJob) => seenJob.id === data.id)
        } else {
          data.liked = false
          data.seen = false
        }
        return data
      } catch (error) {
        console.error('Failed to fetch job id:', error)
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

      try {
        const authStore = useAuthStore()
        const token = authStore.token
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
            if (job) job.liked = true
            return true
          } else {
            const errorText = await response.text()
            throw new Error(`Faile on liking job action: ${response.status} - ${errorText}`)
          }
        }

        const jobUpdated = await response.json()
        if (job) Object.assign(job, jobUpdated)
        return true
      } catch (error) {
        console.error('Failed to like job:', error)
        showNetworkErrorToast()
        return false
      }
    },
    async unlikeJob(jobId: string) {
      const job = this.jobs.find((j) => j.id === jobId)
      if (!job || !this.isJobAlreadyLiked(jobId)) return

      try {
        const authStore = useAuthStore()
        const userId = authStore.currentUser?.id

        if (!userId) {
          throw new Error('User ID is missing')
        }

        const response = await fetch(`${API_URL}/api/jobs/liked-jobs/${jobId}?user_id=${userId}`, {
          method: 'DELETE',
          credentials: 'include',
        })

        if (!response.ok) throw new Error('Unlike job failed')

        const jobUpdated = await response.json()
        const index = this.jobs.findIndex((j) => j.id === jobId.toString())
        if (index !== -1) {
          this.jobs[index] = jobUpdated
        }
        job.liked = false
        return true
      } catch (error) {
        console.error('Failed to unlike job:', error)
        showNetworkErrorToast()
        return false
      }
    },
    async fetchLikedJobsInternal(): Promise<Job[]> {
      if (!this.currentUser?.id) {
        console.error('User ID is missing — cannot toggle like.')
        return []
      }

      try {
        const response = await fetch(`${API_URL}/api/jobs/liked-jobs/${this.currentUser.id}`)
        if (!response.ok) {
          const errorText = await response.text()
          console.error(`HTTP error! status: ${response.status}, body: ${errorText}`)
          return []
        }
        const data: Job[] = await response.json()
        return data
      } catch (error) {
        console.error('Failed to fetch liked jobs internally:', error)
        return []
      }
    },
    async fetchLikedJobs() {
      if (!this.currentUser?.id) {
        console.error('User ID is missing — cannot fetch liked jobs.')
        return
      }

      const likedJobsData = await this.fetchLikedJobsInternal()

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
      if (index !== -1) {
        this.jobs[index] = updatedJob
      }
    },
    async fetchSeenJobsInternal(): Promise<Job[]> {
      if (!this.currentUser?.id) {
        console.error('User ID is missing — cannot toggle like.')
        return []
      }

      try {
        const response = await fetch(`${API_URL}/api/jobs/seen-jobs/${this.currentUser.id}`)
        if (!response.ok) {
          const errorText = await response.text()
          console.error(`HTTP error! status: ${response.status}, body: ${errorText}`)
          return []
        }
        const data: Job[] = await response.json()
        return data
      } catch (error) {
        console.error('Failed to fetch seen jobs internally:', error)
        return []
      }
    },
    async seeJob(jobId: string) {
      const job = this.jobs.find((j) => j.id === jobId)
      if (!job) return false
      if (this.isJobAlreadySeen(jobId)) return true

      try {
        const authStore = useAuthStore()
        const token = authStore.token

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
            if (job) job.seen = true
            return true
          } else {
            const errorText = await response.text()
            throw new Error(`Fail on action see job: ${response.status} - ${errorText}`)
          }
        }

        const jobUpdated = await response.json()
        if (job) Object.assign(job, jobUpdated)
        return true
      } catch (error) {
        console.error('Failed to see job:', error)
        showNetworkErrorToast()
        return false
      }
    },
    async fetchSeenJobs() {
      if (!this.currentUser?.id) {
        console.error('User ID is missing — cannot fetch liked jobs.')
        return
      }

      const seenJobsData = await this.fetchSeenJobsInternal()

      this.jobs.forEach((job) => {
        job.seen = seenJobsData.some((seenJob) => seenJob.id === job.id)
      })
      console.log('Seen jobs status synchronized.')
    },
    updateSeenJobs(jobId: string) {
      const index = this.jobs.findIndex((job) => job.id === jobId)
      if (index !== -1) {
        this.jobs[index].seen = true
      }
    },
    updateAppliedJobs(jobId: string) {
      const index = this.jobs.findIndex((job) => job.id === jobId)
      if (index !== -1) {
        this.jobs[index].applicationSent = true
      }
    },
  },
})
