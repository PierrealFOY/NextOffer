export interface Job {
  id: number
  title: string
  company: string
  url: string
  location: string
  liked: boolean
  seen?: boolean
  applicationSent?: boolean
  salary?: string
  description?: string
  typeContrat?: string
  dateCreation?: Date
}
