import { createFileRoute } from '@tanstack/react-router'
import { VMTable } from '~/components/vm-table'

export const Route = createFileRoute('/')({
  component: HomePage,
})

function HomePage() {
  return (
    <main className="container mx-auto px-4 py-8">
      <h1 className="mb-6 text-3xl font-bold">Virtual Machines</h1>
      <VMTable />
    </main>
  )
}
