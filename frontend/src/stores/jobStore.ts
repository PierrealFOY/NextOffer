import { defineStore } from 'pinia'
import type { Job } from '../types/Job'
import { useAuthStore } from './authStore'
import type { User } from '@/types/User'
import { useToast } from '@/components/ui/toast/use-toast'

const { toast } = useToast()

export const useJobStore = defineStore('jobStore', {
  state: () => ({
    jobs: [] as Job[],
    isLoading: false,
    hasMore: true,
    offset: 0,
    limit: 20,
    _rawLikedJobs: [] as Job[],
  }),
  getters: {
    isJobAlreadyLiked: (state) => (jobId: string) => {
      return state.jobs.some((job) => job.id === jobId && job.liked)
    },
    currentUser: (): User | null => useAuthStore().currentUser,
    getJobById: (state) => (id: string) => state.jobs.find((job) => job.id === id),
    likedJobs: (state) => state.jobs.filter((job) => job.liked),
    seenJobs: (state) => state.jobs.filter((job) => job.seen),
    appliedJobs: (state) => state.jobs.filter((job) => job.seen && job.applicationSent),
    filteredJobs: (state) => (query: string) => {
      const lower = query.toLowerCase()
      return state.jobs.filter(
        (job) =>
          job.title.toLowerCase().includes(lower) ||
          job.company.toLowerCase().includes(lower) ||
          job.location.toLowerCase().includes(lower),
      )
    },
  },
  actions: {
    async fetchJobs(offset: number = 0, limit: number = 20) {
      this.isLoading = true
      try {
        const res = await fetch(`http://localhost:8000/jobs?offset=${offset}&limit=${limit}`)

        if (!res.ok) {
          const errorText = await res.text()
          console.error(`HTTP error! status: ${res.status}, body: ${errorText}`)
          return
        }

        const data: Job[] = await res.json()

        const jobsWithLikedStatus = data.map((job) => ({ ...job, liked: false }))

        this.jobs = offset === 0 ? jobsWithLikedStatus : [...this.jobs, ...jobsWithLikedStatus]

        await this.fetchLikedJobs()

        if (data.length < limit) this.hasMore = false
      } catch (error) {
        console.error('Failed to fetch jobs:', error)
      } finally {
        this.isLoading = false
      }
    },
    async fetchJobById(id: string) {
      try {
        const res = await fetch(`http://localhost:8000/jobs/${id}`)

        if (!res.ok) {
          const errorText = await res.text()
          console.error(`HTTP error! status: ${res.status}, body: ${errorText}`)
          return
        }

        const data: Job = await res.json()

        if (this.currentUser?.id) {
          const likedJobsForUser = await this.fetchLikedJobsInternal()
          data.liked = likedJobsForUser.some((likedJob) => likedJob.id === data.id)
        } else {
          data.liked = false
        }
        return data
      } catch (error) {
        console.error('Failed to fetch job id:', error)
      }
    },
    // toggleLikeJob(jobId: string) {
    //   const index = this.jobs.findIndex((job) => job.id === jobId)
    //   if (index !== -1) {
    //     const job = this.jobs[index]
    //     job.liked = !job.liked

    //     const authStore = useAuthStore()
    //     if (job.liked) authStore.toggleFavoriteJob(jobId)
    //   }
    // },
    async likeJob(jobId: string) {
      if (!this.currentUser?.id) {
        console.error('User ID is missing — cannot like job.')
        const authStore = useAuthStore()

        if (!authStore.isAuthenticated) {
          toast({
            title: 'Impossible de liker le job !',
            description: 'Il faut être connecté pour liker un job',
            class: 'bg-gray-300 text-red-700',
          })
        }
        return
      }

      try {
        const response = await fetch('http://localhost:8000/jobs/liked-jobs', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ job_id: jobId, user_id: this.currentUser.id }),
        })

        if (!response.ok) {
          const errorText = await response.text()
          console.error(`HTTP error! status: ${response.status}, body: ${errorText}`)
          // Provide user feedback for conflict (already liked)
          if (response.status === 409) {
            toast({
              title: 'Job déjà liké !',
              description: 'Vous avez déjà liké ce job.',
              class: 'bg-gray-300 text-orange-800',
            })
          } else {
            toast({
              title: 'Erreur lors du like !',
              description: 'Impossible de liker ce job.',
              class: 'bg-gray-300 text-red-700',
            })
          }
          return
        }

        // on successful like, immediately update the local job status
        const jobToUpdate = this.jobs.find((job) => job.id === jobId)
        if (jobToUpdate) {
          jobToUpdate.liked = true
          toast({
            title: 'Job liké !',
            description: 'Le job a été ajouté à vos favoris.',
            class: 'bg-gray-300 text-green-700',
          })
        }

        const data = await response.json()
        return data
      } catch (error) {
        console.error('Failed to add the job as liked:', error)
        toast({
          title: 'Erreur réseau !',
          description: 'Vérifiez votre connexion et réessayez.',
          class: 'bg-gray-300 text-red-700',
        })
      }
    },

    async unlikeJob(jobId: string) {
      if (!this.currentUser?.id) {
        console.error('User ID is missing — cannot unlike job.')
        return
      }

      try {
        const url = `http://localhost:8000/jobs/liked-jobs/${jobId}?user_id=${this.currentUser.id}`
        const response = await fetch(url, {
          method: 'DELETE',
        })

        if (!response.ok) {
          const errorText = await response.text()
          console.error(`HTTP error! status: ${response.status}, body: ${errorText}`)
          toast({
            title: 'Erreur lors du dé-like !',
            description: 'Impossible de retirer ce job des favoris.',
            class: 'bg-gray-300 text-red-700',
          })
          return
        }

        // update the local job status
        const jobToUpdate = this.jobs.find((job) => job.id === jobId)
        if (jobToUpdate) {
          jobToUpdate.liked = false
          toast({
            title: 'Job retiré !',
            description: 'Le job a été retiré de vos favoris.',
            class: 'bg-gray-300 text-orange-700',
          })
        }

        const data = await response.json()
        return data
      } catch (error) {
        console.error('Failed to unlike job:', error)
        toast({
          title: 'Erreur réseau !',
          description: 'Vérifiez votre connexion et réessayez.',
          class: 'bg-gray-300 text-red-700',
        })
      }
    },

    async fetchLikedJobsInternal(): Promise<Job[]> {
      if (!this.currentUser?.id) {
        console.error('User ID is missing — cannot toggle like.')
        return []
      }

      try {
        const response = await fetch(`http://localhost:8000/jobs/liked-jobs/${this.currentUser.id}`)
        if (!response.ok) {
          const errorText = await response.text()
          console.error(`HTTP error! status: ${response.status}, body: ${errorText}`)
          return []
        }
        const data: Job[] = await response.json()
        console.log('liked jobs internal:', data)
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

      const likedJobsData = await this.fetchLikedJobsInternal(this.currentUser?.id)

      this.jobs.forEach((job) => {
        job.liked = likedJobsData.some((likedJob) => likedJob.id === job.id)
      })
      console.log('Liked jobs status synchronized.')
    },
    async toggleLikeJob(jobId: string, isAlreadyLiked: boolean) {
      if (isAlreadyLiked) {
        return this.unlikeJob(jobId)
      } else {
        return this.likeJob(jobId)
      }
    },
    updateJob(updatedJob: Job) {
      const index = this.jobs.findIndex((job) => job.id === updatedJob.id)
      if (index !== -1) {
        this.jobs[index] = updatedJob
      }
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
