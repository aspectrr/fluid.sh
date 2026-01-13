import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/ansible/')({
  component: AnsiblePage,
})

function AnsiblePage() {
  return (
    <main className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Ansible Runs</h1>
        <p className="text-muted-foreground">View and manage Ansible playbook executions</p>
      </div>
      <div className="bg-card text-muted-foreground rounded-lg border p-8 text-center">
        No Ansible runs yet. Run a playbook from a sandbox to see it here.
      </div>
    </main>
  )
}
