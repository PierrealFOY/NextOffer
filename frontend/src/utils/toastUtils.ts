import { toast } from '@/components/ui/toast'

export function showNetworkErrorToast() {
  toast({
    title: 'Erreur réseau !',
    description: 'Vérifiez votre connexion et réessayez.',
    class: 'bg-gray-300 text-red-700',
  })
}
