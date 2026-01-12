import { createFileRoute } from '@tanstack/react-router'
import { SandboxTable } from '~/components/sandbox-table'

export const Route = createFileRoute('/sandboxes/')({
  component: SandboxesPage,
})

function SandboxesPage() {
  return (
    <main className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Sandboxes</h1>
        <p className="text-muted-foreground">View and manage your virtual machine sandboxes</p>
      </div>
      <SandboxTable />
    </main>
  )
}
